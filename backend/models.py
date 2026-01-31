"""
Data Models for LexConductor
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

Pydantic models for contract analysis, signal fusion, and legal reasoning.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

# ============================================================================
# Enums
# ============================================================================


class ContractType(str, Enum):
    """Contract type enumeration"""

    NDA = "NDA"
    MSA = "MSA"
    SERVICE_AGREEMENT = "Service Agreement"
    EMPLOYMENT = "Employment Agreement"
    LICENSE = "License Agreement"
    OTHER = "Other"


class Jurisdiction(str, Enum):
    """Jurisdiction enumeration"""

    US = "US"
    EU = "EU"
    UK = "UK"
    MULTI = "Multi-Jurisdiction"


class SignalAlignment(str, Enum):
    """Signal alignment classification"""

    MATCH = "MATCH"
    CONFLICT = "CONFLICT"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


class ComplexityLevel(str, Enum):
    """Contract complexity level"""

    ROUTINE = "ROUTINE"
    STANDARD = "STANDARD"
    COMPLEX = "COMPLEX"


class RiskLevel(str, Enum):
    """Risk level classification"""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class WorkflowPath(str, Enum):
    """Workflow routing path"""

    AUTO_APPROVE = "AUTO_APPROVE"
    PARALEGAL_REVIEW = "PARALEGAL_REVIEW"
    GC_ESCALATION = "GC_ESCALATION"


class SeverityLevel(str, Enum):
    """Severity level for compliance gaps"""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# ============================================================================
# Contract Models
# ============================================================================


class ContractClause(BaseModel):
    """Individual contract clause"""

    model_config = ConfigDict(str_strip_whitespace=True)

    section: str = Field(..., description="Section number or identifier")
    title: str = Field(..., description="Clause title")
    text: str = Field(..., min_length=1, description="Full clause text")
    page_number: Optional[int] = Field(None, ge=1, description="Page number in document")


class ContractDocument(BaseModel):
    """Complete contract document"""

    model_config = ConfigDict(str_strip_whitespace=True)

    contract_id: str = Field(..., description="Unique contract identifier")
    file_name: str = Field(..., description="Original file name")
    contract_type: ContractType = Field(..., description="Type of contract")
    jurisdiction: Jurisdiction = Field(..., description="Governing jurisdiction")
    full_text: str = Field(..., min_length=1, description="Complete contract text")
    clauses: List[ContractClause] = Field(default_factory=list, description="Extracted clauses")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="Upload timestamp")
    processed_at: Optional[datetime] = Field(None, description="Processing timestamp")


# ============================================================================
# Signal Analysis Models
# ============================================================================


class InternalSignal(BaseModel):
    """Internal policy signal (Golden Clause)"""

    model_config = ConfigDict(str_strip_whitespace=True)

    source: str = Field(..., description="Source identifier (e.g., 'Golden Clause #42')")
    type: str = Field(..., description="Clause type (e.g., 'liability_cap')")
    text: str = Field(..., description="Clause text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    alignment: SignalAlignment = Field(..., description="Alignment with contract")

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class ExternalSignal(BaseModel):
    """External regulatory signal"""

    model_config = ConfigDict(str_strip_whitespace=True)

    source: str = Field(..., description="Regulation source (e.g., 'CCPA 2026')")
    regulation: str = Field(..., description="Regulation name")
    requirement: str = Field(..., description="Specific requirement text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    alignment: SignalAlignment = Field(..., description="Alignment with contract")
    cos_url: Optional[str] = Field(None, description="COS URL to full regulation")

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class HistoricalSignal(BaseModel):
    """Historical precedent signal"""

    model_config = ConfigDict(str_strip_whitespace=True)

    decision_id: str = Field(..., description="Decision identifier")
    contract_type: ContractType = Field(..., description="Contract type")
    modification: str = Field(..., description="Modification made")
    rationale: str = Field(..., description="Rationale for decision")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity to current case")
    date: datetime = Field(..., description="Decision date")

    @field_validator("confidence", "similarity_score")
    @classmethod
    def validate_scores(cls, v: float) -> float:
        """Ensure scores are between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Score must be between 0.0 and 1.0")
        return v


class ComplianceGap(BaseModel):
    """Identified compliance gap"""

    model_config = ConfigDict(str_strip_whitespace=True)

    clause: str = Field(..., description="Affected clause")
    issue: str = Field(..., description="Description of the issue")
    severity: SeverityLevel = Field(..., description="Severity level")
    recommendation: str = Field(..., description="Recommended action")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    regulatory_basis: List[str] = Field(default_factory=list, description="Regulatory basis")

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class FusionAnalysis(BaseModel):
    """Complete signal fusion analysis"""

    model_config = ConfigDict(str_strip_whitespace=True)

    internal_signals: List[InternalSignal] = Field(
        default_factory=list, description="Internal signals"
    )
    external_signals: List[ExternalSignal] = Field(
        default_factory=list, description="External signals"
    )
    historical_signals: List[HistoricalSignal] = Field(
        default_factory=list, description="Historical signals"
    )
    gaps: List[ComplianceGap] = Field(default_factory=list, description="Compliance gaps")
    overall_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")

    @field_validator("overall_confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Overall confidence must be between 0.0 and 1.0")
        return v


# ============================================================================
# Routing Models
# ============================================================================


class RoutingDecision(BaseModel):
    """Contract routing decision"""

    model_config = ConfigDict(str_strip_whitespace=True)

    complexity: ComplexityLevel = Field(..., description="Complexity classification")
    risk_level: RiskLevel = Field(..., description="Risk level")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Calculated risk score")
    workflow_path: WorkflowPath = Field(..., description="Recommended workflow path")
    human_review_required: bool = Field(..., description="Whether human review is needed")
    justification: str = Field(..., description="Justification for routing decision")
    escalation_level: str = Field(..., description="Escalation level")

    @field_validator("risk_score")
    @classmethod
    def validate_risk_score(cls, v: float) -> float:
        """Ensure risk score is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Risk score must be between 0.0 and 1.0")
        return v


# ============================================================================
# Legal Logic Trace Models
# ============================================================================


class RecommendedAction(BaseModel):
    """Recommended action for a clause"""

    model_config = ConfigDict(str_strip_whitespace=True)

    clause: str = Field(..., description="Clause identifier")
    action: str = Field(..., description="Action type (APPROVE, MODIFY, REJECT, ESCALATE)")
    rationale: str = Field(..., description="Rationale for action")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    priority: str = Field(..., description="Priority level (LOW, MEDIUM, HIGH)")
    current_text: Optional[str] = Field(None, description="Current clause text")
    recommended_text: Optional[str] = Field(None, description="Recommended clause text")

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class LegalLogicTrace(BaseModel):
    """Complete legal logic trace"""

    model_config = ConfigDict(str_strip_whitespace=True)

    contract_id: str = Field(..., description="Contract identifier")
    contract_type: ContractType = Field(..., description="Contract type")
    jurisdiction: Jurisdiction = Field(..., description="Jurisdiction")
    timestamp: datetime = Field(default_factory=datetime.now, description="Trace timestamp")
    processing_time_ms: int = Field(..., ge=0, description="Processing time in milliseconds")

    # Analysis components
    fusion_analysis: FusionAnalysis = Field(..., description="Fusion analysis results")
    routing_decision: RoutingDecision = Field(..., description="Routing decision")

    # Final output
    summary: str = Field(..., description="Executive summary")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")
    recommendations: List[RecommendedAction] = Field(
        default_factory=list, description="Recommendations"
    )
    sources: List[str] = Field(default_factory=list, description="Sources consulted")

    # Metadata
    agent_versions: Dict[str, str] = Field(default_factory=dict, description="Agent versions")
    model_used: str = Field(default="ibm/granite-3-8b-instruct", description="AI model used")

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


# ============================================================================
# Cloudant Data Models
# ============================================================================


class GoldenClause(BaseModel):
    """Golden Clause document for Cloudant"""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: Optional[str] = Field(None, alias="_id", description="Document ID")
    rev: Optional[str] = Field(None, alias="_rev", description="Document revision")
    clause_id: str = Field(..., description="Clause identifier")
    type: str = Field(..., description="Clause type")
    contract_types: List[str] = Field(..., description="Applicable contract types")
    text: str = Field(..., description="Clause text")
    jurisdiction: str = Field(..., description="Jurisdiction")
    mandatory: bool = Field(..., description="Is mandatory")
    risk_level: str = Field(..., description="Risk level")
    last_reviewed: str = Field(..., description="Last review date (ISO format)")
    approved_by: str = Field(..., description="Approver")
    tags: List[str] = Field(default_factory=list, description="Tags")


class HistoricalDecision(BaseModel):
    """Historical decision document for Cloudant"""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: Optional[str] = Field(None, alias="_id", description="Document ID")
    rev: Optional[str] = Field(None, alias="_rev", description="Document revision")
    decision_id: str = Field(..., description="Decision identifier")
    contract_type: str = Field(..., description="Contract type")
    contract_id: str = Field(..., description="Original contract ID")
    clause_modified: str = Field(..., description="Modified clause")
    original_text: str = Field(..., description="Original text")
    modified_text: str = Field(..., description="Modified text")
    rationale: str = Field(..., description="Rationale")
    approved_by: str = Field(..., description="Approver")
    date: str = Field(..., description="Decision date (ISO format)")
    jurisdiction: str = Field(..., description="Jurisdiction")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    tags: List[str] = Field(default_factory=list, description="Tags")
    regulatory_basis: List[str] = Field(default_factory=list, description="Regulatory basis")

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0.0 and 1.0"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class RegulatoryMapping(BaseModel):
    """Regulatory mapping document for Cloudant"""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: Optional[str] = Field(None, alias="_id", description="Document ID")
    rev: Optional[str] = Field(None, alias="_rev", description="Document revision")
    regulation_id: str = Field(..., description="Regulation identifier")
    regulation_name: str = Field(..., description="Regulation name")
    regulation_type: str = Field(..., description="Regulation type")
    jurisdiction: str = Field(..., description="Jurisdiction")
    effective_date: str = Field(..., description="Effective date")
    cos_url: str = Field(..., description="COS URL to document")
    cos_key: str = Field(..., description="COS object key")
    description: str = Field(..., description="Description")
    key_requirements: List[str] = Field(default_factory=list, description="Key requirements")
    last_updated: str = Field(..., description="Last update date (ISO format)")
    tags: List[str] = Field(default_factory=list, description="Tags")


# ============================================================================
# API Request/Response Models
# ============================================================================


class ContractAnalysisRequest(BaseModel):
    """Request for contract analysis"""

    model_config = ConfigDict(str_strip_whitespace=True)

    contract_text: str = Field(..., min_length=1, description="Contract text")
    contract_type: ContractType = Field(..., description="Contract type")
    jurisdiction: Jurisdiction = Field(..., description="Jurisdiction")
    clauses: List[ContractClause] = Field(default_factory=list, description="Extracted clauses")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class RoutingRequest(BaseModel):
    """Request for routing decision"""

    model_config = ConfigDict(str_strip_whitespace=True)

    fusion_analysis: FusionAnalysis = Field(..., description="Fusion analysis results")
    contract_metadata: Dict[str, Any] = Field(default_factory=dict, description="Contract metadata")


class MemoryQueryRequest(BaseModel):
    """Request for memory/precedent query"""

    model_config = ConfigDict(str_strip_whitespace=True)

    contract_type: ContractType = Field(..., description="Contract type")
    jurisdiction: Jurisdiction = Field(..., description="Jurisdiction")
    clause_type: Optional[str] = Field(None, description="Specific clause type")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results")


class TraceRequest(BaseModel):
    """Request for legal logic trace generation"""

    model_config = ConfigDict(str_strip_whitespace=True)

    contract_id: str = Field(..., description="Contract identifier")
    contract_type: ContractType = Field(..., description="Contract type")
    fusion_analysis: FusionAnalysis = Field(..., description="Fusion analysis")
    routing_decision: RoutingDecision = Field(..., description="Routing decision")
    precedents: List[HistoricalSignal] = Field(default_factory=list, description="Precedents")


class HealthCheckResponse(BaseModel):
    """Health check response"""

    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    version: str = Field(default="1.0.0", description="Service version")
    dependencies: Dict[str, str] = Field(default_factory=dict, description="Dependency status")
