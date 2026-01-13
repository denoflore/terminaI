/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import {
  type Skill,
  type SkillMetadata,
  type SkillsConfig,
  type SkillSource,
  type SkillMatch,
  type SkillLoadError,
  DEFAULT_SKILLS_CONFIG,
  getDefaultSkillPaths,
} from './types.js';
import { debugLogger } from '../utils/debugLogger.js';

/**
 * Parse YAML frontmatter from skill content
 */
function parseFrontmatter(content: string): {
  metadata: SkillMetadata;
  body: string;
} {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);

  if (!match) {
    // No frontmatter, try to extract name from first heading
    const nameMatch = content.match(/^#\s+(.+)$/m);
    return {
      metadata: {
        name: nameMatch ? nameMatch[1].trim() : 'unknown',
        description: '',
      },
      body: content,
    };
  }

  const frontmatterContent = match[1];
  const body = match[2];

  // Simple YAML parser for skill frontmatter
  const metadata: SkillMetadata = {
    name: '',
    description: '',
  };

  const lines = frontmatterContent.split('\n');
  let currentKey = '';
  let currentArray: string[] = [];
  let inArray = false;

  for (const line of lines) {
    const trimmed = line.trim();

    // Array item
    if (trimmed.startsWith('- ')) {
      if (inArray && currentKey) {
        currentArray.push(trimmed.slice(2).trim());
      }
      continue;
    }

    // End previous array if we're starting a new key
    if (inArray && currentKey && currentArray.length > 0) {
      (metadata as unknown as Record<string, unknown>)[currentKey] =
        currentArray;
      currentArray = [];
      inArray = false;
    }

    // Key-value pair
    const kvMatch = trimmed.match(/^(\w+):\s*(.*)$/);
    if (kvMatch) {
      const [, key, value] = kvMatch;
      currentKey = key;

      if (value === '') {
        // Array will follow
        inArray = true;
        currentArray = [];
      } else {
        // Simple value
        (metadata as unknown as Record<string, unknown>)[key] = value.replace(
          /^["']|["']$/g,
          '',
        );
        inArray = false;
      }
    }
  }

  // Handle trailing array
  if (inArray && currentKey && currentArray.length > 0) {
    (metadata as unknown as Record<string, unknown>)[currentKey] = currentArray;
  }

  return { metadata, body };
}

/**
 * Skills Loader class
 */
export class SkillLoader {
  private config: SkillsConfig;
  private skills: Map<string, Skill> = new Map();
  private loadErrors: SkillLoadError[] = [];
  private lastLoadTime: Date | null = null;
  private initialized: boolean = false;

  constructor(config: Partial<SkillsConfig> = {}) {
    const defaultPaths = getDefaultSkillPaths();
    this.config = {
      ...DEFAULT_SKILLS_CONFIG,
      ...defaultPaths,
      ...config,
    };
  }

  /**
   * Initialize the skill loader
   */
  async initialize(): Promise<void> {
    if (this.initialized) return;

    if (!this.config.enabled) {
      debugLogger.log('Skills system disabled');
      this.initialized = true;
      return;
    }

    debugLogger.log('Initializing skills loader...');
    await this.loadAllSkills();
    this.initialized = true;
    debugLogger.log(
      `Skills loader initialized with ${this.skills.size} skills`,
    );
  }

  /**
   * Load skills from all configured paths
   */
  async loadAllSkills(): Promise<void> {
    this.skills.clear();
    this.loadErrors = [];
    this.lastLoadTime = new Date();

    const sources: Array<{ source: SkillSource; path?: string }> = [
      { source: 'user', path: this.config.userSkillsPath },
      { source: 'public', path: this.config.publicSkillsPath },
      { source: 'examples', path: this.config.examplesSkillsPath },
      { source: 'workspace', path: this.config.workspaceSkillsPath },
    ];

    for (const { source, path: skillPath } of sources) {
      if (skillPath) {
        await this.loadSkillsFromDirectory(skillPath, source);
      }
    }
  }

  /**
   * Load skills from a specific directory
   */
  private async loadSkillsFromDirectory(
    dirPath: string,
    source: SkillSource,
  ): Promise<void> {
    try {
      // Normalize path for cross-platform support
      const normalizedPath = path.normalize(dirPath);

      // Check if directory exists
      try {
        await fs.access(normalizedPath);
      } catch {
        debugLogger.debug(`Skills directory does not exist: ${normalizedPath}`);
        return;
      }

      const entries = await fs.readdir(normalizedPath, { withFileTypes: true });

      for (const entry of entries) {
        if (entry.isDirectory()) {
          const skillDir = path.join(normalizedPath, entry.name);
          await this.loadSkillFromDirectory(skillDir, source);
        }
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : String(error);
      debugLogger.warn(
        `Failed to load skills from ${dirPath}: ${errorMessage}`,
      );
      this.loadErrors.push({
        path: dirPath,
        error: errorMessage,
        timestamp: new Date(),
      });
    }
  }

  /**
   * Load a single skill from its directory
   */
  private async loadSkillFromDirectory(
    skillDir: string,
    source: SkillSource,
  ): Promise<void> {
    const skillFile = path.join(skillDir, 'SKILL.md');

    try {
      // Check file size
      const stats = await fs.stat(skillFile);
      if (stats.size > this.config.maxSkillSize) {
        throw new Error(
          `Skill file exceeds maximum size of ${this.config.maxSkillSize} bytes`,
        );
      }

      // Read and parse skill
      const content = await fs.readFile(skillFile, 'utf-8');
      const { metadata } = parseFrontmatter(content);

      // Generate skill ID from directory name
      const skillId = path.basename(skillDir);

      // Check for duplicate (higher priority wins)
      const existing = this.skills.get(skillId);
      if (existing) {
        const existingPriority = this.config.priority.indexOf(existing.source);
        const newPriority = this.config.priority.indexOf(source);

        if (existingPriority <= newPriority) {
          debugLogger.debug(
            `Skipping lower priority skill: ${skillId} from ${source}`,
          );
          return;
        }
      }

      const skill: Skill = {
        id: skillId,
        metadata: {
          ...metadata,
          name: metadata.name || skillId,
        },
        content,
        path: skillDir,
        source,
        lastModified: stats.mtime,
        loadedAt: new Date(),
      };

      this.skills.set(skillId, skill);
      debugLogger.debug(`Loaded skill: ${skillId} from ${source}`);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : String(error);
      debugLogger.warn(
        `Failed to load skill from ${skillDir}: ${errorMessage}`,
      );
      this.loadErrors.push({
        path: skillDir,
        error: errorMessage,
        timestamp: new Date(),
      });
    }
  }

  /**
   * Get a skill by ID
   */
  getSkill(id: string): Skill | undefined {
    return this.skills.get(id);
  }

  /**
   * Get all loaded skills
   */
  getAllSkills(): Skill[] {
    return Array.from(this.skills.values());
  }

  /**
   * Get skills by source
   */
  getSkillsBySource(source: SkillSource): Skill[] {
    return this.getAllSkills().filter((s) => s.source === source);
  }

  /**
   * Find skills matching a query (simple substring/trigger match)
   */
  findSkills(query: string): SkillMatch[] {
    const results: SkillMatch[] = [];
    const queryLower = query.toLowerCase();

    for (const skill of this.skills.values()) {
      let confidence = 0;
      let matchedTrigger: string | undefined;

      // Check triggers
      if (skill.metadata.triggers) {
        for (const trigger of skill.metadata.triggers) {
          const triggerLower = trigger.toLowerCase();
          if (queryLower.includes(triggerLower)) {
            confidence = Math.max(confidence, 0.9);
            matchedTrigger = trigger;
          }
        }
      }

      // Check name
      if (queryLower.includes(skill.metadata.name.toLowerCase())) {
        confidence = Math.max(confidence, 0.8);
      }

      // Check description
      if (
        skill.metadata.description &&
        skill.metadata.description.toLowerCase().includes(queryLower)
      ) {
        confidence = Math.max(confidence, 0.6);
      }

      // Check tags
      if (skill.metadata.tags) {
        for (const tag of skill.metadata.tags) {
          if (queryLower.includes(tag.toLowerCase())) {
            confidence = Math.max(confidence, 0.5);
          }
        }
      }

      if (confidence > 0) {
        results.push({ skill, confidence, matchedTrigger });
      }
    }

    // Sort by confidence
    return results.sort((a, b) => b.confidence - a.confidence);
  }

  /**
   * Get the best matching skill for a query
   */
  getBestMatch(query: string, minConfidence: number = 0.5): SkillMatch | null {
    const matches = this.findSkills(query);
    if (matches.length > 0 && matches[0].confidence >= minConfidence) {
      return matches[0];
    }
    return null;
  }

  /**
   * Get skill content formatted for LLM context
   */
  getSkillContent(id: string): string | null {
    const skill = this.skills.get(id);
    if (!skill) return null;

    return `# Skill: ${skill.metadata.name}

## Metadata
- Source: ${skill.source}
- Path: ${skill.path}
${skill.metadata.description ? `- Description: ${skill.metadata.description}` : ''}
${skill.metadata.tags ? `- Tags: ${skill.metadata.tags.join(', ')}` : ''}

## Instructions

${skill.content}
`;
  }

  /**
   * List all available skills (for CLI output)
   */
  listSkills(): Array<{
    id: string;
    name: string;
    source: SkillSource;
    description: string;
  }> {
    return this.getAllSkills().map((skill) => ({
      id: skill.id,
      name: skill.metadata.name,
      source: skill.source,
      description: skill.metadata.description || '',
    }));
  }

  /**
   * Get load errors
   */
  getLoadErrors(): SkillLoadError[] {
    return [...this.loadErrors];
  }

  /**
   * Reload all skills
   */
  async reload(): Promise<void> {
    this.initialized = false;
    await this.loadAllSkills();
    this.initialized = true;
  }

  /**
   * Check if cache should be refreshed
   */
  shouldRefreshCache(): boolean {
    if (!this.lastLoadTime) return true;
    const elapsed = Date.now() - this.lastLoadTime.getTime();
    return elapsed > this.config.cacheTTL;
  }

  /**
   * Get configuration
   */
  getConfig(): SkillsConfig {
    return { ...this.config };
  }

  /**
   * Update configuration
   */
  updateConfig(config: Partial<SkillsConfig>): void {
    this.config = {
      ...this.config,
      ...config,
    };
    this.initialized = false;
  }
}

// Singleton instance
let skillLoaderInstance: SkillLoader | null = null;

/**
 * Get or create the skill loader instance
 */
export function getSkillLoader(config?: Partial<SkillsConfig>): SkillLoader {
  if (!skillLoaderInstance) {
    skillLoaderInstance = new SkillLoader(config);
  } else if (config) {
    skillLoaderInstance.updateConfig(config);
  }
  return skillLoaderInstance;
}

/**
 * Reset the skill loader (for testing)
 */
export function resetSkillLoader(): void {
  skillLoaderInstance = null;
}
