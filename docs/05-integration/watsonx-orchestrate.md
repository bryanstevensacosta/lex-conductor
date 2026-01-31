# Integration Guide - LexConductor

**IBM Dev Day AI Demystified Hackathon**  
**Team**: AI Kings 👑  
**Version**: 1.0  
**Date**: January 30, 2026

---

## Overview

This guide provides step-by-step instructions for integrating LexConductor with IBM watsonx Orchestrate and deploying all components for the hackathon.

---

## Prerequisites

### Required Accounts & Access

- ✅ IBM Cloud account (hackathon provisioned)
- ✅ watsonx Orchestrate access
- ✅ $100 credits available
- ✅ Team member emails confirmed

### Required Software

```bash
# Check versions
python --version  # 3.11+ required
pip --version
git --version

# Install watsonx Orchestrate ADK
pip install ibm-watsonx-orchestrate

# Verify installation
orchestrate --version
```

### Required Knowledge

- Basic Python programming
- REST API concepts
- YAML configuration
- Command line usage

---

## Architecture Overview

```
User → watsonx Orchestrate Chat
    ↓
Conductor Agent (Native Orchestrate)
    ↓
Agent Connect Framework
    ↓
External Agents (Code Engine)
    ├─→ Fusion Agent → Cloudant + COS
    ├─→ Routing Agent → watsonx.ai
    ├─→ Memory Agent → Cloudant
    └─→ Traceability Agent
```

---

## Step 1: IBM Cloud Setup (30 min)

### 1.1 Access IBM Cloud Account

```bash
# Accept team invitation email
# Check spam folder if not received
# Switch to watsonx account in IBM Cloud console
```

### 1.2 Verify Available Services

Navigate to IBM Cloud Resource List and verify:
- ✅ watsonx Orchestrate instance
- ✅ watsonx.ai access
- ✅ Code Engine (Osaka region)
- ✅ Cloudant instance
- ✅ Cloud Object Storage instance

### 1.3 Check Credit Balance

```bash
# Go to: Manage → Billing and usage → Usage
# Verify: $100 credits available
# Set alerts: 25%, 50%, 80%
```

---

## Step 2: watsonx Orchestrate Setup (45 min)

### 2.1 Access watsonx Orchestrate

1. Go to IBM Cloud Resource List
2. Find watsonx Orchestrate under AI/Machine Learning
3. Click "Launch watsonx Orchestrate"
4. Wait for UI to load

### 2.2 Get API Credentials

```bash
# In watsonx Orchestrate UI:
# 1. Click Settings (gear icon)
# 2. Go to API Details
# 3. Copy Service Instance URL
# 4. Generate API Key (save securely)
```

### 2.3 Install and Configure ADK

```bash
# Install ADK
pip install ibm-watsonx-orchestrate

# Add environment
orchestrate env add prod \
  --instance https://your-instance.watson-orchestrate.ibm.com \
  --api-key YOUR_API_KEY

# Activate environment
orchestrate env activate prod

# Login
orchestrate auth login

# Verify connection
orchestrate agents list
```

---

## Step 3: Cloudant Setup (30 min)

### 3.1 Create Cloudant Instance

```bash
# If not already created:
ibmcloud resource service-instance-create \
  lexconductor-cloudant \
  cloudantnosqldb \
  lite \
  us-south
```

### 3.2 Get Cloudant Credentials

```bash
# In IBM Cloud console:
# 1. Go to Cloudant instance
# 2. Service credentials → New credential
# 3. Copy URL and API key
```

### 3.3 Create Databases

```bash
# Using Cloudant Dashboard or curl:

# Create golden_clauses database
curl -X PUT https://YOUR-CLOUDANT-URL/golden_clauses \
  -H "Authorization: Bearer YOUR_API_KEY"

# Create historical_decisions database
curl -X PUT https://YOUR-CLOUDANT-URL/historical_decisions \
  -H "Authorization: Bearer YOUR_API_KEY"

# Create regulatory_mappings database
curl -X PUT https://YOUR-CLOUDANT-URL/regulatory_mappings \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 3.4 Load Sample Data

```bash
# Create sample Golden Clause
curl -X POST https://YOUR-CLOUDANT-URL/golden_clauses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "clause_id": "golden_42",
    "type": "liability_cap",
    "contract_types": ["NDA", "MSA"],
    "text": "Liability shall be capped at $1,000,000 USD...",
    "jurisdiction": "US",
    "mandatory": true,
    "risk_level": "Low",
    "last_reviewed": "2025-12-15"
  }'
```

---

## Step 4: Cloud Object Storage Setup (30 min)

### 4.1 Create COS Instance

```bash
# If not already created:
ibmcloud resource service-instance-create \
  lexconductor-cos \
  cloud-object-storage \
  lite \
  global
```

### 4.2 Create Bucket

```bash
# In IBM Cloud console:
# 1. Go to COS instance
# 2. Create bucket
# 3. Name: watsonx-hackathon-regulations
# 4. Resiliency: Regional (us-south)
# 5. Storage class: Standard
```

### 4.3 Get COS Credentials

```bash
# In IBM Cloud console:
# 1. Go to COS instance
# 2. Service credentials → New credential
# 3. Include HMAC credential: Yes
# 4. Copy:
#    - access_key_id
#    - secret_access_key
#    - endpoints (public)
```

### 4.4 Upload Regulatory Documents

```bash
# Using IBM Cloud CLI or web UI:

# Create folder structure
# EU/
# UK/
# US/
# templates/

# Upload sample PDFs (use public regulatory documents)
# Example: EU AI Act, GDPR, CCPA, etc.
```

---

## Step 5: Code Engine Setup (45 min)

### 5.1 Create Code Engine Project

```bash
# Install IBM Cloud CLI plugin
ibmcloud plugin install code-engine

# Create project in Osaka region
ibmcloud ce project create \
  --name lexconductor \
  --region jp-osa

# Select project
ibmcloud ce project select --name lexconductor
```

### 5.2 Create External Agent Applications

```bash
# We'll deploy 3 FastAPI applications:
# 1. fusion-agent
# 2. routing-agent
# 3. traceability-agent

# For each agent, we'll:
# - Build Docker image
# - Push to IBM Container Registry
# - Deploy to Code Engine
```

### 5.3 Build and Deploy Fusion Agent

```bash
# Create Dockerfile
cat > Dockerfile.fusion <<EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fusion_agent.py .

CMD ["uvicorn", "fusion_agent:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

# Build image
docker build -f Dockerfile.fusion -t fusion-agent:latest .

# Tag for IBM Container Registry
docker tag fusion-agent:latest \
  icr.io/namespace/fusion-agent:latest

# Push to registry
docker push icr.io/namespace/fusion-agent:latest

# Deploy to Code Engine
ibmcloud ce application create \
  --name fusion-agent \
  --image icr.io/namespace/fusion-agent:latest \
  --port 8080 \
  --min-scale 0 \
  --max-scale 5 \
  --cpu 1 \
  --memory 512M \
  --env CLOUDANT_URL=https://... \
  --env CLOUDANT_API_KEY=... \
  --env COS_ENDPOINT=s3.jp-osa.cloud-object-storage.appdomain.cloud \
  --env COS_ACCESS_KEY=... \
  --env COS_SECRET_KEY=...

# Get application URL
ibmcloud ce application get --name fusion-agent
```

### 5.4 Deploy Routing and Traceability Agents

```bash
# Repeat similar process for:
# - routing-agent
# - traceability-agent

# Save all application URLs for agent definitions
```

---

## Step 6: watsonx.ai Setup (15 min)

### 6.1 Get watsonx.ai Credentials

```bash
# In IBM Cloud console:
# 1. Go to watsonx.ai
# 2. Create project or use existing
# 3. Copy Project ID
# 4. Create IBM Cloud API key (Manage → Access IAM → API keys)
```

### 6.2 Test Granite Model Access

```bash
# Using Python SDK:
pip install ibm-watsonx-ai

# Test connection
python <<EOF
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    api_key="YOUR_IBM_CLOUD_API_KEY",
    url="https://us-south.ml.cloud.ibm.com"
)

model = ModelInference(
    model_id="ibm/granite-3-8b-instruct",
    credentials=credentials,
    project_id="YOUR_PROJECT_ID"
)

response = model.generate(prompt="Hello, test")
print(response)
EOF
```

---

## Step 7: Agent Definitions (30 min)

### 7.1 Create Conductor Agent (Native)

```bash
# Create file: orchestrate/agents/conductor_agent.yaml

cat > orchestrate/agents/conductor_agent.yaml <<EOF
name: conductor-agent
version: 1.0.0
description: Primary orchestrator for legal contract review workflow

model:
  provider: watsonx.ai
  model_id: ibm/granite-3-8b-instruct
  parameters:
    max_tokens: 2000
    temperature: 0.3

system_prompt: |
  You are the Conductor Agent for LexConductor, a legal AI system.
  
  Your role:
  1. Classify contract type (NDA, MSA, Service Agreement, etc.)
  2. Delegate analysis to specialized agents
  3. Aggregate their responses
  4. Present a coherent Legal Logic Trace
  
  Be concise, accurate, and professional.

collaborators:
  - fusion-agent
  - routing-agent
  - memory-agent
  - traceability-agent

tools:
  - name: classify_contract
    description: Classify the type of legal contract
  - name: delegate_analysis
    description: Delegate to specialized agents
  - name: aggregate_results
    description: Combine agent responses
EOF
```

### 7.2 Create External Agent Definitions

```bash
# Fusion Agent
cat > orchestrate/agents/fusion_agent.yaml <<EOF
name: fusion-agent
version: 1.0.0
description: Correlates internal policies with external regulations
type: external

connection:
  type: agent_connect
  endpoint: https://fusion-agent.jp-osa.codeengine.appdomain.cloud
  api_key: \${FUSION_AGENT_API_KEY}
  timeout: 30

capabilities:
  - contract_analysis
  - signal_correlation
  - compliance_checking

input_schema:
  type: object
  properties:
    contract_text:
      type: string
    contract_type:
      type: string
    jurisdiction:
      type: string
  required:
    - contract_text
    - contract_type

output_schema:
  type: object
  properties:
    internal_signals:
      type: array
    external_signals:
      type: array
    gaps:
      type: array
    confidence:
      type: number
EOF

# Routing Agent
cat > orchestrate/agents/routing_agent.yaml <<EOF
name: routing-agent
version: 1.0.0
description: Dynamically selects legal processing path
type: external

connection:
  type: agent_connect
  endpoint: https://routing-agent.jp-osa.codeengine.appdomain.cloud
  api_key: \${ROUTING_AGENT_API_KEY}
  timeout: 30

capabilities:
  - risk_assessment
  - complexity_classification
  - workflow_routing
EOF

# Memory Agent
cat > orchestrate/agents/memory_agent.yaml <<EOF
name: memory-agent
version: 1.0.0
description: Manages jurisprudential recall and historical precedents
type: external

connection:
  type: agent_connect
  endpoint: https://memory-agent.jp-osa.codeengine.appdomain.cloud
  api_key: \${MEMORY_AGENT_API_KEY}
  timeout: 30

capabilities:
  - precedent_search
  - historical_analysis
  - golden_clause_retrieval
EOF

# Traceability Agent
cat > orchestrate/agents/traceability_agent.yaml <<EOF
name: traceability-agent
version: 1.0.0
description: Generates explainable decision audit trails
type: external

connection:
  type: agent_connect
  endpoint: https://traceability-agent.jp-osa.codeengine.appdomain.cloud
  api_key: \${TRACEABILITY_AGENT_API_KEY}
  timeout: 30

capabilities:
  - audit_trail_generation
  - legal_logic_trace
  - confidence_scoring
EOF
```

### 7.3 Create Environment Configuration

```bash
# Create .env.example
cat > orchestrate/.env.example <<EOF
# watsonx Orchestrate
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here

# watsonx.ai
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Cloudant
CLOUDANT_URL=https://your-cloudant.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=your_cloudant_key

# Cloud Object Storage
COS_ENDPOINT=s3.jp-osa.cloud-object-storage.appdomain.cloud
COS_ACCESS_KEY=your_access_key
COS_SECRET_KEY=your_secret_key
COS_BUCKET=watsonx-hackathon-regulations

# External Agent API Keys
FUSION_AGENT_API_KEY=generate_random_key_here
ROUTING_AGENT_API_KEY=generate_random_key_here
MEMORY_AGENT_API_KEY=generate_random_key_here
TRACEABILITY_AGENT_API_KEY=generate_random_key_here
EOF

# Copy to .env and fill in actual values
cp orchestrate/.env.example orchestrate/.env
# Edit .env with your actual credentials
```

---

## Step 8: Import Agents to Orchestrate (15 min)

### 8.1 Import Agent Definitions

```bash
# Import Conductor Agent
orchestrate agents import -f orchestrate/agents/conductor_agent.yaml

# Import External Agents
orchestrate agents import -f orchestrate/agents/fusion_agent.yaml
orchestrate agents import -f orchestrate/agents/routing_agent.yaml
orchestrate agents import -f orchestrate/agents/memory_agent.yaml
orchestrate agents import -f orchestrate/agents/traceability_agent.yaml

# Verify imports
orchestrate agents list
```

### 8.2 Deploy Agents

```bash
# Deploy Conductor Agent
orchestrate agents deploy conductor-agent

# Verify deployment
orchestrate agents get conductor-agent
```

---

## Step 9: Testing (30 min)

### 9.1 Test Individual Agents

```bash
# Test Fusion Agent directly
curl -X POST https://fusion-agent.jp-osa.codeengine.appdomain.cloud/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_FUSION_AGENT_API_KEY" \
  -d '{
    "contract_text": "Party A shall indemnify Party B...",
    "contract_type": "NDA",
    "jurisdiction": "US"
  }'

# Test Routing Agent
curl -X POST https://routing-agent.jp-osa.codeengine.appdomain.cloud/route \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_ROUTING_AGENT_API_KEY" \
  -d '{
    "fusion_output": {...},
    "contract_type": "NDA"
  }'
```

### 9.2 Test End-to-End via Orchestrate

```bash
# Test via CLI
orchestrate chat --agent conductor-agent

# In chat, type:
# "Analyze this NDA: [paste sample NDA text]"

# Verify:
# - Conductor receives request
# - External agents are called
# - Results are aggregated
# - Legal Logic Trace is generated
```

### 9.3 Test via Web UI

```bash
# 1. Open watsonx Orchestrate web UI
# 2. Go to Chat
# 3. Select conductor-agent
# 4. Upload sample contract or paste text
# 5. Verify complete workflow
# 6. Check Legal Logic Trace output
```

---

## Step 10: Monitoring & Debugging (15 min)

### 10.1 View Agent Logs

```bash
# Orchestrate logs
orchestrate agents logs conductor-agent --follow

# Code Engine logs
ibmcloud ce application logs --name fusion-agent --follow
ibmcloud ce application logs --name routing-agent --follow
ibmcloud ce application logs --name traceability-agent --follow
```

### 10.2 Check Agent Status

```bash
# Orchestrate agent status
orchestrate agents get conductor-agent

# Code Engine application status
ibmcloud ce application get --name fusion-agent
```

### 10.3 Monitor Costs

```bash
# Check credit usage
# Go to: IBM Cloud → Manage → Billing and usage → Usage
# Monitor:
# - watsonx.ai token usage
# - Code Engine vCPU-seconds
# - Cloudant operations
# - COS storage/bandwidth
```

---

## Troubleshooting

### Common Issues

#### Issue: Agent import fails
```bash
# Solution: Check YAML syntax
yamllint orchestrate/agents/conductor_agent.yaml

# Verify credentials in .env
cat orchestrate/.env
```

#### Issue: External agent not responding
```bash
# Check Code Engine application status
ibmcloud ce application get --name fusion-agent

# Check logs for errors
ibmcloud ce application logs --name fusion-agent --tail 100

# Verify environment variables
ibmcloud ce application get --name fusion-agent --output yaml
```

#### Issue: Cloudant connection fails
```bash
# Test connection
curl -X GET https://YOUR-CLOUDANT-URL/_all_dbs \
  -H "Authorization: Bearer YOUR_API_KEY"

# Verify credentials in .env
```

#### Issue: watsonx.ai quota exceeded
```bash
# Check usage
# Go to: watsonx.ai → Project → Usage

# Optimize prompts to reduce tokens
# Use caching where possible
```

---

## Security Checklist

- [ ] All credentials in `.env` (never committed)
- [ ] `.gitignore` includes `.env`
- [ ] API keys rotated regularly
- [ ] Code Engine environment variables set via secrets
- [ ] No hardcoded credentials in code
- [ ] HTTPS used for all connections
- [ ] Cloudant database ACLs configured
- [ ] COS bucket policies configured

---

## Performance Optimization

### Prompt Optimization
- Keep prompts concise (<500 tokens)
- Use structured output formats (JSON)
- Avoid unnecessary context

### Caching Strategy
- Cache Golden Clauses in memory
- Cache frequently accessed regulations
- Use Cloudant indexes for fast queries

### Parallel Execution
- Fusion + Memory agents run in parallel
- Routing agent runs after Fusion completes
- Minimize sequential dependencies

---

## Next Steps

1. ✅ Complete integration (Steps 1-10)
2. ✅ Test end-to-end workflow
3. ✅ Optimize performance (<10s target)
4. ✅ Prepare demo environment
5. ✅ Record video demo
6. ✅ Write submission statements
7. ✅ Submit before deadline

---

## Support Resources

### Documentation
- [watsonx Orchestrate Docs](https://www.ibm.com/docs/en/watson-orchestrate)
- [Agent Development Kit](https://developer.watson-orchestrate.ibm.com/)
- [Code Engine Docs](https://cloud.ibm.com/docs/codeengine)
- [Cloudant Docs](https://cloud.ibm.com/docs/Cloudant)

### Hackathon Support
- IBM Dev Day Slack: #watsonx-orchestrate
- BeMyApp Support: support@bemyapp.com
- Hackathon Mentors: Via BeMyApp platform

### Team Resources
- [HACKATHON-CHECKLIST.md](HACKATHON-CHECKLIST.md) - Submission checklist
- [docs/Technical.md](docs/Technical.md) - Technical architecture
- [`.kiro/steering/tech.md`](../.kiro/steering/tech.md) - Technical resources

---

**Document Owner**: Team AI Kings  
**Last Updated**: January 30, 2026  
**Status**: Ready for Implementation  
**Estimated Time**: 3-4 hours for complete setup
