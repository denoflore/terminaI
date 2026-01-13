/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import type { ToolRegistry } from '../tools/tool-registry.js';
import type { MessageBus } from '../confirmation-bus/message-bus.js';
import type { BrainClient} from './brain-client.js';
import { getBrainClient } from './brain-client.js';
import {
  BrainStatusTool,
  BrainQueryTool,
  BrainAffectTool,
  BrainModulesTool,
  BrainNSLScanTool,
  BrainProcessTool,
  BrainDreamTool,
} from './brain-tools.js';
import type { SkillLoader} from '../skills/skill-loader.js';
import { getSkillLoader } from '../skills/skill-loader.js';
import type { HandoffManager} from '../ccin/handoff-manager.js';
import { getHandoffManager } from '../ccin/handoff-manager.js';
import type { BrainConfig } from './types.js';
import type { SkillsConfig } from '../skills/types.js';
import type { CCINConfig } from '../ccin/types.js';
import { debugLogger } from '../utils/debugLogger.js';

/**
 * Combined NSCA settings
 */
export interface NSCASettings {
  enabled: boolean;
  brain?: Partial<BrainConfig>;
  skills?: Partial<SkillsConfig>;
  ccin?: Partial<CCINConfig>;
}

/**
 * Default NSCA settings
 */
export const DEFAULT_NSCA_SETTINGS: NSCASettings = {
  enabled: true,
};

/**
 * NSCA Integration Manager
 * Coordinates Brain, Skills, and CCIN subsystems
 */
export class NSCAIntegration {
  private brainClient: BrainClient;
  private skillLoader: SkillLoader;
  private handoffManager: HandoffManager;
  private settings: NSCASettings;
  private initialized: boolean = false;

  constructor(settings: Partial<NSCASettings> = {}, sessionId?: string) {
    this.settings = {
      ...DEFAULT_NSCA_SETTINGS,
      ...settings,
    };

    // Initialize subsystems
    this.brainClient = getBrainClient(this.settings.brain);
    this.skillLoader = getSkillLoader(this.settings.skills);
    this.handoffManager = getHandoffManager(this.settings.ccin, sessionId);
  }

  /**
   * Initialize all NSCA subsystems
   */
  async initialize(): Promise<void> {
    if (this.initialized) return;

    if (!this.settings.enabled) {
      debugLogger.log('NSCA integration disabled');
      this.initialized = true;
      return;
    }

    debugLogger.log('Initializing NSCA integration...');

    // Initialize subsystems in parallel
    await Promise.all([
      this.brainClient.initialize(),
      this.skillLoader.initialize(),
      this.handoffManager.initialize(),
    ]);

    this.initialized = true;
    debugLogger.log('NSCA integration initialized');
  }

  /**
   * Register NSCA brain tools with tool registry
   */
  registerBrainTools(registry: ToolRegistry, messageBus?: MessageBus): void {
    if (!this.settings.enabled) {
      debugLogger.debug('NSCA disabled, skipping brain tool registration');
      return;
    }

    debugLogger.log('Registering NSCA brain tools...');

    // Register all brain tools
    registry.registerTool(new BrainStatusTool(messageBus));
    registry.registerTool(new BrainQueryTool(messageBus));
    registry.registerTool(new BrainAffectTool(messageBus));
    registry.registerTool(new BrainModulesTool(messageBus));
    registry.registerTool(new BrainNSLScanTool(messageBus));
    registry.registerTool(new BrainProcessTool(messageBus));
    registry.registerTool(new BrainDreamTool(messageBus));

    debugLogger.log('NSCA brain tools registered');
  }

  /**
   * Get brain client instance
   */
  getBrainClient(): BrainClient {
    return this.brainClient;
  }

  /**
   * Get skill loader instance
   */
  getSkillLoader(): SkillLoader {
    return this.skillLoader;
  }

  /**
   * Get handoff manager instance
   */
  getHandoffManager(): HandoffManager {
    return this.handoffManager;
  }

  /**
   * Create session start handoff
   */
  async loadPreviousHandoff(): Promise<void> {
    if (!this.settings.enabled) return;

    const latestHandoff = await this.handoffManager.getLatestHandoff();
    if (latestHandoff) {
      debugLogger.log(`Previous handoff available: ${latestHandoff.id}`);
      // The handoff context could be added to system prompts
    }
  }

  /**
   * Create session end handoff
   */
  async createSessionEndHandoff(
    conversationSummary: string,
    priorities: string[] = [],
    workingMemory: string[] = [],
  ): Promise<string | null> {
    if (!this.settings.enabled || !this.settings.ccin?.enabled) {
      return null;
    }

    // Get current affect state from brain if available
    let affect:
      | {
          valence?: number;
          arousal?: number;
          confidence?: number;
          tension?: number;
          spite?: number;
          momentum?: number;
          curiosity?: number;
          coherence?: number;
        }
      | undefined;
    if (this.brainClient.isAvailable()) {
      const affectResponse = await this.brainClient.affect({ action: 'get' });
      if (affectResponse) {
        affect = affectResponse.state;
      }
    }

    const handoff = this.handoffManager.generateHandoff(
      {
        affect,
        priorities,
        workingMemory,
      },
      {
        conversationSummary,
        environment: {
          platform: process.platform,
        },
      },
    );

    const filepath = await this.handoffManager.saveHandoff(handoff);
    debugLogger.log(`Session handoff saved: ${filepath}`);
    return filepath;
  }

  /**
   * Get formatted handoff for inclusion in context
   */
  async getFormattedHandoff(): Promise<string | null> {
    const latestHandoff = await this.handoffManager.getLatestHandoff();
    if (!latestHandoff) return null;

    return this.handoffManager.formatAsCCINMu(latestHandoff);
  }

  /**
   * Load a skill by ID
   */
  getSkillContent(skillId: string): string | null {
    return this.skillLoader.getSkillContent(skillId);
  }

  /**
   * Find matching skills for a query
   */
  findMatchingSkills(query: string, minConfidence: number = 0.5) {
    return this.skillLoader
      .findSkills(query)
      .filter((m) => m.confidence >= minConfidence);
  }

  /**
   * Process interaction through brain (if available)
   */
  async processInteraction(content: string): Promise<void> {
    if (!this.settings.enabled || !this.brainClient.isAvailable()) {
      return;
    }

    await this.brainClient.process({
      content,
      source: 'terminai',
      type: 'interaction',
    });
  }

  /**
   * Query brain for relevant memories
   */
  async queryBrainMemory(query: string, context?: string) {
    if (!this.settings.enabled || !this.brainClient.isAvailable()) {
      return null;
    }

    return this.brainClient.query({ query, context });
  }

  /**
   * Run NSL scan on context
   */
  async scanForMissingContext(context: string) {
    if (!this.settings.enabled || !this.brainClient.isAvailable()) {
      return null;
    }

    return this.brainClient.nslScan({ context });
  }

  /**
   * Shutdown NSCA integration
   */
  async shutdown(): Promise<void> {
    await this.handoffManager.shutdown();
  }

  /**
   * Get status summary
   */
  getStatus(): {
    enabled: boolean;
    brainAvailable: boolean;
    steveAvailable: boolean;
    skillsLoaded: number;
    handoffsAvailable: boolean;
  } {
    return {
      enabled: this.settings.enabled,
      brainAvailable: this.brainClient.isAvailable(),
      steveAvailable: this.brainClient.isSteveAvailable(),
      skillsLoaded: this.skillLoader.getAllSkills().length,
      handoffsAvailable: this.handoffManager.getConfig().enabled,
    };
  }
}

// Singleton instance
let nscaIntegrationInstance: NSCAIntegration | null = null;

/**
 * Get or create the NSCA integration instance
 */
export function getNSCAIntegration(
  settings?: Partial<NSCASettings>,
  sessionId?: string,
): NSCAIntegration {
  if (!nscaIntegrationInstance) {
    nscaIntegrationInstance = new NSCAIntegration(settings, sessionId);
  }
  return nscaIntegrationInstance;
}

/**
 * Reset the NSCA integration (for testing)
 */
export function resetNSCAIntegration(): void {
  if (nscaIntegrationInstance) {
    void nscaIntegrationInstance.shutdown();
  }
  nscaIntegrationInstance = null;
}
