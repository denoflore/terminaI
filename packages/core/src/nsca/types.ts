/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Brain module ports configuration
 */
export interface BrainModulePorts {
  // Core Brain Modules
  hippocampus: number; // 8300 - Fast encoding + dreams
  neocortex: number; // 8301 - Slow consolidation
  thalamus: number; // 8302 - Sensory gateway (ALL INPUT)
  amygdala: number; // 8303 - 8D VACTS-M emotion
  basal_ganglia: number; // 8304 - Spite Q-learning
  acc: number; // 8305 - SALIENCE SWITCH (CEN vs DMN)
  cerebellum: number; // 8306 - OH_SHIT cascades
  hypothalamus: number; // 8307 - Spite reservoir + drives
  brainstem: number; // 8308 - Multimodal arousal
  dmn: number; // 8309 - Background incubation
  sleep_controller: number; // 8310 - Consolidation timing
  homeostasis: number; // 8311 - System stability (D_t)

  // Parallel Architecture
  self_watcher: number; // 8312 - Observer plane (SELF)
  consolidator: number; // 8313 - Memory pipeline
  promotion_gate: number; // 8314 - Dream→Wake bridge
  hippocampus_dream: number; // 8315 - Dream memory (DREAM)

  // Infrastructure
  qdrant: number; // 6333 - Vector storage
  holographic_memory: number; // 8200 - Consciousness substrate
  openmemory: number; // 8181 - 5-sector cognitive memory
  llama_embeddings: number; // 8280 - E5-Mistral-7B (4096D)
  llama_subconscious: number; // 8281 - Ministral-3B background
  dashboard: number; // 8400 - Monitoring UI
}

/**
 * Default port configuration
 */
export const DEFAULT_BRAIN_PORTS: BrainModulePorts = {
  hippocampus: 8300,
  neocortex: 8301,
  thalamus: 8302,
  amygdala: 8303,
  basal_ganglia: 8304,
  acc: 8305,
  cerebellum: 8306,
  hypothalamus: 8307,
  brainstem: 8308,
  dmn: 8309,
  sleep_controller: 8310,
  homeostasis: 8311,
  self_watcher: 8312,
  consolidator: 8313,
  promotion_gate: 8314,
  hippocampus_dream: 8315,
  qdrant: 6333,
  holographic_memory: 8200,
  openmemory: 8181,
  llama_embeddings: 8280,
  llama_subconscious: 8281,
  dashboard: 8400,
};

/**
 * Steve server configuration (embeddings server)
 */
export interface SteveConfig {
  host: string;
  port: number;
  embedding_model: string;
  subconscious_model: string;
  fallback: {
    mode: 'local_docker' | 'disabled';
    embeddings_port: number;
    subconscious_port: number;
  };
}

/**
 * Default Steve configuration
 */
export const DEFAULT_STEVE_CONFIG: SteveConfig = {
  host: '10.10.0.10',
  port: 1234,
  embedding_model: 'text-embedding-e5-mistral-7b-instruct',
  subconscious_model: 'ministral-3-3b-instruct-2512@q8_k_xl',
  fallback: {
    mode: 'local_docker',
    embeddings_port: 8280,
    subconscious_port: 8281,
  },
};

/**
 * Brain connection configuration
 */
export interface BrainConfig {
  host: string;
  ports: Partial<BrainModulePorts>;
  steve: SteveConfig;
  enabled: boolean;
  gracefulDegradation: boolean;
  connectionTimeout: number;
  retryAttempts: number;
  retryDelay: number;
}

/**
 * Default brain configuration
 */
export const DEFAULT_BRAIN_CONFIG: BrainConfig = {
  host: 'localhost',
  ports: DEFAULT_BRAIN_PORTS,
  steve: DEFAULT_STEVE_CONFIG,
  enabled: true,
  gracefulDegradation: true,
  connectionTimeout: 5000,
  retryAttempts: 3,
  retryDelay: 1000,
};

/**
 * VACTS-M 8D emotion state
 */
export interface VACTSState {
  valence: number; // -1 to 1
  arousal: number; // 0 to 1
  confidence: number; // 0 to 1
  tension: number; // 0 to 1
  spite: number; // 0 to 1 (Claudette-specific)
  momentum: number; // -1 to 1
  curiosity: number; // 0 to 1
  coherence: number; // 0 to 1
}

/**
 * Brain status response
 */
export interface BrainStatus {
  online: boolean;
  phi: number; // Φ̂ - integrated information
  coherence: number; // System coherence
  drift: number; // Value drift measure
  modules: {
    [key: string]: {
      online: boolean;
      latency?: number;
      lastCheck?: string;
    };
  };
  timestamp: string;
}

/**
 * Brain query parameters
 */
export interface BrainQueryParams {
  query: string;
  context?: string;
  topK?: number;
  threshold?: number;
  sectors?: string[];
}

/**
 * Memory entry from brain query
 */
export interface MemoryEntry {
  id: string;
  content: string;
  resonance: number; // How strongly it resonates
  sector: string; // Which memory sector
  timestamp: string;
  metadata?: Record<string, unknown>;
}

/**
 * Brain query response
 */
export interface BrainQueryResponse {
  memories: MemoryEntry[];
  totalResonance: number;
  queryTime: number;
}

/**
 * Brain process parameters
 */
export interface BrainProcessParams {
  content: string;
  source: string;
  type?: 'interaction' | 'observation' | 'insight' | 'decision';
  importance?: number;
  associations?: string[];
}

/**
 * Brain process response
 */
export interface BrainProcessResponse {
  processed: boolean;
  memoryId?: string;
  consolidationQueue?: boolean;
  timestamp: string;
}

/**
 * Brain affect parameters
 */
export interface BrainAffectParams {
  action: 'get' | 'modulate';
  stimulus?: string;
  intensity?: number;
  targetDimension?: keyof VACTSState;
}

/**
 * Brain affect response
 */
export interface BrainAffectResponse {
  state: VACTSState;
  previousState?: VACTSState;
  delta?: Partial<VACTSState>;
  timestamp: string;
}

/**
 * NSL (Negative Space Learning) scan parameters
 */
export interface BrainNSLScanParams {
  context: string;
  depth?: 'shallow' | 'medium' | 'deep';
  focus?: string[];
}

/**
 * NSL absence detection result
 */
export interface NSLAbsence {
  category: string;
  description: string;
  importance: number;
  suggestedQuestions?: string[];
}

/**
 * Brain NSL scan response
 */
export interface BrainNSLScanResponse {
  absences: NSLAbsence[];
  scanDepth: string;
  scanTime: number;
  recommendations: string[];
}

/**
 * Brain dream parameters
 */
export interface BrainDreamParams {
  mode: 'consolidate' | 'integrate' | 'deep_clean' | 'wander';
  duration?: number;
  focus?: string;
}

/**
 * Brain dream response
 */
export interface BrainDreamResponse {
  completed: boolean;
  mode: string;
  memoriesProcessed?: number;
  connectionsFound?: number;
  duration: number;
  insights?: string[];
}

/**
 * Module status entry
 */
export interface ModuleStatus {
  name: string;
  port: number;
  online: boolean;
  latency?: number;
  version?: string;
  lastError?: string;
  lastSuccess?: string;
}

/**
 * Brain modules response
 */
export interface BrainModulesResponse {
  modules: ModuleStatus[];
  healthyCount: number;
  totalCount: number;
  timestamp: string;
}

/**
 * Approval tier for brain operations
 */
export type BrainApprovalTier = 'A' | 'B' | 'C';

/**
 * Brain tool definition
 */
export interface BrainToolDefinition {
  name: string;
  description: string;
  tier: BrainApprovalTier;
  endpoint: string;
  port: keyof BrainModulePorts;
}

/**
 * All brain tool definitions
 */
export const BRAIN_TOOL_DEFINITIONS: BrainToolDefinition[] = [
  {
    name: 'brain_status',
    description: 'Get overall brain health, Φ̂, coherence, and drift metrics',
    tier: 'A',
    endpoint: '/health',
    port: 'homeostasis',
  },
  {
    name: 'brain_query',
    description: 'Query memory with resonance-based retrieval',
    tier: 'A',
    endpoint: '/query',
    port: 'hippocampus',
  },
  {
    name: 'brain_affect',
    description: 'Get or modulate VACTS-M emotional state',
    tier: 'A', // 'get' action is A, 'modulate' is B - handled in tool
    endpoint: '/affect',
    port: 'amygdala',
  },
  {
    name: 'brain_modules',
    description: 'Get per-module health status',
    tier: 'A',
    endpoint: '/modules',
    port: 'homeostasis',
  },
  {
    name: 'brain_nsl_scan',
    description: 'Run NSL absence detection on context',
    tier: 'A',
    endpoint: '/nsl/scan',
    port: 'acc',
  },
  {
    name: 'brain_process',
    description: 'Process and store information in memory',
    tier: 'B',
    endpoint: '/input',
    port: 'thalamus',
  },
  {
    name: 'brain_dream',
    description: 'Trigger DMN processing for memory consolidation',
    tier: 'B', // 'deep_clean' mode is C - handled in tool
    endpoint: '/dream',
    port: 'dmn',
  },
];
