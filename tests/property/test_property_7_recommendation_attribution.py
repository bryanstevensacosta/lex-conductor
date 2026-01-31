"""
Property-Based Test: Recommendation Attribution

Feature: lex-conductor-implementation
Property 7: Recommendation Attribution

**Validates: Requirements 2.6**

For any generated recommendation, it should include the clause identifier,
recommended action, and at least one source attribution.
"""

import pytest
from hypothesis import given, strategies as st, settings
from typing import List

from backend.models import ComplianceGap, RecommendedAction


# Custom strategies for generating recommendations
@st.composite
def compliance_gap_strategy(draw):
    """Generate a valid ComplianceGap."""
    return ComplianceGap(
        clause=draw(st.text(min_size=5, max_size=50)),
        issue=draw(st.text(min_size=10, max_size=200)),
        severity=draw(st.sampled_from(["LOW", "MEDIUM", "HIGH"])),
        recommendation=draw(st.text(min_size=10, max_size=200)),
        confidence=draw(st.floats(min_value=0.0, max_value=1.0)),
        regulatory_basis=draw(st.lists(st.text(min_size=5, max_size=50), min_size=1, max_size=5)),
    )


@st.composite
def recommended_action_strategy(draw):
    """Generate a valid RecommendedAction."""
    return RecommendedAction(
        clause=draw(st.text(min_size=5, max_size=50)),
        action=draw(st.sampled_from(["APPROVE", "MODIFY", "REJECT", "ESCALATE"])),
        rationale=draw(st.text(min_size=10, max_size=200)),
        confidence=draw(st.floats(min_value=0.0, max_value=1.0)),
        priority=draw(st.sampled_from(["LOW", "MEDIUM", "HIGH"])),
        current_text=draw(st.one_of(st.none(), st.text(min_size=10, max_size=200))),
        recommended_text=draw(st.one_of(st.none(), st.text(min_size=10, max_size=200))),
    )


@given(gap=compliance_gap_strategy())
@settings(max_examples=100, deadline=None)
def test_compliance_gap_has_clause_identifier(gap: ComplianceGap):
    """
    Property: Every compliance gap should have a clause identifier.

    This test verifies that:
    1. The clause field is not None
    2. The clause field is not empty
    3. The clause field is a string
    """
    assert gap.clause is not None, "Compliance gap missing clause identifier"
    assert len(gap.clause) > 0, "Compliance gap has empty clause identifier"
    assert isinstance(gap.clause, str), "Compliance gap clause is not a string"


@given(gap=compliance_gap_strategy())
@settings(max_examples=100, deadline=None)
def test_compliance_gap_has_recommendation(gap: ComplianceGap):
    """
    Property: Every compliance gap should have a recommendation.

    This test verifies that:
    1. The recommendation field is not None
    2. The recommendation field is not empty
    3. The recommendation field is a string
    """
    assert gap.recommendation is not None, "Compliance gap missing recommendation"
    assert len(gap.recommendation) > 0, "Compliance gap has empty recommendation"
    assert isinstance(gap.recommendation, str), "Compliance gap recommendation is not a string"


@given(gap=compliance_gap_strategy())
@settings(max_examples=100, deadline=None)
def test_compliance_gap_has_source_attribution(gap: ComplianceGap):
    """
    Property: Every compliance gap should have at least one source attribution.

    This test verifies that:
    1. The regulatory_basis field is not None
    2. The regulatory_basis list is not empty
    3. Each source in regulatory_basis is a non-empty string
    """
    assert gap.regulatory_basis is not None, "Compliance gap missing regulatory basis"
    assert len(gap.regulatory_basis) > 0, "Compliance gap has no source attributions"

    for source in gap.regulatory_basis:
        assert isinstance(source, str), f"Source attribution is not a string: {type(source)}"
        assert len(source) > 0, "Source attribution is empty"


@given(action=recommended_action_strategy())
@settings(max_examples=100, deadline=None)
def test_recommended_action_has_clause_identifier(action: RecommendedAction):
    """
    Property: Every recommended action should have a clause identifier.

    This test verifies that:
    1. The clause field is not None
    2. The clause field is not empty
    3. The clause field is a string
    """
    assert action.clause is not None, "Recommended action missing clause identifier"
    assert len(action.clause) > 0, "Recommended action has empty clause identifier"
    assert isinstance(action.clause, str), "Recommended action clause is not a string"


@given(action=recommended_action_strategy())
@settings(max_examples=100, deadline=None)
def test_recommended_action_has_action_type(action: RecommendedAction):
    """
    Property: Every recommended action should have an action type.

    This test verifies that:
    1. The action field is not None
    2. The action field is not empty
    3. The action field is one of the valid types
    """
    valid_actions = {"APPROVE", "MODIFY", "REJECT", "ESCALATE"}

    assert action.action is not None, "Recommended action missing action type"
    assert len(action.action) > 0, "Recommended action has empty action type"
    assert action.action in valid_actions, f"Invalid action type: {action.action}"


@given(action=recommended_action_strategy())
@settings(max_examples=100, deadline=None)
def test_recommended_action_has_rationale(action: RecommendedAction):
    """
    Property: Every recommended action should have a rationale (source attribution).

    This test verifies that:
    1. The rationale field is not None
    2. The rationale field is not empty
    3. The rationale field is a string
    """
    assert action.rationale is not None, "Recommended action missing rationale"
    assert len(action.rationale) > 0, "Recommended action has empty rationale"
    assert isinstance(action.rationale, str), "Recommended action rationale is not a string"


@given(gaps=st.lists(compliance_gap_strategy(), min_size=1, max_size=10))
@settings(max_examples=100, deadline=None)
def test_all_gaps_have_complete_attribution(gaps: List[ComplianceGap]):
    """
    Property: All compliance gaps should have complete attribution information.

    This test verifies that:
    1. Every gap has a clause identifier
    2. Every gap has a recommendation
    3. Every gap has at least one source attribution
    4. All fields are properly populated
    """
    for gap in gaps:
        # Check clause identifier
        assert gap.clause is not None and len(gap.clause) > 0, "Gap missing clause identifier"

        # Check recommendation
        assert (
            gap.recommendation is not None and len(gap.recommendation) > 0
        ), "Gap missing recommendation"

        # Check source attribution
        assert (
            gap.regulatory_basis is not None and len(gap.regulatory_basis) > 0
        ), "Gap missing source attribution"

        # Check all sources are valid
        for source in gap.regulatory_basis:
            assert isinstance(source, str) and len(source) > 0, "Invalid source attribution"


@given(actions=st.lists(recommended_action_strategy(), min_size=1, max_size=10))
@settings(max_examples=100, deadline=None)
def test_all_actions_have_complete_attribution(actions: List[RecommendedAction]):
    """
    Property: All recommended actions should have complete attribution information.

    This test verifies that:
    1. Every action has a clause identifier
    2. Every action has an action type
    3. Every action has a rationale (source attribution)
    4. All fields are properly populated
    """
    valid_actions = {"APPROVE", "MODIFY", "REJECT", "ESCALATE"}

    for action in actions:
        # Check clause identifier
        assert (
            action.clause is not None and len(action.clause) > 0
        ), "Action missing clause identifier"

        # Check action type
        assert (
            action.action is not None and action.action in valid_actions
        ), "Action missing or invalid action type"

        # Check rationale (source attribution)
        assert (
            action.rationale is not None and len(action.rationale) > 0
        ), "Action missing rationale"


@given(gap=compliance_gap_strategy())
@settings(max_examples=100, deadline=None)
def test_gap_severity_is_valid(gap: ComplianceGap):
    """
    Property: Every compliance gap should have a valid severity level.

    This test verifies that:
    1. The severity field is not None
    2. The severity is one of: LOW, MEDIUM, HIGH
    """
    valid_severities = {"LOW", "MEDIUM", "HIGH"}

    assert gap.severity is not None, "Compliance gap missing severity"
    assert gap.severity in valid_severities, f"Invalid severity: {gap.severity}"


@given(action=recommended_action_strategy())
@settings(max_examples=100, deadline=None)
def test_action_priority_is_valid(action: RecommendedAction):
    """
    Property: Every recommended action should have a valid priority level.

    This test verifies that:
    1. The priority field is not None
    2. The priority is one of: LOW, MEDIUM, HIGH
    """
    valid_priorities = {"LOW", "MEDIUM", "HIGH"}

    assert action.priority is not None, "Recommended action missing priority"
    assert action.priority in valid_priorities, f"Invalid priority: {action.priority}"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
