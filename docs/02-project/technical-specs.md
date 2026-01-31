# Technical Architecture - LexConductor

**IBM Dev Day AI Demystified Hackathon**  
**Team**: AI Kings 👑  
**Version**: 1.0  
**Date**: January 30, 2026

---

## Architecture Overview

LexConductor implements a **hybrid multi-agent architecture** combining native watsonx Orchestrate agents with external specialized agents for maximum flexibility and governance.

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│              watsonx Orchestrate Chat UI                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Orchestration Layer                         │
│         Conductor Agent (Native Orchestrate)                 │
│              IBM Granite 3 8B Instruct                       │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   Agent Connect          │  │   Agent Connect          │
│   Framework              │  │   Framework              │
└──────────────────────────┘  └──────────────────────────┘
            │                             │
            ▼                             ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│  External Agents Layer   │  │  External Agents Layer   │
│  (IBM Code Engine)       │  │  (IBM Code Engine)       │
│                          │  │                          │
│  • Fusion Agent          │  │  • Routing Agent         │
│  • Memory Agent          │  │  • Traceability Agent    │
└──────────────────────────┘  └──────────────────────────┘
            │                             │
            ▼                             ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│    Data Layer            │  │    AI Inference Layer    │
│                          │  │                          │
│  • Cloudant (Policies)   │  │  • watsonx.ai            │
│  • COS (Regulations)     │  │  • Granite 3 8B Instruct │
└──────────────────────────┘  └──────────────────────────┘
```

---

## Agent Architecture

### 1. Conductor Agent (Native Orchestrate)

**Type**: Native watsonx Orchestrate Agent  
**Role**: Primary orchestrator managing entire workflow  
**Location**: watsonx Orchestrate SaaS

#### Responsibilities
- Receive contract review requests via Chat UI
- Classify contract type (NDA, MSA, Service Agreement, etc.)
- Delegate to specialized sub-agents in parallel
- Aggregate results from all agents
- Present final Legal Logic Trace to user
- Manage conversation flow and user interaction

#### Technology Stack
- **Platform**: IBM watsonx Orchestrate
- **Model**: IBM Granite 3 8B Instruct
- **Interface**: Chat UI (web-based)
- **Configuration**: YAML agent definition

#### Agent Definition Structure
```yaml
name: conductor-agent
version: 1.0.0
description: Primary orchestrator for legal contract review
model:
  provider: watsonx.ai
  model_id: ibm/granite-3-8b-instruct
collaborators:
  - fusion-agent
  - routing-agent
  - memory-agent
  - traceability-agent
```

---

### 2. Fusion Agent (External)

**Type**: External Agent via Agent Connect Framework  
**Role**: Correlates internal policies with external regulations  
**Location**: IBM Code Engine (Osaka region)

#### Responsibilities
- Query Cloudant for "Golden Clauses" (internal policies)
- Retrieve regulatory PDFs from Cloud Object Storage
- Perform signal correlation analysis
- Identify compliance gaps between signals
- Return structured analysis with confidence scores

#### Technology Stack
- **Backend**: Python 3.11+ with FastAPI
- **Hosting**: IBM Code Engine (jp-osa)
- **Database**: IBM Cloudant
- **Storage**: IBM Cloud Object Storage
- **Connection**: Agent Connect Framework (chat completions API)

#### API Endpoints
```python
POST /analyze-contract
{
  "contract_text": "...",
  "contract_type": "NDA",
  "jurisdiction": "US"
}

Response:
{
  "internal_signals": [...],
  "external_signals": [...],
  "gaps": [...],
  "confidence": 0.92
}
```

#### Data Flow
```
Contract Text
    ↓
Cloudant Query (Golden Clauses)
    ↓
COS Query (Regulatory PDFs)
    ↓
Signal Correlation Logic
    ↓
Gap Analysis
    ↓
Structured Response
```

---

### 3. Routing Agent (External)

**Type**: External Agent via watsonx.ai  
**Role**: Dynamically selects legal processing path  
**Location**: watsonx.ai inference

#### Responsibilities
- Analyze risk level from Fusion Agent output
- Classify contract complexity (Routine/Standard/Complex)
- Determine appropriate workflow path
- Provide risk scoring and justification
- Recommend human-in-loop requirements

#### Technology Stack
- **Model**: IBM Granite 3 8B Instruct
- **Platform**: watsonx.ai
- **Prompt**: Custom legal risk assessment prompt
- **Connection**: Agent Connect Framework

#### Routing Logic
```python
def route_contract(fusion_output):
    risk_score = calculate_risk(fusion_output)
    
    if risk_score < 0.3:
        return "ROUTINE"  # Auto-approve
    elif risk_score < 0.7:
        return "STANDARD"  # Paralegal review
    else:
        return "COMPLEX"  # GC escalation
```

#### Risk Factors
- Number of compliance gaps detected
- Severity of regulatory conflicts
- Contract value and strategic importance
- Historical precedent availability
- Jurisdiction complexity

---

### 4. Memory Agent (External)

**Type**: External Agent via Cloudant  
**Role**: Manages "Jurisprudential Recall"  
**Location**: IBM Cloudant

#### Responsibilities
- Store historical contract decisions
- Retrieve similar past cases
- Provide precedent-based recommendations
- Maintain "Golden Clause" library
- Track clause modification patterns

#### Technology Stack
- **Database**: IBM Cloudant (NoSQL)
- **Data Format**: JSON documents
- **Indexing**: Cloudant Query indexes
- **Access**: RESTful API

#### Data Schema
```json
{
  "_id": "decision_2025_Q4_001",
  "contract_type": "NDA",
  "clause_modified": "Section 4 - Indemnification",
  "original_text": "...",
  "modified_text": "...",
  "rationale": "CCPA 2026 compliance",
  "approved_by": "Head of Legal",
  "date": "2025-12-15",
  "jurisdiction": "US",
  "confidence": 0.95,
  "tags": ["data-breach", "liability-cap", "ccpa"]
}
```

#### Query Patterns
- Find similar contracts by type and jurisdiction
- Retrieve clauses modified in last N months
- Search by regulatory requirement
- Filter by confidence score threshold

---

### 5. Traceability Agent (External)

**Type**: External Agent via Code Engine  
**Role**: Generates explainable decision audit trails  
**Location**: IBM Code Engine

#### Responsibilities
- Document decision logic at each step
- Create "Legal Logic Trace" reports
- Ensure transparency and auditability
- Provide confidence scores for each recommendation
- Generate structured output for compliance

#### Technology Stack
- **Backend**: Python 3.11+ with FastAPI
- **Hosting**: IBM Code Engine
- **Logging**: Structured JSON logging
- **Reporting**: Markdown/JSON output formats

#### Output Format
```markdown
═══════════════════════════════════════════════════
LEGAL LOGIC TRACE
═══════════════════════════════════════════════════

Contract: NDA-2026-0130-001
Timestamp: 2026-01-30 14:23:15 UTC

SIGNAL ANALYSIS:
✓ Internal Signal: Golden Clause #42 (Confidence: 0.95)
⚠ External Signal: CCPA 2026 conflict (Confidence: 0.92)
✓ Historical Signal: 3 precedents found (Confidence: 0.88)

RISK ASSESSMENT:
Overall Risk: MEDIUM
Routing Decision: STANDARD (Paralegal Review)

RECOMMENDED ACTION:
Modify Section 4 - Add data breach carve-out
Confidence: 0.92

═══════════════════════════════════════════════════
```

---

## Data Architecture

### Cloudant Database (Pattern Memory)

**Purpose**: Store Golden Clauses and historical decisions

#### Collections

**1. golden_clauses**
```json
{
  "clause_id": "golden_42",
  "type": "liability_cap",
  "contract_types": ["NDA", "MSA"],
  "text": "Liability capped at $1M...",
  "jurisdiction": "US",
  "mandatory": true,
  "risk_level": "Low",
  "last_reviewed": "2025-12-15"
}
```

**2. historical_decisions**
```json
{
  "decision_id": "dec_2025_Q4_001",
  "contract_type": "NDA",
  "modifications": [...],
  "rationale": "...",
  "confidence": 0.95,
  "approved_by": "Head of Legal"
}
```

**3. regulatory_mappings**
```json
{
  "regulation_id": "CCPA_2026",
  "jurisdiction": "US",
  "requirements": [...],
  "affected_clauses": ["indemnification", "data_breach"],
  "cos_url": "s3://regulations/US/CCPA-2026.pdf"
}
```

#### Indexes
- By contract type
- By jurisdiction
- By confidence score
- By date range
- By regulatory requirement

---

### Cloud Object Storage (Evidence Locker)

**Purpose**: Store regulatory PDFs and reference documents

#### Bucket Structure
```
watsonx-hackathon-regulations/
├── EU/
│   ├── AI-Act-2024.pdf
│   ├── GDPR-Full-Text.pdf
│   ├── DSA-2023.pdf
│   └── ...
├── UK/
│   ├── Data-Protection-Act-2018.pdf
│   ├── Companies-Act-2006.pdf
│   └── ...
├── US/
│   ├── CCPA-2026-Amendment.pdf
│   ├── HIPAA-Privacy-Rule.pdf
│   └── ...
└── templates/
    ├── NDA-Standard.pdf
    └── MSA-Template.pdf
```

#### Access Pattern
1. Fusion Agent queries Cloudant for regulatory mapping
2. Cloudant returns COS URL for relevant PDF
3. Fusion Agent retrieves PDF from COS
4. Extract relevant sections for analysis
5. Cache frequently accessed documents

---

## AI/ML Architecture

### Model Selection

**Primary Model**: IBM Granite 3 8B Instruct

**Rationale**:
- ✅ Optimized for speed (<10s response time)
- ✅ Cost-efficient (~$0.0001 per 1,000 tokens)
- ✅ Fits within $100 credit limit
- ✅ Strong reasoning capabilities
- ✅ Multilingual support (EU/UK/US regulations)

**Prohibited Models** (DO NOT USE):
- ❌ llama-3-405b-instruct (too expensive)
- ❌ mistral-medium-2505 (may impact judging)
- ❌ mistral-small-3-1-24b-instruct-2503 (may impact judging)

### Prompt Engineering

#### Conductor Agent Prompt
```
You are the Conductor Agent for LexConductor, a legal AI system.

Your role:
1. Classify the contract type (NDA, MSA, Service Agreement, etc.)
2. Delegate analysis to specialized agents
3. Aggregate their responses
4. Present a coherent Legal Logic Trace

Input: Contract text and metadata
Output: Structured JSON with agent delegation plan

Be concise, accurate, and professional.
```

#### Fusion Agent Prompt
```
You are a Legal Signal Fusion Specialist.

Task: Correlate internal policies with external regulations.

Given:
- Contract clause text
- Golden Clause from company policy
- Regulatory requirement from [REGULATION]

Identify:
1. Alignment between signals (0.0 to 1.0)
2. Compliance gaps
3. Recommended modifications

Output: Structured JSON with confidence scores.
```

#### Routing Agent Prompt
```
You are a Legal Risk Assessment Specialist.

Task: Classify contract complexity and risk level.

Given:
- Fusion Agent analysis
- Number of compliance gaps
- Contract type and value

Determine:
1. Risk Level: LOW / MEDIUM / HIGH
2. Routing Decision: ROUTINE / STANDARD / COMPLEX
3. Justification

Output: Structured JSON with risk assessment.
```

---

## Integration Architecture

### Agent Connect Framework

**Purpose**: Connect watsonx Orchestrate to external agents

#### Communication Protocol
- **API**: Chat Completions API (OpenAI-compatible)
- **Format**: JSON over HTTPS
- **Authentication**: API keys via environment variables
- **Timeout**: 30 seconds per agent call

#### External Agent YAML Definition
```yaml
name: fusion-agent
version: 1.0.0
type: external
connection:
  type: agent_connect
  endpoint: https://fusion-agent.jp-osa.codeengine.appdomain.cloud
  api_key: ${FUSION_AGENT_API_KEY}
  timeout: 30
capabilities:
  - contract_analysis
  - signal_correlation
  - compliance_checking
```

---

## Deployment Architecture

### IBM Code Engine Deployment

**Region**: Osaka (jp-osa)  
**Runtime**: Python 3.11  
**Framework**: FastAPI

#### Service Configuration
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: fusion-agent
spec:
  template:
    spec:
      containers:
      - image: icr.io/namespace/fusion-agent:latest
        env:
        - name: CLOUDANT_URL
          valueFrom:
            secretKeyRef:
              name: cloudant-credentials
              key: url
        - name: COS_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: cos-credentials
              key: endpoint
        resources:
          limits:
            memory: 512Mi
            cpu: 1000m
```

#### Auto-scaling
- Min instances: 0 (scale to zero)
- Max instances: 5
- Concurrency: 10 requests per instance
- Scale-up threshold: 80% CPU

---

## Security Architecture

### Authentication & Authorization

**watsonx Orchestrate**:
- API key authentication
- Service instance URL
- Environment-based configuration

**Code Engine**:
- IAM-based authentication
- Service-to-service credentials
- Secrets management via Kubernetes secrets

**Cloudant**:
- API key authentication
- Database-level access control
- TLS encryption in transit

**Cloud Object Storage**:
- HMAC credentials
- Bucket-level access policies
- Server-side encryption at rest

### Secrets Management

```bash
# .env file (NEVER commit)
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
CLOUDANT_URL=https://your-cloudant.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=your_cloudant_key
COS_ENDPOINT=s3.jp-osa.cloud-object-storage.appdomain.cloud
COS_API_KEY=your_cos_key
COS_INSTANCE_ID=your_instance_id
```

### Data Security

- ✅ All data in transit encrypted (TLS 1.2+)
- ✅ All data at rest encrypted (AES-256)
- ✅ No PII or confidential data stored
- ✅ Public regulatory documents only
- ✅ Synthetic contract examples for demo

---

## Performance Architecture

### Response Time Targets

| Operation | Target | Acceptable |
|-----------|--------|------------|
| Contract classification | <1s | <2s |
| Fusion analysis | <5s | <8s |
| Routing decision | <1s | <2s |
| Memory recall | <2s | <3s |
| Traceability report | <1s | <2s |
| **Total end-to-end** | **<10s** | **<15s** |

### Optimization Strategies

1. **Prompt Optimization**
   - Concise, focused prompts
   - Structured output formats
   - Minimal token usage

2. **Caching**
   - Cache Golden Clauses in memory
   - Cache frequently accessed regulations
   - Cache historical precedents

3. **Parallel Execution**
   - Fusion + Memory agents run in parallel
   - Routing agent runs after Fusion completes
   - Traceability agent runs last

4. **Model Selection**
   - Granite 3 8B (fast, cost-efficient)
   - Avoid larger models (slower, expensive)

---

## Cost Architecture

### Estimated Costs (within $100 limit)

**watsonx.ai (Granite 3 8B Instruct)**:
- Cost: ~$0.0001 per 1,000 tokens
- Estimated usage: 100 contracts × 5,000 tokens = 500,000 tokens
- **Total**: ~$0.05 USD

**Code Engine**:
- Free tier: 100,000 vCPU-seconds/month
- Estimated usage: Minimal for hackathon
- **Total**: $0 USD (within free tier)

**Cloudant**:
- Free tier: 1 GB storage, 20 reads/sec
- Estimated usage: <100 MB, <10 reads/sec
- **Total**: $0 USD (within free tier)

**Cloud Object Storage**:
- Free tier: 25 GB storage
- Estimated usage: <1 GB (regulatory PDFs)
- **Total**: $0 USD (within free tier)

**Grand Total**: <$5 USD (well within $100 limit)

---

## Monitoring & Observability

### Logging Strategy

**Structured Logging** (JSON format):
```json
{
  "timestamp": "2026-01-30T14:23:15Z",
  "level": "INFO",
  "agent": "fusion-agent",
  "operation": "signal_correlation",
  "contract_id": "NDA-2026-0130-001",
  "duration_ms": 1234,
  "confidence": 0.92,
  "status": "success"
}
```

### Metrics

- Request count per agent
- Response time percentiles (p50, p95, p99)
- Error rate
- Confidence score distribution
- Token usage per request

### Alerting (Optional)

- Response time >15s
- Error rate >5%
- Credit usage >80%

---

## Disaster Recovery

### Backup Strategy

**Cloudant**:
- Automatic continuous backup
- Point-in-time recovery
- Cross-region replication (optional)

**Cloud Object Storage**:
- Versioning enabled
- Cross-region replication (optional)
- Immutable objects

### Failure Scenarios

| Scenario | Impact | Recovery |
|----------|--------|----------|
| Code Engine down | High | Retry logic, fallback to cached data |
| Cloudant unavailable | Medium | Use cached Golden Clauses |
| COS unavailable | Low | Use cached regulations |
| watsonx.ai timeout | Medium | Retry with exponential backoff |

---

## Testing Strategy

### Unit Tests
- Individual agent logic
- Signal correlation algorithms
- Risk scoring functions
- Data access layers

### Integration Tests
- Agent-to-agent communication
- Orchestrate → Code Engine flow
- Database queries
- COS access

### End-to-End Tests
- Complete contract review workflow
- All three routing paths (Routine/Standard/Complex)
- Error handling scenarios
- Performance benchmarks

### Demo Preparation
- Record backup video
- Test with multiple contract types
- Verify all agents responding
- Check Legal Logic Trace output

---

## Appendix

### Technology Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Orchestration | watsonx Orchestrate | Primary platform (MANDATORY) |
| AI Inference | watsonx.ai | Granite 3 8B Instruct |
| External Agents | Python 3.11 + FastAPI | Custom agent logic |
| Hosting | IBM Code Engine | Serverless deployment |
| Database | IBM Cloudant | NoSQL for policies |
| Storage | IBM Cloud Object Storage | Regulatory PDFs |
| Integration | Agent Connect Framework | Agent communication |

### API Reference

See `INTEGRATION-GUIDE.md` for detailed API documentation.

### Configuration Reference

See `orchestrate/README.md` for deployment configuration.

---

**Document Owner**: Team AI Kings  
**Last Updated**: January 30, 2026  
**Status**: Draft - Awaiting Team Selection  
**Next Review**: After project selection
