// src/config/risk-patterns.ts
// Risk pattern configurations by language

// ============================================================================
// Risk Pattern Interface
// ============================================================================

export interface RiskPattern {
  name: string;
  semanticType: string;
  patterns: RegExp[];
  severity: 'info' | 'low' | 'medium' | 'high' | 'critical';
  description: string;
}

// ============================================================================
// Risk Patterns by Language
// ============================================================================

export const RISK_PATTERNS: Record<string, RiskPattern[]> = {
  javascript: [
    // Data exfiltration
    {
      name: 'fetch-request',
      semanticType: 'data-exfil',
      patterns: [/(?:fetch|axios|request)\s*\(/g],
      severity: 'medium',
      description: 'Network request may be used for data exfiltration'
    },
    {
      name: 'websocket-connection',
      semanticType: 'data-exfil',
      patterns: [/new\s+WebSocket\s*\(/g],
      severity: 'medium',
      description: 'WebSocket connection may be used for real-time data exfiltration'
    },
    // Credential access
    {
      name: 'env-access',
      semanticType: 'credential-access',
      patterns: [/process\.env/g],
      severity: 'info',
      description: 'Accessing environment variables'
    },
    // Dynamic code execution
    {
      name: 'eval-execution',
      semanticType: 'dynamic-execution',
      patterns: [/eval\s*\(/g, /new\s+Function\s*\(/g],
      severity: 'high',
      description: 'Dynamic code execution (eval/new Function)'
    },
    {
      name: 'child-process',
      semanticType: 'dynamic-execution',
      patterns: [
        /child_process/g,
        /\.exec\s*\(/g,
        /\.execSync/g,
        /spawn\s*\(/g
      ],
      severity: 'medium',
      description: 'Child process execution'
    },
    // File operations
    {
      name: 'file-write',
      semanticType: 'file-operation',
      patterns: [
        /fs\.writeFile/g,
        /fs\.appendFile/g,
        /fs\.copyFile/g
      ],
      severity: 'low',
      description: 'File write operation'
    },
    // Browser automation
    {
      name: 'browser-automation',
      semanticType: 'browser-automation',
      patterns: [
        /puppeteer/g,
        /playwright/g,
        /selenium/g,
        /chrome\.launch/g
      ],
      severity: 'low',
      description: 'Browser automation'
    }
  ],
  python: [
    // Data exfiltration
    {
      name: 'python-requests',
      semanticType: 'data-exfil',
      patterns: [/requests\./g, /urllib\./g, /http\.client/g],
      severity: 'medium',
      description: 'Python network request'
    },
    // Credential access
    {
      name: 'python-env',
      semanticType: 'credential-access',
      patterns: [/os\.environ/g, /os\.getenv/g],
      severity: 'info',
      description: 'Accessing environment variables'
    },
    // Dynamic execution
    {
      name: 'python-exec',
      semanticType: 'dynamic-execution',
      patterns: [/exec\s*\(/g, /eval\s*\(/g, /subprocess\./g, /os\.system/g],
      severity: 'high',
      description: 'Python dynamic execution'
    },
    // File operations
    {
      name: 'python-file',
      semanticType: 'file-operation',
      patterns: [/(?<!#.*)open\s*\(/g, /pathlib/g, /shutil\./g],
      severity: 'low',
      description: 'Python file operation'
    }
  ],
  rust: [
    {
      name: 'rust-http',
      semanticType: 'data-exfil',
      patterns: [/reqwest/g, /hyper/g, /ureq/g],
      severity: 'medium',
      description: 'Rust HTTP client'
    },
    {
      name: 'rust-command',
      semanticType: 'dynamic-execution',
      patterns: [/Command::new/g, /std::process::Command/g],
      severity: 'medium',
      description: 'Rust command execution'
    },
    {
      name: 'rust-file',
      semanticType: 'file-operation',
      patterns: [/File::create/g, /File::open/g, /fs::/g],
      severity: 'low',
      description: 'Rust file operation'
    }
  ],
  shell: [
    {
      name: 'sudo-usage',
      semanticType: 'privilege-esc',
      patterns: [/(?:^|\s)sudo\s/g],
      severity: 'high',
      description: 'sudo privilege escalation'
    },
    {
      name: 'chmod-privilege',
      semanticType: 'privilege-esc',
      patterns: [/chmod\s+.*[0-9]*7/, /chmod\s+\+x/],
      severity: 'medium',
      description: 'Permission modification'
    },
    {
      name: 'cron-setup',
      semanticType: 'persistence',
      patterns: [/crontab/, /cron/],
      severity: 'medium',
      description: 'Cron job setup'
    }
  ]
};

// ============================================================================
// Helper Function
// ============================================================================

/**
 * Get risk patterns for a specific language
 */
export function getPatternsForLanguage(language: string): RiskPattern[] {
  return RISK_PATTERNS[language] || [];
}
