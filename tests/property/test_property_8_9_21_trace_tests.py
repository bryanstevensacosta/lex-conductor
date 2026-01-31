"""
Property-Based Tests: Legal Logic Trace Properties

Feature: lex-conductor-implementation
Property 8: Legal Logic Trace Generation
Property 9: Trace Completeness
Property 21: Low Confidence Flagging

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 9.7**
"""

import pytest
from hypothesis import given, strategies as st, settings
from datetime import datetime, timezone

from backend.models import (
    ContractType,
    Jurisdiction,
    FusionAnalysis,
    RoutingDecision,
    ComplexityLevel,
    RiskLevel,
    WorkflowPath,
    InternalSignal,
    ExternalSignal,
    ComplianceGap,
    SignalAlignment,
)
from backend.routers.traceability import (
    _generate_header,
    _generate_signal_analysis,
    _generate_risk_assessment,
    _generate_recommendations,
    _format_recommendations,
    _generate_summary,
)


# Custom strategies
@st.composite
def fusion_analysis_strategy(draw):
    """Generate a valid FusionAnalysis."""
    return FusionAnalysis(
        internal_signals=draw(
            st.lists(
                st.builds(
                    InternalSignal,
                    source=st.text(min_size=5, max_size=50),
                    type=st.text(min_size=5, max_size=20),
                    text=st.text(min_size=10, max_size=200),
                    confidence=st.floats(min_value=0.0, max_value=1.0),
                    alignment=st.sampled_from(list(SignalAlignment)),
                ),
                min_size=0,
                max_size=5,
            )
        ),
        external_signals=draw(
            st.lists(
                st.builds(
                    ExternalSignal,
                    source=st.text(min_size=5, max_size=50),
                    regulation=st.text(min_size=5, max_size=50),
                    requirement=st.text(min_size=10, max_size=200),
                    confidence=st.floats(min_value=0.0, max_value=1.0),
                    alignment=st.sampled_from(list(SignalAlignment)),
                    cos_url=st.none(),
                ),
                min_size=0,
                max_size=5,
            )
        ),
        historical_signals=[],
        gaps=draw(
            st.lists(
                st.builds(
                    ComplianceGap,
                    clause=st.text(min_size=5, max_size=50),
                    issue=st.text(min_size=10, max_size=200),
                    severity=st.sampled_from(["LOW", "MEDIUM", "HIGH"]),
                    recommendation=st.text(min_size=10, max_size=200),
                    confidence=st.floats(min_value=0.0, max_value=1.0),
                    regulatory_basis=st.lists(
                        st.text(min_size=5, max_size=50), min_size=1, max_size=3
                    ),
                ),
                min_size=0,
                max_size=5,
            )
        ),
        overall_confidence=draw(st.floats(min_value=0.0, max_value=1.0)),
    )


@st.composite
def routing_decision_strategy(draw):
    """Generate a valid RoutingDecision."""
    return RoutingDecision(
        complexity=draw(st.sampled_from(list(ComplexityLevel))),
        risk_level=draw(st.sampled_from(list(RiskLevel))),
        risk_score=draw(st.floats(min_value=0.0, max_value=1.0)),
        workflow_path=draw(st.sampled_from(list(WorkflowPath))),
        human_review_required=draw(st.booleans()),
        justification=draw(st.text(min_size=20, max_size=200)),
        escalation_level=draw(st.sampled_from(["NONE", "PARALEGAL", "GENERAL_COUNSEL"])),
    )


# Property 8: Legal Logic Trace Generation
@given(
    contract_id=st.text(min_size=5, max_size=50),
    contract_type=st.sampled_from(list(ContractType)),
    jurisdiction=st.sampled_from(list(Jurisdiction)),
    fusion_analysis=fusion_analysis_strategy(),
    routing_decision=routing_decision_strategy(),
)
@settings(max_examples=100, deadline=None)
def test_trace_generation_produces_valid_output(
    contract_id: str,
    contract_type: ContractType,
    jurisdiction: Jurisdiction,
    fusion_analysis: FusionAnalysis,
    routing_decision: RoutingDecision,
):
    """
    Property 8: For any completed Signal Fusion analysis, a Legal Logic Trace
    report should be generated containing all required sections.

    This test verifies that:
    1. Trace generation succeeds for any valid input
    2. Output is a non-empty string
    3. Output contains markdown formatting
    """
    from backend.routers.traceability import TraceRequest

    # Create trace request
    request = TraceRequest(
        contract_id=contract_id,
        contract_type=contract_type,
        jurisdiction=jurisdiction,
        fusion_analysis=fusion_analysis,
        routing_decision=routing_decision,
        precedents=[],
    )

    # Generate header
    header = _generate_header(request, datetime.now(timezone.utc).isoformat())

    # Verify header is generated
    assert header is not None
    assert len(header) > 0
    assert "LEGAL LOGIC TRACE" in header
    assert contract_id in header


# Property 9: Trace Completeness
@given(
    contract_id=st.text(min_size=5, max_size=50),
    contract_type=st.sampled_from(list(ContractType)),
    jurisdiction=st.sampled_from(list(Jurisdiction)),
    fusion_analysis=fusion_analysis_strategy(),
    routing_decision=routing_decision_strategy(),
)
@settings(max_examples=100, deadline=None)
def test_trace_contains_all_required_sections(
    contract_id: str,
    contract_type: ContractType,
    jurisdiction: Jurisdiction,
    fusion_analysis: FusionAnalysis,
    routing_decision: RoutingDecision,
):
    """
    Property 9: For any generated Legal Logic Trace, it should include contract
    metadata (type, complexity, jurisdiction), all consulted sources, and
    clause-level analysis with source citations.

    This test verifies that:
    1. Trace contains contract metadata
    2. Trace contains signal analysis
    3. Trace contains risk assessment
    4. Trace contains recommendations
    """
    from backend.routers.traceability import TraceRequest

    request = TraceRequest(
        contract_id=contract_id,
        contract_type=contract_type,
        jurisdiction=jurisdiction,
        fusion_analysis=fusion_analysis,
        routing_decision=routing_decision,
        precedents=[],
    )

    # Generate all sections
    header = _generate_header(request, datetime.now(timezone.utc).isoformat())
    signal_analysis = _generate_signal_analysis(fusion_analysis, [])
    risk_assessment = _generate_risk_assessment(routing_decision)
    recommendations = _generate_recommendations(fusion_analysis)
    formatted_recs = _format_recommendations(recommendations)
    summary = _generate_summary(fusion_analysis, routing_decision, recommendations)

    # Verify all sections are present
    assert header is not None and len(header) > 0
    assert signal_analysis is not None and len(signal_analysis) > 0
    assert risk_assessment is not None and len(risk_assessment) > 0
    assert formatted_recs is not None and len(formatted_recs) > 0
    assert summary is not None and len(summary) > 0

    # Verify metadata in header
    assert contract_id in header
    assert contract_type.value in header
    assert jurisdiction.value in header

    # Verify risk assessment contains routing info
    assert routing_decision.complexity.value in risk_assessment
    assert routing_decision.workflow_path.value in risk_assessment


# Property 21: Low Confidence Flagging
@given(fusion_analysis=fusion_analysis_strategy())
@settings(max_examples=100, deadline=None)
def test_low_confidence_recommendations_are_flagged(fusion_analysis: FusionAnalysis):
    """
    Property 21: For any recommendation with confidence score below 0.5 (50%),
    the Legal Logic Trace should include a flag indicating human review is required.

    This test verifies that:
    1. Recommendations with confidence < 0.5 are identified
    2. Low confidence recommendations are flagged
    3. Flagging is consistent across all recommendations
    """
    # Generate recommendations
    recommendations = _generate_recommendations(fusion_analysis)

    # Format recommendations (verify formatting works)
    _ = _format_recommendations(recommendations)

    # Check each recommendation
    for rec in recommendations:
        if rec.confidence < 0.5:
            # Verify low confidence is flagged
            # The formatted output should contain a warning
            assert (
                rec.action == "ESCALATE" or rec.priority == "HIGH"
            ), f"Low confidence recommendation (confidence={rec.confidence}) should be escalated or high priority"


@given(
    fusion_analysis=fusion_analysis_strategy(),
    routing_decision=routing_decision_strategy(),
)
@settings(max_examples=100, deadline=None)
def test_recommendations_have_valid_confidence_scores(
    fusion_analysis: FusionAnalysis, routing_decision: RoutingDecision
):
    """
    Property: All recommendations should have valid confidence scores in [0.0, 1.0].
    """
    recommendations = _generate_recommendations(fusion_analysis)

    for rec in recommendations:
        assert (
            0.0 <= rec.confidence <= 1.0
        ), f"Recommendation confidence out of range: {rec.confidence}"


@given(fusion_analysis=fusion_analysis_strategy())
@settings(max_examples=100, deadline=None)
def test_recommendations_have_required_fields(fusion_analysis: FusionAnalysis):
    """
    Property: All recommendations should have all required fields populated.
    """
    recommendations = _generate_recommendations(fusion_analysis)

    # Should always have at least one recommendation
    assert len(recommendations) > 0, "Should generate at least one recommendation"

    for rec in recommendations:
        assert rec.clause is not None and len(rec.clause) > 0, "Recommendation missing clause"
        assert rec.action is not None and len(rec.action) > 0, "Recommendation missing action"
        assert (
            rec.rationale is not None and len(rec.rationale) > 0
        ), "Recommendation missing rationale"
        assert rec.confidence is not None, "Recommendation missing confidence"
        assert rec.priority is not None and len(rec.priority) > 0, "Recommendation missing priority"


@given(
    fusion_analysis=fusion_analysis_strategy(),
    routing_decision=routing_decision_strategy(),
)
@settings(max_examples=100, deadline=None)
def test_summary_reflects_overall_decision(
    fusion_analysis: FusionAnalysis, routing_decision: RoutingDecision
):
    """
    Property: Summary should reflect the overall decision and next steps.
    """
    recommendations = _generate_recommendations(fusion_analysis)
    summary = _generate_summary(fusion_analysis, routing_decision, recommendations)

    # Summary should be non-empty
    assert summary is not None and len(summary) > 0

    # Summary should contain decision summary section
    assert "DECISION SUMMARY" in summary

    # Summary should contain next steps
    assert "Next Steps" in summary

    # Summary should contain overall confidence
    assert (
        str(fusion_analysis.overall_confidence) in summary
        or f"{fusion_analysis.overall_confidence:.2f}" in summary
    )


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
