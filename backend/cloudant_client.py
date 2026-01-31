"""
Cloudant Client Wrapper
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

Wrapper for IBM Cloudant database operations with error handling and retry logic.
"""

import os
import time
from typing import List, Optional, Dict, Any
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from backend.models import GoldenClause, HistoricalDecision, RegulatoryMapping
import logging

logger = logging.getLogger(__name__)


class CloudantClient:
    """
    Cloudant database client with connection management and query methods.

    Provides methods for querying Golden Clauses, historical precedents,
    and regulatory mappings with built-in error handling and retry logic.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize Cloudant client.

        Args:
            url: Cloudant URL (defaults to CLOUDANT_URL env var)
            api_key: Cloudant API key (defaults to CLOUDANT_API_KEY env var)
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries in seconds
        """
        self.url = url or os.getenv("CLOUDANT_URL")
        self.api_key = api_key or os.getenv("CLOUDANT_API_KEY")
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        if not self.url or not self.api_key:
            raise ValueError(
                "Cloudant credentials required. Set CLOUDANT_URL and CLOUDANT_API_KEY "
                "environment variables or pass them to constructor."
            )

        # Database names
        self.db_golden_clauses = os.getenv("CLOUDANT_DB_GOLDEN_CLAUSES", "golden_clauses")
        self.db_historical_decisions = os.getenv(
            "CLOUDANT_DB_HISTORICAL_DECISIONS", "historical_decisions"
        )
        self.db_regulatory_mappings = os.getenv(
            "CLOUDANT_DB_REGULATORY_MAPPINGS", "regulatory_mappings"
        )

        # Initialize client
        authenticator = IAMAuthenticator(self.api_key)
        self.client = CloudantV1(authenticator=authenticator)
        self.client.set_service_url(self.url)

        logger.info(f"Cloudant client initialized: {self.url}")

    def _retry_operation(self, operation, *args, **kwargs):
        """
        Execute operation with retry logic.

        Args:
            operation: Function to execute
            *args: Positional arguments for operation
            **kwargs: Keyword arguments for operation

        Returns:
            Result of operation

        Raises:
            Exception: If all retries fail
        """
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return operation(*args, **kwargs)
            except Exception as e:
                last_exception = e
                error_msg = str(e).lower()

                # Don't retry on certain errors
                if "not found" in error_msg or "invalid" in error_msg:
                    raise

                # Retry on rate limiting or temporary errors
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)  # Exponential backoff
                    logger.warning(
                        f"Cloudant operation failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    logger.error(
                        f"Cloudant operation failed after {self.max_retries} attempts: {e}"
                    )

        raise last_exception

    def query_golden_clauses(
        self,
        contract_type: str,
        jurisdiction: Optional[str] = None,
        mandatory_only: bool = False,
        limit: int = 100,
    ) -> List[GoldenClause]:
        """
        Query Golden Clauses by contract type.

        Args:
            contract_type: Contract type to filter by
            jurisdiction: Optional jurisdiction filter
            mandatory_only: If True, return only mandatory clauses
            limit: Maximum number of results

        Returns:
            List of GoldenClause objects
        """

        def _query():
            # Build selector
            selector = {"contract_types": {"$elemMatch": {"$eq": contract_type}}}

            if jurisdiction:
                selector["jurisdiction"] = jurisdiction

            if mandatory_only:
                selector["mandatory"] = True

            # Execute query
            result = self.client.post_find(
                db=self.db_golden_clauses, selector=selector, limit=limit
            ).get_result()

            # Convert to GoldenClause objects
            clauses = []
            for doc in result.get("docs", []):
                try:
                    clause = GoldenClause(**doc)
                    clauses.append(clause)
                except Exception as e:
                    logger.warning(f"Failed to parse Golden Clause: {e}")

            logger.info(f"Retrieved {len(clauses)} Golden Clauses for {contract_type}")
            return clauses

        return self._retry_operation(_query)

    def get_precedents(
        self,
        contract_type: str,
        jurisdiction: Optional[str] = None,
        min_confidence: float = 0.0,
        limit: int = 10,
    ) -> List[HistoricalDecision]:
        """
        Get historical precedents for a contract type.

        Args:
            contract_type: Contract type to filter by
            jurisdiction: Optional jurisdiction filter
            min_confidence: Minimum confidence score
            limit: Maximum number of results

        Returns:
            List of HistoricalDecision objects sorted by confidence (descending)
        """

        def _query():
            # Build selector
            selector = {
                "contract_type": contract_type,
                "confidence": {"$gte": min_confidence},
            }

            if jurisdiction:
                selector["jurisdiction"] = jurisdiction

            # Execute query with sorting
            result = self.client.post_find(
                db=self.db_historical_decisions,
                selector=selector,
                sort=[{"confidence": "desc"}],
                limit=limit,
            ).get_result()

            # Convert to HistoricalDecision objects
            decisions = []
            for doc in result.get("docs", []):
                try:
                    decision = HistoricalDecision(**doc)
                    decisions.append(decision)
                except Exception as e:
                    logger.warning(f"Failed to parse Historical Decision: {e}")

            logger.info(
                f"Retrieved {len(decisions)} precedents for {contract_type} "
                f"(min confidence: {min_confidence})"
            )
            return decisions

        return self._retry_operation(_query)

    def store_precedent(self, decision: HistoricalDecision) -> str:
        """
        Store a new historical decision.

        Args:
            decision: HistoricalDecision object to store

        Returns:
            Document ID of stored decision
        """

        def _store():
            # Convert to dict
            doc = decision.model_dump(by_alias=True, exclude_none=True)

            # Remove _id and _rev if present (will be assigned by Cloudant)
            doc.pop("_id", None)
            doc.pop("_rev", None)

            # Store document
            result = self.client.post_document(
                db=self.db_historical_decisions, document=doc
            ).get_result()

            doc_id = result.get("id")
            logger.info(f"Stored precedent: {doc_id}")
            return doc_id

        return self._retry_operation(_store)

    def get_regulatory_mappings(
        self,
        jurisdiction: Optional[str] = None,
        regulation_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[RegulatoryMapping]:
        """
        Get regulatory mappings.

        Args:
            jurisdiction: Optional jurisdiction filter
            regulation_type: Optional regulation type filter
            limit: Maximum number of results

        Returns:
            List of RegulatoryMapping objects
        """

        def _query():
            # Build selector
            selector = {}

            if jurisdiction:
                selector["jurisdiction"] = jurisdiction

            if regulation_type:
                selector["regulation_type"] = regulation_type

            # If no filters, get all
            if not selector:
                selector = {"_id": {"$gt": None}}

            # Execute query
            result = self.client.post_find(
                db=self.db_regulatory_mappings, selector=selector, limit=limit
            ).get_result()

            # Convert to RegulatoryMapping objects
            mappings = []
            for doc in result.get("docs", []):
                try:
                    mapping = RegulatoryMapping(**doc)
                    mappings.append(mapping)
                except Exception as e:
                    logger.warning(f"Failed to parse Regulatory Mapping: {e}")

            logger.info(
                f"Retrieved {len(mappings)} regulatory mappings "
                f"(jurisdiction: {jurisdiction}, type: {regulation_type})"
            )
            return mappings

        return self._retry_operation(_query)

    def get_document_by_id(self, db_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID.

        Args:
            db_name: Database name
            doc_id: Document ID

        Returns:
            Document as dict or None if not found
        """

        def _get():
            try:
                result = self.client.get_document(db=db_name, doc_id=doc_id).get_result()
                return result
            except Exception as e:
                if "not found" in str(e).lower():
                    return None
                raise

        return self._retry_operation(_get)

    def health_check(self) -> Dict[str, Any]:
        """
        Check Cloudant connection health.

        Returns:
            Dict with health status
        """
        try:
            # Try to get server information
            info = self.client.get_server_information().get_result()

            # Check databases exist
            databases = {}
            for db_name in [
                self.db_golden_clauses,
                self.db_historical_decisions,
                self.db_regulatory_mappings,
            ]:
                try:
                    db_info = self.client.get_database_information(db=db_name).get_result()
                    databases[db_name] = {
                        "status": "ok",
                        "doc_count": db_info.get("doc_count", 0),
                    }
                except Exception as e:
                    databases[db_name] = {"status": "error", "error": str(e)}

            return {
                "status": "healthy",
                "version": info.get("version"),
                "databases": databases,
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# ============================================================================
# Singleton instance
# ============================================================================

_cloudant_client: Optional[CloudantClient] = None


def get_cloudant_client() -> CloudantClient:
    """
    Get singleton Cloudant client instance.

    Returns:
        CloudantClient instance
    """
    global _cloudant_client
    if _cloudant_client is None:
        _cloudant_client = CloudantClient()
    return _cloudant_client
