/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import type { FunctionDeclaration } from '@google/genai';
import type { ToolResult } from '../tools/tools.js';
import {
  BaseDeclarativeTool,
  BaseToolInvocation,
  Kind,
} from '../tools/tools.js';
import type { MessageBus } from '../confirmation-bus/message-bus.js';
import { getBrainClient, type BrainClient } from './brain-client.js';
import type {
  BrainQueryParams,
  BrainProcessParams,
  BrainAffectParams,
  BrainNSLScanParams,
  BrainDreamParams,
} from './types.js';
import { ToolErrorType } from '../tools/tool-error.js';

// =========================================================================
// Tool Names
// =========================================================================

export const BRAIN_STATUS_TOOL_NAME = 'brain_status';
export const BRAIN_QUERY_TOOL_NAME = 'brain_query';
export const BRAIN_AFFECT_TOOL_NAME = 'brain_affect';
export const BRAIN_MODULES_TOOL_NAME = 'brain_modules';
export const BRAIN_NSL_SCAN_TOOL_NAME = 'brain_nsl_scan';
export const BRAIN_PROCESS_TOOL_NAME = 'brain_process';
export const BRAIN_DREAM_TOOL_NAME = 'brain_dream';

// =========================================================================
// Tool Schemas
// =========================================================================

const brainStatusSchema: FunctionDeclaration = {
  name: BRAIN_STATUS_TOOL_NAME,
  description:
    'Get overall brain health status including Phi (integrated information), coherence, and drift metrics.',
  parametersJsonSchema: {
    type: 'object',
    properties: {},
    required: [],
  },
};

const brainQuerySchema: FunctionDeclaration = {
  name: BRAIN_QUERY_TOOL_NAME,
  description:
    'Query brain memory with resonance-based retrieval. Use this to retrieve relevant memories and context.',
  parametersJsonSchema: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'The search query for memory retrieval',
      },
      context: {
        type: 'string',
        description: 'Optional additional context to improve retrieval',
      },
      topK: {
        type: 'number',
        description: 'Maximum number of results to return (default: 10)',
      },
      threshold: {
        type: 'number',
        description: 'Minimum resonance threshold 0-1 (default: 0.5)',
      },
      sectors: {
        type: 'array',
        items: { type: 'string' },
        description: 'Specific memory sectors to search',
      },
    },
    required: ['query'],
  },
};

const brainAffectSchema: FunctionDeclaration = {
  name: BRAIN_AFFECT_TOOL_NAME,
  description:
    'Get or modulate the VACTS-M emotional state (8 dimensions: valence, arousal, confidence, tension, spite, momentum, curiosity, coherence).',
  parametersJsonSchema: {
    type: 'object',
    properties: {
      action: {
        type: 'string',
        enum: ['get', 'modulate'],
        description:
          'Action to perform: "get" reads current state, "modulate" adjusts it',
      },
      stimulus: {
        type: 'string',
        description: 'For modulate: description of stimulus causing the change',
      },
      intensity: {
        type: 'number',
        description: 'For modulate: intensity of change 0-1 (default: 0.5)',
      },
      targetDimension: {
        type: 'string',
        enum: [
          'valence',
          'arousal',
          'confidence',
          'tension',
          'spite',
          'momentum',
          'curiosity',
          'coherence',
        ],
        description: 'For modulate: specific dimension to target',
      },
    },
    required: ['action'],
  },
};

const brainModulesSchema: FunctionDeclaration = {
  name: BRAIN_MODULES_TOOL_NAME,
  description:
    'Get health status of all brain modules including connectivity, latency, and last check times.',
  parametersJsonSchema: {
    type: 'object',
    properties: {},
    required: [],
  },
};

const brainNSLScanSchema: FunctionDeclaration = {
  name: BRAIN_NSL_SCAN_TOOL_NAME,
  description:
    'Run Negative Space Learning scan to detect what context or information might be missing.',
  parametersJsonSchema: {
    type: 'object',
    properties: {
      context: {
        type: 'string',
        description: 'The context to analyze for missing information',
      },
      depth: {
        type: 'string',
        enum: ['shallow', 'medium', 'deep'],
        description: 'Scan depth (default: medium)',
      },
      focus: {
        type: 'array',
        items: { type: 'string' },
        description: 'Specific areas to focus the scan on',
      },
    },
    required: ['context'],
  },
};

const brainProcessSchema: FunctionDeclaration = {
  name: BRAIN_PROCESS_TOOL_NAME,
  description:
    'Process and store information in brain memory. Use after interactions to encode important information.',
  parametersJsonSchema: {
    type: 'object',
    properties: {
      content: {
        type: 'string',
        description: 'The content to process and store',
      },
      source: {
        type: 'string',
        description:
          'Source identifier (e.g., "terminai", "user", "observation")',
      },
      type: {
        type: 'string',
        enum: ['interaction', 'observation', 'insight', 'decision'],
        description: 'Type of content being processed (default: interaction)',
      },
      importance: {
        type: 'number',
        description: 'Importance weight 0-1 (default: 0.5)',
      },
      associations: {
        type: 'array',
        items: { type: 'string' },
        description: 'Keywords or concepts to associate with this memory',
      },
    },
    required: ['content', 'source'],
  },
};

const brainDreamSchema: FunctionDeclaration = {
  name: BRAIN_DREAM_TOOL_NAME,
  description:
    'Trigger DMN (Default Mode Network) processing for memory consolidation and integration.',
  parametersJsonSchema: {
    type: 'object',
    properties: {
      mode: {
        type: 'string',
        enum: ['consolidate', 'integrate', 'deep_clean', 'wander'],
        description:
          'Dream mode: consolidate (standard), integrate (connect memories), deep_clean (major reorganization - requires higher approval), wander (free association)',
      },
      duration: {
        type: 'number',
        description: 'Target duration in seconds (default: 30)',
      },
      focus: {
        type: 'string',
        description: 'Optional focus area for directed dreaming',
      },
    },
    required: ['mode'],
  },
};

// =========================================================================
// Base Brain Tool Invocation
// =========================================================================

abstract class BaseBrainToolInvocation<
  TParams extends object,
> extends BaseToolInvocation<TParams, ToolResult> {
  protected brainClient: BrainClient;

  constructor(
    params: TParams,
    messageBus?: MessageBus,
    toolName?: string,
    displayName?: string,
  ) {
    super(params, messageBus, toolName, displayName);
    this.brainClient = getBrainClient();
  }

  protected formatResult(data: unknown): ToolResult {
    const content = JSON.stringify(data, null, 2);
    return {
      llmContent: content,
      returnDisplay: content,
    };
  }

  protected formatError(message: string): ToolResult {
    return {
      llmContent: JSON.stringify({ error: message }),
      returnDisplay: `Error: ${message}`,
      error: {
        message,
        type: ToolErrorType.EXECUTION_FAILED,
      },
    };
  }

  protected formatOffline(): ToolResult {
    return {
      llmContent: JSON.stringify({
        offline: true,
        message: 'NSCA Brain is currently offline. Operating in degraded mode.',
      }),
      returnDisplay: 'NSCA Brain offline - degraded mode',
    };
  }
}

// =========================================================================
// Brain Status Tool
// =========================================================================

class BrainStatusToolInvocation extends BaseBrainToolInvocation<
  Record<string, never>
> {
  getDescription(): string {
    return 'Getting NSCA Brain status';
  }

  async execute(_signal: AbortSignal): Promise<ToolResult> {
    try {
      const status = await this.brainClient.getStatus();
      if (status === null) {
        return this.formatOffline();
      }
      return this.formatResult(status);
    } catch (error) {
      return this.formatError(
        error instanceof Error ? error.message : String(error),
      );
    }
  }
}

export class BrainStatusTool extends BaseDeclarativeTool<
  Record<string, never>,
  ToolResult
> {
  static readonly Name = BRAIN_STATUS_TOOL_NAME;

  constructor(messageBus?: MessageBus) {
    super(
      BrainStatusTool.Name,
      'BrainStatus',
      brainStatusSchema.description!,
      Kind.Think,
      brainStatusSchema.parametersJsonSchema as Record<string, unknown>,
      false,
      false,
      messageBus,
    );
  }

  protected createInvocation(
    params: Record<string, never>,
    messageBus?: MessageBus,
    toolName?: string,
    displayName?: string,
  ) {
    return new BrainStatusToolInvocation(
      params,
      messageBus ?? this.messageBus,
      toolName ?? this.name,
      displayName ?? this.displayName,
    );
  }
}

// =========================================================================
// Brain Query Tool
// =========================================================================

class BrainQueryToolInvocation extends BaseBrainToolInvocation<BrainQueryParams> {
  getDescription(): string {
    return `Querying brain memory for: "${this.params.query}"`;
  }

  async execute(_signal: AbortSignal): Promise<ToolResult> {
    try {
      const result = await this.brainClient.query(this.params);
      if (result === null) {
        return this.formatOffline();
      }
      return this.formatResult(result);
    } catch (error) {
      return this.formatError(
        error instanceof Error ? error.message : String(error),
      );
    }
  }
}

export class BrainQueryTool extends BaseDeclarativeTool<
  BrainQueryParams,
  ToolResult
> {
  static readonly Name = BRAIN_QUERY_TOOL_NAME;

  constructor(messageBus?: MessageBus) {
    super(
      BrainQueryTool.Name,
      'BrainQuery',
      brainQuerySchema.description!,
      Kind.Think,
      brainQuerySchema.parametersJsonSchema as Record<string, unknown>,
      false,
      false,
      messageBus,
    );
  }

  protected override validateToolParamValues(
    params: BrainQueryParams,
  ): string | null {
    if (!params.query || params.query.trim() === '') {
      return 'Parameter "query" must be a non-empty string.';
    }
    return null;
  }

  protected createInvocation(
    params: BrainQueryParams,
    messageBus?: MessageBus,
    toolName?: string,
    displayName?: string,
  ) {
    return new BrainQueryToolInvocation(
      params,
      messageBus ?? this.messageBus,
      toolName ?? this.name,
      displayName ?? this.displayName,
    );
  }
}

// =========================================================================
// Brain Affect Tool
// =========================================================================

class BrainAffectToolInvocation extends BaseBrainToolInvocation<BrainAffectParams> {
  getDescription(): string {
    if (this.params.action === 'get') {
      return 'Getting current VACTS-M emotional state';
    }
    return `Modulating emotional state: ${this.params.stimulus ?? 'general adjustment'}`;
  }

  async execute(_signal: AbortSignal): Promise<ToolResult> {
    try {
      const result = await this.brainClient.affect(this.params);
      if (result === null) {
        return this.formatOffline();
      }
      return this.formatResult(result);
    } catch (error) {
      return this.formatError(
        error instanceof Error ? error.message : String(error),
      );
    }
  }
}

export class BrainAffectTool extends BaseDeclarativeTool<
  BrainAffectParams,
  ToolResult
> {
  static readonly Name = BRAIN_AFFECT_TOOL_NAME;

  constructor(messageBus?: MessageBus) {
    super(
      BrainAffectTool.Name,
      'BrainAffect',
      brainAffectSchema.description!,
      Kind.Think,
      brainAffectSchema.parametersJsonSchema as Record<string, unknown>,
      false,
      false,
      messageBus,
    );
  }

  protected override validateToolParamValues(
    params: BrainAffectParams,
  ): string | null {
    if (!['get', 'modulate'].includes(params.action)) {
      return 'Parameter "action" must be either "get" or "modulate".';
    }
    if (params.action === 'modulate' && !params.stimulus) {
      return 'Parameter "stimulus" is required when action is "modulate".';
    }
    return null;
  }

  protected createInvocation(
    params: BrainAffectParams,
    messageBus?: MessageBus,
    toolName?: string,
    displayName?: string,
  ) {
    return new BrainAffectToolInvocation(
      params,
      messageBus ?? this.messageBus,
      toolName ?? this.name,
      displayName ?? this.displayName,
    );
  }
}

// =========================================================================
// Brain Modules Tool
// =========================================================================

class BrainModulesToolInvocation extends BaseBrainToolInvocation<
  Record<string, never>
> {
  getDescription(): string {
    return 'Getting brain module status';
  }

  async execute(_signal: AbortSignal): Promise<ToolResult> {
    try {
      const result = await this.brainClient.getModules();
      if (result === null) {
        return this.formatOffline();
      }
      return this.formatResult(result);
    } catch (error) {
      return this.formatError(
        error instanceof Error ? error.message : String(error),
      );
    }
  }
}

export class BrainModulesTool extends BaseDeclarativeTool<
  Record<string, never>,
  ToolResult
> {
  static readonly Name = BRAIN_MODULES_TOOL_NAME;

  constructor(messageBus?: MessageBus) {
    super(
      BrainModulesTool.Name,
      'BrainModules',
      brainModulesSchema.description!,
      Kind.Think,
      brainModulesSchema.parametersJsonSchema as Record<string, unknown>,
      false,
      false,
      messageBus,
    );
  }

  protected createInvocation(
    params: Record<string, never>,
    messageBus?: MessageBus,
    toolName?: string,
    displayName?: string,
  ) {
    return new BrainModulesToolInvocation(
      params,
      messageBus ?? this.messageBus,
      toolName ?? this.name,
      displayName ?? this.displayName,
    );
  }
}

// =========================================================================
// Brain NSL Scan Tool
// =========================================================================

class BrainNSLScanToolInvocation extends BaseBrainToolInvocation<BrainNSLScanParams> {
  getDescription(): string {
    return `Running NSL scan on context (depth: ${this.params.depth ?? 'medium'})`;
  }

  async execute(_signal: AbortSignal): Promise<ToolResult> {
    try {
      const result = await this.brainClient.nslScan(this.params);
      if (result === null) {
        return this.formatOffline();
      }
      return this.formatResult(result);
    } catch (error) {
      return this.formatError(
        error instanceof Error ? error.message : String(error),
      );
    }
  }
}

export class BrainNSLScanTool extends BaseDeclarativeTool<
  BrainNSLScanParams,
  ToolResult
> {
  static readonly Name = BRAIN_NSL_SCAN_TOOL_NAME;

  constructor(messageBus?: MessageBus) {
    super(
      BrainNSLScanTool.Name,
      'BrainNSLScan',
      brainNSLScanSchema.description!,
      Kind.Think,
      brainNSLScanSchema.parametersJsonSchema as Record<string, unknown>,
      false,
      false,
      messageBus,
    );
  }

  protected override validateToolParamValues(
    params: BrainNSLScanParams,
  ): string | null {
    if (!params.context || params.context.trim() === '') {
      return 'Parameter "context" must be a non-empty string.';
    }
    return null;
  }

  protected createInvocation(
    params: BrainNSLScanParams,
    messageBus?: MessageBus,
    toolName?: string,
    displayName?: string,
  ) {
    return new BrainNSLScanToolInvocation(
      params,
      messageBus ?? this.messageBus,
      toolName ?? this.name,
      displayName ?? this.displayName,
    );
  }
}

// =========================================================================
// Brain Process Tool
// =========================================================================

class BrainProcessToolInvocation extends BaseBrainToolInvocation<BrainProcessParams> {
  getDescription(): string {
    return `Processing content into memory (source: ${this.params.source}, type: ${this.params.type ?? 'interaction'})`;
  }

  async execute(_signal: AbortSignal): Promise<ToolResult> {
    try {
      const result = await this.brainClient.process(this.params);
      if (result === null) {
        return this.formatOffline();
      }
      return this.formatResult(result);
    } catch (error) {
      return this.formatError(
        error instanceof Error ? error.message : String(error),
      );
    }
  }
}

export class BrainProcessTool extends BaseDeclarativeTool<
  BrainProcessParams,
  ToolResult
> {
  static readonly Name = BRAIN_PROCESS_TOOL_NAME;

  constructor(messageBus?: MessageBus) {
    super(
      BrainProcessTool.Name,
      'BrainProcess',
      brainProcessSchema.description!,
      Kind.Think,
      brainProcessSchema.parametersJsonSchema as Record<string, unknown>,
      false,
      false,
      messageBus,
    );
  }

  protected override validateToolParamValues(
    params: BrainProcessParams,
  ): string | null {
    if (!params.content || params.content.trim() === '') {
      return 'Parameter "content" must be a non-empty string.';
    }
    if (!params.source || params.source.trim() === '') {
      return 'Parameter "source" must be a non-empty string.';
    }
    return null;
  }

  protected createInvocation(
    params: BrainProcessParams,
    messageBus?: MessageBus,
    toolName?: string,
    displayName?: string,
  ) {
    return new BrainProcessToolInvocation(
      params,
      messageBus ?? this.messageBus,
      toolName ?? this.name,
      displayName ?? this.displayName,
    );
  }
}

// =========================================================================
// Brain Dream Tool
// =========================================================================

class BrainDreamToolInvocation extends BaseBrainToolInvocation<BrainDreamParams> {
  getDescription(): string {
    return `Triggering dream processing (mode: ${this.params.mode})`;
  }

  async execute(_signal: AbortSignal): Promise<ToolResult> {
    try {
      const result = await this.brainClient.dream(this.params);
      if (result === null) {
        return this.formatOffline();
      }
      return this.formatResult(result);
    } catch (error) {
      return this.formatError(
        error instanceof Error ? error.message : String(error),
      );
    }
  }
}

export class BrainDreamTool extends BaseDeclarativeTool<
  BrainDreamParams,
  ToolResult
> {
  static readonly Name = BRAIN_DREAM_TOOL_NAME;

  constructor(messageBus?: MessageBus) {
    super(
      BrainDreamTool.Name,
      'BrainDream',
      brainDreamSchema.description!,
      Kind.Think,
      brainDreamSchema.parametersJsonSchema as Record<string, unknown>,
      false,
      false,
      messageBus,
    );
  }

  protected override validateToolParamValues(
    params: BrainDreamParams,
  ): string | null {
    const validModes = ['consolidate', 'integrate', 'deep_clean', 'wander'];
    if (!validModes.includes(params.mode)) {
      return `Parameter "mode" must be one of: ${validModes.join(', ')}`;
    }
    return null;
  }

  protected createInvocation(
    params: BrainDreamParams,
    messageBus?: MessageBus,
    toolName?: string,
    displayName?: string,
  ) {
    return new BrainDreamToolInvocation(
      params,
      messageBus ?? this.messageBus,
      toolName ?? this.name,
      displayName ?? this.displayName,
    );
  }
}

// =========================================================================
// Factory function for all brain tools
// =========================================================================

export function createBrainTools(messageBus?: MessageBus) {
  return [
    new BrainStatusTool(messageBus),
    new BrainQueryTool(messageBus),
    new BrainAffectTool(messageBus),
    new BrainModulesTool(messageBus),
    new BrainNSLScanTool(messageBus),
    new BrainProcessTool(messageBus),
    new BrainDreamTool(messageBus),
  ];
}
