# watsonx Orchestrate Deployment Guide - LexConductor

**IBM Dev Day AI Demystified Hackathon**  
**Team**: AI Kings 👑  
**Version**: 1.0  
**Date**: January 30, 2026

---

## Overview

This directory contains all watsonx Orchestrate agent definitions and configuration for LexConductor. Follow this guide to deploy the complete multi-agent system.

---

## Directory Structure

```
orchestrate/
├── agents/                          # Agent YAML definitions
│   ├── conductor_agent.yaml         # Native orchestrator (REQUIRED)
│   ├── fusion_agent.yaml            # External signal fusion agent
│   ├── routing_agent.yaml           # External routing agent
│   ├── memory_agent.yaml            # External memory agent
│   └── traceability_agent.yaml      # External traceability agent
├── .env.example                     # Environment configuration template
└── README.md                        # This file
```

---

## Prerequisites

### 1. IBM Cloud Account
- [ ] IBM Cloud account activated
- [ ] watsonx Orchestrate instance accessible
- [ ] $100 credits verified

### 2. watsonx Orchestrate ADK
```bash
# Install ADK
pip install ibm-watsonx-orchestrate

# Verify installation
orchestrate --version
```

### 3. External Agents Deployed
- [ ] Fusion Agent deployed to Code Engine
- [ ] Routing Agent deployed to Code Engine
- [ ] Memory Agent deployed to Code Engine
- [ ] Traceability Agent deployed to Code Engine
- [ ] All agent URLs obtained

### 4. Environment Configuration
- [ ] `.env` file created from `.env.example`
- [ ] All credentials filled in
- [ ] External agent endpoints configured

---

## Quick Start (15 minutes)

### Step 1: Configure Environment (5 min)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Required values:
# - WO_INSTANCE
# - WO_API_KEY
# - WATSONX_API_KEY
# - WATSONX_PROJECT_ID
# - FUSION_AGENT_ENDPOINT
# - ROUTING_AGENT_ENDPOINT
# - MEMORY_AGENT_ENDPOINT
# - TRACEABILITY_AGENT_ENDPOINT
# - All agent API keys

# Load environment
source .env  # or use direnv
```

### Step 2: Configure ADK (3 min)

```bash
# Add watsonx Orchestrate environment
orchestrate env add prod \
  --instance $WO_INSTANCE \
  --api-key $WO_API_KEY

# Activate environment
orchestrate env activate prod

# Login
orchestrate auth login

# Verify connection
orchestrate agents list
```

### Step 3: Import Agents (5 min)

```bash
# Import Conductor Agent (Native)
orchestrate agents import -f agents/conductor_agent.yaml

# Import External Agents
orchestrate agents import -f agents/fusion_agent.yaml
orchestrate agents import -f agents/routing_agent.yaml
orchestrate agents import -f agents/memory_agent.yaml
orchestrate agents import -f agents/traceability_agent.yaml

# Verify imports
orchestrate agents list
```

### Step 4: Deploy Conductor Agent (2 min)

```bash
# Deploy the native orchestrator
orchestrate agents deploy conductor-agent

# Verify deployment
orchestrate agents get conductor-agent
```

---

## Agent Descriptions

### 1. Conductor Agent (Native)
**Type**: Native watsonx Orchestrate Agent  
**File**: `agents/conductor_agent.yaml`  
**Role**: Primary orchestrator managing entire workflow

**Responsibilities**:
- Receive contract review requests via Chat UI
- Classify contract type and jurisdiction
- Delegate to specialized sub-agents in parallel
- Aggregate results from all agents
- Present final Legal Logic Trace to user

**Model**: IBM Granite 3 8B Instruct  
**Interface**: watsonx Orchestrate Chat UI

### 2. Fusion Agent (External)
**Type**: External Agent via Agent Connect Framework  
**File**: `agents/fusion_agent.yaml`  
**Role**: Signal correlation and compliance analysis

**Responsibilities**:
- Query Cloudant for Golden Clauses
- Retrieve regulatory PDFs from COS
- Correlate internal + external + contract signals
- Identify compliance gaps
- Return structured analysis with confidence scores

**Endpoint**: Code Engine (Osaka)  
**Data Sources**: Cloudant + Cloud Object Storage

### 3. Routing Agent (External)
**Type**: External Agent via Agent Connect Framework  
**File**: `agents/routing_agent.yaml`  
**Role**: Risk assessment and workflow routing

**Responsibilities**:
- Analyze Fusion Agent output
- Calculate risk score (0.0 to 1.0)
- Classify complexity (LOW/MEDIUM/HIGH)
- Determine routing (ROUTINE/STANDARD/COMPLEX)
- Specify human-in-loop requirements

**Endpoint**: Code Engine (Osaka)  
**Decision Logic**: Rule-based + AI-powered

### 4. Memory Agent (External)
**Type**: External Agent via Agent Connect Framework  
**File**: `agents/memory_agent.yaml`  
**Role**: Institutional memory and precedent search

**Responsibilities**:
- Search historical contract decisions
- Retrieve Golden Clauses from library
- Find similar past cases
- Identify modification patterns
- Provide precedent-based recommendations

**Endpoint**: Code Engine (Osaka)  
**Data Source**: Cloudant (historical_decisions)

### 5. Traceability Agent (External)
**Type**: External Agent via Agent Connect Framework  
**File**: `agents/traceability_agent.yaml`  
**Role**: Audit trail and explainability

**Responsibilities**:
- Synthesize all agent outputs
- Generate Legal Logic Trace
- Document decision reasoning
- Calculate confidence scores
- Create audit trail for compliance

**Endpoint**: Code Engine (Osaka)  
**Output Format**: Markdown + JSON

---

## Agent Collaboration Flow

```
User Question (Chat UI)
    ↓
Conductor Agent (Native)
    ↓
    ├─→ Fusion Agent (External)
    │   ├─→ Cloudant (Golden Clauses)
    │   └─→ COS (Regulations)
    │
    ├─→ Memory Agent (External)
    │   └─→ Cloudant (Historical Decisions)
    │
    └─→ Routing Agent (External)
        └─→ Risk Classification
    ↓
Traceability Agent (External)
    ↓
Conductor Agent
    ↓
Legal Logic Trace → User
```

---

## Testing

### Test Individual Agents

```bash
# Test Conductor Agent via CLI
orchestrate chat --agent conductor-agent

# In chat, type:
"Analyze this NDA: Party A agrees to keep confidential information secret for 2 years. Liability is capped at $500,000."

# Expected: Conductor delegates to all agents and returns Legal Logic Trace
```

### Test via Web UI

1. Open watsonx Orchestrate web UI
2. Navigate to Chat
3. Select `conductor-agent`
4. Upload sample contract or paste text
5. Verify complete workflow executes
6. Check Legal Logic Trace output

### Test External Agents Directly

```bash
# Test Fusion Agent
curl -X POST $FUSION_AGENT_ENDPOINT/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $FUSION_AGENT_API_KEY" \
  -d '{
    "contract_text": "Party A shall indemnify Party B...",
    "contract_type": "NDA",
    "jurisdiction": "US"
  }'

# Expected: JSON response with signals and gaps
```

---

## Monitoring

### View Agent Logs

```bash
# Conductor Agent logs
orchestrate agents logs conductor-agent --follow

# Check agent status
orchestrate agents get conductor-agent

# List all agents
orchestrate agents list
```

### External Agent Logs

```bash
# View Code Engine logs
ibmcloud ce application logs --name fusion-agent --follow
ibmcloud ce application logs --name routing-agent --follow
ibmcloud ce application logs --name memory-agent --follow
ibmcloud ce application logs --name traceability-agent --follow
```

---

## Troubleshooting

### Issue: Agent import fails

```bash
# Check YAML syntax
yamllint agents/conductor_agent.yaml

# Verify environment variables
echo $WO_INSTANCE
echo $WO_API_KEY

# Check ADK authentication
orchestrate auth status
```

### Issue: External agent not responding

```bash
# Verify agent endpoint
curl -I $FUSION_AGENT_ENDPOINT/health

# Check Code Engine application status
ibmcloud ce application get --name fusion-agent

# Verify API key in .env matches deployed agent
echo $FUSION_AGENT_API_KEY
```

### Issue: Conductor can't reach external agents

```bash
# Verify Agent Connect configuration in YAML
cat agents/fusion_agent.yaml | grep endpoint

# Test external agent directly
curl -X POST $FUSION_AGENT_ENDPOINT/analyze \
  -H "X-API-Key: $FUSION_AGENT_API_KEY" \
  -d '{"test": true}'

# Check Orchestrate logs for connection errors
orchestrate agents logs conductor-agent --tail 50
```

---

## Updating Agents

### Update Agent Definition

```bash
# Edit YAML file
vim agents/conductor_agent.yaml

# Re-import agent
orchestrate agents import -f agents/conductor_agent.yaml --force

# Redeploy if needed
orchestrate agents deploy conductor-agent
```

### Update External Agent Code

```bash
# Update Code Engine application
ibmcloud ce application update \
  --name fusion-agent \
  --image icr.io/namespace/fusion-agent:v2

# Verify update
ibmcloud ce application get --name fusion-agent
```

---

## Performance Optimization

### Response Time Targets

| Agent | Target | Max |
|-------|--------|-----|
| Conductor | <1s | <2s |
| Fusion | <5s | <8s |
| Routing | <1s | <2s |
| Memory | <2s | <3s |
| Traceability | <1s | <2s |
| **Total** | **<10s** | **<15s** |

### Optimization Tips

1. **Caching**
   - Cache Golden Clauses in memory
   - Cache frequently accessed regulations
   - Use Cloudant indexes for fast queries

2. **Parallel Execution**
   - Fusion + Memory agents run in parallel
   - Routing runs after Fusion completes
   - Minimize sequential dependencies

3. **Prompt Optimization**
   - Keep prompts concise (<500 tokens)
   - Use structured output formats (JSON)
   - Avoid unnecessary context

---

## Security Best Practices

### Credentials Management

```bash
# ✅ DO
- Store credentials in .env (never commit)
- Use environment variables in YAML (${VAR_NAME})
- Rotate API keys regularly
- Use different keys for dev/prod

# ❌ DON'T
- Hardcode credentials in YAML
- Commit .env to version control
- Share API keys in chat/email
- Use same keys across environments
```

### Agent API Keys

```bash
# Generate secure random keys
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set in .env
FUSION_AGENT_API_KEY=<generated_key>
ROUTING_AGENT_API_KEY=<generated_key>
MEMORY_AGENT_API_KEY=<generated_key>
TRACEABILITY_AGENT_API_KEY=<generated_key>
```

---

## Cost Monitoring

### watsonx.ai Usage

```bash
# Estimated token usage per contract:
# - Conductor: ~1,000 tokens
# - Fusion: ~2,000 tokens
# - Routing: ~500 tokens
# - Traceability: ~1,500 tokens
# Total: ~5,000 tokens per contract

# Cost: 5,000 tokens × $0.0001 per 1K = $0.0005 per contract
# Budget: $100 ÷ $0.0005 = 200,000 contracts (theoretical max)
```

### Monitor Usage

```bash
# Check credit usage in IBM Cloud console:
# Manage → Billing and usage → Usage

# Set alerts at:
# - 25% ($25)
# - 50% ($50)
# - 80% ($80)
```

---

## Backup & Recovery

### Export Agent Definitions

```bash
# Export all agents
orchestrate agents export conductor-agent > backup/conductor_agent.yaml
orchestrate agents export fusion-agent > backup/fusion_agent.yaml
orchestrate agents export routing-agent > backup/routing_agent.yaml
orchestrate agents export memory-agent > backup/memory_agent.yaml
orchestrate agents export traceability-agent > backup/traceability_agent.yaml

# Backup .env (securely)
cp .env backup/.env.backup
```

### Restore Agents

```bash
# Re-import from backup
orchestrate agents import -f backup/conductor_agent.yaml --force
orchestrate agents import -f backup/fusion_agent.yaml --force
# ... repeat for all agents

# Redeploy
orchestrate agents deploy conductor-agent
```

---

## Demo Preparation

### Pre-Demo Checklist

- [ ] All agents deployed and responding
- [ ] End-to-end test successful
- [ ] Response time <10 seconds
- [ ] Legal Logic Trace formatting correct
- [ ] Sample contracts prepared
- [ ] Backup video recorded

### Demo Script

1. **Open watsonx Orchestrate Chat UI** (5s)
2. **Select conductor-agent** (3s)
3. **Upload sample NDA** (5s)
4. **Show Conductor receiving request** (10s)
5. **Display agent execution** (30s)
   - Fusion Agent analyzing
   - Memory Agent searching
   - Routing Agent classifying
6. **Show Legal Logic Trace** (30s)
   - Signal analysis
   - Risk assessment
   - Recommendations
   - Confidence scores
7. **Highlight watsonx Orchestrate UI** (10s)

**Total**: ~90 seconds

---

## Support Resources

### Documentation
- [watsonx Orchestrate Docs](https://www.ibm.com/docs/en/watson-orchestrate)
- [Agent Development Kit](https://developer.watson-orchestrate.ibm.com/)
- [Agent Connect Framework](https://developer.watson-orchestrate.ibm.com/agent-connect)

### Hackathon Support
- IBM Dev Day Slack: #watsonx-orchestrate
- BeMyApp Support: support@bemyapp.com
- Hackathon Mentors: Via BeMyApp platform

### Team Resources
- [INTEGRATION-GUIDE.md](../INTEGRATION-GUIDE.md) - Complete setup guide
- [HACKATHON-CHECKLIST.md](../HACKATHON-CHECKLIST.md) - Submission checklist
- [docs/Technical.md](../docs/Technical.md) - Technical architecture

---

## Quick Reference Commands

```bash
# Environment
orchestrate env list
orchestrate env activate prod
orchestrate auth login

# Agents
orchestrate agents list
orchestrate agents import -f agents/conductor_agent.yaml
orchestrate agents deploy conductor-agent
orchestrate agents get conductor-agent
orchestrate agents logs conductor-agent --follow

# Testing
orchestrate chat --agent conductor-agent

# Troubleshooting
orchestrate agents logs conductor-agent --tail 100
orchestrate auth status
```

---

## Appendix: YAML Schema Reference

### Native Agent Schema

```yaml
name: string                    # Agent name (required)
version: string                 # Semantic version (required)
description: string             # Agent description
model:
  provider: string              # "watsonx.ai"
  model_id: string              # "ibm/granite-3-8b-instruct"
  parameters:
    max_tokens: integer
    temperature: float
system_prompt: string           # Agent instructions
collaborators: array            # List of agent names
tools: array                    # Tool definitions
```

### External Agent Schema

```yaml
name: string                    # Agent name (required)
version: string                 # Semantic version (required)
description: string             # Agent description
type: external                  # Must be "external"
connection:
  type: agent_connect           # Connection type
  endpoint: string              # Agent URL
  api_key: string               # API key (use ${VAR})
  timeout: integer              # Timeout in seconds
capabilities: array             # List of capabilities
input_schema: object            # JSON Schema
output_schema: object           # JSON Schema
```

---

**Document Owner**: Team AI Kings  
**Last Updated**: January 30, 2026  
**Status**: Ready for Deployment  
**Estimated Setup Time**: 15-30 minutes
