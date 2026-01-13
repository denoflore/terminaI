/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Skill metadata from frontmatter
 */
export interface SkillMetadata {
  name: string;
  description: string;
  version?: string;
  author?: string;
  tags?: string[];
  dependencies?: string[];
  triggers?: string[];
}

/**
 * Parsed skill definition
 */
export interface Skill {
  /** Unique identifier for the skill */
  id: string;

  /** Skill metadata from frontmatter */
  metadata: SkillMetadata;

  /** Full content of the SKILL.md file */
  content: string;

  /** Path to the skill directory */
  path: string;

  /** Source category (user, public, examples) */
  source: SkillSource;

  /** When skill was last modified */
  lastModified: Date;

  /** When skill was loaded */
  loadedAt: Date;
}

/**
 * Skill source categories
 */
export type SkillSource = 'user' | 'public' | 'examples' | 'workspace';

/**
 * Skills configuration
 */
export interface SkillsConfig {
  /** Enable/disable skills system */
  enabled: boolean;

  /** User skills directory (highest priority) */
  userSkillsPath?: string;

  /** Public skills directory */
  publicSkillsPath?: string;

  /** Example skills directory */
  examplesSkillsPath?: string;

  /** Workspace-specific skills (relative to workspace root) */
  workspaceSkillsPath?: string;

  /** Priority order for skill resolution */
  priority: SkillSource[];

  /** Auto-reload skills on file changes */
  watchForChanges: boolean;

  /** Maximum skill file size in bytes */
  maxSkillSize: number;

  /** Cache TTL in milliseconds */
  cacheTTL: number;
}

/**
 * Default skills configuration
 */
export const DEFAULT_SKILLS_CONFIG: SkillsConfig = {
  enabled: true,
  priority: ['user', 'workspace', 'public', 'examples'],
  watchForChanges: false,
  maxSkillSize: 1024 * 1024, // 1MB
  cacheTTL: 5 * 60 * 1000, // 5 minutes
};

/**
 * Platform-specific default paths
 */
export function getDefaultSkillPaths(): Partial<SkillsConfig> {
  const isWindows = process.platform === 'win32';

  if (isWindows) {
    // Windows paths (Artemis configuration)
    const dropboxBase = 'D:\\Dropbox\\0 Claudette\\skills\\';
    return {
      userSkillsPath: `${dropboxBase}user\\`,
      publicSkillsPath: `${dropboxBase}public\\`,
      examplesSkillsPath: `${dropboxBase}examples\\`,
    };
  } else {
    // Unix paths
    const homeDir = process.env['HOME'] || '/home/user';
    return {
      userSkillsPath: `${homeDir}/.terminai/skills/user/`,
      publicSkillsPath: `${homeDir}/.terminai/skills/public/`,
      examplesSkillsPath: `${homeDir}/.terminai/skills/examples/`,
    };
  }
}

/**
 * Skill match result from trigger matching
 */
export interface SkillMatch {
  skill: Skill;
  confidence: number;
  matchedTrigger?: string;
}

/**
 * Skill loading error
 */
export interface SkillLoadError {
  path: string;
  error: string;
  timestamp: Date;
}
