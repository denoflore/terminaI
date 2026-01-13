/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * CCIN Handoff structure
 */
export interface CCINHandoff {
  /** Version of the CCIN format */
  version: string;

  /** Unique handoff identifier */
  id: string;

  /** Timestamp of handoff generation */
  timestamp: string;

  /** Source session information */
  source: {
    sessionId: string;
    agentName?: string;
    platform?: string;
  };

  /** Registry of stems/symbols used in this handoff */
  registry: CCINRegistry;

  /** Current system/entity state */
  state: CCINState;

  /** Relevant context */
  context: CCINContext;

  /** Task to be performed */
  task?: CCINTask;

  /** Constraints and limitations */
  constraints?: CCINConstraints;
}

/**
 * CCIN Registry for symbols/stems
 */
export interface CCINRegistry {
  /** Symbol definitions used in this handoff */
  symbols: Record<string, string>;

  /** Abbreviations */
  abbreviations?: Record<string, string>;
}

/**
 * Current state information
 */
export interface CCINState {
  /** Emotional/affect state (VACTS if available) */
  affect?: {
    valence?: number;
    arousal?: number;
    confidence?: number;
    tension?: number;
    spite?: number;
    momentum?: number;
    curiosity?: number;
    coherence?: number;
  };

  /** Current priorities/goals */
  priorities?: string[];

  /** Active context identifiers */
  activeContexts?: string[];

  /** Working memory highlights */
  workingMemory?: string[];

  /** Recent decisions */
  recentDecisions?: Array<{
    decision: string;
    timestamp: string;
    reasoning?: string;
  }>;

  /** Custom state data */
  custom?: Record<string, unknown>;
}

/**
 * Context information
 */
export interface CCINContext {
  /** User information */
  user?: {
    name?: string;
    preferences?: Record<string, unknown>;
    patterns?: string[];
  };

  /** Environment information */
  environment?: {
    platform?: string;
    workspace?: string;
    project?: string;
    branch?: string;
  };

  /** Relevant memories/facts */
  relevantMemories?: string[];

  /** Active skills */
  activeSkills?: string[];

  /** Conversation summary */
  conversationSummary?: string;

  /** Custom context data */
  custom?: Record<string, unknown>;
}

/**
 * Task to be performed
 */
export interface CCINTask {
  /** Task description */
  description: string;

  /** Task steps */
  steps?: string[];

  /** Expected outcome */
  expectedOutcome?: string;

  /** Files involved */
  files?: string[];

  /** Dependencies */
  dependencies?: string[];
}

/**
 * Constraints and limitations
 */
export interface CCINConstraints {
  /** Things to avoid */
  mustNot?: string[];

  /** Required behaviors */
  mustDo?: string[];

  /** Time constraints */
  timeConstraints?: {
    deadline?: string;
    urgency?: 'low' | 'medium' | 'high' | 'critical';
  };

  /** Resource constraints */
  resources?: {
    maxTokens?: number;
    availableTools?: string[];
    unavailableServices?: string[];
  };
}

/**
 * CCIN configuration
 */
export interface CCINConfig {
  /** Enable/disable CCIN system */
  enabled: boolean;

  /** Directory for handoff storage */
  handoffsDir?: string;

  /** Auto-checkpoint interval (ms, 0 = disabled) */
  checkpointInterval: number;

  /** Maximum handoffs to retain */
  maxHandoffs: number;

  /** Compress handoff data */
  compress: boolean;
}

/**
 * Default CCIN configuration
 */
export const DEFAULT_CCIN_CONFIG: CCINConfig = {
  enabled: true,
  checkpointInterval: 0, // Disabled by default
  maxHandoffs: 50,
  compress: false,
};

/**
 * Get platform-specific handoffs directory
 */
export function getDefaultHandoffsDir(): string {
  const isWindows = process.platform === 'win32';

  if (isWindows) {
    const appData =
      process.env['APPDATA'] || 'C:\\Users\\Default\\AppData\\Roaming';
    return `${appData}\\terminai\\handoffs\\`;
  } else {
    const homeDir = process.env['HOME'] || '/home/user';
    return `${homeDir}/.terminai/handoffs/`;
  }
}
