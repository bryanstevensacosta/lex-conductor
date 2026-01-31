"""
Memory Agent router for historical precedent retrieval.

This module provides the endpoint for querying historical contract decisions
and retrieving similar past cases to inform current analysis.
"""

import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.models import ContractType, Jurisdiction, HistoricalSignal
from backend.cloudant_client import CloudantClient

router = APIRouter()

# Client instance (initialized lazily)
_cloudant_client = None


def get_cloudant_client() -> CloudantClient:
    """Get or create Cloudant client instance."""
    global _cloudant_client
    if _cloudant_client is None:
        _cloudant_client = CloudantClient(
            url=os.getenv("CLOUDANT_URL"), api_key=os.getenv("CLOUDANT_API_KEY")
        )
    return _cloudant_client


class MemoryQueryRequest(BaseModel):
    """Request model for memory query."""

    contract_type: ContractType = Field(..., description="Type of contract")
    jurisdiction: Jurisdiction = Field(..., description="Legal jurisdiction")
    clause_type: Optional[str] = Field(None, description="Specific clause type to search for")
    limit: int = Field(
        default=10, ge=1, le=50, description="Maximum number of precedents to return"
    )


class MemoryQueryResponse(BaseModel):
    """Response model for memory query."""

    precedents: List[HistoricalSignal] = Field(..., description="List of historical precedents")
    total_found: int = Field(..., description="Total number of precedents found")
    avg_confidence: float = Field(..., description="Average confidence score of precedents")


@router.post("/query", response_model=MemoryQueryResponse)
async def query_precedents(request: MemoryQueryRequest):
    """
    Query historical precedents from Cloudant.

    This endpoint:
    1. Queries Cloudant historical_decisions database
    2. Filters by contract type and jurisdiction
    3. Optionally filters by clause type
    4. Calculates similarity scores (simplified for MVP)
    5. Returns list of HistoricalSignal objects with precedents

    Args:
        request: MemoryQueryRequest with query parameters

    Returns:
        MemoryQueryResponse: List of precedents with metadata

    Raises:
        HTTPException: If query fails
    """
    try:
        cloudant_client = get_cloudant_client()

        # Query Cloudant for historical decisions
        precedents_data = cloudant_client.get_precedents(
            contract_type=request.contract_type.value,
            jurisdiction=request.jurisdiction.value,
            limit=request.limit,
        )

        # Convert to HistoricalSignal objects
        precedents = []
        for prec in precedents_data:
            try:
                # Calculate similarity score (simplified - in production, use embeddings)
                similarity_score = _calculate_similarity_score(prec, request.clause_type)

                historical_signal = HistoricalSignal(
                    decision_id=prec.get("decision_id", "unknown"),
                    contract_type=ContractType(
                        prec.get("contract_type", request.contract_type.value)
                    ),
                    modification=prec.get("modified_text", ""),
                    rationale=prec.get("rationale", ""),
                    confidence=prec.get("confidence", 0.7),
                    similarity_score=similarity_score,
                    date=prec.get("date", "2025-01-01"),
                )
                precedents.append(historical_signal)
            except Exception as e:
                print(f"Warning: Failed to parse precedent {prec.get('decision_id')}: {e}")
                continue

        # Calculate average confidence
        avg_confidence = (
            sum(p.confidence for p in precedents) / len(precedents) if precedents else 0.0
        )

        return MemoryQueryResponse(
            precedents=precedents,
            total_found=len(precedents),
            avg_confidence=round(avg_confidence, 2),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "MEMORY_QUERY_FAILED",
                "message": f"Failed to query precedents: {str(e)}",
            },
        )


def _calculate_similarity_score(precedent: dict, clause_type: Optional[str]) -> float:
    """
    Calculate similarity score for a precedent.

    This is a simplified implementation. In production, would use:
    - Text embeddings (e.g., sentence-transformers)
    - Semantic similarity
    - Keyword matching with TF-IDF

    Args:
        precedent: Precedent data from Cloudant
        clause_type: Optional clause type to match

    Returns:
        Similarity score from 0.0 to 1.0
    """
    # Base similarity score
    score = 0.7

    # Boost score if clause type matches
    if clause_type:
        precedent_tags = precedent.get("tags", [])
        if clause_type.lower() in [tag.lower() for tag in precedent_tags]:
            score += 0.2

    # Boost score based on confidence
    precedent_confidence = precedent.get("confidence", 0.7)
    score = (score + precedent_confidence) / 2

    # Ensure score is in valid range
    return max(0.0, min(1.0, score))
