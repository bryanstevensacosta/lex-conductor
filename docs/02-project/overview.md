---
inclusion: always
---

# Product Overview

Boardroom AI is a multi-agent decision orchestration system that simulates a boardroom of AI experts collaborating on complex business decisions.

## Core Concept

The system receives a business question through IBM watsonx Orchestrate and coordinates specialized agents (Strategy, Finance, Risk, Operations) that analyze from domain perspectives, debate trade-offs, and synthesize reasoning through a Coordinator agent to produce an explainable final decision.

## Key Characteristics

- **Multi-agent orchestration** using IBM watsonx Orchestrate (REQUIRED for hackathon)
- **Hybrid architecture** combining Orchestrate native agents with external FastAPI agents
- **AI intelligence** powered by IBM watsonx.ai Granite foundation models
- **Explainable AI reasoning** with transparent decision trails
- **Demo-ready** hackathon prototype (not production-grade)
- **Enterprise integration** via Agent Connect Framework

## Architecture Highlights

- **watsonx Orchestrate**: Primary orchestration platform managing agent collaboration
- **External Agents**: Custom Python agents with domain expertise
- **watsonx.ai Integration**: Granite models provide reasoning for each agent
- **Standardized Communication**: Chat completions API for agent-to-agent communication

## Success Criteria

- Agents produce coherent, structured reasoning
- Final decisions are explainable and actionable
- System runs reliably during live demos
- **watsonx Orchestrate integration is clearly demonstrated** (CRITICAL)
- Multi-agent collaboration is visible and transparent
- Granite model usage is evident in agent responses
