/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import * as fs from 'node:fs/promises';
import * as path from 'node:path';
import { randomUUID } from 'node:crypto';
import {
  type CCINHandoff,
  type CCINState,
  type CCINContext,
  type CCINTask,
  type CCINConstraints,
  type CCINConfig,
  DEFAULT_CCIN_CONFIG,
  getDefaultHandoffsDir,
} from './types.js';
import { debugLogger } from '../utils/debugLogger.js';

/**
 * CCIN Handoff Manager
 */
export class HandoffManager {
  private config: CCINConfig;
  private currentSessionId: string;
  private checkpointTimer: NodeJS.Timeout | null = null;
  private initialized: boolean = false;
  private handoffsDir: string;

  constructor(config: Partial<CCINConfig> = {}, sessionId?: string) {
    this.config = {
      ...DEFAULT_CCIN_CONFIG,
      ...config,
    };
    this.handoffsDir = this.config.handoffsDir || getDefaultHandoffsDir();
    this.currentSessionId = sessionId || randomUUID();
  }

  /**
   * Initialize the handoff manager
   */
  async initialize(): Promise<void> {
    if (this.initialized) return;

    if (!this.config.enabled) {
      debugLogger.log('CCIN handoff system disabled');
      this.initialized = true;
      return;
    }

    // Ensure handoffs directory exists
    await fs.mkdir(this.handoffsDir, { recursive: true });

    // Start checkpoint timer if configured
    if (this.config.checkpointInterval > 0) {
      this.startCheckpointTimer();
    }

    // Cleanup old handoffs
    await this.cleanupOldHandoffs();

    this.initialized = true;
    debugLogger.log('CCIN handoff manager initialized');
  }

  /**
   * Generate a handoff document
   */
  generateHandoff(
    state: Partial<CCINState>,
    context: Partial<CCINContext>,
    task?: CCINTask,
    constraints?: CCINConstraints,
  ): CCINHandoff {
    const handoff: CCINHandoff = {
      version: '1.0',
      id: randomUUID(),
      timestamp: new Date().toISOString(),
      source: {
        sessionId: this.currentSessionId,
        platform: process.platform,
      },
      registry: {
        symbols: {
          CCIN_μ: 'Compressed handoff notation',
          VACTS: 'Valence-Arousal-Confidence-Tension-Spite emotion model',
          NSL: 'Negative Space Learning',
          DMN: 'Default Mode Network',
        },
      },
      state: {
        ...state,
      },
      context: {
        ...context,
        environment: {
          platform: process.platform,
          ...context.environment,
        },
      },
    };

    if (task) {
      handoff.task = task;
    }

    if (constraints) {
      handoff.constraints = constraints;
    }

    return handoff;
  }

  /**
   * Save a handoff to disk
   */
  async saveHandoff(handoff: CCINHandoff): Promise<string> {
    const filename = `handoff_${handoff.timestamp.replace(/[:.]/g, '-')}_${handoff.id.slice(0, 8)}.json`;
    const filepath = path.join(this.handoffsDir, filename);

    const content = JSON.stringify(handoff, null, 2);

    await fs.writeFile(filepath, content, 'utf-8');
    debugLogger.debug(`Handoff saved: ${filepath}`);

    return filepath;
  }

  /**
   * Load a handoff from disk
   */
  async loadHandoff(filepath: string): Promise<CCINHandoff | null> {
    try {
      const content = await fs.readFile(filepath, 'utf-8');
      return JSON.parse(content) as CCINHandoff;
    } catch (_error) {
      debugLogger.warn(`Failed to load handoff: ${filepath}`);
      return null;
    }
  }

  /**
   * Get the latest handoff
   */
  async getLatestHandoff(): Promise<CCINHandoff | null> {
    try {
      const files = await fs.readdir(this.handoffsDir);
      const handoffFiles = files
        .filter((f) => f.startsWith('handoff_') && f.endsWith('.json'))
        .sort()
        .reverse();

      if (handoffFiles.length === 0) {
        return null;
      }

      return await this.loadHandoff(
        path.join(this.handoffsDir, handoffFiles[0]),
      );
    } catch (_error) {
      return null;
    }
  }

  /**
   * List all available handoffs
   */
  async listHandoffs(): Promise<
    Array<{ id: string; timestamp: string; filepath: string }>
  > {
    try {
      const files = await fs.readdir(this.handoffsDir);
      const handoffFiles = files
        .filter((f) => f.startsWith('handoff_') && f.endsWith('.json'))
        .sort()
        .reverse();

      const results: Array<{
        id: string;
        timestamp: string;
        filepath: string;
      }> = [];

      for (const file of handoffFiles) {
        // Parse info from filename: handoff_TIMESTAMP_ID.json
        const match = file.match(/handoff_(.+)_([a-f0-9]+)\.json/);
        if (match) {
          results.push({
            id: match[2],
            timestamp: match[1].replace(/-/g, ':'),
            filepath: path.join(this.handoffsDir, file),
          });
        }
      }

      return results;
    } catch (_error) {
      return [];
    }
  }

  /**
   * Create a checkpoint (auto-save current state)
   */
  async createCheckpoint(
    state: Partial<CCINState>,
    context: Partial<CCINContext>,
  ): Promise<void> {
    const handoff = this.generateHandoff(state, context);
    await this.saveHandoff(handoff);
  }

  /**
   * Start the checkpoint timer
   */
  private startCheckpointTimer(): void {
    if (this.checkpointTimer) {
      clearInterval(this.checkpointTimer);
    }

    this.checkpointTimer = setInterval(() => {
      // Note: The actual checkpoint creation would need state from the caller
      debugLogger.debug('Checkpoint interval triggered');
    }, this.config.checkpointInterval);
  }

  /**
   * Stop the checkpoint timer
   */
  stopCheckpointTimer(): void {
    if (this.checkpointTimer) {
      clearInterval(this.checkpointTimer);
      this.checkpointTimer = null;
    }
  }

  /**
   * Cleanup old handoffs beyond max retention
   */
  async cleanupOldHandoffs(): Promise<void> {
    try {
      const files = await fs.readdir(this.handoffsDir);
      const handoffFiles = files
        .filter((f) => f.startsWith('handoff_') && f.endsWith('.json'))
        .sort()
        .reverse();

      // Remove files beyond max retention
      const toRemove = handoffFiles.slice(this.config.maxHandoffs);

      for (const file of toRemove) {
        await fs.unlink(path.join(this.handoffsDir, file));
        debugLogger.debug(`Removed old handoff: ${file}`);
      }
    } catch (_error) {
      debugLogger.warn('Failed to cleanup old handoffs');
    }
  }

  /**
   * Generate CCIN_μ formatted string (compressed notation)
   */
  formatAsCCINMu(handoff: CCINHandoff): string {
    const lines: string[] = [];

    lines.push('「CCIN_μ HANDOFF v1.0」');
    lines.push('');

    // Registry
    lines.push('「REG!');
    for (const [symbol, meaning] of Object.entries(handoff.registry.symbols)) {
      lines.push(`  ${symbol} := ${meaning}`);
    }
    lines.push('」');
    lines.push('');

    // State
    lines.push('「STATE」');
    if (handoff.state.affect) {
      const affect = handoff.state.affect;
      const affectStr = Object.entries(affect)
        .filter(([, v]) => v !== undefined)
        .map(([k, v]) => `${k[0].toUpperCase()}:${(v).toFixed(2)}`)
        .join(' ');
      lines.push(`  VACTS: ${affectStr}`);
    }
    if (handoff.state.priorities && handoff.state.priorities.length > 0) {
      lines.push(`  PRIO: ${handoff.state.priorities.join(' > ')}`);
    }
    if (handoff.state.workingMemory && handoff.state.workingMemory.length > 0) {
      lines.push('  WM:');
      for (const mem of handoff.state.workingMemory) {
        lines.push(`    - ${mem}`);
      }
    }
    lines.push('');

    // Context
    lines.push('「CONTEXT」');
    if (handoff.context.user?.name) {
      lines.push(`  USER: ${handoff.context.user.name}`);
    }
    if (handoff.context.environment) {
      const env = handoff.context.environment;
      lines.push(
        `  ENV: ${env.platform || 'unknown'} @ ${env.workspace || 'unknown'}`,
      );
    }
    if (handoff.context.conversationSummary) {
      lines.push(`  SUMMARY: ${handoff.context.conversationSummary}`);
    }
    lines.push('');

    // Task
    if (handoff.task) {
      lines.push('「TASK」');
      lines.push(`  ${handoff.task.description}`);
      if (handoff.task.steps && handoff.task.steps.length > 0) {
        lines.push('  STEPS:');
        for (let i = 0; i < handoff.task.steps.length; i++) {
          lines.push(`    ${i + 1}. ${handoff.task.steps[i]}`);
        }
      }
      lines.push('');
    }

    // Constraints
    if (handoff.constraints) {
      lines.push('「CONSTRAINTS」');
      if (
        handoff.constraints.mustNot &&
        handoff.constraints.mustNot.length > 0
      ) {
        lines.push('  MUST_NOT:');
        for (const c of handoff.constraints.mustNot) {
          lines.push(`    - ${c}`);
        }
      }
      if (handoff.constraints.mustDo && handoff.constraints.mustDo.length > 0) {
        lines.push('  MUST_DO:');
        for (const c of handoff.constraints.mustDo) {
          lines.push(`    - ${c}`);
        }
      }
      lines.push('');
    }

    lines.push('「END HANDOFF」');

    return lines.join('\n');
  }

  /**
   * Get current session ID
   */
  getSessionId(): string {
    return this.currentSessionId;
  }

  /**
   * Set session ID (for session resume)
   */
  setSessionId(sessionId: string): void {
    this.currentSessionId = sessionId;
  }

  /**
   * Get configuration
   */
  getConfig(): CCINConfig {
    return { ...this.config };
  }

  /**
   * Update configuration
   */
  updateConfig(config: Partial<CCINConfig>): void {
    this.config = {
      ...this.config,
      ...config,
    };

    if (config.handoffsDir) {
      this.handoffsDir = config.handoffsDir;
    }

    // Restart checkpoint timer if interval changed
    if (config.checkpointInterval !== undefined) {
      this.stopCheckpointTimer();
      if (this.config.checkpointInterval > 0) {
        this.startCheckpointTimer();
      }
    }
  }

  /**
   * Cleanup on shutdown
   */
  async shutdown(): Promise<void> {
    this.stopCheckpointTimer();
  }
}

// Singleton instance
let handoffManagerInstance: HandoffManager | null = null;

/**
 * Get or create the handoff manager instance
 */
export function getHandoffManager(
  config?: Partial<CCINConfig>,
  sessionId?: string,
): HandoffManager {
  if (!handoffManagerInstance) {
    handoffManagerInstance = new HandoffManager(config, sessionId);
  } else if (config) {
    handoffManagerInstance.updateConfig(config);
  }
  return handoffManagerInstance;
}

/**
 * Reset the handoff manager (for testing)
 */
export function resetHandoffManager(): void {
  if (handoffManagerInstance) {
    void handoffManagerInstance.shutdown();
  }
  handoffManagerInstance = null;
}
