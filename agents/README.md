# watsonx Orchestrate Agent Definitions

This directory contains agent definitions for LexConductor to be deployed on IBM watsonx Orchestrate.

## Agent Architecture

LexConductor uses a **hybrid architecture** combining:
- **1 Native Agent**: Conductor Agent (runs on watsonx Orchestrate)
- **4 External Agents**: Fusion, Memory, Routing, Traceability (run on Code Engine via Agent Connect)

## Agent Definitions

### Native Agent

**conductor_agent.yaml**
- Primary orchestrator for the entire workflow
- Receives user queries via watsonx Orchestrate Chat
- Delegates to external agents
- Synthesizes final Legal Logic Trace
- Model: IBM Granite 3 8B Instruct

### External Agents

**fusion_agent_external.yaml**
- Correlates internal policies with external regulations
- Queries Cloudant for Golden Clauses
- Retrieves regulatory PDFs from COS
- Identifies compliance gaps
- Endpoint: `${FUSION_AGENT_ENDPOINT}`

**memory_agent_external.yaml**
- Manages institutional memory and precedents
- Searches historical contract decisions
- Retrieves Golden Clauses
- Identifies modification patterns
- Endpoint: `${MEMORY_AGENT_ENDPOINT}`

**routing_agent_external.yaml**
- Assesses contract risk and complexity
- Classifies into ROUTINE/STANDARD/COMPLEX
- Determines human-in-loop requirements
- Routes to appropriate workflow
- Endpoint: `${ROUTING_AGENT_ENDPOINT}`

**traceability_agent_external.yaml**
- Generates comprehensive audit trails
- Creates Legal Logic Traces
- Documents decision provenance
- Ensures explainable AI
- Endpoint: `${TRACEABILITY_AGENT_ENDPOINT}`

## Prerequisites

1. **watsonx Orchestrate Environment Configured**
   ```bash
   orchestrate env list
   # Should show 'prod' environment as active
   ```

2. **Environment Variables Set**
   
   External agent endpoints will be set after Code Engine deployment:
   ```bash
   export FUSION_AGENT_ENDPOINT="https://fusion-agent.xxx.jp-osa.codeengine.appdomain.cloud"
   export FUSION_AGENT_API_KEY="your-api-key"
   export MEMORY_AGENT_ENDPOINT="https://memory-agent.xxx.jp-osa.codeengine.appdomain.cloud"
   export MEMORY_AGENT_API_KEY="your-api-key"
   export ROUTING_AGENT_ENDPOINT="https://routing-agent.xxx.jp-osa.codeengine.appdomain.cloud"
   export ROUTING_AGENT_API_KEY="your-api-key"
   export TRACEABILITY_AGENT_ENDPOINT="https://traceability-agent.xxx.jp-osa.codeengine.appdomain.cloud"
   export TRACEABILITY_AGENT_API_KEY="your-api-key"
   ```

3. **Backend Services Deployed**
   
   External agents must be running on Code Engine before importing to Orchestrate.

## Deployment Steps

### Step 1: Deploy Backend Services to Code Engine

First, deploy the FastAPI backend services that implement the external agents:

```bash
# From project root
cd backend
# Follow deployment instructions in backend/README.md
```

### Step 2: Import Conductor Agent (Native)

Import the native orchestrator agent:

```bash
orchestrate agents import -f orchestrate/agents/conductor_agent.yaml
```

Verify import:
```bash
orchestrate agents list
# Should show 'conductor-agent'
```

### Step 3: Import External Agents

Import external agent connectors (after backend is deployed):

```bash
# Fusion Agent
orchestrate agents import -f orchestrate/agents/fusion_agent_external.yaml

# Memory Agent
orchestrate agents import -f orchestrate/agents/memory_agent_external.yaml

# Routing Agent
orchestrate agents import -f orchestrate/agents/routing_agent_external.yaml

# Traceability Agent
orchestrate agents import -f orchestrate/agents/traceability_agent_external.yaml
```

Verify all agents:
```bash
orchestrate agents list
```

Expected output:
```
conductor-agent (native)
fusion-agent (external)
memory-agent (external)
routing-agent (external)
traceability-agent (external)
```

### Step 4: Deploy Agents

Deploy all agents to watsonx Orchestrate:

```bash
orchestrate agents deploy conductor-agent
orchestrate agents deploy fusion-agent
orchestrate agents deploy memory-agent
orchestrate agents deploy routing-agent
orchestrate agents deploy traceability-agent
```

### Step 5: Test Agent Communication

Test the conductor agent via chat:

```bash
orchestrate chat --agent conductor-agent
```

Example test query:
```
Please analyze this NDA clause:
"Party A shall indemnify Party B for any damages up to $1,000,000."
```

## Agent Collaboration Flow

```
User Query
    ↓
Conductor Agent (Native)
    ↓
    ├─→ Fusion Agent (External) ──→ Cloudant + COS
    ├─→ Memory Agent (External) ──→ Cloudant
    └─→ Routing Agent (External) ──→ Risk Analysis
    ↓
Conductor Agent (Aggregates)
    ↓
Traceability Agent (External) ──→ Audit Trail
    ↓
Conductor Agent (Final Response)
    ↓
User (Legal Logic Trace)
```

## Monitoring & Debugging

### View Agent Logs

```bash
# Conductor agent logs
orchestrate agents logs conductor-agent --follow

# External agent logs (from Code Engine)
ibmcloud ce app logs --name fusion-agent --follow
ibmcloud ce app logs --name memory-agent --follow
ibmcloud ce app logs --name routing-agent --follow
ibmcloud ce app logs --name traceability-agent --follow
```

### Check Agent Status

```bash
orchestrate agents get conductor-agent
orchestrate agents get fusion-agent
orchestrate agents get memory-agent
orchestrate agents get routing-agent
orchestrate agents get traceability-agent
```

### Test Individual Agents

```bash
# Test conductor
orchestrate chat --agent conductor-agent

# Test external agents via their HTTP endpoints
curl -X POST "${FUSION_AGENT_ENDPOINT}/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${FUSION_AGENT_API_KEY}" \
  -d '{
    "contract_text": "Test clause",
    "contract_type": "NDA"
  }'
```

## Troubleshooting

### Agent Import Fails

**Error**: `Invalid YAML format`
- Check YAML syntax with `yamllint orchestrate/agents/*.yaml`
- Ensure proper indentation (2 spaces)

**Error**: `Environment variable not set`
- Verify all `${VARIABLE}` placeholders have values
- Run `env | grep AGENT` to check

### Agent Not Responding

**External agents timeout**:
1. Check Code Engine app status: `ibmcloud ce app get --name fusion-agent`
2. Verify endpoint is accessible: `curl ${FUSION_AGENT_ENDPOINT}/health`
3. Check API key is correct
4. Review agent logs for errors

**Conductor agent fails**:
1. Check collaborator agents are deployed
2. Verify model access (Granite 3 8B)
3. Review agent logs: `orchestrate agents logs conductor-agent`

### Agent Connect Issues

**Error**: `Failed to connect to external agent`
- Verify Code Engine apps are running
- Check network connectivity
- Ensure API keys match
- Review firewall/security group rules

## Configuration Updates

### Update Agent Definition

1. Edit YAML file
2. Re-import agent:
   ```bash
   orchestrate agents import -f orchestrate/agents/conductor_agent.yaml --force
   ```
3. Redeploy:
   ```bash
   orchestrate agents deploy conductor-agent
   ```

### Update External Agent Endpoint

1. Update environment variable
2. Re-import external agent definition
3. Restart agent connection

## Performance Tuning

### Response Time Targets

- Fusion Agent: < 5 seconds
- Memory Agent: < 2 seconds
- Routing Agent: < 1 second
- Traceability Agent: < 2 seconds
- **Total End-to-End**: < 10 seconds

### Optimization Tips

1. **Caching**: Enable caching for Golden Clauses (1 hour TTL)
2. **Parallel Execution**: Fusion, Memory, Routing run in parallel
3. **Connection Pooling**: Reuse HTTP connections to external agents
4. **Model Selection**: Granite 3 8B balances speed and quality
5. **Prompt Optimization**: Keep prompts concise to reduce tokens

## Security Considerations

### API Key Management

- Never commit API keys to git
- Use environment variables
- Rotate keys regularly
- Use separate keys per agent

### Network Security

- All traffic over HTTPS
- Code Engine private endpoints (optional)
- API key authentication required
- Rate limiting enabled

### Data Protection

- No PII in agent definitions
- Audit trails encrypted at rest
- TLS 1.2+ for all connections
- Compliance with hackathon rules

## Related Documentation

- [Agent Architecture](../docs/03-agents/agent-architecture.md)
- [Backend Implementation](../backend/README.md)
- [Code Engine Deployment](../docs/07-infrastructure/ibm-cloud.md)
- [watsonx Orchestrate Docs](https://www.ibm.com/docs/en/watson-orchestrate)
- [Agent Development Kit](https://developer.watson-orchestrate.ibm.com/)

## Support

### IBM Dev Day Hackathon

- **Slack**: #watsonx-orchestrate
- **BeMyApp Support**: support@bemyapp.com
- **Team**: AI Kings 👑

### Useful Commands

```bash
# List all agents
orchestrate agents list

# Get agent details
orchestrate agents get <agent-name>

# View agent logs
orchestrate agents logs <agent-name> --follow

# Test agent via chat
orchestrate chat --agent <agent-name>

# Delete agent
orchestrate agents delete <agent-name>

# Check environment
orchestrate env list
```

---

**Created**: January 30, 2026  
**Team**: AI Kings 👑  
**Hackathon**: IBM Dev Day AI Demystified 2026  
**Deadline**: February 1, 2026 - 10:00 AM ET
