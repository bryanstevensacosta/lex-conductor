"""
Property Test 10: Confidence Score Validity
Feature: lex-conductor-implementation
Validates: Requirements 3.5

For any recommendation in a Legal Logic Trace, the confidence score should be
a number in the range [0.0, 1.0].
"""

import pytest
from hypothesis import given, strategies as st, settings
from backend.models import (
    InternalSignal,
    ExternalSignal,
    HistoricalSignal,
    ComplianceGap,
    RecommendedAction,
    HistoricalDecision,
    SignalAlignment,
    SeverityLevel,
    ContractType,
)
from datetime import datetime
from pydantic import ValidationError

# ============================================================================
# Hypothesis Strategies
# ============================================================================


@st.composite
def valid_confidence_score(draw):
    """Generate valid confidence scores between 0.0 and 1.0"""
    return draw(st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False))


@st.composite
def invalid_confidence_score(draw):
    """Generate invalid confidence scores outside [0.0, 1.0]"""
    return draw(
        st.one_of(
            st.floats(min_value=-100.0, max_value=-0.01),  # Negative
            st.floats(min_value=1.01, max_value=100.0),  # > 1.0
            st.just(float("inf")),  # Infinity
            st.just(float("-inf")),  # Negative infinity
        )
    )


# ============================================================================
# Property Tests
# ============================================================================


class TestProperty10ConfidenceScoreValidity:
    """
    Property 10: Confidence Score Validity

    For any model with a confidence score field, the score must be in [0.0, 1.0].
    """

    @given(confidence=valid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_internal_signal_valid_confidence(self, confidence):
        """InternalSignal accepts valid confidence scores"""
        signal = InternalSignal(
            source="Test Source",
            type="test_type",
            text="Test text",
            confidence=confidence,
            alignment=SignalAlignment.MATCH,
        )
        assert 0.0 <= signal.confidence <= 1.0

    @given(confidence=invalid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_internal_signal_invalid_confidence(self, confidence):
        """InternalSignal rejects invalid confidence scores"""
        with pytest.raises(ValidationError) as exc_info:
            InternalSignal(
                source="Test Source",
                type="test_type",
                text="Test text",
                confidence=confidence,
                alignment=SignalAlignment.MATCH,
            )
        assert "confidence" in str(exc_info.value).lower()

    @given(confidence=valid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_external_signal_valid_confidence(self, confidence):
        """ExternalSignal accepts valid confidence scores"""
        signal = ExternalSignal(
            source="Test Regulation",
            regulation="Test Reg",
            requirement="Test requirement",
            confidence=confidence,
            alignment=SignalAlignment.MATCH,
        )
        assert 0.0 <= signal.confidence <= 1.0

    @given(confidence=invalid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_external_signal_invalid_confidence(self, confidence):
        """ExternalSignal rejects invalid confidence scores"""
        with pytest.raises(ValidationError) as exc_info:
            ExternalSignal(
                source="Test Regulation",
                regulation="Test Reg",
                requirement="Test requirement",
                confidence=confidence,
                alignment=SignalAlignment.MATCH,
            )
        assert "confidence" in str(exc_info.value).lower()

    @given(confidence=valid_confidence_score(), similarity=valid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_historical_signal_valid_scores(self, confidence, similarity):
        """HistoricalSignal accepts valid confidence and similarity scores"""
        signal = HistoricalSignal(
            decision_id="test_001",
            contract_type=ContractType.NDA,
            modification="Test modification",
            rationale="Test rationale",
            confidence=confidence,
            similarity_score=similarity,
            date=datetime.now(),
        )
        assert 0.0 <= signal.confidence <= 1.0
        assert 0.0 <= signal.similarity_score <= 1.0

    @given(confidence=invalid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_historical_signal_invalid_confidence(self, confidence):
        """HistoricalSignal rejects invalid confidence scores"""
        with pytest.raises(ValidationError) as exc_info:
            HistoricalSignal(
                decision_id="test_001",
                contract_type=ContractType.NDA,
                modification="Test modification",
                rationale="Test rationale",
                confidence=confidence,
                similarity_score=0.5,
                date=datetime.now(),
            )
        # Should fail validation
        assert exc_info.value is not None

    @given(confidence=valid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_compliance_gap_valid_confidence(self, confidence):
        """ComplianceGap accepts valid confidence scores"""
        gap = ComplianceGap(
            clause="Section 1",
            issue="Test issue",
            severity=SeverityLevel.MEDIUM,
            recommendation="Test recommendation",
            confidence=confidence,
        )
        assert 0.0 <= gap.confidence <= 1.0

    @given(confidence=invalid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_compliance_gap_invalid_confidence(self, confidence):
        """ComplianceGap rejects invalid confidence scores"""
        with pytest.raises(ValidationError) as exc_info:
            ComplianceGap(
                clause="Section 1",
                issue="Test issue",
                severity=SeverityLevel.MEDIUM,
                recommendation="Test recommendation",
                confidence=confidence,
            )
        assert exc_info.value is not None

    @given(confidence=valid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_recommended_action_valid_confidence(self, confidence):
        """RecommendedAction accepts valid confidence scores"""
        action = RecommendedAction(
            clause="Section 1",
            action="MODIFY",
            rationale="Test rationale",
            confidence=confidence,
            priority="MEDIUM",
        )
        assert 0.0 <= action.confidence <= 1.0

    @given(confidence=invalid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_recommended_action_invalid_confidence(self, confidence):
        """RecommendedAction rejects invalid confidence scores"""
        with pytest.raises(ValidationError) as exc_info:
            RecommendedAction(
                clause="Section 1",
                action="MODIFY",
                rationale="Test rationale",
                confidence=confidence,
                priority="MEDIUM",
            )
        assert exc_info.value is not None

    @given(confidence=valid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_historical_decision_valid_confidence(self, confidence):
        """HistoricalDecision accepts valid confidence scores"""
        decision = HistoricalDecision(
            decision_id="dec_001",
            contract_type="NDA",
            contract_id="contract_001",
            clause_modified="Section 1",
            original_text="Original",
            modified_text="Modified",
            rationale="Test rationale",
            approved_by="Test Approver",
            date=datetime.now().isoformat(),
            jurisdiction="US",
            confidence=confidence,
        )
        assert 0.0 <= decision.confidence <= 1.0

    @given(confidence=invalid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_historical_decision_invalid_confidence(self, confidence):
        """HistoricalDecision rejects invalid confidence scores"""
        with pytest.raises(ValidationError) as exc_info:
            HistoricalDecision(
                decision_id="dec_001",
                contract_type="NDA",
                contract_id="contract_001",
                clause_modified="Section 1",
                original_text="Original",
                modified_text="Modified",
                rationale="Test rationale",
                approved_by="Test Approver",
                date=datetime.now().isoformat(),
                jurisdiction="US",
                confidence=confidence,
            )
        assert exc_info.value is not None

    @given(confidence=valid_confidence_score())
    @settings(max_examples=100, deadline=5000)
    def test_boundary_values(self, confidence):
        """Test that boundary values 0.0 and 1.0 are accepted"""
        # Test with exact boundaries
        for boundary in [0.0, 1.0]:
            signal = InternalSignal(
                source="Test",
                type="test",
                text="Test",
                confidence=boundary,
                alignment=SignalAlignment.MATCH,
            )
            assert signal.confidence == boundary

        # Test with generated value
        signal = InternalSignal(
            source="Test",
            type="test",
            text="Test",
            confidence=confidence,
            alignment=SignalAlignment.MATCH,
        )
        assert 0.0 <= signal.confidence <= 1.0


# ============================================================================
# Edge Case Tests
# ============================================================================


class TestConfidenceScoreEdgeCases:
    """Test edge cases for confidence score validation"""

    def test_exact_zero(self):
        """Test that exactly 0.0 is valid"""
        signal = InternalSignal(
            source="Test",
            type="test",
            text="Test",
            confidence=0.0,
            alignment=SignalAlignment.MATCH,
        )
        assert signal.confidence == 0.0

    def test_exact_one(self):
        """Test that exactly 1.0 is valid"""
        signal = InternalSignal(
            source="Test",
            type="test",
            text="Test",
            confidence=1.0,
            alignment=SignalAlignment.MATCH,
        )
        assert signal.confidence == 1.0

    def test_slightly_below_zero(self):
        """Test that -0.01 is invalid"""
        with pytest.raises(ValidationError):
            InternalSignal(
                source="Test",
                type="test",
                text="Test",
                confidence=-0.01,
                alignment=SignalAlignment.MATCH,
            )

    def test_slightly_above_one(self):
        """Test that 1.01 is invalid"""
        with pytest.raises(ValidationError):
            InternalSignal(
                source="Test",
                type="test",
                text="Test",
                confidence=1.01,
                alignment=SignalAlignment.MATCH,
            )

    def test_nan_rejected(self):
        """Test that NaN is rejected"""
        with pytest.raises(ValidationError):
            InternalSignal(
                source="Test",
                type="test",
                text="Test",
                confidence=float("nan"),
                alignment=SignalAlignment.MATCH,
            )

    def test_infinity_rejected(self):
        """Test that infinity is rejected"""
        with pytest.raises(ValidationError):
            InternalSignal(
                source="Test",
                type="test",
                text="Test",
                confidence=float("inf"),
                alignment=SignalAlignment.MATCH,
            )

    def test_negative_infinity_rejected(self):
        """Test that negative infinity is rejected"""
        with pytest.raises(ValidationError):
            InternalSignal(
                source="Test",
                type="test",
                text="Test",
                confidence=float("-inf"),
                alignment=SignalAlignment.MATCH,
            )
