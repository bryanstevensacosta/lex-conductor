"""
Fusion Agent router for Signal Fusion analysis.

This module provides the endpoint for analyzing contracts by correlating:
- Internal signals (Golden Clauses from Cloudant)
- External signals (Regulatory documents from COS)
- Historical signals (Precedents from Cloudant)

The Fusion Agent identifies compliance gaps and conflicts, generating
clause-level recommendations with source attribution.
"""

import os
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.models import (
    ContractType,
    Jurisdiction,
    ContractClause,
    InternalSignal,
    ExternalSignal,
    ComplianceGap,
    FusionAnalysis,
    SignalAlignment,
)
from backend.cloudant_client import CloudantClient
from backend.cos_client import COSClient
from backend.watsonx_client import WatsonxClient

router = APIRouter()

# Client instances (initialized lazily)
_cloudant_client = None
_cos_client = None
_watsonx_client = None


def get_cloudant_client() -> CloudantClient:
    """Get or create Cloudant client instance."""
    global _cloudant_client
    if _cloudant_client is None:
        _cloudant_client = CloudantClient(
            url=os.getenv("CLOUDANT_URL"), api_key=os.getenv("CLOUDANT_API_KEY")
        )
    return _cloudant_client


def get_cos_client() -> COSClient:
    """Get or create COS client instance."""
    global _cos_client
    if _cos_client is None:
        _cos_client = COSClient(
            endpoint=os.getenv("COS_ENDPOINT"),
            api_key=os.getenv("COS_API_KEY"),
            instance_id=os.getenv("COS_INSTANCE_ID"),
        )
    return _cos_client


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


class ContractAnalysisRequest(BaseModel):
    """Request model for contract analysis."""

    contract_text: str = Field(..., description="Full text of the contract")
    contract_type: ContractType = Field(..., description="Type of contract")
    jurisdiction: Jurisdiction = Field(..., description="Legal jurisdiction")
    clauses: List[ContractClause] = Field(
        default_factory=list, description="Extracted contract clauses"
    )


@router.post("/analyze", response_model=FusionAnalysis)
async def analyze_contract(request: ContractAnalysisRequest):
    """
    Analyze contract by performing Signal Fusion.

    This endpoint:
    1. Queries Cloudant for relevant Golden Clauses
    2. Retrieves regulatory documents from COS
    3. Extracts relevant sections from regulations
    4. Performs signal correlation analysis using watsonx.ai
    5. Identifies compliance gaps and conflicts
    6. Returns FusionAnalysis with confidence scores and source attribution

    Args:
        request: ContractAnalysisRequest with contract details

    Returns:
        FusionAnalysis: Complete analysis with signals, gaps, and confidence scores

    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Step 1: Query Cloudant for Golden Clauses
        golden_clauses = await _get_golden_clauses(request.contract_type)

        # Step 2: Query COS for regulatory documents
        regulations = await _get_regulations(request.jurisdiction)

        # Step 3: Extract relevant sections from regulatory PDFs
        regulatory_sections = await _extract_regulatory_sections(
            regulations, request.contract_text, request.contract_type
        )

        # Step 4: Perform signal correlation analysis
        internal_signals = await _analyze_internal_signals(
            request.contract_text, request.clauses, golden_clauses
        )

        external_signals = await _analyze_external_signals(
            request.contract_text, request.clauses, regulatory_sections
        )

        # Step 5: Identify compliance gaps and conflicts
        gaps = await _identify_compliance_gaps(
            request.contract_text, request.clauses, internal_signals, external_signals
        )

        # Step 6: Calculate overall confidence
        overall_confidence = _calculate_overall_confidence(internal_signals, external_signals, gaps)

        # Return FusionAnalysis
        return FusionAnalysis(
            internal_signals=internal_signals,
            external_signals=external_signals,
            historical_signals=[],  # Will be populated by Memory Agent
            gaps=gaps,
            overall_confidence=overall_confidence,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "FUSION_ANALYSIS_FAILED",
                "message": f"Failed to perform fusion analysis: {str(e)}",
            },
        )


async def _get_golden_clauses(contract_type: ContractType) -> List[dict]:
    """
    Retrieve Golden Clauses from Cloudant for the given contract type.

    Args:
        contract_type: Type of contract

    Returns:
        List of Golden Clause documents
    """
    try:
        cloudant_client = get_cloudant_client()
        clauses = cloudant_client.query_golden_clauses(contract_type.value)
        return clauses if clauses else []
    except Exception as e:
        # Log warning but don't fail - graceful degradation
        print(f"Warning: Failed to retrieve Golden Clauses: {e}")
        return []


async def _get_regulations(jurisdiction: Jurisdiction) -> List[dict]:
    """
    Retrieve regulatory documents from COS for the given jurisdiction.

    Args:
        jurisdiction: Legal jurisdiction

    Returns:
        List of regulation metadata
    """
    try:
        cos_client = get_cos_client()
        regulations = cos_client.list_regulations(jurisdiction.value)
        return regulations if regulations else []
    except Exception as e:
        # Log warning but don't fail - graceful degradation
        print(f"Warning: Failed to retrieve regulations: {e}")
        return []


async def _extract_regulatory_sections(
    regulations: List[dict], contract_text: str, contract_type: ContractType
) -> List[dict]:
    """
    Extract relevant sections from regulatory PDFs using watsonx.ai.

    Args:
        regulations: List of regulation metadata
        contract_text: Full contract text
        contract_type: Type of contract

    Returns:
        List of relevant regulatory sections
    """
    if not regulations:
        return []

    sections = []
    cos_client = get_cos_client()
    watsonx_client = get_watsonx_client()

    # For each regulation, extract relevant sections
    for reg in regulations[:5]:  # Limit to 5 regulations to control costs
        try:
            # Get regulation content from COS
            reg_content = cos_client.get_regulation(
                reg.get("jurisdiction", "US"), reg.get("name", "")
            )

            if not reg_content:
                continue

            # Use watsonx.ai to identify relevant sections
            prompt = f"""Analyze this regulatory document and identify sections relevant to a {contract_type.value} contract.

Regulatory Document: {reg_content[:2000]}...

Contract Type: {contract_type.value}

Extract the most relevant regulatory requirements (max 3 sections). For each section, provide:
1. Section reference
2. Requirement text
3. Relevance explanation

Format as JSON array."""

            response = watsonx_client.generate(prompt=prompt, max_tokens=500, temperature=0.1)

            # Parse response and add to sections
            sections.append(
                {
                    "source": reg.get("name", "Unknown"),
                    "jurisdiction": reg.get("jurisdiction", "Unknown"),
                    "content": response,
                    "url": reg.get("url", ""),
                }
            )

        except Exception as e:
            print(f"Warning: Failed to extract sections from {reg.get('name')}: {e}")
            continue

    return sections


async def _analyze_internal_signals(
    contract_text: str, clauses: List[ContractClause], golden_clauses: List[dict]
) -> List[InternalSignal]:
    """
    Analyze internal signals by comparing contract clauses with Golden Clauses.

    Args:
        contract_text: Full contract text
        clauses: Extracted contract clauses
        golden_clauses: Golden Clauses from Cloudant

    Returns:
        List of InternalSignal objects
    """
    if not golden_clauses:
        return []

    internal_signals = []
    watsonx_client = get_watsonx_client()

    for golden in golden_clauses[:10]:  # Limit to 10 clauses
        try:
            # Handle both dict and Pydantic model
            if isinstance(golden, dict):
                clause_id = golden.get("clause_id", "unknown")
                clause_type = golden.get("type", "unknown")
                clause_text = golden.get("text", "")
            else:
                clause_id = getattr(golden, "clause_id", "unknown")
                clause_type = getattr(golden, "type", "unknown")
                clause_text = getattr(golden, "text", "")

            # Use watsonx.ai to compare Golden Clause with contract
            prompt = f"""Compare this Golden Clause with the contract text and determine alignment.

Golden Clause ({clause_type}):
{clause_text}

Contract Text (excerpt):
{contract_text[:1000]}...

Determine:
1. Alignment: MATCH, CONFLICT, PARTIAL, or UNKNOWN
2. Confidence score (0.0-1.0)
3. Brief explanation

Format as JSON: {{"alignment": "...", "confidence": 0.0, "explanation": "..."}}"""

            response = watsonx_client.generate(prompt=prompt, max_tokens=200, temperature=0.1)

            # Parse response (simplified - in production, use proper JSON parsing)
            alignment = SignalAlignment.UNKNOWN
            confidence = 0.7

            if "MATCH" in response.upper():
                alignment = SignalAlignment.MATCH
                confidence = 0.9
            elif "CONFLICT" in response.upper():
                alignment = SignalAlignment.CONFLICT
                confidence = 0.85
            elif "PARTIAL" in response.upper():
                alignment = SignalAlignment.PARTIAL
                confidence = 0.75

            internal_signals.append(
                InternalSignal(
                    source=f"Golden Clause #{clause_id}",
                    type=clause_type,
                    text=clause_text[:200],  # Truncate for response size
                    confidence=confidence,
                    alignment=alignment,
                )
            )

        except Exception as e:
            print(f"Warning: Failed to analyze Golden Clause: {e}")
            continue

    return internal_signals


async def _analyze_external_signals(
    contract_text: str, clauses: List[ContractClause], regulatory_sections: List[dict]
) -> List[ExternalSignal]:
    """
    Analyze external signals by comparing contract with regulatory requirements.

    Args:
        contract_text: Full contract text
        clauses: Extracted contract clauses
        regulatory_sections: Relevant regulatory sections

    Returns:
        List of ExternalSignal objects
    """
    if not regulatory_sections:
        return []

    external_signals = []
    watsonx_client = get_watsonx_client()

    for section in regulatory_sections[:5]:  # Limit to 5 sections
        try:
            # Use watsonx.ai to analyze regulatory compliance
            prompt = f"""Analyze if this contract complies with the regulatory requirement.

Regulatory Requirement:
{section.get('content', '')[:500]}

Contract Text (excerpt):
{contract_text[:1000]}...

Determine:
1. Alignment: MATCH, CONFLICT, PARTIAL, or UNKNOWN
2. Confidence score (0.0-1.0)
3. Specific requirement text

Format as JSON: {{"alignment": "...", "confidence": 0.0, "requirement": "..."}}"""

            response = watsonx_client.generate(prompt=prompt, max_tokens=200, temperature=0.1)

            # Parse response (simplified)
            alignment = SignalAlignment.UNKNOWN
            confidence = 0.75

            if "MATCH" in response.upper():
                alignment = SignalAlignment.MATCH
                confidence = 0.9
            elif "CONFLICT" in response.upper():
                alignment = SignalAlignment.CONFLICT
                confidence = 0.85
            elif "PARTIAL" in response.upper():
                alignment = SignalAlignment.PARTIAL
                confidence = 0.75

            external_signals.append(
                ExternalSignal(
                    source=section.get("source", "Unknown Regulation"),
                    regulation=section.get("source", "Unknown"),
                    requirement=response[:200],  # Truncate
                    confidence=confidence,
                    alignment=alignment,
                    cos_url=section.get("url"),
                )
            )

        except Exception as e:
            print(f"Warning: Failed to analyze regulatory section: {e}")
            continue

    return external_signals


async def _identify_compliance_gaps(
    contract_text: str,
    clauses: List[ContractClause],
    internal_signals: List[InternalSignal],
    external_signals: List[ExternalSignal],
) -> List[ComplianceGap]:
    """
    Identify compliance gaps based on signal analysis.

    Args:
        contract_text: Full contract text
        clauses: Extracted contract clauses
        internal_signals: Internal signal analysis
        external_signals: External signal analysis

    Returns:
        List of ComplianceGap objects
    """
    gaps = []
    watsonx_client = get_watsonx_client()

    # Identify gaps from conflicting signals
    for signal in internal_signals + external_signals:
        if signal.alignment == SignalAlignment.CONFLICT:
            # Determine severity based on confidence
            severity = "HIGH" if signal.confidence > 0.8 else "MEDIUM"

            # Generate recommendation using watsonx.ai
            prompt = f"""Generate a specific recommendation to resolve this compliance conflict.

Conflict: {signal.source} conflicts with contract
Confidence: {signal.confidence}

Provide:
1. Specific clause to modify
2. Recommended action
3. Regulatory basis

Keep response concise (max 100 words)."""

            try:
                recommendation = watsonx_client.generate(
                    prompt=prompt, max_tokens=150, temperature=0.1
                )

                gaps.append(
                    ComplianceGap(
                        clause="Section TBD",  # Would need clause extraction logic
                        issue=f"Conflict with {signal.source}",
                        severity=severity,
                        recommendation=recommendation[:200],
                        confidence=signal.confidence,
                        regulatory_basis=[signal.source],
                    )
                )
            except Exception as e:
                print(f"Warning: Failed to generate recommendation: {e}")
                continue

    return gaps


def _calculate_overall_confidence(
    internal_signals: List[InternalSignal],
    external_signals: List[ExternalSignal],
    gaps: List[ComplianceGap],
) -> float:
    """
    Calculate overall confidence score for the analysis.

    Args:
        internal_signals: Internal signal analysis
        external_signals: External signal analysis
        gaps: Identified compliance gaps

    Returns:
        Overall confidence score (0.0-1.0)
    """
    if not internal_signals and not external_signals:
        return 0.5  # Default confidence when no signals

    # Calculate average confidence from all signals
    all_confidences = [s.confidence for s in internal_signals] + [
        s.confidence for s in external_signals
    ]

    if not all_confidences:
        return 0.5

    avg_confidence = sum(all_confidences) / len(all_confidences)

    # Reduce confidence if there are many gaps
    gap_penalty = min(0.2, len(gaps) * 0.05)

    final_confidence = max(0.0, min(1.0, avg_confidence - gap_penalty))

    return round(final_confidence, 2)
