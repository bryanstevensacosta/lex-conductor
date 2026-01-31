#!/bin/bash
# Install Git hooks for the project
# IBM Dev Day AI Demystified Hackathon 2026
# Team: AI Kings 👑

echo "🔧 Installing Git hooks..."

# Copy hooks to .git/hooks/
cp .githooks/pre-commit .git/hooks/pre-commit
cp .githooks/pre-merge-commit .git/hooks/pre-merge-commit

# Make them executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-merge-commit

echo "✅ Git hooks installed successfully!"
echo ""
echo "Hooks installed:"
echo "  - pre-commit: Prevents direct commits to master/main"
echo "  - pre-merge-commit: Prevents local merges"
echo ""
echo "Branch workflow enforced:"
echo "  ✅ Feature branches allowed"
echo "  ❌ Direct commits to master/main blocked"
echo "  ❌ Local merges blocked (use PRs instead)"
