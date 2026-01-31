"""
watsonx.ai Client Wrapper
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

Wrapper for IBM watsonx.ai foundation model inference with retry logic and token tracking.
"""

import os
import time
from typing import Optional, Dict, Any, List
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
import logging

logger = logging.getLogger(__name__)


class WatsonxClient:
    """
    watsonx.ai client for Granite model inference.

    Provides methods for text generation with built-in retry logic,
    error handling, and token usage tracking.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        url: Optional[str] = None,
        model_id: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize watsonx.ai client.

        Args:
            api_key: IBM Cloud API key (defaults to WATSONX_API_KEY env var)
            project_id: watsonx.ai project ID (defaults to WATSONX_PROJECT_ID env var)
            url: watsonx.ai URL (defaults to WATSONX_URL env var)
            model_id: Model ID (defaults to WATSONX_MODEL_ID env var or granite-3-8b-instruct)
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries in seconds
        """
        self.api_key = api_key or os.getenv("WATSONX_API_KEY")
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
        self.url = url or os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.model_id = model_id or os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-8b-instruct")
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        if not all([self.api_key, self.project_id]):
            raise ValueError(
                "watsonx.ai credentials required. Set WATSONX_API_KEY and "
                "WATSONX_PROJECT_ID environment variables."
            )

        # Initialize API client
        credentials = Credentials(api_key=self.api_key, url=self.url)

        self.api_client = APIClient(credentials)
        self.api_client.set.default_project(self.project_id)

        # Token usage tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0

        logger.info(f"watsonx.ai client initialized: {self.model_id}")

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
                if (
                    "invalid" in error_msg
                    or "unauthorized" in error_msg
                    or "forbidden" in error_msg
                ):
                    logger.error(f"Non-retryable error: {e}")
                    raise

                # Retry on rate limiting or temporary errors
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)  # Exponential backoff
                    logger.warning(
                        f"watsonx.ai operation failed (attempt {attempt + 1}/{self.max_retries}): {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    logger.error(
                        f"watsonx.ai operation failed after {self.max_retries} attempts: {e}"
                    )

        raise last_exception

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        return_options: Optional[Dict[str, bool]] = None,
    ) -> Dict[str, Any]:
        """
        Generate text using watsonx.ai foundation model.

        Args:
            prompt: Input prompt text
            max_tokens: Maximum tokens to generate (default from env or 2000)
            temperature: Sampling temperature (default from env or 0.1)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            repetition_penalty: Repetition penalty
            stop_sequences: List of stop sequences
            return_options: Options for what to return (input_text, generated_tokens, etc.)

        Returns:
            Dict with generated text and metadata:
            {
                'text': str,  # Generated text
                'input_tokens': int,  # Number of input tokens
                'output_tokens': int,  # Number of output tokens
                'stop_reason': str,  # Why generation stopped
                'model_id': str  # Model used
            }
        """
        # Set defaults from environment or hardcoded
        max_tokens = max_tokens or int(os.getenv("WATSONX_MAX_TOKENS", "2000"))
        temperature = (
            temperature
            if temperature is not None
            else float(os.getenv("WATSONX_TEMPERATURE", "0.1"))
        )

        def _generate():
            # Build parameters
            params = {
                GenParams.MAX_NEW_TOKENS: max_tokens,
                GenParams.TEMPERATURE: temperature,
            }

            if top_p is not None:
                params[GenParams.TOP_P] = top_p

            if top_k is not None:
                params[GenParams.TOP_K] = top_k

            if repetition_penalty is not None:
                params[GenParams.REPETITION_PENALTY] = repetition_penalty

            if stop_sequences:
                params[GenParams.STOP_SEQUENCES] = stop_sequences

            if return_options:
                params[GenParams.RETURN_OPTIONS] = return_options
            else:
                # Default return options
                params[GenParams.RETURN_OPTIONS] = {
                    "input_text": False,
                    "generated_tokens": True,
                    "input_tokens": True,
                    "token_logprobs": False,
                    "token_ranks": False,
                    "top_n_tokens": False,
                }

            # Create model inference
            model = ModelInference(
                model_id=self.model_id,
                api_client=self.api_client,
                params=params,
                project_id=self.project_id,
            )

            # Generate
            result = model.generate_text(prompt=prompt)

            # Extract metadata if available
            metadata = {}
            if hasattr(model, "get_details") and callable(model.get_details):
                try:
                    details = model.get_details()
                    if details and "results" in details:
                        result_details = details["results"][0] if details["results"] else {}
                        metadata = {
                            "input_tokens": result_details.get("input_token_count", 0),
                            "output_tokens": result_details.get("generated_token_count", 0),
                            "stop_reason": result_details.get("stop_reason", "unknown"),
                        }
                except Exception as e:
                    logger.warning(f"Could not extract metadata: {e}")

            # Update token tracking
            input_tokens = metadata.get("input_tokens", 0)
            output_tokens = metadata.get("output_tokens", 0)

            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.total_requests += 1

            logger.info(
                f"Generated {output_tokens} tokens (input: {input_tokens}, "
                f"total requests: {self.total_requests})"
            )

            return {
                "text": result,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "stop_reason": metadata.get("stop_reason", "unknown"),
                "model_id": self.model_id,
            }

        return self._retry_operation(_generate)

    def generate_with_system_prompt(
        self, system_prompt: str, user_prompt: str, **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text with system and user prompts.

        Args:
            system_prompt: System instruction
            user_prompt: User query
            **kwargs: Additional generation parameters

        Returns:
            Generation result dict
        """
        # Combine prompts (Granite format)
        combined_prompt = f"""<|system|>
{system_prompt}
<|user|>
{user_prompt}
<|assistant|>
"""

        return self.generate(prompt=combined_prompt, **kwargs)

    def get_token_usage(self) -> Dict[str, int]:
        """
        Get token usage statistics.

        Returns:
            Dict with token counts:
            {
                'total_input_tokens': int,
                'total_output_tokens': int,
                'total_tokens': int,
                'total_requests': int,
                'estimated_cost_usd': float  # Based on $0.0001 per 1000 tokens
            }
        """
        total_tokens = self.total_input_tokens + self.total_output_tokens

        # Calculate estimated cost (1000 tokens = 1 RU = $0.0001 USD)
        estimated_cost = (total_tokens / 1000) * 0.0001

        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": total_tokens,
            "total_requests": self.total_requests,
            "estimated_cost_usd": round(estimated_cost, 6),
        }

    def reset_token_usage(self):
        """Reset token usage counters."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0
        logger.info("Token usage counters reset")

    def health_check(self) -> Dict[str, Any]:
        """
        Check watsonx.ai connection health.

        Returns:
            Dict with health status
        """
        try:
            # Try a simple generation
            result = self.generate(prompt="Test", max_tokens=5, temperature=0.0)

            return {
                "status": "healthy",
                "model_id": self.model_id,
                "project_id": self.project_id,
                "test_generation": result["text"][:50],
                "token_usage": self.get_token_usage(),
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# ============================================================================
# Singleton instance
# ============================================================================

_watsonx_client: Optional[WatsonxClient] = None


def get_watsonx_client() -> WatsonxClient:
    """
    Get singleton watsonx.ai client instance.

    Returns:
        WatsonxClient instance
    """
    global _watsonx_client
    if _watsonx_client is None:
        _watsonx_client = WatsonxClient()
    return _watsonx_client
