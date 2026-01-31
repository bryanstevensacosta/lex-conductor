"""
Traceability Agent router for Legal Logic Trace generation.

This module provides the endpoint for generating structured Legal Logic Trace
reports that document the reasoning, confidence scores, and recommendations
for contract analysis.
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.models import (
    ContractType,
    Jurisdiction,
    FusionAnalysis,
    RoutingDecision,
    HistoricalSignal,
    RecommendedAction,
)

router = APIRouter()


class TraceRequest(BaseModel):
    """Request model for trace generation."""

    contract_id: str = Field(..., description="Unique contract identifier")
    contract_type: ContractType = Field(..., description="Type of contract")
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.US, description="Legal jurisdiction")
    fusion_analysis: FusionAnalysis = Field(..., description="Fusion analysis results")
    routing_decision: RoutingDecision = Field(..., description="Routing decision")
    precedents: List[HistoricalSignal] = Field(
        default_factory=list, description="Historical precedents"
    )


class TraceResponse(BaseModel):
    """Response model for trace generation."""

    trace: str = Field(..., description="Formatted Legal Logic Trace in markdown")
    contract_id: str = Field(..., description="Contract identifier")
    timestamp: str = Field(..., description="Generation timestamp")


@router.post("/generate", response_model=TraceResponse)
async def generate_trace(request: TraceRequest):
    """
    Generate Legal Logic Trace report.

    This endpoint:
    1. Generates structured Legal Logic Trace in markdown format
    2. Includes all required sections: metadata, signal analysis, risk assessment, recommendations
    3. Assigns confidence scores to each recommendation
    4. Flags low-confidence recommendations (<0.5) for human review
    5. Returns formatted Legal Logic Trace string

    Args:
        request: TraceRequest with all analysis data

    Returns:
        TraceResponse: Formatted trace with metadata

    Raises:
        HTTPException: If trace generation fails
    """
    try:
        # Generate timestamp
        timestamp = datetime.utcnow().isoformat()

        # Build trace sections
        trace_parts = []

        # Header
        trace_parts.append(_generate_header(request, timestamp))

        # Signal Analysis
        trace_parts.append(_generate_signal_analysis(request.fusion_analysis, request.precedents))

        # Risk Assessment
        trace_parts.append(_generate_risk_assessment(request.routing_decision))

        # Recommendations
        recommendations = _generate_recommendations(request.fusion_analysis)
        trace_parts.append(_format_recommendations(recommendations))

        # Summary
        trace_parts.append(
            _generate_summary(request.fusion_analysis, request.routing_decision, recommendations)
        )

        # Combine all parts
        trace = "\n\n".join(trace_parts)

        return TraceResponse(trace=trace, contract_id=request.contract_id, timestamp=timestamp)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "TRACE_GENERATION_FAILED",
                "message": f"Failed to generate trace: {str(e)}",
            },
        )


def _generate_header(request: TraceRequest, timestamp: str) -> str:
    """Generate trace header with metadata."""
    return f"""═══════════════════════════════════════════════════
LEGAL LOGIC TRACE
═══════════════════════════════════════════════════

Contract ID: {request.contract_id}
Contract Type: {request.contract_type.value}
Jurisdiction: {request.jurisdiction.value}
Timestamp: {timestamp}
Processing Time: N/A"""


def _generate_signal_analysis(
    fusion_analysis: FusionAnalysis, precedents: List[HistoricalSignal]
) -> str:
    """Generate signal analysis section."""
    lines = [
        "───────────────────────────────────────────────────",
        "SIGNAL ANALYSIS",
        "───────────────────────────────────────────────────",
    ]

    # Internal Signals
    if fusion_analysis.internal_signals:
        lines.append("\n**Internal Signals (Golden Clauses)**:")
        for signal in fusion_analysis.internal_signals[:5]:  # Limit to 5
            icon = "✓" if signal.alignment.value == "MATCH" else "⚠"
            lines.append(f"\n{icon} {signal.source} (Confidence: {signal.confidence:.2f})")
            lines.append(f"  Type: {signal.type}")
            lines.append(f"  Status: {signal.alignment.value}")

    # External Signals
    if fusion_analysis.external_signals:
        lines.append("\n**External Signals (Regulations)**:")
        for signal in fusion_analysis.external_signals[:5]:  # Limit to 5
            icon = "✓" if signal.alignment.value == "MATCH" else "⚠"
            lines.append(f"\n{icon} {signal.source} (Confidence: {signal.confidence:.2f})")
            lines.append(f"  Regulation: {signal.regulation}")
            lines.append(f"  Status: {signal.alignment.value}")

    # Historical Signals
    if precedents:
        lines.append("\n**Historical Signals (Precedents)**:")
        lines.append(f"\n✓ Precedents Found: {len(precedents)} similar cases")
        avg_confidence = (
            sum(p.confidence for p in precedents) / len(precedents) if precedents else 0
        )
        lines.append(f"  Average Confidence: {avg_confidence:.2f}")
        lines.append("  Status: SUPPORTS ANALYSIS")

    return "\n".join(lines)


def _generate_risk_assessment(routing_decision: RoutingDecision) -> str:
    """Generate risk assessment section."""
    lines = [
        "───────────────────────────────────────────────────",
        "RISK ASSESSMENT",
        "───────────────────────────────────────────────────",
    ]

    lines.append(
        f"\nOverall Risk Score: {routing_decision.risk_score:.2f} ({routing_decision.risk_level.value})"
    )
    lines.append(f"Complexity Classification: {routing_decision.complexity.value}")
    lines.append(f"Routing Decision: {routing_decision.workflow_path.value}")
    lines.append(
        f"Human Review Required: {'YES' if routing_decision.human_review_required else 'NO'}"
    )

    lines.append("\n**Justification:**")
    lines.append(routing_decision.justification)

    return "\n".join(lines)


def _generate_recommendations(
    fusion_analysis: FusionAnalysis,
) -> List[RecommendedAction]:
    """Generate recommended actions from fusion analysis."""
    recommendations = []

    # Generate recommendations from compliance gaps
    for gap in fusion_analysis.gaps:
        # Determine action based on severity
        if gap.severity == "HIGH":
            action = "MODIFY"
            priority = "HIGH"
        elif gap.severity == "MEDIUM":
            action = "MODIFY"
            priority = "MEDIUM"
        else:
            action = "REVIEW"
            priority = "LOW"

        # Flag low confidence recommendations
        needs_review = gap.confidence < 0.5
        if needs_review:
            action = "ESCALATE"
            priority = "HIGH"

        recommendation = RecommendedAction(
            clause=gap.clause,
            action=action,
            rationale=gap.recommendation,
            confidence=gap.confidence,
            priority=priority,
            current_text=None,
            recommended_text=gap.recommendation if action == "MODIFY" else None,
        )
        recommendations.append(recommendation)

    # If no gaps, recommend approval (but check confidence)
    if not recommendations:
        # If overall confidence is low, escalate instead of approve
        if fusion_analysis.overall_confidence < 0.5:
            recommendations.append(
                RecommendedAction(
                    clause="Overall Contract",
                    action="ESCALATE",
                    rationale="Low confidence in analysis. Human review required despite no detected gaps.",
                    confidence=fusion_analysis.overall_confidence,
                    priority="HIGH",
                )
            )
        else:
            recommendations.append(
                RecommendedAction(
                    clause="Overall Contract",
                    action="APPROVE",
                    rationale="No compliance gaps detected. Contract aligns with all analyzed sources.",
                    confidence=fusion_analysis.overall_confidence,
                    priority="LOW",
                )
            )

    return recommendations


def _format_recommendations(recommendations: List[RecommendedAction]) -> str:
    """Format recommendations section."""
    lines = [
        "───────────────────────────────────────────────────",
        "RECOMMENDED ACTIONS",
        "───────────────────────────────────────────────────",
    ]

    for i, rec in enumerate(recommendations, 1):
        lines.append(f"\n**Action {i}: {rec.action} {rec.clause}**")
        lines.append(f"Confidence: {rec.confidence:.2f}")
        lines.append(f"Priority: {rec.priority}")

        # Flag low confidence
        if rec.confidence < 0.5:
            lines.append("⚠️  **LOW CONFIDENCE - HUMAN REVIEW REQUIRED**")

        lines.append("\n**Rationale:**")
        lines.append(rec.rationale)

        if rec.recommended_text:
            lines.append("\n**Recommended Text:**")
            lines.append(
                rec.recommended_text[:200] + "..."
                if len(rec.recommended_text) > 200
                else rec.recommended_text
            )

    return "\n".join(lines)


def _generate_summary(
    fusion_analysis: FusionAnalysis,
    routing_decision: RoutingDecision,
    recommendations: List[RecommendedAction],
) -> str:
    """Generate summary section."""
    lines = [
        "───────────────────────────────────────────────────",
        "DECISION SUMMARY",
        "───────────────────────────────────────────────────",
    ]

    # Determine overall decision
    has_high_priority = any(r.priority == "HIGH" for r in recommendations)
    has_low_confidence = any(r.confidence < 0.5 for r in recommendations)

    if has_low_confidence:
        decision = "⚠️  REQUIRES EXPERT REVIEW"
    elif has_high_priority:
        decision = "⚠️  APPROVED WITH MODIFICATIONS"
    elif routing_decision.workflow_path.value == "AUTO_APPROVE":
        decision = "✓ APPROVED"
    else:
        decision = "⚠️  REQUIRES REVIEW"

    lines.append(f"\n{decision}")
    lines.append(f"Overall Confidence: {fusion_analysis.overall_confidence:.2f}")

    lines.append("\n**Next Steps:**")
    if routing_decision.workflow_path.value == "AUTO_APPROVE":
        lines.append("1. Contract ready for signature")
        lines.append("2. No additional legal review required")
    elif routing_decision.workflow_path.value == "PARALEGAL_REVIEW":
        lines.append("1. Route to paralegal for review")
        lines.append("2. Apply recommended modifications")
        lines.append("3. Verify compliance with flagged issues")
    else:
        lines.append("1. Escalate to General Counsel")
        lines.append("2. Comprehensive legal review required")
        lines.append("3. Address all high-priority recommendations")

    lines.append("\n═══════════════════════════════════════════════════")

    return "\n".join(lines)
