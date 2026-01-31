# Agent Architecture

Complete architecture and design patterns for Lex Conductor agents.

## Overview

Lex Conductor uses a multi-agent architecture where specialized agents collaborate through IBM watsonx Orchestrate to provide comprehensive analysis and decision-making support.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                       │
│                  (watsonx Orchestrate Chat)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Conductor Agent                           │
│                   (Native Orchestrator)                      │
│  - Receives user queries                                     │
│  - Routes to appropriate agents                              │
│  - Manages agent lifecycle                                   │
│  - Synthesizes final response                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Routing    │  │    Memory    │  │    Fusion    │
│    Agent     │  │    Agent     │  │    Agent     │
│  (External)  │  │  (External)  │  │  (External)  │
└──────────────┘  └──────────────┘  └──────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                  ┌──────────────┐
                  │ Traceability │
                  │    Agent     │
                  │  (External)  │
                  └──────────────┘
                           │
                           ▼
                  ┌──────────────┐
                  │  watsonx.ai  │
                  │   (Granite)  │
                  └──────────────┘
```

## Agent Types

### Native Agents

Run directly on watsonx Orchestrate platform.

**Characteristics:**
- Hosted by IBM
- Managed lifecycle
- Built-in observability
- Automatic scaling
- No infrastructure management

**Example:**
- Conductor Agent (Main orchestrator)

### External Agents

Run on custom infrastructure, connected via Agent Connect Framework.

**Characteristics:**
- Custom hosting (FastAPI, Flask, etc.)
- Full control over logic
- Custom dependencies
- Flexible deployment
- Agent Connect integration required

**Examples:**
- Routing Agent
- Memory Agent
- Fusion Agent
- Traceability Agent

## Design Principles

### 1. Stateless Design

All agents are stateless - they don't maintain session state internally.

**Benefits:**
- Easy to scale horizontally
- No state synchronization issues
- Simple error recovery
- Independent agent restarts

**Implementation:**
- State managed by Memory Agent
- Each request is self-contained
- Context passed explicitly
- No shared memory between requests

### 2. Single Responsibility

Each agent has one clear purpose.

**Routing Agent:**
- Classifies query intent
- Determines required agents
- Routes to appropriate handlers

**Memory Agent:**
- Stores conversation history
- Retrieves relevant context
- Manages session state

**Fusion Agent:**
- Aggregates responses
- Resolves conflicts
- Synthesizes final output

**Traceability Agent:**
- Logs all interactions
- Tracks decision provenance
- Provides audit trail

### 3. Loose Coupling

Agents communicate through standardized interfaces.

**Benefits:**
- Easy to replace agents
- Independent development
- Parallel execution
- Flexible composition

**Implementation:**
- Standard request/response format
- Agent Connect Framework
- JSON-based communication
- No direct agent-to-agent calls

### 4. Fail-Safe Design

Graceful degradation when agents fail.

**Strategies:**
- Timeout handling
- Fallback responses
- Error propagation
- Partial results

**Example:**
```python
try:
    response = await routing_agent.classify(query)
except TimeoutError:
    # Fallback to default routing
    response = default_route(query)
except AgentError as e:
    # Log error and continue with degraded service
    logger.error(f"Routing agent failed: {e}")
    response = fallback_response()
```

## Communication Patterns

### Request-Response

Standard synchronous communication.

```
Conductor → Request → Agent
Agent → Response → Conductor
```

**Use Cases:**
- Query classification
- Context retrieval
- Response synthesis

### Parallel Execution

Multiple agents execute simultaneously.

```
Conductor → Request → [Agent1, Agent2, Agent3]
[Agent1, Agent2, Agent3] → Responses → Conductor
```

**Use Cases:**
- Independent analyses
- Multi-perspective evaluation
- Performance optimization

### Sequential Pipeline

Agents execute in sequence, passing results forward.

```
Conductor → Agent1 → Agent2 → Agent3 → Conductor
```

**Use Cases:**
- Context enrichment
- Progressive refinement
- Dependent operations

## Data Flow

### 1. Query Reception

```
User → watsonx Orchestrate Chat → Conductor Agent
```

### 2. Query Classification

```
Conductor → Routing Agent
Routing Agent → Classification Result
```

### 3. Context Retrieval

```
Conductor → Memory Agent
Memory Agent → Relevant Context
```

### 4. Parallel Analysis

```
Conductor → [Routing, Memory, Fusion] (parallel)
[Routing, Memory, Fusion] → Individual Results
```

### 5. Response Synthesis

```
Conductor → Fusion Agent (with all results)
Fusion Agent → Synthesized Response
```

### 6. Traceability Logging

```
Conductor → Traceability Agent (async)
Traceability Agent → Audit Log
```

### 7. Final Response

```
Conductor → watsonx Orchestrate Chat → User
```

## Agent Interface

### Standard Request Format

```json
{
  "query": "User's question or command",
  "context": {
    "session_id": "unique-session-id",
    "user_id": "user-identifier",
    "timestamp": "2026-01-30T10:00:00Z"
  },
  "metadata": {
    "source": "chat",
    "priority": "normal"
  }
}
```

### Standard Response Format

```json
{
  "status": "success",
  "result": {
    "answer": "Agent's response",
    "confidence": 0.95,
    "reasoning": "Explanation of decision"
  },
  "metadata": {
    "agent": "routing-agent",
    "execution_time_ms": 150,
    "model_used": "granite-3-8b-instruct"
  }
}
```

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "AGENT_TIMEOUT",
    "message": "Agent did not respond within timeout",
    "details": "Connection timeout after 10 seconds"
  },
  "metadata": {
    "agent": "memory-agent",
    "timestamp": "2026-01-30T10:00:10Z"
  }
}
```

## Scalability Patterns

### Horizontal Scaling

Add more agent instances as load increases.

```
Load Balancer
    ├── Agent Instance 1
    ├── Agent Instance 2
    └── Agent Instance 3
```

### Caching

Cache frequent queries and responses.

```python
@cache(ttl=300)  # 5 minutes
async def classify_query(query: str):
    return await routing_agent.classify(query)
```

### Async Processing

Non-blocking agent calls.

```python
# Parallel execution
results = await asyncio.gather(
    routing_agent.classify(query),
    memory_agent.retrieve_context(session_id),
    fusion_agent.prepare()
)
```

## Security Considerations

### Authentication

- API key validation
- JWT tokens
- OAuth 2.0 integration

### Authorization

- Role-based access control
- Agent-level permissions
- Resource restrictions

### Data Protection

- Encryption in transit (TLS)
- Encryption at rest
- PII handling
- Data retention policies

## Performance Optimization

### Response Time Targets

- Routing Agent: < 500ms
- Memory Agent: < 1s
- Fusion Agent: < 2s
- Total end-to-end: < 10s

### Optimization Strategies

1. **Parallel Execution**: Run independent agents simultaneously
2. **Caching**: Cache frequent queries and context
3. **Connection Pooling**: Reuse HTTP connections
4. **Prompt Optimization**: Reduce token usage
5. **Model Selection**: Use appropriate model sizes

## Monitoring & Observability

### Metrics to Track

- Request latency per agent
- Success/failure rates
- Token usage
- Error rates
- Agent availability

### Logging

```python
logger.info("Agent request", extra={
    "agent": "routing-agent",
    "query_id": query_id,
    "execution_time_ms": 150
})
```

### Tracing

- Request ID propagation
- Distributed tracing
- Agent execution timeline
- Decision provenance

## Related Documentation

- [Conductor Agent](./conductor-agent.md)
- [Routing Agent](./routing-agent.md)
- [Memory Agent](./memory-agent.md)
- [Fusion Agent](./fusion-agent.md)
- [Traceability Agent](./traceability-agent.md)

---

**Architecture Pattern**: Multi-Agent Orchestration  
**Communication**: Agent Connect Framework  
**Hosting**: Hybrid (Native + External)
