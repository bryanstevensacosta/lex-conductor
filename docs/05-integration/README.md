# Integration Guide

Complete guide for integrating Lex Conductor with IBM watsonx platforms.

## 📋 Contents

- **[watsonx Orchestrate](./watsonx-orchestrate.md)** - Main orchestration platform setup
- **[watsonx.ai](./watsonx-ai.md)** - AI inference integration (optional)
- **[Agent Connect](./agent-connect.md)** - External agent integration framework
- **[API Reference](./api-reference.md)** - API documentation

## 🎯 Integration Overview

Lex Conductor integrates with IBM watsonx ecosystem:

```
Lex Conductor
    ├── watsonx Orchestrate (REQUIRED)
    │   └── Native Conductor Agent
    │
    ├── Agent Connect Framework (REQUIRED)
    │   └── External Agents (Routing, Memory, Fusion, Traceability)
    │
    └── watsonx.ai (OPTIONAL)
        └── Granite Models for AI reasoning
```

## 🔧 Required Integrations

### 1. watsonx Orchestrate (MANDATORY)

Primary orchestration platform that manages agent collaboration.

**Setup Steps:**
1. Access IBM Cloud account
2. Launch watsonx Orchestrate
3. Get API credentials
4. Install Agent Development Kit (ADK)
5. Deploy agent definitions

**Documentation**: [watsonx Orchestrate Guide](./watsonx-orchestrate.md)

### 2. Agent Connect Framework (MANDATORY)

Enables external agents to communicate with watsonx Orchestrate.

**Setup Steps:**
1. Define external agents in YAML
2. Implement agent endpoints (FastAPI planned)
3. Configure Agent Connect
4. Test connectivity

**Documentation**: [Agent Connect Guide](./agent-connect.md)

## 🎨 Optional Integrations

### watsonx.ai (OPTIONAL)

AI inference platform for custom model usage.

**Use Cases:**
- Custom prompt engineering
- Model experimentation
- Advanced AI capabilities

**Documentation**: [watsonx.ai Guide](./watsonx-ai.md)

## 🚀 Quick Integration Setup

### Step 1: watsonx Orchestrate

```bash
# Install ADK
pip install ibm-watsonx-orchestrate

# Configure environment
orchestrate env add prod --instance $WO_INSTANCE --api-key $WO_API_KEY
orchestrate env activate prod
orchestrate auth login

# Deploy agents
cd docs/03-agents/agent-definitions/
orchestrate agents import -f conductor_agent.yaml
```

### Step 2: Agent Connect

```bash
# Configure external agents
# Edit agent YAML files with your endpoint URLs

# Test connectivity
orchestrate agents test conductor-agent
```

### Step 3: Verify Integration

```bash
# List deployed agents
orchestrate agents list

# Test end-to-end
orchestrate chat --agent conductor-agent
```

## 🔑 API Credentials

### watsonx Orchestrate

```bash
# Required environment variables
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here
```

**Getting Credentials:**
1. Open watsonx Orchestrate
2. Go to Settings → API Details
3. Copy Service Instance URL
4. Generate API Key

### watsonx.ai (Optional)

```bash
# Optional environment variables
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Getting Credentials:**
1. Go to watsonx.ai home page
2. Navigate to Developer access
3. Copy Project ID
4. Create IBM Cloud API key

## 📊 Integration Architecture

```
User
  ↓
watsonx Orchestrate Chat UI
  ↓
Conductor Agent (Native)
  ↓
Agent Connect Framework
  ↓
External Agents (FastAPI)
  ↓ (optional)
watsonx.ai (Granite Models)
```

## 🧪 Testing Integration

### Test Orchestrate Connection

```bash
# Verify authentication
orchestrate auth status

# List agents
orchestrate agents list

# Test agent
orchestrate chat --agent conductor-agent
```

### Test Agent Connect

```bash
# Check agent status
orchestrate agents get conductor-agent

# View logs
orchestrate agents logs conductor-agent
```

## 🐛 Troubleshooting

### Common Issues

**Authentication Failed:**
- Verify API key is correct
- Check instance URL format
- Ensure account is active

**Agent Not Found:**
- Verify agent is deployed
- Check agent name spelling
- Review deployment logs

**Connection Timeout:**
- Check network connectivity
- Verify endpoint URLs
- Review firewall settings

**Agent Not Responding:**
- Check Agent Connect configuration
- Verify external agent is running
- Review agent logs

## 📚 Integration Patterns

### Pattern 1: Native Only
All agents run on watsonx Orchestrate (simplest).

### Pattern 2: Hybrid (Recommended)
Orchestrator native, specialists external (flexible).

### Pattern 3: External Only
All agents external, Orchestrate as coordinator (advanced).

## 🔐 Security Best Practices

- Store credentials in `.env` (never commit)
- Use separate keys for dev/prod
- Rotate keys regularly
- Enable audit logging
- Follow IBM security guidelines

## 📖 Related Documentation

- [Getting Started](../01-getting-started/) - Initial setup
- [Agents](../03-agents/) - Agent documentation
- [Development](../04-development/) - Development guide
- [Hackathon](../06-hackathon/) - Submission requirements

## 🆘 Support

- **watsonx Orchestrate Docs**: https://www.ibm.com/docs/en/watson-orchestrate
- **Agent Development Kit**: https://developer.watson-orchestrate.ibm.com/
- **IBM Dev Day Slack**: #watsonx-orchestrate
- **BeMyApp Support**: support@bemyapp.com

---

**Integration Status**: 🚧 In Progress  
**Required**: watsonx Orchestrate + Agent Connect  
**Optional**: watsonx.ai
