# Local Development Setup

Complete guide for setting up a local development environment for Lex Conductor.

## Prerequisites

Before starting, ensure you have completed:
- ✅ [Prerequisites Guide](../01-getting-started/prerequisites.md)
- ✅ [Setup Guide](../01-getting-started/setup.md)
- ✅ IBM Cloud account with watsonx Orchestrate access

## Development Environment

### 1. Clone Repository

```bash
git clone https://github.com/bryanstevensacosta/lex-conductor.git
cd lex-conductor
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Verify activation
which python  # Should show .venv/bin/python
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt  # If exists

# Verify installation
pip list
```

### 4. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

Required variables:
```bash
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here
WATSONX_API_KEY=your_ibm_cloud_api_key  # Optional
WATSONX_PROJECT_ID=your_project_id      # Optional
```

See [Environment Configuration](../01-getting-started/environment-config.md) for details.

### 5. Install Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

Pre-commit hooks include:
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking

### 6. Configure watsonx Orchestrate CLI

```bash
# Add environment
orchestrate env add dev \
  --instance $WO_INSTANCE \
  --api-key $WO_API_KEY

# Activate environment
orchestrate env activate dev

# Login
orchestrate auth login

# Verify
orchestrate auth status
```

## Project Structure

```
lex-conductor/
├── .venv/                  # Virtual environment (not committed)
├── docs/                   # Documentation
├── src/                    # Source code (future)
│   ├── agents/            # Agent implementations
│   ├── services/          # Business logic
│   └── utils/             # Utilities
├── tests/                  # Test suite (future)
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env                    # Environment variables (not committed)
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit configuration
├── requirements.txt       # Python dependencies
└── README.md              # Project README
```

## Development Workflow

### 1. Create Feature Branch

```bash
# Create and switch to new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 2. Make Changes

```bash
# Edit files
code src/agents/new_agent.py

# Test changes locally
python -m pytest tests/

# Run pre-commit checks
pre-commit run --all-files
```

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new routing logic to conductor agent"

# Pre-commit hooks run automatically
```

### 4. Push and Create PR

```bash
# Push to remote
git push origin feature/your-feature-name

# Create pull request on GitHub
```

## Running Agents Locally

### Deploy to watsonx Orchestrate

```bash
# Navigate to agent definitions
cd docs/03-agents/agent-definitions/

# Import agent
orchestrate agents import -f conductor_agent.yaml

# Verify deployment
orchestrate agents list

# Test agent
orchestrate chat --agent conductor-agent
```

### View Agent Logs

```bash
# Follow logs in real-time
orchestrate agents logs conductor-agent --follow

# View last 100 lines
orchestrate agents logs conductor-agent --tail 100

# View logs from specific time
orchestrate agents logs conductor-agent --since 1h
```

## Testing Locally

### Run Unit Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_conductor.py

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Run Integration Tests

```bash
# Run integration tests
pytest tests/integration/

# Run with verbose output
pytest tests/integration/ -v
```

### Manual Testing

```bash
# Test agent via CLI
orchestrate chat --agent conductor-agent

# Test with specific query
echo "Analyze market expansion" | orchestrate chat --agent conductor-agent
```

## Debugging

### Enable Debug Logging

```bash
# In .env file
LOG_LEVEL=DEBUG
DEBUG=true
```

### Debug Agent Execution

```bash
# View detailed logs
orchestrate agents logs conductor-agent --level debug

# Check agent status
orchestrate agents get conductor-agent

# Validate agent definition
orchestrate agents validate -f conductor_agent.yaml
```

### Python Debugging

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint()
breakpoint()

# Run with debugger
python -m pdb script.py
```

## Code Quality Tools

### Black (Code Formatting)

```bash
# Format all Python files
black .

# Check without modifying
black --check .

# Format specific file
black src/agents/conductor.py
```

### Ruff (Linting)

```bash
# Lint all files
ruff check .

# Auto-fix issues
ruff check --fix .

# Check specific file
ruff check src/agents/conductor.py
```

### Mypy (Type Checking)

```bash
# Type check all files
mypy .

# Check specific file
mypy src/agents/conductor.py

# Ignore missing imports
mypy --ignore-missing-imports .
```

## Common Development Tasks

### Add New Agent

```bash
# 1. Create agent YAML definition
cd docs/03-agents/agent-definitions/
cp conductor_agent.yaml new_agent.yaml
# Edit new_agent.yaml

# 2. Import to Orchestrate
orchestrate agents import -f new_agent.yaml

# 3. Test agent
orchestrate chat --agent new-agent
```

### Update Existing Agent

```bash
# 1. Edit agent YAML
nano docs/03-agents/agent-definitions/conductor_agent.yaml

# 2. Re-import agent
orchestrate agents import -f conductor_agent.yaml --force

# 3. Verify changes
orchestrate agents get conductor-agent
```

### Add New Dependency

```bash
# 1. Install package
pip install new-package

# 2. Update requirements.txt
pip freeze > requirements.txt

# 3. Commit changes
git add requirements.txt
git commit -m "deps: add new-package"
```

## Environment Management

### Multiple Environments

```bash
# Development
orchestrate env add dev --instance $DEV_INSTANCE --api-key $DEV_KEY

# Staging
orchestrate env add staging --instance $STAGING_INSTANCE --api-key $STAGING_KEY

# Production
orchestrate env add prod --instance $PROD_INSTANCE --api-key $PROD_KEY

# Switch environments
orchestrate env activate dev
orchestrate env activate prod

# List environments
orchestrate env list
```

### Environment Variables

```bash
# Development (.env.development)
APP_ENV=development
LOG_LEVEL=DEBUG
DEBUG=true

# Production (.env.production)
APP_ENV=production
LOG_LEVEL=WARNING
DEBUG=false
```

## Troubleshooting

### Virtual Environment Issues

```bash
# Deactivate and recreate
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Dependency Conflicts

```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Orchestrate Connection Issues

```bash
# Re-authenticate
orchestrate auth logout
orchestrate auth login

# Check environment
orchestrate env list
orchestrate env activate dev
orchestrate auth status
```

### Pre-commit Hook Failures

```bash
# Skip hooks temporarily (not recommended)
git commit --no-verify

# Fix issues and retry
black .
ruff check --fix .
git commit
```

## Best Practices

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings
- Keep functions small and focused
- Use meaningful variable names

### Git Workflow
- Create feature branches
- Write clear commit messages
- Keep commits atomic
- Rebase before merging
- Review your own code first

### Testing
- Write tests for new features
- Maintain test coverage >80%
- Test edge cases
- Use fixtures for common setup
- Mock external dependencies

### Documentation
- Update docs with code changes
- Add docstrings to functions
- Document complex logic
- Keep README up to date
- Add examples where helpful

## Related Documentation

- [Setup Guide](../01-getting-started/setup.md)
- [Testing Guide](./testing.md)
- [Deployment Guide](./deployment.md)
- [Agent Architecture](../03-agents/agent-architecture.md)

---

**Development Environment**: Local  
**Python Version**: 3.11+  
**Primary Tools**: watsonx Orchestrate ADK, pytest, black, ruff
