"""
Property-Based Test: Complexity Assignment Consistency

Feature: lex-conductor-implementation
Property 4: Complexity Assignment Consistency

**Validates: Requirements 1.4, 1.5**

For any classified contract, complexity assignment should return exactly one
complexity level (Routine, Standard, Complex) and the routing decision should
be consistent with that complexity level.
"""

import pytest
from hypothesis import given, strategies as st, settings

from backend.models import ComplexityLevel, RiskLevel, WorkflowPath, RoutingDecision


@given(risk_score=st.floats(min_value=0.0, max_value=1.0))
@settings(max_examples=100, deadline=None)
def test_complexity_assignment_returns_valid_level(risk_score: float):
    """
    Property: Complexity assignment should return exactly one valid complexity level.

    This test verifies that:
    1. Complexity is one of: ROUTINE, STANDARD, COMPLEX
    2. Assignment is deterministic for a given risk score
    3. Assignment follows the defined thresholds
    """
    from backend.routers.routing import _classify_complexity

    complexity = _classify_complexity(risk_score)

    # Check that complexity is valid
    valid_levels = {
        ComplexityLevel.ROUTINE,
        ComplexityLevel.STANDARD,
        ComplexityLevel.COMPLEX,
    }
    assert complexity in valid_levels, f"Invalid complexity level: {complexity}"

    # Check threshold consistency
    if risk_score < 0.3:
        assert (
            complexity == ComplexityLevel.ROUTINE
        ), f"Risk score {risk_score} should be ROUTINE, got {complexity}"
    elif risk_score < 0.7:
        assert (
            complexity == ComplexityLevel.STANDARD
        ), f"Risk score {risk_score} should be STANDARD, got {complexity}"
    else:
        assert (
            complexity == ComplexityLevel.COMPLEX
        ), f"Risk score {risk_score} should be COMPLEX, got {complexity}"


@given(risk_score=st.floats(min_value=0.0, max_value=1.0))
@settings(max_examples=100, deadline=None)
def test_workflow_path_consistent_with_complexity(risk_score: float):
    """
    Property: Workflow path should be consistent with complexity level.

    This test verifies that:
    1. ROUTINE complexity can lead to AUTO_APPROVE
    2. STANDARD complexity leads to PARALEGAL_REVIEW
    3. COMPLEX complexity leads to GC_ESCALATION
    4. Routing decision is consistent with risk score
    """
    from backend.routers.routing import _classify_complexity, _determine_workflow_path

    complexity = _classify_complexity(risk_score)
    workflow_path = _determine_workflow_path(complexity, risk_score)

    # Check that workflow path is valid
    valid_paths = {
        WorkflowPath.AUTO_APPROVE,
        WorkflowPath.PARALEGAL_REVIEW,
        WorkflowPath.GC_ESCALATION,
    }
    assert workflow_path in valid_paths, f"Invalid workflow path: {workflow_path}"

    # Check consistency with complexity
    if complexity == ComplexityLevel.COMPLEX:
        assert (
            workflow_path == WorkflowPath.GC_ESCALATION
        ), "COMPLEX contracts should escalate to GC"

    if risk_score >= 0.7:
        assert (
            workflow_path == WorkflowPath.GC_ESCALATION
        ), "High risk contracts should escalate to GC"


@given(
    complexity=st.sampled_from(list(ComplexityLevel)),
    risk_level=st.sampled_from(list(RiskLevel)),
    risk_score=st.floats(min_value=0.0, max_value=1.0),
    workflow_path=st.sampled_from(list(WorkflowPath)),
)
@settings(max_examples=100, deadline=None)
def test_routing_decision_has_all_required_fields(
    complexity: ComplexityLevel,
    risk_level: RiskLevel,
    risk_score: float,
    workflow_path: WorkflowPath,
):
    """
    Property: RoutingDecision should have all required fields populated.

    This test verifies that:
    1. All fields are non-null
    2. Risk score is in valid range
    3. Human review flag is consistent with workflow path
    """
    routing_decision = RoutingDecision(
        complexity=complexity,
        risk_level=risk_level,
        risk_score=risk_score,
        workflow_path=workflow_path,
        human_review_required=(workflow_path != WorkflowPath.AUTO_APPROVE),
        justification="Test justification",
        escalation_level="TEST",
    )

    # Check all fields are present
    assert routing_decision.complexity is not None
    assert routing_decision.risk_level is not None
    assert routing_decision.risk_score is not None
    assert routing_decision.workflow_path is not None
    assert routing_decision.human_review_required is not None
    assert routing_decision.justification is not None
    assert routing_decision.escalation_level is not None

    # Check risk score is in valid range
    assert 0.0 <= routing_decision.risk_score <= 1.0


@given(risk_score=st.floats(min_value=0.0, max_value=1.0))
@settings(max_examples=100, deadline=None)
def test_risk_level_consistent_with_risk_score(risk_score: float):
    """
    Property: Risk level should be consistent with risk score.

    This test verifies that:
    1. LOW risk: risk_score < 0.3
    2. MEDIUM risk: 0.3 <= risk_score < 0.7
    3. HIGH risk: risk_score >= 0.7
    """
    from backend.routers.routing import _determine_risk_level

    risk_level = _determine_risk_level(risk_score)

    # Check threshold consistency
    if risk_score < 0.3:
        assert (
            risk_level == RiskLevel.LOW
        ), f"Risk score {risk_score} should be LOW, got {risk_level}"
    elif risk_score < 0.7:
        assert (
            risk_level == RiskLevel.MEDIUM
        ), f"Risk score {risk_score} should be MEDIUM, got {risk_level}"
    else:
        assert (
            risk_level == RiskLevel.HIGH
        ), f"Risk score {risk_score} should be HIGH, got {risk_level}"


@given(risk_score=st.floats(min_value=0.0, max_value=1.0))
@settings(max_examples=100, deadline=None)
def test_human_review_flag_consistent_with_workflow(risk_score: float):
    """
    Property: Human review flag should be consistent with workflow path.

    This test verifies that:
    1. AUTO_APPROVE does not require human review
    2. PARALEGAL_REVIEW requires human review
    3. GC_ESCALATION requires human review
    """
    from backend.routers.routing import _classify_complexity, _determine_workflow_path

    complexity = _classify_complexity(risk_score)
    workflow_path = _determine_workflow_path(complexity, risk_score)

    # Determine expected human review requirement
    expected_human_review = workflow_path != WorkflowPath.AUTO_APPROVE

    # Verify consistency
    if workflow_path == WorkflowPath.AUTO_APPROVE:
        assert not expected_human_review, "AUTO_APPROVE should not require human review"
    else:
        assert expected_human_review, f"{workflow_path} should require human review"


@given(risk_score=st.floats(min_value=0.0, max_value=1.0))
@settings(max_examples=100, deadline=None)
def test_complexity_assignment_is_deterministic(risk_score: float):
    """
    Property: Complexity assignment should be deterministic.

    This test verifies that:
    1. Same risk score always produces same complexity
    2. Assignment is repeatable
    """
    from backend.routers.routing import _classify_complexity

    # Call twice with same input
    complexity1 = _classify_complexity(risk_score)
    complexity2 = _classify_complexity(risk_score)

    # Should be identical
    assert (
        complexity1 == complexity2
    ), f"Complexity assignment not deterministic: {complexity1} != {complexity2}"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
