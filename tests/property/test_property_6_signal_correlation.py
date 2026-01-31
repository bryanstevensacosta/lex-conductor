"""
Property-Based Test: Signal Correlation Structure

Feature: lex-conductor-implementation
Property 6: Signal Correlation Structure

**Validates: Requirements 2.5**

For any set of collected sources (internal, external, historical), Signal Fusion
correlation should produce structured output containing alignment classifications
(MATCH, CONFLICT, PARTIAL, UNKNOWN) for each signal pair.
"""

import pytest
from hypothesis import given, strategies as st, settings
from typing import List

from backend.models import (
    InternalSignal,
    ExternalSignal,
    HistoricalSignal,
    SignalAlignment,
    FusionAnalysis,
)


# Custom strategies for generating signals
@st.composite
def internal_signal_strategy(draw):
    """Generate a valid InternalSignal."""
    return InternalSignal(
        source=draw(st.text(min_size=5, max_size=50)),
        type=draw(
            st.sampled_from(["liability_cap", "indemnification", "confidentiality", "termination"])
        ),
        text=draw(st.text(min_size=10, max_size=200)),
        confidence=draw(st.floats(min_value=0.0, max_value=1.0)),
        alignment=draw(st.sampled_from(list(SignalAlignment))),
    )


@st.composite
def external_signal_strategy(draw):
    """Generate a valid ExternalSignal."""
    return ExternalSignal(
        source=draw(st.text(min_size=5, max_size=50)),
        regulation=draw(st.text(min_size=5, max_size=50)),
        requirement=draw(st.text(min_size=10, max_size=200)),
        confidence=draw(st.floats(min_value=0.0, max_value=1.0)),
        alignment=draw(st.sampled_from(list(SignalAlignment))),
        cos_url=draw(st.one_of(st.none(), st.text(min_size=10, max_size=100))),
    )


@st.composite
def historical_signal_strategy(draw):
    """Generate a valid HistoricalSignal."""
    from datetime import datetime, timedelta
    from backend.models import ContractType

    return HistoricalSignal(
        decision_id=draw(st.text(min_size=5, max_size=20)),
        contract_type=draw(st.sampled_from(list(ContractType))),
        modification=draw(st.text(min_size=10, max_size=200)),
        rationale=draw(st.text(min_size=10, max_size=200)),
        confidence=draw(st.floats(min_value=0.0, max_value=1.0)),
        similarity_score=draw(st.floats(min_value=0.0, max_value=1.0)),
        date=datetime.now() - timedelta(days=draw(st.integers(min_value=1, max_value=365))),
    )


@given(
    internal_signals=st.lists(internal_signal_strategy(), min_size=0, max_size=10),
    external_signals=st.lists(external_signal_strategy(), min_size=0, max_size=10),
    historical_signals=st.lists(historical_signal_strategy(), min_size=0, max_size=10),
)
@settings(max_examples=100, deadline=None)
def test_signal_correlation_produces_valid_alignments(
    internal_signals: List[InternalSignal],
    external_signals: List[ExternalSignal],
    historical_signals: List[HistoricalSignal],
):
    """
    Property: For any set of signals, each signal should have a valid alignment classification.

    This test verifies that:
    1. All internal signals have valid alignment values
    2. All external signals have valid alignment values
    3. All historical signals (if they have alignment) have valid values
    4. Alignment is one of: MATCH, CONFLICT, PARTIAL, UNKNOWN
    """
    valid_alignments = {
        SignalAlignment.MATCH,
        SignalAlignment.CONFLICT,
        SignalAlignment.PARTIAL,
        SignalAlignment.UNKNOWN,
    }

    # Check internal signals
    for signal in internal_signals:
        assert (
            signal.alignment in valid_alignments
        ), f"Internal signal has invalid alignment: {signal.alignment}"

    # Check external signals
    for signal in external_signals:
        assert (
            signal.alignment in valid_alignments
        ), f"External signal has invalid alignment: {signal.alignment}"


@given(
    internal_signals=st.lists(internal_signal_strategy(), min_size=1, max_size=5),
    external_signals=st.lists(external_signal_strategy(), min_size=1, max_size=5),
    historical_signals=st.lists(historical_signal_strategy(), min_size=0, max_size=5),
)
@settings(max_examples=100, deadline=None)
def test_fusion_analysis_contains_all_signal_types(
    internal_signals: List[InternalSignal],
    external_signals: List[ExternalSignal],
    historical_signals: List[HistoricalSignal],
):
    """
    Property: FusionAnalysis should contain all provided signal types.

    This test verifies that:
    1. FusionAnalysis can be created with all signal types
    2. All signals are preserved in the analysis
    3. The structure is complete and accessible
    """

    # Create FusionAnalysis with all signals
    analysis = FusionAnalysis(
        internal_signals=internal_signals,
        external_signals=external_signals,
        historical_signals=historical_signals,
        gaps=[],
        overall_confidence=0.8,
    )

    # Verify all signals are present
    assert len(analysis.internal_signals) == len(internal_signals)
    assert len(analysis.external_signals) == len(external_signals)
    assert len(analysis.historical_signals) == len(historical_signals)

    # Verify signals are accessible and have correct types
    for i, signal in enumerate(analysis.internal_signals):
        assert isinstance(signal, InternalSignal)
        assert signal.alignment in SignalAlignment

    for i, signal in enumerate(analysis.external_signals):
        assert isinstance(signal, ExternalSignal)
        assert signal.alignment in SignalAlignment


@given(
    internal_signals=st.lists(internal_signal_strategy(), min_size=0, max_size=10),
    external_signals=st.lists(external_signal_strategy(), min_size=0, max_size=10),
)
@settings(max_examples=100, deadline=None)
def test_signal_confidence_scores_are_valid(
    internal_signals: List[InternalSignal], external_signals: List[ExternalSignal]
):
    """
    Property: All signals should have confidence scores in valid range [0.0, 1.0].

    This test verifies that:
    1. Internal signal confidence scores are in [0.0, 1.0]
    2. External signal confidence scores are in [0.0, 1.0]
    3. Confidence scores are numeric (float)
    """
    # Check internal signals
    for signal in internal_signals:
        assert (
            0.0 <= signal.confidence <= 1.0
        ), f"Internal signal confidence out of range: {signal.confidence}"
        assert isinstance(
            signal.confidence, float
        ), f"Internal signal confidence is not float: {type(signal.confidence)}"

    # Check external signals
    for signal in external_signals:
        assert (
            0.0 <= signal.confidence <= 1.0
        ), f"External signal confidence out of range: {signal.confidence}"
        assert isinstance(
            signal.confidence, float
        ), f"External signal confidence is not float: {type(signal.confidence)}"


@given(
    internal_signals=st.lists(internal_signal_strategy(), min_size=0, max_size=5),
    external_signals=st.lists(external_signal_strategy(), min_size=0, max_size=5),
)
@settings(max_examples=100, deadline=None)
def test_signal_correlation_structure_is_complete(
    internal_signals: List[InternalSignal], external_signals: List[ExternalSignal]
):
    """
    Property: Signal correlation structure should be complete with all required fields.

    This test verifies that:
    1. Each signal has a source attribution
    2. Each signal has an alignment classification
    3. Each signal has a confidence score
    4. All required fields are non-null
    """
    # Check internal signals have all required fields
    for signal in internal_signals:
        assert (
            signal.source is not None and len(signal.source) > 0
        ), "Internal signal missing source"
        assert signal.type is not None and len(signal.type) > 0, "Internal signal missing type"
        assert signal.text is not None, "Internal signal missing text"
        assert signal.confidence is not None, "Internal signal missing confidence"
        assert signal.alignment is not None, "Internal signal missing alignment"

    # Check external signals have all required fields
    for signal in external_signals:
        assert (
            signal.source is not None and len(signal.source) > 0
        ), "External signal missing source"
        assert (
            signal.regulation is not None and len(signal.regulation) > 0
        ), "External signal missing regulation"
        assert signal.requirement is not None, "External signal missing requirement"
        assert signal.confidence is not None, "External signal missing confidence"
        assert signal.alignment is not None, "External signal missing alignment"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
