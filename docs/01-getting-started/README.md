# Getting Started with Lex Conductor

Quick start guide to set up and run Lex Conductor locally.

## 📋 Contents

- **[Prerequisites](./prerequisites.md)** - Required tools, technologies, and IBM Cloud setup
- **[Setup Guide](./setup.md)** - Step-by-step installation and configuration
- **[Quick Start](./quick-start.md)** - Get running in 5 minutes
- **[Environment Configuration](./environment-config.md)** - Configure your .env file

## 🚀 Quick Start (TL;DR)

```bash
# 1. Clone the repository
git clone https://github.com/bryanstevensacosta/lex-conductor.git
cd lex-conductor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your IBM Cloud credentials

# 4. Run setup script
./setup.sh

# 5. Deploy agents to watsonx Orchestrate
cd docs/03-agents/agent-definitions/
# Follow deployment instructions
```

## 📚 What You'll Learn

1. **Prerequisites** - What you need before starting
2. **Installation** - How to install all dependencies
3. **Configuration** - How to set up your environment
4. **Verification** - How to test everything works

## ⚡ Prerequisites Overview

### Required
- ✅ Python 3.11+
- ✅ IBM Cloud account (hackathon provisioned)
- ✅ watsonx Orchestrate access
- ✅ Git

### Optional
- Docker (for containerized deployment)
- Terraform (for infrastructure as code)

## 🎯 Next Steps

After completing the setup:
1. Read the [Project Overview](../02-project/overview.md)
2. Understand the [Architecture](../02-project/architecture.md)
3. Learn about [Agents](../03-agents/)
4. Start [Development](../04-development/)

## 🆘 Troubleshooting

**Common Issues:**
- **IBM Cloud access denied**: Check your invitation email and account activation
- **Python version mismatch**: Use Python 3.11 or higher
- **Missing dependencies**: Run `pip install -r requirements.txt` again
- **Environment variables not loading**: Verify your `.env` file exists and has correct values

For more help, see the [Development Guide](../04-development/).

---

**Estimated Setup Time**: 15-30 minutes  
**Difficulty**: Beginner-friendly
