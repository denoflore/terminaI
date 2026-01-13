/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import * as path from 'node:path';
import * as fs from 'node:fs/promises';
import { debugLogger } from './debugLogger.js';

/**
 * Check if running on Windows
 */
export function isWindows(): boolean {
  return process.platform === 'win32';
}

/**
 * Get the correct curl command for the platform
 * On Windows, PowerShell has a curl alias that behaves differently
 */
export function getCurlCommand(): string {
  if (isWindows()) {
    return 'curl.exe';
  }
  return 'curl';
}

/**
 * Normalize a path for the current platform
 */
export function normalizePath(inputPath: string): string {
  // Handle Windows/Unix path separator differences
  let normalized = path.normalize(inputPath);

  if (isWindows()) {
    // Convert forward slashes to backslashes on Windows
    normalized = normalized.replace(/\//g, '\\');
  } else {
    // Convert backslashes to forward slashes on Unix
    normalized = normalized.replace(/\\/g, '/');
  }

  return normalized;
}

/**
 * Convert a Unix-style path to Windows-style if on Windows
 */
export function toNativePath(unixPath: string): string {
  if (!isWindows()) {
    return unixPath;
  }

  // Handle common Unix paths that don't exist on Windows
  if (unixPath.startsWith('/mnt/')) {
    // WSL-style path: /mnt/c/... -> C:\...
    const parts = unixPath.split('/');
    if (parts.length >= 3 && parts[2].length === 1) {
      const drive = parts[2].toUpperCase();
      const rest = parts.slice(3).join('\\');
      return `${drive}:\\${rest}`;
    }
  }

  if (unixPath.startsWith('/home/')) {
    // Unix home -> Windows user profile
    const parts = unixPath.split('/');
    const rest = parts.slice(3).join('\\');
    return path.join(process.env['USERPROFILE'] || 'C:\\Users\\Default', rest);
  }

  // Generic conversion
  return unixPath.replace(/\//g, '\\');
}

/**
 * Convert a Windows-style path to Unix-style
 */
export function toUnixPath(windowsPath: string): string {
  if (isWindows()) {
    return windowsPath;
  }

  // Handle drive letters: C:\... -> /mnt/c/...
  const driveMatch = windowsPath.match(/^([A-Za-z]):\\/);
  if (driveMatch) {
    const drive = driveMatch[1].toLowerCase();
    const rest = windowsPath.slice(3).replace(/\\/g, '/');
    return `/mnt/${drive}/${rest}`;
  }

  return windowsPath.replace(/\\/g, '/');
}

/**
 * MCP config validation issues
 */
export interface MCPConfigIssue {
  serverName: string;
  issue: string;
  severity: 'error' | 'warning';
  suggestion?: string;
}

/**
 * Validate MCP configuration for common issues
 */
export function validateMCPConfig(
  config: Record<string, unknown>,
): MCPConfigIssue[] {
  const issues: MCPConfigIssue[] = [];

  const mcpServers = config['mcpServers'] as
    | Record<
        string,
        {
          command?: string;
          args?: string[];
        }
      >
    | undefined;

  if (!mcpServers) {
    return issues;
  }

  for (const [name, server] of Object.entries(mcpServers)) {
    // Check for invalid characters in server name
    if (name.includes('.') || name.includes(':')) {
      issues.push({
        serverName: name,
        issue:
          'Invalid characters in server name (dots and colons not allowed)',
        severity: 'error',
        suggestion: `Rename to: ${name.replace(/[.:]/g, '-')}`,
      });
    }

    // Check for non-existent @anthropics packages
    if (
      server.command === 'npx' &&
      server.args?.[0]?.includes('@anthropics/')
    ) {
      issues.push({
        serverName: name,
        issue: '@anthropics/ packages may not exist, verify package name',
        severity: 'warning',
        suggestion: 'Check npm registry for correct package name',
      });
    }

    // Check for Unix paths on Windows
    if (isWindows()) {
      if (server.args) {
        for (const arg of server.args) {
          if (typeof arg === 'string' && arg.startsWith('/mnt/')) {
            issues.push({
              serverName: name,
              issue: `Unix-style path detected: ${arg}`,
              severity: 'error',
              suggestion: `Convert to Windows path: ${toNativePath(arg)}`,
            });
          }
        }
      }
    }
  }

  return issues;
}

/**
 * Get Claude Desktop config path
 */
export function getClaudeDesktopConfigPath(): string {
  if (isWindows()) {
    return path.join(
      process.env['APPDATA'] || 'C:\\Users\\Default\\AppData\\Roaming',
      'Claude',
      'claude_desktop_config.json',
    );
  }

  return path.join(
    process.env['HOME'] || '/home/user',
    'Library',
    'Application Support',
    'Claude',
    'claude_desktop_config.json',
  );
}

/**
 * Load and validate Claude Desktop config
 */
export async function loadAndValidateClaudeConfig(): Promise<{
  config: Record<string, unknown> | null;
  issues: MCPConfigIssue[];
}> {
  const configPath = getClaudeDesktopConfigPath();

  try {
    const content = await fs.readFile(configPath, 'utf-8');
    const config = JSON.parse(content) as Record<string, unknown>;
    const issues = validateMCPConfig(config);
    return { config, issues };
  } catch (error) {
    debugLogger.debug(
      `Could not load Claude config: ${error instanceof Error ? error.message : 'Unknown error'}`,
    );
    return { config: null, issues: [] };
  }
}

/**
 * Common typo corrections map (Chris-specific)
 */
const TYPO_CORRECTIONS: Record<string, string> = {
  waht: 'what',
  teh: 'the',
  jsut: 'just',
  wiht: 'with',
  hte: 'the',
  taht: 'that',
  adn: 'and',
  fro: 'for',
  yuo: 'you',
  dont: "don't",
  wont: "won't",
  cant: "can't",
  im: "I'm",
  ive: "I've",
  youre: "you're",
  theyre: "they're",
  thats: "that's",
  lets: "let's",
  heres: "here's",
  whats: "what's",
};

/**
 * Apply typo corrections to input text
 */
export function correctTypos(input: string): string {
  let corrected = input;

  for (const [typo, correction] of Object.entries(TYPO_CORRECTIONS)) {
    // Word boundary regex to avoid partial matches
    const regex = new RegExp(`\\b${typo}\\b`, 'gi');
    corrected = corrected.replace(regex, correction);
  }

  return corrected;
}

/**
 * Parse intent from potentially typo-ridden input
 * Returns the corrected input and whether corrections were made
 */
export function parseTypoTolerantInput(input: string): {
  original: string;
  corrected: string;
  hadTypos: boolean;
} {
  const corrected = correctTypos(input);
  return {
    original: input,
    corrected,
    hadTypos: corrected !== input,
  };
}

/**
 * Coherence check flags
 */
export interface CoherenceFlag {
  type:
    | 'stale_reference'
    | 'scope_creep'
    | 'similar_past_solution'
    | 'ambiguous';
  message: string;
  suggestion?: string;
}

/**
 * Check for potential coherence issues in user input
 * (Simple implementation - can be enhanced with brain integration)
 */
export function checkCoherence(
  input: string,
  context: {
    offlineServices?: string[];
    openPriorities?: string[];
  } = {},
): CoherenceFlag[] {
  const flags: CoherenceFlag[] = [];
  const inputLower = input.toLowerCase();

  // Check for references to offline services
  if (context.offlineServices) {
    for (const service of context.offlineServices) {
      if (inputLower.includes(service.toLowerCase())) {
        flags.push({
          type: 'stale_reference',
          message: `You mentioned "${service}" but it's currently offline`,
          suggestion: 'Did you mean a different service?',
        });
      }
    }
  }

  // Check for scope creep
  if (context.openPriorities && context.openPriorities.length >= 3) {
    const priorityKeywords = ['also', 'another', 'new', 'additionally', 'plus'];
    if (priorityKeywords.some((kw) => inputLower.includes(kw))) {
      flags.push({
        type: 'scope_creep',
        message: `Adding a ${context.openPriorities.length + 1}th priority while ${context.openPriorities.length} are open`,
        suggestion:
          'Is this intentional, or should we finish existing priorities first?',
      });
    }
  }

  return flags;
}
