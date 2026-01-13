/**
 * @license
 * Copyright 2025 Google LLC
 * Portions Copyright 2025 TerminaI Authors
 * SPDX-License-Identifier: Apache-2.0
 */

// Types
export * from './types.js';

// Brain client
export {
  BrainClient,
  getBrainClient,
  resetBrainClient,
} from './brain-client.js';

// Brain tools
export {
  BRAIN_STATUS_TOOL_NAME,
  BRAIN_QUERY_TOOL_NAME,
  BRAIN_AFFECT_TOOL_NAME,
  BRAIN_MODULES_TOOL_NAME,
  BRAIN_NSL_SCAN_TOOL_NAME,
  BRAIN_PROCESS_TOOL_NAME,
  BRAIN_DREAM_TOOL_NAME,
  BrainStatusTool,
  BrainQueryTool,
  BrainAffectTool,
  BrainModulesTool,
  BrainNSLScanTool,
  BrainProcessTool,
  BrainDreamTool,
  createBrainTools,
} from './brain-tools.js';

// NSCA Integration
export {
  NSCAIntegration,
  getNSCAIntegration,
  resetNSCAIntegration,
  type NSCASettings,
  DEFAULT_NSCA_SETTINGS,
} from './nsca-integration.js';
