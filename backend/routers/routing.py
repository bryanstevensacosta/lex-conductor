"""
Routing Agent router for contract complexity classification.

This module provides the endpoint for classifying contract complexity and
determining the appropriate workflow path based on risk assessment.
"""

import os
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.models import (
    FusionAnalysis,
    RoutingDecision,
    ComplexityLevel,
    RiskLevel,
    WorkflowPath,
)
from backend.watsonx_client import WatsonxClient

router = APIRouter()

# Client instance (initialized lazily)
_watsonx_client = None


def get_watsonx_client() -> WatsonxClient:
    """Get or create Watsonx client instance."""
    global _watsonx_client
    if _watsonx_client is None:
        _watsonx_client = WatsonxClient(
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
        )
    return _watsonx_client


class ContractMetadata(BaseModel):
    """Metadata about the contract."""

    type: str = Field(..., description="Contract type")
    value: Optional[float] = Field(None, description="Contract value in USD")
    jurisdiction: str = Field(..., description="Legal jurisdiction")


class RoutingRequest(BaseModel):
    """Request model for routing classification."""

    fusion_analysis: FusionAnalysis = Field(..., description="Fusion analysis results")
    contract_metadata: ContractMetadata = Field(..., description="Contract metadata")


@router.post("/classify", response_model=RoutingDecision)
async def classify_contract(request: RoutingRequest):
    """
    Classify contract complexity and determine routing path.

    This endpoint:
    1. Calculates risk score from fusion analysis (gap count, severity, confidence)
    2. Classifies complexity level (ROUTINE <0.3, STANDARD <0.7, COMPLEX >=0.7)
    3. Determines workflow path (AUTO_APPROVE, PARALEGAL_REVIEW, GC_ESCALATION)
    4. Generates justification using watsonx.ai
    5. Returns RoutingDecision with risk assessment

    Args:
        request: RoutingRequest with fusion analysis and contract metadata

    Returns:
        RoutingDecision: Classification with risk assessment and justification

    Raises:
        HTTPException: If classification fails
    """
    try:
        # Step 1: Calculate risk score
        risk_score = _calculate_risk_score(request.fusion_analysis)

        # Step 2: Classify complexity level
        complexity = _classify_complexity(risk_score)

        # Step 3: Determine risk level
        risk_level = _determine_risk_level(risk_score)

        # Step 4: Determine workflow path
        workflow_path = _determine_workflow_path(complexity, risk_score)

        # Step 5: Determine if human review is required
        human_review_required = workflow_path != WorkflowPath.AUTO_APPROVE

        # Step 6: Generate justification using watsonx.ai
        justification = await _generate_justification(
            request.fusion_analysis,
            request.contract_metadata,
            complexity,
            risk_score,
            workflow_path,
        )

        # Step 7: Determine escalation level
        escalation_level = _determine_escalation_level(workflow_path)

        return RoutingDecision(
            complexity=complexity,
            risk_level=risk_level,
            risk_score=risk_score,
            workflow_path=workflow_path,
            human_review_required=human_review_required,
            justification=justification,
            escalation_level=escalation_level,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ROUTING_CLASSIFICATION_FAILED",
                "message": f"Failed to classify contract: {str(e)}",
            },
        )


def _calculate_risk_score(fusion_analysis: FusionAnalysis) -> float:
    """
    Calculate risk score from fusion analysis.

    Risk score is calculated based on:
    - Number of compliance gaps
    - Severity of gaps (HIGH=0.7, MEDIUM=0.3, LOW=0.1)
    - Overall confidence (lower confidence = higher risk)

    Args:
        fusion_analysis: Fusion analysis results

    Returns:
        Risk score from 0.0 (low risk) to 1.0 (high risk)
    """
    # Severity weights
    severity_weights = {"LOW": 0.1, "MEDIUM": 0.3, "HIGH": 0.7}

    # Calculate gap risk
    gap_count = len(fusion_analysis.gaps)
    if gap_count == 0:
        gap_risk = 0.0
    else:
        # Sum weighted severities
        total_severity = sum(
            severity_weights.get(gap.severity, 0.3) for gap in fusion_analysis.gaps
        )
        # Normalize by number of gaps (average severity)
        gap_risk = min(1.0, total_severity / max(1, gap_count) * gap_count * 0.2)

    # Calculate confidence risk (inverse of confidence)
    confidence_risk = 1.0 - fusion_analysis.overall_confidence

    # Combine risks (60% gap risk, 40% confidence risk)
    risk_score = (gap_risk * 0.6) + (confidence_risk * 0.4)

    # Ensure risk score is in valid range
    return max(0.0, min(1.0, risk_score))


def _classify_complexity(risk_score: float) -> ComplexityLevel:
    """
    Classify complexity level based on risk score.

    Classification thresholds:
    - ROUTINE: risk_score < 0.3
    - STANDARD: 0.3 <= risk_score < 0.7
    - COMPLEX: risk_score >= 0.7

    Args:
        risk_score: Calculated risk score

    Returns:
        ComplexityLevel classification
    """
    if risk_score < 0.3:
        return ComplexityLevel.ROUTINE
    elif risk_score < 0.7:
        return ComplexityLevel.STANDARD
    else:
        return ComplexityLevel.COMPLEX


def _determine_risk_level(risk_score: float) -> RiskLevel:
    """
    Determine risk level based on risk score.

    Risk level thresholds:
    - LOW: risk_score < 0.3
    - MEDIUM: 0.3 <= risk_score < 0.7
    - HIGH: risk_score >= 0.7

    Args:
        risk_score: Calculated risk score

    Returns:
        RiskLevel classification
    """
    if risk_score < 0.3:
        return RiskLevel.LOW
    elif risk_score < 0.7:
        return RiskLevel.MEDIUM
    else:
        return RiskLevel.HIGH


def _determine_workflow_path(complexity: ComplexityLevel, risk_score: float) -> WorkflowPath:
    """
    Determine workflow path based on complexity and risk score.

    Workflow paths:
    - AUTO_APPROVE: ROUTINE complexity and risk_score < 0.2
    - PARALEGAL_REVIEW: STANDARD complexity or 0.2 <= risk_score < 0.7
    - GC_ESCALATION: COMPLEX complexity or risk_score >= 0.7

    Args:
        complexity: Complexity level
        risk_score: Calculated risk score

    Returns:
        WorkflowPath determination
    """
    if complexity == ComplexityLevel.COMPLEX or risk_score >= 0.7:
        return WorkflowPath.GC_ESCALATION
    elif complexity == ComplexityLevel.STANDARD or risk_score >= 0.2:
        return WorkflowPath.PARALEGAL_REVIEW
    else:
        return WorkflowPath.AUTO_APPROVE


async def _generate_justification(
    fusion_analysis: FusionAnalysis,
    contract_metadata: ContractMetadata,
    complexity: ComplexityLevel,
    risk_score: float,
    workflow_path: WorkflowPath,
) -> str:
    """
    Generate justification for routing decision using watsonx.ai.

    Args:
        fusion_analysis: Fusion analysis results
        contract_metadata: Contract metadata
        complexity: Classified complexity level
        risk_score: Calculated risk score
        workflow_path: Determined workflow path

    Returns:
        Justification text
    """
    try:
        watsonx_client = get_watsonx_client()

        # Prepare analysis summary
        gap_count = len(fusion_analysis.gaps)
        confidence = fusion_analysis.overall_confidence

        # Create prompt for justification
        prompt = f"""Generate a concise justification for this contract routing decision.

Contract Type: {contract_metadata.type}
Jurisdiction: {contract_metadata.jurisdiction}
Compliance Gaps: {gap_count}
Overall Confidence: {confidence:.2f}
Risk Score: {risk_score:.2f}
Complexity: {complexity.value}
Workflow Path: {workflow_path.value}

Provide a 2-3 sentence justification explaining:
1. Why this complexity level was assigned
2. Key risk factors
3. Why this workflow path is appropriate

Keep response professional and concise."""

        justification = watsonx_client.generate(prompt=prompt, max_tokens=150, temperature=0.1)

        return justification.strip()

    except Exception as e:
        # Fallback to template-based justification
        print(f"Warning: Failed to generate AI justification: {e}")
        return _generate_template_justification(
            gap_count, confidence, risk_score, complexity, workflow_path
        )


def _generate_template_justification(
    gap_count: int,
    confidence: float,
    risk_score: float,
    complexity: ComplexityLevel,
    workflow_path: WorkflowPath,
) -> str:
    """
    Generate template-based justification as fallback.

    Args:
        gap_count: Number of compliance gaps
        confidence: Overall confidence score
        risk_score: Calculated risk score
        complexity: Complexity level
        workflow_path: Workflow path

    Returns:
        Template-based justification
    """
    if complexity == ComplexityLevel.ROUTINE:
        return f"Contract classified as ROUTINE with {gap_count} gap(s) and high confidence ({confidence:.2f}). Risk score of {risk_score:.2f} supports {workflow_path.value}."
    elif complexity == ComplexityLevel.STANDARD:
        return f"Contract classified as STANDARD with {gap_count} gap(s) and moderate confidence ({confidence:.2f}). Risk score of {risk_score:.2f} requires {workflow_path.value}."
    else:
        return f"Contract classified as COMPLEX with {gap_count} gap(s) and confidence ({confidence:.2f}). Risk score of {risk_score:.2f} necessitates {workflow_path.value}."


def _determine_escalation_level(workflow_path: WorkflowPath) -> str:
    """
    Determine escalation level based on workflow path.

    Args:
        workflow_path: Workflow path

    Returns:
        Escalation level string
    """
    if workflow_path == WorkflowPath.AUTO_APPROVE:
        return "NONE"
    elif workflow_path == WorkflowPath.PARALEGAL_REVIEW:
        return "PARALEGAL"
    else:
        return "GENERAL_COUNSEL"
