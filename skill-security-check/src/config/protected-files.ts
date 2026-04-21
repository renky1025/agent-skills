// src/config/protected-files.ts
// Protected files configuration

// ============================================================================
// Default Protected Files List
// ============================================================================

export const DEFAULT_PROTECTED_FILES = [
  // AI memory files
  'MEMORY.md',
  'CLAUDE.md',
  'CLAUDE.local.md',
  '.claude/MEMORY.md',
  '.claude/CLAUDE.md',

  // SSH keys
  '~/.ssh/id_rsa',
  '~/.ssh/id_ed25519',
  '~/.ssh/id_rsa.pub',
  '~/.ssh/id_ed25519.pub',
  '~/.ssh/known_hosts',
  '~/.ssh/config',
  '~/.ssh/authorized_keys',
  '~/.ssh/',

  // Git credentials
  '~/.gitconfig',
  '~/.git-credentials',
  '~/.config/git/config',

  // Environment variables
  '~/.env',
  '~/.bashrc',
  '~/.bash_profile',
  '~/.zshrc',
  '~/.zprofile',
  '~/.profile',
  '~/.config/fish/config.fish',

  // Browser data
  '~/Library/Application Support/Google/Chrome',
  '~/Library/Application Support/Google/Chrome/Default',
  '~/.config/google-chrome',
  '~/.config/google-chrome/Default',
  '~/Library/Application Support/Firefox',
  '~/.mozilla/firefox',

  // System sensitive files
  '/etc/passwd',
  '/etc/shadow',
  '/etc/hosts',
  '/etc/resolv.conf',

  // macOS Keychain
  '~/Library/Keychains',
  '~/Library/Keychains/login.keychain-db',

  // Cloud service credentials
  '~/.aws',
  '~/.aws/credentials',
  '~/.aws/config',
  '~/.kube/config',
  '~/.docker/config.json',

  // npm/yarn credentials
  '~/.npmrc',
  '~/.yarnrc',

  // SSH related
  '~/.ssh/',

  // Other sensitive
  '~/.netrc',
  '~/.pgpass',
  '~/.my.cnf'
] as const;

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Expand ~ to user's home directory
 */
export function expandHomePath(filePath: string): string {
  if (filePath.startsWith('~/')) {
    return filePath.replace('~', process.env.HOME || '');
  }
  return filePath;
}

/**
 * Check if a file path is in the protected files list
 */
export function isProtectedFile(filePath: string, overrides: string[] = []): boolean {
  const expanded = expandHomePath(filePath);
  const allProtected = [...DEFAULT_PROTECTED_FILES, ...overrides];

  return allProtected.some(protectedPath => {
    const expandedProtected = expandHomePath(protectedPath);
    return expanded === expandedProtected ||
           expanded.startsWith(expandedProtected + '/') ||
           expanded.startsWith(expandedProtected + '\\');
  });
}
