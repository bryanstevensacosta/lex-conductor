# Technical Resources - IBM Dev Day AI Demystified Hackathon

This guide covers the technical resources, platforms, and tools available for the hackathon.

## Required Technology

### IBM watsonx Orchestrate (MANDATORY)

**What it is**: AI-powered platform for building and deploying intelligent agents that automate business workflows.

**Why it's required**: All submissions MUST use watsonx Orchestrate to be eligible for prizes.

**Key Capabilities**:
- No-code and low-code agent building
- Multi-agent orchestration and collaboration
- Agent Development Kit (ADK) for developers
- Pre-built agents and tools catalog
- Integration with external systems via Agent Connect
- Built-in governance and observability
- Chat interface for agent interaction

**Access**:
- Provided via IBM Cloud account (hackathon provisioned)
- Launch from IBM Cloud Resource List → AI/Machine Learning
- Web UI + CLI (ADK) available

**Documentation**:
- Main docs: https://www.ibm.com/docs/en/watson-orchestrate
- ADK guide: https://developer.watson-orchestrate.ibm.com/

---

## Optional Technologies

### IBM watsonx.ai (Optional)

**What it is**: AI studio for working with foundation models, including IBM Granite models.

**Use cases**:
- Enhance agents with custom AI models
- Use Prompt Lab for experimentation
- Integrate as inference provider for agents
- Access to multiple foundation models

**Key Features**:
- Prompt Lab for model experimentation
- IBM Granite models (recommended)
- Other foundation models (Llama, Mistral, etc.)
- Python/Node.js SDK for programmatic access
- Jupyter Notebooks for development

**Cost Considerations**:
- Foundation model inferencing: 1,000 tokens = 1 RU = $0.0001 USD
- Notebook runtimes: $1.02 USD per CUH
- Use lower runtime environments to conserve credits
- Plan usage carefully with $100 credit limit

**PROHIBITED Models** (Do NOT use):
- ❌ llama-3-405b-instruct
- ❌ mistral-medium-2505
- ❌ mistral-small-3-1-24b-instruct-2503

Using these may negatively impact judging.

**Recommended Models**:
- ✅ ibm/granite-3-8b-instruct
- ✅ ibm/granite-3-2b-instruct
- ✅ meta-llama/llama-3-2-90b-vision-instruct
- ✅ meta-llama/llama-3-1-70b-instruct

**Documentation**:
- Main docs: https://www.ibm.com/docs/en/watsonx-as-a-service
- Prompt Lab: Access via watsonx.ai dashboard
- API reference: Available in documentation

---

## Available IBM Cloud Services

Your hackathon IBM Cloud account includes:

### Code Engine
- Serverless platform for containerized workloads
- Deploy applications and jobs
- Auto-scaling capabilities
- Good for backend services

### Natural Language Understanding
- Text analysis and NLP capabilities
- Entity extraction, sentiment analysis
- Keyword extraction, categorization
- Can enhance agent intelligence

### Speech-to-Text
- Convert audio to text
- Multiple language support
- Real-time and batch processing
- Useful for voice-enabled agents

### Text-to-Speech
- Convert text to natural speech
- Multiple voices and languages
- Useful for agent responses

### Cloudant
- NoSQL database service
- JSON document storage
- Good for agent state/memory
- RESTful API access

**Note**: These services are optional. Use only if they add value to your solution.

---

## Agent Development Approaches

### 1. No-Code Agent Builder (Easiest)

**Best for**: Quick prototyping, simple workflows

**How to use**:
1. Access watsonx Orchestrate web UI
2. Use visual agent builder
3. Configure agents through UI
4. Add tools from catalog
5. Deploy directly

**Pros**:
- Fast to build
- No coding required
- Built-in tools available
- Easy to test

**Cons**:
- Limited customization
- Less control over logic

### 2. Agent Development Kit (ADK) (Recommended)

**Best for**: Custom agents, complex logic, developer control

**What it is**: CLI and framework for building agents with code

**Installation**:
```bash
pip install ibm-watsonx-orchestrate
```

**Key Features**:
- Define agents in YAML/JSON
- Create custom Python tools
- Manage agent lifecycle via CLI
- Local development environment
- Deploy to watsonx Orchestrate SaaS

**Agent Types**:
- **Native agents**: Run on watsonx Orchestrate
- **External agents**: Run on your infrastructure, connected via Agent Connect
- **Collaborator agents**: Agents that work together

**Common Commands**:
```bash
# Environment management
orchestrate env add prod --instance URL --api-key KEY
orchestrate env activate prod
orchestrate auth login

# Agent management
orchestrate agents import -f agent.yaml
orchestrate agents list
orchestrate agents deploy agent-name
orchestrate agents logs agent-name

# Testing
orchestrate chat --agent agent-name
```

**Documentation**: https://developer.watson-orchestrate.ibm.com/getting_started/installing

### 3. External Agent Integration

**Best for**: Existing agents, custom frameworks, advanced use cases

**Supported Frameworks**:
- LangChain / LangGraph
- CrewAI
- LlamaIndex
- BeeAI
- AutoGen
- Custom implementations

**Integration Methods**:
- Agent Connect Framework (chat completions API)
- MCP (Model Context Protocol) servers
- OpenAPI specifications
- Salesforce Agentforce integration
- A2A (Agent-to-Agent) protocol

**How it works**:
1. Build agent with your preferred framework
2. Expose via HTTP endpoint
3. Define external agent in Orchestrate (YAML)
4. Connect via Agent Connect Framework
5. Orchestrate can now call your agent

---

## AI Agent Frameworks & Libraries

### LangChain / LangGraph
- Popular Python framework for LLM applications
- Chain-based and graph-based workflows
- Extensive tool ecosystem
- Good watsonx.ai integration

**Resources**:
- Tutorials in hackathon guide
- watsonx.ai integration examples

### CrewAI
- Multi-agent collaboration framework
- Role-based agent design
- Task delegation patterns
- Memory and context management

**Resources**:
- CrewAI + watsonx examples in guide
- Template apps available

### LlamaIndex
- Data framework for LLM applications
- RAG (Retrieval Augmented Generation)
- Document indexing and querying
- Workflow orchestration

**Resources**:
- LlamaIndex + watsonx tutorials
- Workflow templates

### BeeAI
- IBM's agent framework
- Optimized for Granite models
- Production-ready patterns

**Resources**:
- BeeAI examples in hackathon guide

---

## Development Environment Setup

### Prerequisites

**Required**:
- Python 3.11+ (for ADK and most frameworks)
- pip (Python package manager)
- IBM Cloud account (hackathon provisioned)
- watsonx Orchestrate access

**Optional**:
- Docker (for ADK development server)
- Node.js (if using Node.js SDK)
- Git (for version control)
- Code editor (VS Code, PyCharm, etc.)

### Getting Started

1. **Setup IBM Cloud Account**
   - Accept team invitation email
   - Switch to watsonx account
   - Verify access to services

2. **Access watsonx Orchestrate**
   - Go to IBM Cloud Resource List
   - Find watsonx Orchestrate under AI/Machine Learning
   - Click "Launch watsonx Orchestrate"

3. **Install ADK** (if using)
   ```bash
   pip install ibm-watsonx-orchestrate
   ```

4. **Configure Environment**
   - Get API credentials from Orchestrate settings
   - Set up environment variables
   - Configure ADK environment

5. **Start Building**
   - Create agent definitions
   - Develop custom tools (if needed)
   - Test locally
   - Deploy to Orchestrate

---

## API Access & Credentials

### watsonx Orchestrate API

**Getting Credentials**:
1. Open watsonx Orchestrate
2. Go to Settings → API Details
3. Copy Service Instance URL
4. Generate API Key

**Environment Variables**:
```bash
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here
```

### watsonx.ai API (if using)

**Getting Credentials**:
1. Go to watsonx.ai home page
2. Scroll to "Developer access" section
3. Select your project/space
4. Copy Project ID
5. Create IBM Cloud API key (Manage → Access IAM → API keys)

**Environment Variables**:
```bash
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Important**: Never commit API keys to public repositories!

---

## Best Practices

### Security
- ✅ Use environment variables for credentials
- ✅ Use .env files (never commit)
- ✅ Configure .gitignore properly
- ✅ Rotate keys regularly
- ❌ Never hardcode credentials
- ❌ Never commit .env files

### Performance
- Keep agent responses under 10 seconds
- Use appropriate model sizes (smaller = faster)
- Implement caching where possible
- Optimize prompts to reduce tokens
- Test with realistic data volumes

### Development
- Start simple, iterate
- Test agents individually before orchestration
- Use local development environment
- Version control your agent definitions
- Document your architecture

### Cost Management
- Monitor credit usage (alerts at 25%, 50%, 80%)
- Use smaller models when possible
- Avoid unnecessary API calls
- Test with minimal data first
- Plan usage carefully ($100 limit)

---

## Testing & Debugging

### Local Testing
```bash
# Test agent locally (ADK)
orchestrate chat --agent your-agent

# View agent logs
orchestrate agents logs your-agent --follow

# Check agent status
orchestrate agents get your-agent
```

### Integration Testing
- Test each agent individually
- Test agent collaboration
- Test end-to-end workflows
- Verify error handling
- Check performance

### Debugging Tools
- watsonx Orchestrate logs
- IBM Telemetry (built-in observability)
- Agent execution traces
- API response inspection

---

## Common Technical Patterns

### Multi-Agent Orchestration
```
Orchestrator Agent (Native)
    ↓
Specialist Agents (Native or External)
    ↓
Coordinator/Synthesizer Agent
    ↓
Final Output
```

### External Agent Integration
```
watsonx Orchestrate
    ↓ Agent Connect
Your Backend (FastAPI, Flask, etc.)
    ↓
Your Agent Logic
    ↓ (optional)
watsonx.ai for AI inference
```

### RAG Pattern
```
User Query
    ↓
Agent retrieves relevant documents
    ↓
Agent augments prompt with context
    ↓
LLM generates response
    ↓
Agent returns answer
```

---

## Resources & Documentation

### Official Documentation
- **watsonx Orchestrate**: https://www.ibm.com/docs/en/watson-orchestrate
- **Agent Development Kit**: https://developer.watson-orchestrate.ibm.com/
- **watsonx.ai**: https://www.ibm.com/docs/en/watsonx-as-a-service
- **IBM Granite Models**: https://www.ibm.com/granite

### Tutorials & Examples
- Hackathon guide includes multiple tutorials
- Sample agents and workflows
- Framework integration examples
- Best practices guides

### Community & Support
- IBM Dev Day Slack channels
- BeMyApp platform mentors
- watsonx community forums
- Stack Overflow (tag: ibm-watsonx)

---

## Quick Reference

### Must Use
- ✅ IBM watsonx Orchestrate (REQUIRED)

### Can Use
- ✅ watsonx.ai (optional)
- ✅ IBM Cloud services (optional)
- ✅ Any programming language
- ✅ Any agent framework
- ✅ Any open-source libraries

### Cannot Use
- ❌ Prohibited AI models (listed above)
- ❌ Prohibited data sources
- ❌ Technologies that violate terms of service

### Remember
- $100 credit limit per team
- Account closes February 4, 2026
- Save work regularly
- Test thoroughly before demo
- Demo stability > complexity

---

**Last Updated**: January 30, 2026
**For**: IBM Dev Day AI Demystified Hackathon
