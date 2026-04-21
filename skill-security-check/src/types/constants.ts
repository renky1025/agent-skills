// src/types/constants.ts
// Constants for skill-security-check

// ============================================================================
// Risk Categories
// ============================================================================

export const RISK_CATEGORIES = {
  LOW_TRUST_REPO: 'low-trust-repo',
  UNVERIFIED_AUTHOR: 'unverified-author',
  STALE_PROJECT: 'stale-project',
  UNTRUSTED_AUTHOR: 'untrusted-author',
  UNDECLARED_CAPABILITY: 'undeclared-capability',
  DECLARED_NOT_IMPLEMENTED: 'declared-not-implemented',
  BEHAVIOR_MISMATCH: 'behavior-mismatch',
  MULTI_LAYER_ENCODING: 'multi-layer-encoding',
  RUNTIME_CODE_GENERATION: 'runtime-code-generation',
  DISGUISED_OPERATION: 'disguised-operation',
  CODE_OBFUSCATION: 'code-obfuscation',
  CREDENTIAL_DATA_FLOW: 'credential-data-flow',
  ATTACK_CHAIN_DETECTED: 'attack-chain-detected'
} as const;

// ============================================================================
// Severity Weights
// ============================================================================

export const SEVERITY_WEIGHTS = {
  info: 0,
  low: 1,
  medium: 3,
  high: 6,
  critical: 10
} as const;

// ============================================================================
// Confidence Thresholds
// ============================================================================

export const CONFIDENCE_THRESHOLDS = {
  HIGH: 0.8,
  MEDIUM: 0.5,
  LOW: 0.3
} as const;

// ============================================================================
// Baseline Version
// ============================================================================

export const BASELINE_VERSION = '1.0';
