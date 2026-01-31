"""
Agent Connect Framework endpoints for watsonx Orchestrate integration.

This module implements the /v1/chat/completions endpoint following the
Agent Connect protocol for external agent communication.
"""

import logging
import time
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.routers import fusion, routing, memory, traceability

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message in Agent Connect format."""

    role: str
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    """Chat completion request following Agent Connect protocol."""

    messages: List[ChatMessage]
    stream: bool = False


class ChatCompletionResponse(BaseModel):
    """Chat completion response."""

    role: str = "assistant"
    content: str


def extract_contract_info(messages: List[ChatMessage]) -> Dict[str, str]:
    """
    Extract contract information from chat messages.

    Looks for contract text, type, and jurisdiction in the user messages.
    """
    # Get the last user message
    user_messages = [msg for msg in messages if msg.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user message found")

    last_message = user_messages[-1].content

    # Simple extraction logic
    contract_text = last_message
    contract_type = "NDA"  # Default
    jurisdiction = "US"  # Default

    # Try to extract type
    if "NDA" in last_message.upper() or "CONFIDENTIALITY" in last_message.upper():
        contract_type = "NDA"
    elif "MSA" in last_message.upper() or "SERVICE AGREEMENT" in last_message.upper():
        contract_type = "MSA"
    elif "SLA" in last_message.upper():
        contract_type = "SLA"

    # Try to extract jurisdiction
    if "US" in last_message or "United States" in last_message:
        jurisdiction = "US"
    elif "EU" in last_message or "European" in last_message:
        jurisdiction = "EU"
    elif "UK" in last_message or "United Kingdom" in last_message:
        jurisdiction = "UK"

    return {
        "contract_text": contract_text,
        "contract_type": contract_type,
        "jurisdiction": jurisdiction,
    }


@router.post("/fusion/v1/chat/completions")
async def fusion_chat_completions(request: ChatCompletionRequest):
    """
    Fusion Agent chat completions endpoint for Agent Connect.

    Converts chat format to Fusion Agent's expected format.
    """
    try:
        # Extract contract info from messages
        contract_info = extract_contract_info(request.messages)

        # Create Fusion Agent request
        fusion_request = fusion.FusionAnalysisRequest(
            contract_text=contract_info["contract_text"],
            contract_type=contract_info["contract_type"],
            jurisdiction=contract_info["jurisdiction"],
        )

        # Call Fusion Agent
        result = await fusion.analyze_contract(fusion_request)

        # Format response as chat completion
        response_text = f"""**SIGNAL ANALYSIS (Fusion Agent)**

**Compliance Gaps Detected:** {len(result.compliance_gaps)}

**Gap Details:**
"""
        for gap in result.compliance_gaps:
            response_text += f"\n- **{gap.gap_type}** (Severity: {gap.severity})\n"
            response_text += f"  {gap.description}\n"
            response_text += f"  Recommendation: {gap.recommendation}\n"

        response_text += f"\n**Confidence Score:** {result.confidence_score:.2f}"

        return ChatCompletionResponse(role="assistant", content=response_text)

    except Exception as e:
        logger.error(f"Fusion chat completions error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/routing/v1/chat/completions")
async def routing_chat_completions(request: ChatCompletionRequest):
    """
    Routing Agent chat completions endpoint for Agent Connect.
    """
    try:
        contract_info = extract_contract_info(request.messages)

        routing_request = routing.RoutingRequest(
            contract_text=contract_info["contract_text"],
            contract_type=contract_info["contract_type"],
            jurisdiction=contract_info["jurisdiction"],
        )

        result = await routing.classify_contract(routing_request)

        response_text = f"""**RISK ASSESSMENT (Routing Agent)**

**Complexity Level:** {result.complexity_level}
**Risk Score:** {result.risk_score:.2f}
**Routing Decision:** {result.routing_decision}

**Human-in-Loop Required:** {"Yes" if result.human_in_loop.required else "No"}
"""
        if result.human_in_loop.required:
            response_text += f"**Reason:** {result.human_in_loop.reason}\n"
            response_text += f"**Reviewer Type:** {result.human_in_loop.reviewer_type}\n"

        response_text += f"\n**Justification:** {result.justification}"
        response_text += f"\n**Confidence Score:** {result.confidence_score:.2f}"

        return ChatCompletionResponse(role="assistant", content=response_text)

    except Exception as e:
        logger.error(f"Routing chat completions error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/memory/v1/chat/completions")
async def memory_chat_completions(request: ChatCompletionRequest):
    """
    Memory Agent chat completions endpoint for Agent Connect.
    """
    try:
        contract_info = extract_contract_info(request.messages)

        memory_request = memory.MemoryQueryRequest(
            contract_type=contract_info["contract_type"], jurisdiction=contract_info["jurisdiction"]
        )

        result = await memory.query_memory(memory_request)

        response_text = f"""**HISTORICAL PRECEDENTS (Memory Agent)**

**Golden Clauses Found:** {len(result.golden_clauses)}
**Historical Precedents:** {len(result.historical_precedents)}

**Key Golden Clauses:**
"""
        for clause in result.golden_clauses[:3]:  # Top 3
            response_text += f"\n- **{clause.type}** (Risk: {clause.risk_level})\n"
            response_text += f"  {clause.text[:100]}...\n"

        response_text += "\n**Modification Patterns:**\n"
        for pattern in result.modification_patterns[:3]:  # Top 3
            response_text += f"- {pattern.pattern} (Frequency: {pattern.frequency})\n"

        response_text += f"\n**Average Confidence:** {result.summary.average_confidence:.2f}"

        return ChatCompletionResponse(role="assistant", content=response_text)

    except Exception as e:
        logger.error(f"Memory chat completions error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/traceability/v1/chat/completions")
async def traceability_chat_completions(request: ChatCompletionRequest):
    """
    Traceability Agent chat completions endpoint for Agent Connect.
    """
    try:
        # For traceability, we need outputs from other agents
        # Extract from tool_calls in messages if available
        contract_info = extract_contract_info(request.messages)

        # Create minimal traceability request
        trace_request = traceability.TraceabilityRequest(
            contract_id=f"contract_{int(time.time())}",
            contract_type=contract_info["contract_type"],
            fusion_output={},  # Would be populated from previous tool calls
            routing_output={},
        )

        result = await traceability.generate_trace(trace_request)

        response_text = f"""**LEGAL LOGIC TRACE (Traceability Agent)**

**Contract Classification:**
- Type: {result.legal_logic_trace.contract_classification.type}
- Jurisdiction: {result.legal_logic_trace.contract_classification.jurisdiction}
- Complexity: {result.legal_logic_trace.contract_classification.complexity}

**Overall Confidence:** {result.legal_logic_trace.confidence_scores.overall:.2f}

**Summary:**
{result.summary.decision}

**Next Steps:** {result.summary.next_steps}
"""

        return ChatCompletionResponse(role="assistant", content=response_text)

    except Exception as e:
        logger.error(f"Traceability chat completions error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
