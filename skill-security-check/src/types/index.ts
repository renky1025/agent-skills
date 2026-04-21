// src/types/index.ts
// Core type definitions for skill-security-check

// ============================================================================
// Scan Context Types
// ============================================================================

export interface ScanContext {
  source: SourceInfo;
  files: CodeFile[];
  declaredCapabilities: Capability[];
  reviewBaseline: ReviewBaseline;
}

export interface SourceInfo {
  kind: 'local' | 'github' | 'npm' | 'pypi' | 'crates.io';
  url?: string;
  author?: string;
  repoStats?: RepoStats;
  dependencies: DependencyInfo[];
}

export interface RepoStats {
  stars: number;
  forks: number;
  createdAt: Date;
  lastUpdated: Date;
  isVerified: boolean;
}

export interface DependencyInfo {
  name: string;
  version: string;
  source: string;
}

// ============================================================================
// Code File Types
// ============================================================================

export interface CodeFile {
  path: string;
  content: string;
  ast?: any;
  language: string;
  imports: Import[];
  exports: Export[];
}

export interface Import {
  source: string;
  names: string[];
  isDynamic: boolean;
}

export interface Export {
  name: string;
  type: 'function' | 'class' | 'variable' | 'default';
}

export interface Capability {
  name: string;
  type: string;
  required: boolean;
  description: string;
}

// ============================================================================
// Risk Finding Types
// ============================================================================

export interface RiskFinding {
  id: string;
  file: string;
  line: number;
  column: number;
  layer: 'source' | 'capability' | 'behavior' | 'link' | 'disguise';
  category: string;
  pattern: string;
  context: string;
  confidence: number;
  semanticType: SemanticType;
  isAllowlisted: boolean;
  requiresConfirmation: boolean;
  severity: 'info' | 'low' | 'medium' | 'high' | 'critical';
  evidenceChain: Evidence[];
  message: string;
}

export type SemanticType =
  | 'data-exfil'
  | 'credential-access'
  | 'file-operation'
  | 'dynamic-execution'
  | 'privilege-esc'
  | 'persistence'
  | 'runtime-install'
  | 'obfuscation'
  | 'process-scan'
  | 'browser-automation'
  | 'behavior-mismatch';

export interface Evidence {
  type: 'code-snippet' | 'cross-reference' | 'similarity-match' | 'proximity' | 'target-analysis' | 'execution-context' | 'encoding-detected' | 'decoding-layer';
  data: any;
  confidence: number;
}

// ============================================================================
// Baseline Types
// ============================================================================

export interface ReviewBaseline {
  version: string;
  lastUpdated: Date;
  project: ProjectBaseline;
  user: UserBaseline;
}

export interface ProjectBaseline {
  allowlistedFindings: string[];
  customRules: CustomRule[];
  protectedFilesOverride: string[];
}

export interface UserBaseline {
  globalAllowlist: string[];
  authorTrust: Record<string, AuthorTrust>;
  learningPatterns: LearningPatterns;
}

export interface AuthorTrust {
  trustLevel: 'untrusted' | 'neutral' | 'trusted' | 'verified';
  lastReviewed: Date;
}

export interface LearningPatterns {
  acceptedJustifications: string[];
}

export interface CustomRule {
  name: string;
  pattern: string;
  severity: string;
}

// ============================================================================
// Risk Assessment Types
// ============================================================================

export interface RiskAssessment {
  level: 'LOW' | 'MEDIUM' | 'HIGH';
  rating: 'SAFE' | 'REVIEW_NEEDED' | 'UNSAFE';
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  findings: RiskFinding[];
  compositeScores: Record<string, number>;
  requiresConfirmation: boolean;
}

// ============================================================================
// Semantic Analysis Types
// ============================================================================

export interface SemanticAnalysis {
  purpose: string;
  confidence: number;
  evidence: Evidence[];
  suspicious: boolean;
  target?: string;
}
