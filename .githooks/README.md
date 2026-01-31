# Git Hooks - Boardroom AI

## Overview

Custom Git hooks to enforce branch-based workflow and prevent common mistakes.

## Installed Hooks

### 1. pre-commit
**Purpose**: Prevents direct commits to protected branches (master/main)

**Behavior**:
- ✅ Allows commits on feature branches
- ❌ Blocks commits on master/main branches
- Provides helpful instructions for creating feature branches

**Example Error**:
```
❌ ERROR: Direct commits to 'master' branch are not allowed!

Please create a feature branch instead:
  git checkout -b feature/your-feature-name
```

### 2. pre-merge-commit
**Purpose**: Prevents local merges (enforces PR workflow)

**Behavior**:
- ❌ Blocks all local merge commits
- Encourages using Pull Requests for code review
- Suggests using rebase for updating branches

**Example Error**:
```
❌ ERROR: Local merges are not allowed!

Please use Pull Requests for merging branches.

Workflow:
  1. Push your feature branch: git push origin feature/your-feature
  2. Create a Pull Request on GitHub/GitLab
  3. Review and merge through the web interface
```

## Installation

### First Time Setup
```bash
# Run the installation script
./githooks/install.sh
```

### Manual Installation
```bash
# Copy hooks to .git/hooks/
cp .githooks/pre-commit .git/hooks/pre-commit
cp .githooks/pre-merge-commit .git/hooks/pre-merge-commit

# Make them executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-merge-commit
```

## Recommended Workflow

### Creating a Feature Branch
```bash
# From master/main
git checkout master
git pull origin master

# Create feature branch
git checkout -b feature/add-new-agent

# Make changes and commit
git add .
git commit -m "Add new strategy agent"
```

### If You Have Uncommitted Changes on Master
```bash
# Stash your changes
git stash

# Create feature branch
git checkout -b feature/your-feature

# Apply stashed changes
git stash pop

# Now commit
git add .
git commit -m "Your commit message"
```

### Updating Your Branch with Latest Changes
```bash
# Fetch latest changes
git fetch origin

# Rebase your branch (recommended)
git rebase origin/master

# Or merge (if rebase causes issues)
git merge origin/master
```

### Merging Your Work
```bash
# Push your feature branch
git push origin feature/your-feature

# Create Pull Request on GitHub/GitLab
# Review and merge through web interface
```

## Branch Naming Conventions

Use descriptive branch names with prefixes:

- `feature/` - New features
  - `feature/add-finance-agent`
  - `feature/orchestrate-integration`

- `fix/` - Bug fixes
  - `fix/api-timeout`
  - `fix/agent-response-format`

- `docs/` - Documentation updates
  - `docs/update-readme`
  - `docs/add-integration-guide`

- `refactor/` - Code refactoring
  - `refactor/agent-base-class`
  - `refactor/prompt-structure`

- `test/` - Test additions/updates
  - `test/add-agent-tests`
  - `test/integration-tests`

## Bypassing Hooks (Emergency Only)

⚠️ **Not recommended** - Only use in emergencies:

```bash
# Skip pre-commit hook
git commit --no-verify -m "Emergency fix"

# Skip all hooks
git commit -n -m "Emergency fix"
```

**Note**: This should only be used in exceptional circumstances and with team approval.

## Protected Branches

The following branches are protected by the pre-commit hook:
- `master`
- `main`

All work must be done on feature branches.

## Troubleshooting

### Hook Not Running
```bash
# Check if hooks are executable
ls -la .git/hooks/

# If not, make them executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-merge-commit
```

### Hook Running But Not Working
```bash
# Verify hook content
cat .git/hooks/pre-commit

# Reinstall hooks
./githooks/install.sh
```

### Need to Commit to Master (Emergency)
```bash
# Use --no-verify flag (not recommended)
git commit --no-verify -m "Emergency hotfix"

# Or temporarily disable hook
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
# Make your commit
git commit -m "Emergency fix"
# Re-enable hook
mv .git/hooks/pre-commit.disabled .git/hooks/pre-commit
```

## Team Setup

When a new team member clones the repository:

```bash
# Clone repository
git clone <repository-url>
cd boardroom-ai

# Install hooks
./githooks/install.sh

# Verify installation
ls -la .git/hooks/
```

## Why These Hooks?

### Prevents Accidental Master Commits
- Protects main branch from direct commits
- Enforces feature branch workflow
- Reduces merge conflicts

### Enforces Code Review
- Blocks local merges
- Requires Pull Requests
- Ensures team visibility
- Maintains code quality

### Maintains Clean History
- Encourages atomic commits
- Promotes better commit messages
- Makes git history readable

## Additional Resources

- [Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)
- [Pull Request Best Practices](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)

---

**IBM Dev Day AI Demystified Hackathon 2026**  
**Team: AI Kings 👑**
