"""
Property Test 18: Precedent Persistence Round-Trip
Feature: lex-conductor-implementation
Validates: Requirements 5.6

For any historical precedent stored in Cloudant, retrieving it by decision ID
should return an equivalent object with all metadata intact.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from backend.models import HistoricalDecision
from backend.cloudant_client import CloudantClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Skip tests if Cloudant credentials not available
pytestmark = pytest.mark.skipif(
    not os.getenv("CLOUDANT_URL") or not os.getenv("CLOUDANT_API_KEY"),
    reason="Cloudant credentials not configured",
)


# ============================================================================
# Hypothesis Strategies
# ============================================================================


@st.composite
def historical_decision_strategy(draw):
    """Generate valid HistoricalDecision objects"""
    contract_types = [
        "NDA",
        "MSA",
        "Service Agreement",
        "Employment Agreement",
        "License Agreement",
    ]
    jurisdictions = ["US", "EU", "UK", "Multi-Jurisdiction"]

    decision_id = f"test_dec_{draw(st.integers(min_value=1000, max_value=9999))}"

    return HistoricalDecision(
        decision_id=decision_id,
        contract_type=draw(st.sampled_from(contract_types)),
        contract_id=f"contract_{draw(st.integers(min_value=100, max_value=999))}",
        clause_modified=draw(
            st.text(
                min_size=5,
                max_size=50,
                alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd", "P", "Zs")),
            )
        ),
        original_text=draw(
            st.text(
                min_size=20,
                max_size=200,
                alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd", "P", "Zs")),
            )
        ),
        modified_text=draw(
            st.text(
                min_size=20,
                max_size=200,
                alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd", "P", "Zs")),
            )
        ),
        rationale=draw(
            st.text(
                min_size=20,
                max_size=200,
                alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd", "P", "Zs")),
            )
        ),
        approved_by=draw(
            st.text(
                min_size=5,
                max_size=50,
                alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Zs")),
            )
        ),
        date=datetime.now().isoformat(),
        jurisdiction=draw(st.sampled_from(jurisdictions)),
        confidence=draw(
            st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
        ),
        tags=draw(
            st.lists(
                st.text(
                    min_size=3,
                    max_size=20,
                    alphabet=st.characters(whitelist_categories=("Ll", "Nd")),
                ),
                min_size=0,
                max_size=5,
            )
        ),
        regulatory_basis=draw(
            st.lists(
                st.text(
                    min_size=3,
                    max_size=30,
                    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd", "P")),
                ),
                min_size=0,
                max_size=3,
            )
        ),
    )


# ============================================================================
# Property Tests
# ============================================================================


class TestProperty18PrecedentPersistence:
    """
    Property 18: Precedent Persistence Round-Trip

    For any historical precedent, storing and retrieving should return
    an equivalent object with all metadata intact.
    """

    @pytest.fixture(scope="class")
    def cloudant_client(self):
        """Create Cloudant client for tests"""
        try:
            client = CloudantClient()
            # Verify connection
            health = client.health_check()
            if health["status"] != "healthy":
                pytest.skip("Cloudant not healthy")
            return client
        except Exception as e:
            pytest.skip(f"Could not connect to Cloudant: {e}")

    @given(decision=historical_decision_strategy())
    @settings(max_examples=20, deadline=10000)  # Reduced examples for DB operations
    def test_store_and_retrieve_precedent(self, cloudant_client, decision):
        """
        Property: Storing and retrieving a precedent returns equivalent data
        """
        # Ensure decision_id is unique for this test
        decision.decision_id = f"prop18_test_{decision.decision_id}_{datetime.now().timestamp()}"

        try:
            # Store the precedent
            doc_id = cloudant_client.store_precedent(decision)
            assert doc_id is not None, "Document ID should be returned"

            # Retrieve by querying (since we don't have direct get by decision_id)
            retrieved_decisions = cloudant_client.get_precedents(
                contract_type=decision.contract_type,
                jurisdiction=decision.jurisdiction,
                limit=100,
            )

            # Find our decision in the results
            retrieved = None
            for d in retrieved_decisions:
                if d.decision_id == decision.decision_id:
                    retrieved = d
                    break

            assert retrieved is not None, f"Should retrieve stored decision {decision.decision_id}"

            # Verify all fields match (excluding _id and _rev which are added by Cloudant)
            assert retrieved.decision_id == decision.decision_id
            assert retrieved.contract_type == decision.contract_type
            assert retrieved.contract_id == decision.contract_id
            assert retrieved.clause_modified == decision.clause_modified
            assert retrieved.original_text == decision.original_text
            assert retrieved.modified_text == decision.modified_text
            assert retrieved.rationale == decision.rationale
            assert retrieved.approved_by == decision.approved_by
            assert retrieved.jurisdiction == decision.jurisdiction
            assert abs(retrieved.confidence - decision.confidence) < 0.0001  # Float comparison
            assert set(retrieved.tags) == set(decision.tags)
            assert set(retrieved.regulatory_basis) == set(decision.regulatory_basis)

        except Exception as e:
            # If rate limited, skip this example
            if "rate" in str(e).lower() or "429" in str(e):
                assume(False)  # Skip this example
            raise

    def test_store_retrieve_specific_example(self, cloudant_client):
        """Test with a specific known example"""
        decision = HistoricalDecision(
            decision_id=f"test_specific_{datetime.now().timestamp()}",
            contract_type="NDA",
            contract_id="contract_test_001",
            clause_modified="Section 4 - Confidentiality",
            original_text="Party A shall keep information confidential.",
            modified_text="Party A shall keep information confidential for 5 years.",
            rationale="Added specific time period for clarity",
            approved_by="Test Approver",
            date=datetime.now().isoformat(),
            jurisdiction="US",
            confidence=0.95,
            tags=["confidentiality", "term"],
            regulatory_basis=["Best Practice"],
        )

        # Store
        doc_id = cloudant_client.store_precedent(decision)
        assert doc_id is not None

        # Retrieve
        retrieved_decisions = cloudant_client.get_precedents(
            contract_type="NDA", jurisdiction="US", limit=100
        )

        # Find our decision
        retrieved = None
        for d in retrieved_decisions:
            if d.decision_id == decision.decision_id:
                retrieved = d
                break

        assert retrieved is not None
        assert retrieved.decision_id == decision.decision_id
        assert retrieved.confidence == 0.95
        assert "confidentiality" in retrieved.tags

    def test_retrieve_with_filters(self, cloudant_client):
        """Test that filtering works correctly"""
        # Store a test decision
        decision = HistoricalDecision(
            decision_id=f"test_filter_{datetime.now().timestamp()}",
            contract_type="MSA",
            contract_id="contract_filter_001",
            clause_modified="Section 1",
            original_text="Original text",
            modified_text="Modified text",
            rationale="Test rationale",
            approved_by="Test Approver",
            date=datetime.now().isoformat(),
            jurisdiction="EU",
            confidence=0.88,
            tags=["test"],
            regulatory_basis=[],
        )

        doc_id = cloudant_client.store_precedent(decision)
        assert doc_id is not None

        # Retrieve with matching filters
        results = cloudant_client.get_precedents(
            contract_type="MSA", jurisdiction="EU", min_confidence=0.85, limit=100
        )

        # Should find our decision
        found = any(d.decision_id == decision.decision_id for d in results)
        assert found, "Should find decision with matching filters"

        # Retrieve with non-matching confidence filter
        results_high_conf = cloudant_client.get_precedents(
            contract_type="MSA", jurisdiction="EU", min_confidence=0.95, limit=100
        )

        # Should not find our decision (confidence is 0.88)
        found_high = any(d.decision_id == decision.decision_id for d in results_high_conf)
        assert not found_high, "Should not find decision with higher confidence filter"

    def test_confidence_score_preserved(self, cloudant_client):
        """Test that confidence scores are preserved exactly"""
        test_confidences = [0.0, 0.25, 0.5, 0.75, 0.88, 0.95, 1.0]

        for conf in test_confidences:
            decision = HistoricalDecision(
                decision_id=f"test_conf_{conf}_{datetime.now().timestamp()}",
                contract_type="NDA",
                contract_id="contract_conf_001",
                clause_modified="Section 1",
                original_text="Original",
                modified_text="Modified",
                rationale="Test",
                approved_by="Tester",
                date=datetime.now().isoformat(),
                jurisdiction="US",
                confidence=conf,
                tags=[],
                regulatory_basis=[],
            )

            # Store
            doc_id = cloudant_client.store_precedent(decision)
            assert doc_id is not None

            # Retrieve
            results = cloudant_client.get_precedents(
                contract_type="NDA", jurisdiction="US", limit=100
            )

            # Find and verify
            retrieved = None
            for d in results:
                if d.decision_id == decision.decision_id:
                    retrieved = d
                    break

            assert retrieved is not None
            assert (
                abs(retrieved.confidence - conf) < 0.0001
            ), f"Confidence {conf} should be preserved"


# ============================================================================
# Integration Tests
# ============================================================================


class TestCloudantIntegration:
    """Integration tests for Cloudant client"""

    @pytest.fixture(scope="class")
    def cloudant_client(self):
        """Create Cloudant client for tests"""
        try:
            return CloudantClient()
        except Exception as e:
            pytest.skip(f"Could not connect to Cloudant: {e}")

    def test_query_golden_clauses(self, cloudant_client):
        """Test querying Golden Clauses"""
        clauses = cloudant_client.query_golden_clauses(contract_type="NDA", limit=10)

        assert isinstance(clauses, list)
        # Should have some clauses (we populated them earlier)
        assert len(clauses) > 0

        # Verify structure
        for clause in clauses:
            assert hasattr(clause, "clause_id")
            assert hasattr(clause, "text")
            assert "NDA" in clause.contract_types

    def test_get_regulatory_mappings(self, cloudant_client):
        """Test getting regulatory mappings"""
        mappings = cloudant_client.get_regulatory_mappings(jurisdiction="US", limit=10)

        assert isinstance(mappings, list)
        assert len(mappings) > 0

        # Verify structure
        for mapping in mappings:
            assert hasattr(mapping, "regulation_id")
            assert hasattr(mapping, "regulation_name")
            assert mapping.jurisdiction == "US"

    def test_health_check(self, cloudant_client):
        """Test health check"""
        health = cloudant_client.health_check()

        assert "status" in health
        assert health["status"] in ["healthy", "unhealthy"]

        if health["status"] == "healthy":
            assert "databases" in health
            assert "golden_clauses" in health["databases"]
            assert "historical_decisions" in health["databases"]
            assert "regulatory_mappings" in health["databases"]
