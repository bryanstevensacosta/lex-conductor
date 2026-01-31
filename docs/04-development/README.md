# Development Guide

Guidelines for developing and contributing to Lex Conductor.

## 📋 Contents

- **[Local Setup](./local-setup.md)** - Set up your development environment
- **[Environment Configuration](./environment-config.md)** - Configure environment variables
- **[Testing](./testing.md)** - Testing strategies and guidelines
- **[Deployment](./deployment.md)** - Deploy to watsonx Orchestrate

## 🚀 Quick Development Setup

```bash
# 1. Clone and navigate
git clone https://github.com/bryanstevensacosta/lex-conductor.git
cd lex-conductor

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Run pre-commit hooks
pre-commit install
```

## 🛠️ Development Workflow

1. **Create a branch** for your feature
2. **Make changes** following code standards
3. **Test locally** before committing
4. **Run pre-commit hooks** (black, ruff, mypy)
5. **Commit with clear messages**
6. **Push and create PR**

## 📝 Code Standards

### Python
- Use Python 3.11+
- Follow PEP 8 style guide
- Use type hints
- Write docstrings
- Keep functions small and focused

### Pre-commit Hooks
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking

### Commit Messages
```
feat: add new routing agent capability
fix: resolve memory agent context issue
docs: update integration guide
refactor: simplify fusion agent logic
test: add unit tests for conductor
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=src
```

### Test Structure
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── e2e/           # End-to-end tests
```

## 🔧 Environment Variables

Required variables in `.env`:
```bash
# watsonx Orchestrate
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key

# watsonx.ai (optional)
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

## 📦 Project Structure

```
lex-conductor/
├── docs/              # Documentation
├── src/               # Source code (future)
├── tests/             # Test suite (future)
├── terraform/         # Infrastructure as code
├── .env.example       # Environment template
├── requirements.txt   # Python dependencies
└── setup.sh          # Setup script
```

## 🚀 Deployment

### Deploy to watsonx Orchestrate
```bash
# Import agents
cd docs/03-agents/agent-definitions/
orchestrate agents import -f conductor_agent.yaml

# Verify deployment
orchestrate agents list

# Test agent
orchestrate chat --agent conductor-agent
```

## 🐛 Debugging

### View Agent Logs
```bash
orchestrate agents logs conductor-agent --follow
```

### Check Agent Status
```bash
orchestrate agents get conductor-agent
```

### Test Locally
```bash
# Test agent definitions
orchestrate agents validate -f conductor_agent.yaml
```

## 📚 Best Practices

1. **Keep agents stateless** - Use Memory Agent for state
2. **Handle errors gracefully** - Implement fallbacks
3. **Optimize prompts** - Reduce token usage
4. **Test thoroughly** - Unit, integration, and E2E tests
5. **Document changes** - Update docs with code
6. **Security first** - Never commit secrets

## 🔐 Security

- Never commit `.env` files
- Use `.env.example` for templates
- Rotate API keys regularly
- Follow IBM Cloud security guidelines
- Review `.gitignore` before commits

## 📖 Related Documentation

- [Getting Started](../01-getting-started/) - Initial setup
- [Agents](../03-agents/) - Agent documentation
- [Integration](../05-integration/) - watsonx integration
- [Infrastructure](../07-infrastructure/) - Infrastructure setup

---

**Development Status**: 🚧 Active Development  
**Python Version**: 3.11+  
**Framework**: watsonx Orchestrate + Agent Connect
