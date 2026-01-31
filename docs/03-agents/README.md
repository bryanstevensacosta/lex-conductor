# Lex Conductor - Agent Documentation

Complete documentation for all agents in the Lex Conductor system.

## 📋 Contents

- **[Agent Architecture](./agent-architecture.md)** - Overall agent design and patterns
- **[Conductor Agent](./conductor-agent.md)** - Main orchestrator agent
- **[Routing Agent](./routing-agent.md)** - Query routing and classification
- **[Memory Agent](./memory-agent.md)** - Context and history management
- **[Fusion Agent](./fusion-agent.md)** - Response synthesis and aggregation
- **[Traceability Agent](./traceability-agent.md)** - Decision provenance tracking
- **[Agent Definitions](./agent-definitions/)** - YAML files for watsonx Orchestrate

## 🤖 Agent Overview

Lex Conductor uses a multi-agent architecture where specialized agents collaborate to provide comprehensive analysis and decision-making support.

### Agent Hierarchy

```
Conductor Agent (Orchestrator)
    ├── Routing Agent
    ├── Memory Agent
    ├── Fusion Agent
    └── Traceability Agent
```

## 📊 Agent Inventory

| Agent | Type | Purpose | Status |
|-------|------|---------|--------|
| **Conductor** | Native | Orchestrates all agents | ✅ Defined |
| **Routing** | External | Routes queries | ✅ Defined |
| **Memory** | External | Manages context | ✅ Defined |
| **Fusion** | External | Synthesizes responses | ✅ Defined |
| **Traceability** | External | Tracks decisions | ✅ Defined |

## 🎯 Agent Types

### Native Agents
Run directly on watsonx Orchestrate platform.
- **Conductor Agent** - Main orchestrator

### External Agents
Run on custom infrastructure, connected via Agent Connect Framework.
- **Routing Agent**
- **Memory Agent**
- **Fusion Agent**
- **Traceability Agent**

## 🔄 Agent Collaboration Flow

```
1. User submits query
   ↓
2. Conductor Agent receives query
   ↓
3. Routing Agent classifies query type
   ↓
4. Memory Agent retrieves relevant context
   ↓
5. Specialized agents process in parallel
   ↓
6. Fusion Agent synthesizes responses
   ↓
7. Traceability Agent logs decision trail
   ↓
8. Conductor returns final response
```

## 📝 Agent Responsibilities

### Conductor Agent (Orchestrator)
- Receives user queries
- Delegates to appropriate agents
- Manages agent lifecycle
- Returns synthesized responses
- Handles errors and fallbacks

### Routing Agent
- Classifies query intent
- Determines required agents
- Routes to appropriate handlers
- Manages query prioritization

### Memory Agent
- Maintains conversation context
- Stores decision history
- Retrieves relevant past decisions
- Manages session state

### Fusion Agent
- Aggregates agent responses
- Resolves conflicts
- Synthesizes final decision
- Formats output

### Traceability Agent
- Logs all agent interactions
- Tracks decision provenance
- Provides audit trail
- Enables explainability

## 🛠️ Working with Agents

### Deploying Agents

```bash
# Navigate to agent definitions
cd docs/03-agents/agent-definitions/

# Deploy to watsonx Orchestrate
orchestrate agents import -f conductor_agent.yaml
orchestrate agents import -f routing_agent.yaml
orchestrate agents import -f memory_agent.yaml
orchestrate agents import -f fusion_agent.yaml
orchestrate agents import -f traceability_agent.yaml

# Verify deployment
orchestrate agents list
```

### Testing Agents

```bash
# Test individual agent
orchestrate chat --agent conductor-agent

# View agent logs
orchestrate agents logs conductor-agent --follow
```

### Modifying Agents

1. Edit the YAML definition in `agent-definitions/`
2. Update the agent documentation
3. Redeploy to watsonx Orchestrate
4. Test the changes

## 📚 Agent Design Patterns

### Stateless Design
All agents are stateless - state is managed by Memory Agent.

### Error Handling
Each agent implements graceful degradation and fallback strategies.

### Parallel Execution
Agents can execute in parallel when dependencies allow.

### Standardized Interface
All agents follow the same request/response pattern.

## 🔧 Agent Configuration

Agent configurations are stored in YAML files:
- `conductor_agent.yaml` - Orchestrator configuration
- `routing_agent.yaml` - Routing logic
- `memory_agent.yaml` - Memory management
- `fusion_agent.yaml` - Synthesis rules
- `traceability_agent.yaml` - Logging configuration

## 📖 Related Documentation

- [Architecture](../02-project/architecture.md) - System architecture
- [Integration Guide](../05-integration/watsonx-orchestrate.md) - watsonx setup
- [Development](../04-development/) - Development guidelines

## 🆘 Troubleshooting

**Agent not responding:**
- Check agent deployment status
- Review agent logs
- Verify Agent Connect configuration

**Slow responses:**
- Check parallel execution
- Review agent dependencies
- Optimize agent prompts

**Errors in synthesis:**
- Check Fusion Agent configuration
- Review agent response formats
- Verify data validation

---

**Total Agents**: 5  
**Native Agents**: 1 (Conductor)  
**External Agents**: 4 (Routing, Memory, Fusion, Traceability)
