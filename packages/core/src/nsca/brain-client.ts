/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import {
  type BrainConfig,
  type BrainStatus,
  type BrainQueryParams,
  type BrainQueryResponse,
  type BrainProcessParams,
  type BrainProcessResponse,
  type BrainAffectParams,
  type BrainAffectResponse,
  type BrainNSLScanParams,
  type BrainNSLScanResponse,
  type BrainDreamParams,
  type BrainDreamResponse,
  type BrainModulesResponse,
  type BrainModulePorts,
  DEFAULT_BRAIN_CONFIG,
  DEFAULT_BRAIN_PORTS,
} from './types.js';

import { debugLogger } from '../utils/debugLogger.js';

/**
 * Connection state for a brain module
 */
interface ModuleConnection {
  online: boolean;
  lastCheck: Date;
  lastError?: string;
  latency?: number;
}

/**
 * Brain service client with fallback logic
 */
export class BrainClient {
  private config: BrainConfig;
  private moduleConnections: Map<string, ModuleConnection> = new Map();
  private steveOnline: boolean = false;
  private initialized: boolean = false;

  constructor(config: Partial<BrainConfig> = {}) {
    this.config = {
      ...DEFAULT_BRAIN_CONFIG,
      ...config,
      ports: {
        ...DEFAULT_BRAIN_PORTS,
        ...config.ports,
      },
      steve: {
        ...DEFAULT_BRAIN_CONFIG.steve,
        ...config.steve,
      },
    };
  }

  /**
   * Initialize the brain client and check module availability
   */
  async initialize(): Promise<void> {
    if (this.initialized) return;

    if (!this.config.enabled) {
      debugLogger.log('NSCA Brain client disabled by configuration');
      this.initialized = true;
      return;
    }

    debugLogger.log('Initializing NSCA Brain client...');

    // Check Steve availability first
    await this.checkSteveConnection();

    // Check core brain modules
    await this.checkModuleConnections();

    this.initialized = true;
    debugLogger.log('NSCA Brain client initialized');
  }

  /**
   * Check Steve embeddings server availability
   */
  private async checkSteveConnection(): Promise<void> {
    try {
      const response = await this.fetchWithTimeout(
        `http://${this.config.steve.host}:${this.config.steve.port}/health`,
        { method: 'GET' },
        this.config.connectionTimeout,
      );

      this.steveOnline = response.ok;
      debugLogger.log(
        `Steve server status: ${this.steveOnline ? 'online' : 'offline'}`,
      );
    } catch (error) {
      this.steveOnline = false;
      debugLogger.warn(
        `Steve server offline: ${error instanceof Error ? error.message : 'Unknown error'}`,
      );
    }
  }

  /**
   * Check connectivity to brain modules
   */
  private async checkModuleConnections(): Promise<void> {
    const ports = this.config.ports as BrainModulePorts;

    // Check homeostasis (main health endpoint)
    await this.checkModule('homeostasis', ports.homeostasis);

    // Check other critical modules
    const criticalModules: Array<keyof BrainModulePorts> = [
      'thalamus',
      'hippocampus',
      'amygdala',
      'acc',
      'dmn',
    ];

    await Promise.all(
      criticalModules.map((module) => this.checkModule(module, ports[module])),
    );
  }

  /**
   * Check a single module's connectivity
   */
  private async checkModule(name: string, port: number): Promise<void> {
    const start = Date.now();

    try {
      const response = await this.fetchWithTimeout(
        `http://${this.config.host}:${port}/health`,
        { method: 'GET' },
        this.config.connectionTimeout,
      );

      const latency = Date.now() - start;

      this.moduleConnections.set(name, {
        online: response.ok,
        lastCheck: new Date(),
        latency,
      });
    } catch (error) {
      this.moduleConnections.set(name, {
        online: false,
        lastCheck: new Date(),
        lastError: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  /**
   * Fetch with timeout wrapper
   */
  private async fetchWithTimeout(
    url: string,
    options: RequestInit,
    timeout: number,
  ): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      return response;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * Make a request to a brain module with retry logic
   */
  private async brainRequest<T>(
    module: keyof BrainModulePorts,
    endpoint: string,
    method: 'GET' | 'POST' = 'GET',
    body?: unknown,
  ): Promise<T | null> {
    if (!this.config.enabled) {
      return null;
    }

    const ports = this.config.ports as BrainModulePorts;
    const port = ports[module];
    const url = `http://${this.config.host}:${port}${endpoint}`;

    let lastError: Error | null = null;

    for (let attempt = 0; attempt < this.config.retryAttempts; attempt++) {
      try {
        const options: RequestInit = {
          method,
          headers: {
            'Content-Type': 'application/json',
          },
        };

        if (body && method === 'POST') {
          options.body = JSON.stringify(body);
        }

        const response = await this.fetchWithTimeout(
          url,
          options,
          this.config.connectionTimeout,
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return (await response.json()) as T;
      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));
        debugLogger.warn(
          `Brain request to ${module}${endpoint} failed (attempt ${attempt + 1}/${this.config.retryAttempts}): ${lastError.message}`,
        );

        if (attempt < this.config.retryAttempts - 1) {
          await this.sleep(this.config.retryDelay * Math.pow(2, attempt));
        }
      }
    }

    // If graceful degradation is enabled, return null instead of throwing
    if (this.config.gracefulDegradation) {
      debugLogger.warn(
        `Brain module ${module} unavailable, degrading gracefully`,
      );
      return null;
    }

    throw (
      lastError || new Error(`Failed to connect to brain module: ${module}`)
    );
  }

  /**
   * Sleep helper
   */
  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Get embeddings using Steve or fallback
   */
  async getEmbeddings(text: string): Promise<number[] | null> {
    if (!this.config.enabled) {
      return null;
    }

    // Try Steve first
    if (this.steveOnline) {
      try {
        const response = await this.fetchWithTimeout(
          `http://${this.config.steve.host}:${this.config.steve.port}/v1/embeddings`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              input: text,
              model: this.config.steve.embedding_model,
            }),
          },
          this.config.connectionTimeout,
        );

        if (response.ok) {
          const data = (await response.json()) as {
            data: Array<{ embedding: number[] }>;
          };
          return data.data?.[0]?.embedding || null;
        }
      } catch (_error) {
        debugLogger.warn('Steve embeddings failed, trying fallback');
        this.steveOnline = false;
      }
    }

    // Fallback to local Docker
    if (this.config.steve.fallback.mode === 'local_docker') {
      try {
        const response = await this.fetchWithTimeout(
          `http://localhost:${this.config.steve.fallback.embeddings_port}/v1/embeddings`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: text }),
          },
          this.config.connectionTimeout,
        );

        if (response.ok) {
          const data = (await response.json()) as {
            data: Array<{ embedding: number[] }>;
          };
          return data.data?.[0]?.embedding || null;
        }
      } catch (_error) {
        debugLogger.warn('Local embeddings fallback also failed');
      }
    }

    return null;
  }

  // =========================================================================
  // Brain Tool Interface Methods
  // =========================================================================

  /**
   * Get brain status (Tier A)
   */
  async getStatus(): Promise<BrainStatus | null> {
    const result = await this.brainRequest<BrainStatus>(
      'homeostasis',
      '/health',
    );

    // Add connection info if result is null
    if (result === null && this.config.gracefulDegradation) {
      return {
        online: false,
        phi: 0,
        coherence: 0,
        drift: 0,
        modules: Object.fromEntries(
          Array.from(this.moduleConnections.entries()).map(([k, v]) => [
            k,
            {
              online: v.online,
              latency: v.latency,
              lastCheck: v.lastCheck.toISOString(),
            },
          ]),
        ),
        timestamp: new Date().toISOString(),
      };
    }

    return result;
  }

  /**
   * Query brain memory (Tier A)
   */
  async query(params: BrainQueryParams): Promise<BrainQueryResponse | null> {
    return this.brainRequest<BrainQueryResponse>(
      'hippocampus',
      '/query',
      'POST',
      params,
    );
  }

  /**
   * Get or modulate affect state (Tier A/B based on action)
   */
  async affect(params: BrainAffectParams): Promise<BrainAffectResponse | null> {
    return this.brainRequest<BrainAffectResponse>(
      'amygdala',
      '/affect',
      'POST',
      params,
    );
  }

  /**
   * Get module status (Tier A)
   */
  async getModules(): Promise<BrainModulesResponse | null> {
    const result = await this.brainRequest<BrainModulesResponse>(
      'homeostasis',
      '/modules',
    );

    // Provide local status if brain is offline
    if (result === null && this.config.gracefulDegradation) {
      const modules = Array.from(this.moduleConnections.entries()).map(
        ([name, conn]) => ({
          name,
          port:
            (this.config.ports as BrainModulePorts)[
              name as keyof BrainModulePorts
            ] || 0,
          online: conn.online,
          latency: conn.latency,
          lastError: conn.lastError,
          lastSuccess: conn.lastCheck.toISOString(),
        }),
      );

      return {
        modules,
        healthyCount: modules.filter((m) => m.online).length,
        totalCount: modules.length,
        timestamp: new Date().toISOString(),
      };
    }

    return result;
  }

  /**
   * Run NSL scan (Tier A)
   */
  async nslScan(
    params: BrainNSLScanParams,
  ): Promise<BrainNSLScanResponse | null> {
    return this.brainRequest<BrainNSLScanResponse>(
      'acc',
      '/nsl/scan',
      'POST',
      params,
    );
  }

  /**
   * Process information into memory (Tier B)
   */
  async process(
    params: BrainProcessParams,
  ): Promise<BrainProcessResponse | null> {
    return this.brainRequest<BrainProcessResponse>(
      'thalamus',
      '/input',
      'POST',
      params,
    );
  }

  /**
   * Trigger dream processing (Tier B/C based on mode)
   */
  async dream(params: BrainDreamParams): Promise<BrainDreamResponse | null> {
    return this.brainRequest<BrainDreamResponse>(
      'dmn',
      '/dream',
      'POST',
      params,
    );
  }

  // =========================================================================
  // State and utility methods
  // =========================================================================

  /**
   * Check if brain is available
   */
  isAvailable(): boolean {
    return (
      this.config.enabled &&
      (this.moduleConnections.get('homeostasis')?.online ?? false)
    );
  }

  /**
   * Check if Steve is available
   */
  isSteveAvailable(): boolean {
    return this.steveOnline;
  }

  /**
   * Get configuration
   */
  getConfig(): BrainConfig {
    return { ...this.config };
  }

  /**
   * Update configuration
   */
  updateConfig(config: Partial<BrainConfig>): void {
    this.config = {
      ...this.config,
      ...config,
      ports: {
        ...this.config.ports,
        ...config.ports,
      },
      steve: {
        ...this.config.steve,
        ...config.steve,
      },
    };
    this.initialized = false;
  }

  /**
   * Refresh module connections
   */
  async refresh(): Promise<void> {
    this.initialized = false;
    await this.initialize();
  }
}

// Singleton instance
let brainClientInstance: BrainClient | null = null;

/**
 * Get or create the brain client instance
 */
export function getBrainClient(config?: Partial<BrainConfig>): BrainClient {
  if (!brainClientInstance) {
    brainClientInstance = new BrainClient(config);
  } else if (config) {
    brainClientInstance.updateConfig(config);
  }
  return brainClientInstance;
}

/**
 * Reset the brain client (for testing)
 */
export function resetBrainClient(): void {
  brainClientInstance = null;
}
