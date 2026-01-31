"""
Cloud Object Storage Client Wrapper
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

Wrapper for IBM Cloud Object Storage operations with caching and error handling.
"""

import os
import io
import time
from typing import List, Optional, Dict, Any
import ibm_boto3
from ibm_botocore.client import Config
from ibm_botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class COSClient:
    """
    Cloud Object Storage client with S3-compatible API.

    Provides methods for retrieving regulatory documents with caching
    for frequently accessed files.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        instance_id: Optional[str] = None,
        endpoint: Optional[str] = None,
        bucket_name: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        cache_ttl: int = 3600,  # 1 hour cache TTL
    ):
        """
        Initialize COS client.

        Args:
            api_key: IBM Cloud API key (defaults to COS_API_KEY env var)
            instance_id: COS instance ID (defaults to COS_INSTANCE_ID env var)
            endpoint: COS endpoint (defaults to COS_ENDPOINT env var)
            bucket_name: Bucket name (defaults to COS_BUCKET_NAME env var)
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries in seconds
            cache_ttl: Cache time-to-live in seconds
        """
        self.api_key = api_key or os.getenv("COS_API_KEY")
        self.instance_id = instance_id or os.getenv("COS_INSTANCE_ID")
        self.endpoint = endpoint or os.getenv("COS_ENDPOINT")
        self.bucket_name = bucket_name or os.getenv("COS_BUCKET_NAME")
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.cache_ttl = cache_ttl

        if not all([self.api_key, self.instance_id, self.endpoint, self.bucket_name]):
            raise ValueError(
                "COS credentials required. Set COS_API_KEY, COS_INSTANCE_ID, "
                "COS_ENDPOINT, and COS_BUCKET_NAME environment variables."
            )

        # Initialize S3 client
        self.client = ibm_boto3.client(
            "s3",
            ibm_api_key_id=self.api_key,
            ibm_service_instance_id=self.instance_id,
            config=Config(signature_version="oauth"),
            endpoint_url=f"https://{self.endpoint}",
        )

        # Cache for frequently accessed documents
        self._cache: Dict[str, Dict[str, Any]] = {}

        logger.info(f"COS client initialized: {self.endpoint}/{self.bucket_name}")

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
            except ClientError as e:
                last_exception = e
                error_code = e.response.get("Error", {}).get("Code", "")

                # Don't retry on certain errors
                if error_code in ["NoSuchKey", "NoSuchBucket", "InvalidArgument"]:
                    raise

                # Retry on rate limiting or temporary errors
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)  # Exponential backoff
                    logger.warning(
                        f"COS operation failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    logger.error(f"COS operation failed after {self.max_retries} attempts: {e}")
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    logger.warning(
                        f"COS operation failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    logger.error(f"COS operation failed after {self.max_retries} attempts: {e}")

        raise last_exception

    def _get_from_cache(self, key: str) -> Optional[str]:
        """
        Get document from cache if available and not expired.

        Args:
            key: Cache key

        Returns:
            Cached content or None if not found/expired
        """
        if key in self._cache:
            cached = self._cache[key]
            if time.time() - cached["timestamp"] < self.cache_ttl:
                logger.debug(f"Cache hit: {key}")
                return cached["content"]
            else:
                # Expired, remove from cache
                del self._cache[key]
                logger.debug(f"Cache expired: {key}")
        return None

    def _add_to_cache(self, key: str, content: str):
        """
        Add document to cache.

        Args:
            key: Cache key
            content: Content to cache
        """
        self._cache[key] = {"content": content, "timestamp": time.time()}
        logger.debug(f"Cached: {key}")

    def get_regulation(
        self, jurisdiction: str, regulation_name: str, use_cache: bool = True
    ) -> Optional[str]:
        """
        Get regulatory document content.

        Args:
            jurisdiction: Jurisdiction folder (e.g., "US", "EU", "UK")
            regulation_name: Regulation file name
            use_cache: Whether to use cache

        Returns:
            Document content as string or None if not found
        """
        # Construct object key
        object_key = f"{jurisdiction}/{regulation_name}"

        # Check cache first
        if use_cache:
            cached = self._get_from_cache(object_key)
            if cached is not None:
                return cached

        def _get():
            try:
                # Get object from COS
                response = self.client.get_object(Bucket=self.bucket_name, Key=object_key)

                # Read content
                content = response["Body"].read()

                # Decode based on content type
                content_type = response.get("ContentType", "")
                if "text" in content_type or regulation_name.endswith(".txt"):
                    text_content = content.decode("utf-8")
                else:
                    # For PDF or other binary formats, return as-is
                    # (caller should use extract_text_from_pdf if needed)
                    text_content = content.decode("utf-8", errors="ignore")

                # Cache the content
                if use_cache:
                    self._add_to_cache(object_key, text_content)

                logger.info(f"Retrieved regulation: {object_key}")
                return text_content

            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code", "")
                if error_code == "NoSuchKey":
                    logger.warning(f"Regulation not found: {object_key}")
                    return None
                raise

        return self._retry_operation(_get)

    def list_regulations(
        self, jurisdiction: Optional[str] = None, prefix: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List regulatory documents in bucket.

        Args:
            jurisdiction: Optional jurisdiction filter
            prefix: Optional prefix filter

        Returns:
            List of objects with metadata
        """

        def _list():
            # Determine prefix
            list_prefix = prefix or ""
            if jurisdiction:
                list_prefix = f"{jurisdiction}/"

            # List objects
            response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=list_prefix)

            # Extract object metadata
            objects = []
            for obj in response.get("Contents", []):
                objects.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                        "etag": obj["ETag"],
                    }
                )

            logger.info(f"Listed {len(objects)} regulations (prefix: {list_prefix})")
            return objects

        return self._retry_operation(_list)

    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF content.

        Note: For hackathon, we're using placeholder text files instead of PDFs.
        This method is included for completeness but may not be used.

        Args:
            pdf_content: PDF file content as bytes

        Returns:
            Extracted text
        """
        try:
            import PyPDF2

            # Create PDF reader from bytes
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extract text from all pages
            text_parts = []
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())

            text = "\n\n".join(text_parts)
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text

        except ImportError:
            logger.error("PyPDF2 not installed. Install with: pip install PyPDF2")
            raise
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise

    def get_regulation_text(
        self, jurisdiction: str, regulation_name: str, use_cache: bool = True
    ) -> Optional[str]:
        """
        Get regulatory document text (handles both text and PDF files).

        Args:
            jurisdiction: Jurisdiction folder
            regulation_name: Regulation file name
            use_cache: Whether to use cache

        Returns:
            Document text or None if not found
        """
        # Get raw content
        content = self.get_regulation(jurisdiction, regulation_name, use_cache)

        if content is None:
            return None

        # If it's a PDF, extract text
        if regulation_name.lower().endswith(".pdf"):
            try:
                return self.extract_text_from_pdf(content.encode("latin-1"))
            except Exception as e:
                logger.error(f"Failed to extract PDF text: {e}")
                return None

        # Otherwise return as-is
        return content

    def health_check(self) -> Dict[str, Any]:
        """
        Check COS connection health.

        Returns:
            Dict with health status
        """
        try:
            # Try to list objects (limit to 1)
            response = self.client.list_objects_v2(Bucket=self.bucket_name, MaxKeys=1)

            # Get bucket info
            bucket_info = {
                "name": self.bucket_name,
                "object_count": response.get("KeyCount", 0),
                "is_truncated": response.get("IsTruncated", False),
            }

            return {
                "status": "healthy",
                "bucket": bucket_info,
                "cache_size": len(self._cache),
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def clear_cache(self):
        """Clear the document cache."""
        self._cache.clear()
        logger.info("Cache cleared")


# ============================================================================
# Singleton instance
# ============================================================================

_cos_client: Optional[COSClient] = None


def get_cos_client() -> COSClient:
    """
    Get singleton COS client instance.

    Returns:
        COSClient instance
    """
    global _cos_client
    if _cos_client is None:
        _cos_client = COSClient()
    return _cos_client
