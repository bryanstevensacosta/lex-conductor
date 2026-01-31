# Quick Start Guide

Get Lex Conductor running in 5 minutes.

## TL;DR

```bash
# 1. Clone and setup
git clone https://github.com/bryanstevensacosta/lex-conductor.git
cd lex-conductor
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your IBM Cloud credentials

# 4. Setup watsonx Orchestrate
orchestrate env add prod --instance $WO_INSTANCE --api-key $WO_API_KEY
orchestrate env activate prod
orchestrate auth login

# 5. Deploy agents
cd docs/03-agents/agent-definitions/
orchestrate agents import -f conductor_agent.yaml
orchestrate agents import -f routing_agent.yaml
orchestrate agents import -f memory_agent.yaml
orchestrate agents import -f fusion_agent.yaml
orchestrate agents import -f traceability_agent.yaml

# 6. Test
orchestrate chat --agent conductor-agent
```

## Prerequisites

- Python 3.11+
- IBM Cloud account with watsonx Orchestrate access
- Git

## Step 1: Clone Repository

```bash
git clone https://github.com/bryanstevensacosta/lex-conductor.git
cd lex-conductor
```

## Step 2: Setup Environment

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Credentials

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here
```

**Getting Credentials:**
1. Go to IBM Cloud → Resource List
2. Launch watsonx Orchestrate
3. Settings → API Details
4. Copy Instance URL and generate API Key

## Step 4: Configure watsonx Orchestrate

```bash
# Add environment
orchestrate env add prod --instance $WO_INSTANCE --api-key $WO_API_KEY

# Activate and login
orchestrate env activate prod
orchestrate auth login
```

## Step 5: Deploy Agents

```bash
# Navigate to agent definitions
cd docs/03-agents/agent-definitions/

# Import all agents
orchestrate agents import -f conductor_agent.yaml
orchestrate agents import -f routing_agent.yaml
orchestrate agents import -f memory_agent.yaml
orchestrate agents import -f fusion_agent.yaml
orchestrate agents import -f traceability_agent.yaml

# Verify deployment
orchestrate agents list
```

## Step 6: Test the System

```bash
# Test conductor agent
orchestrate chat --agent conductor-agent

# Example query
> "Analyze the decision to expand into a new market"

# View logs
orchestrate agents logs conductor-agent
```

## Verify Everything Works

```bash
# Check authentication
orchestrate auth status

# List all agents
orchestrate agents list

# Check agent status
orchestrate agents get conductor-agent

# View recent logs
orchestrate agents logs conductor-agent --tail 50
```

## Common Issues

### Authentication Failed
```bash
# Re-login
orchestrate auth login

# Check environment
orchestrate env list
orchestrate env activate prod
```

### Agent Not Found
```bash
# Re-import agent
cd docs/03-agents/agent-definitions/
orchestrate agents import -f conductor_agent.yaml

# Verify
orchestrate agents list
```

### Connection Timeout
```bash
# Check instance URL
echo $WO_INSTANCE

# Verify API key
orchestrate auth status
```

## Next Steps

### Learn the System
1. Read [Project Overview](../02-project/overview.md)
2. Understand [Architecture](../02-project/architecture.md)
3. Review [Agent Documentation](../03-agents/)

### Start Developing
1. Follow [Development Guide](../04-development/)
2. Review [Integration Guide](../05-integration/)
3. Check [Testing Guide](../04-development/testing.md)

### Prepare for Hackathon
1. Review [Hackathon Requirements](../06-hackathon/requirements.md)
2. Check [Submission Guide](../06-hackathon/submission-guide.md)
3. Use [Submission Checklist](../06-hackathon/checklist.md)

## Quick Commands Reference

```bash
# Environment management
orchestrate env list
orchestrate env activate prod
orchestrate auth status

# Agent management
orchestrate agents list
orchestrate agents get <agent-name>
orchestrate agents logs <agent-name>

# Testing
orchestrate chat --agent <agent-name>

# Deployment
orchestrate agents import -f <agent-file.yaml>
orchestrate agents deploy <agent-name>
```

## Support

- **Setup Help**: [Full Setup Guide](./setup.md)
- **Prerequisites**: [Prerequisites Guide](./prerequisites.md)
- **Documentation**: [docs/README.md](../README.md)
- **Hackathon Support**: support@bemyapp.com

---

**Time to Complete**: ~5 minutes  
**Difficulty**: Easy  
**Status**: Ready to use
