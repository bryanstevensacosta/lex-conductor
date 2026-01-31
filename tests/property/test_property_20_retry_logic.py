"""
Property Test 20: Retry Logic Execution
Feature: lex-conductor-implementation
Validates: Requirements 9.5

For any transient error, the retry logic should execute up to max_retries times
with exponential backoff delays between attempts.
"""

import pytest
from hypothesis import given, strategies as st, settings
from unittest.mock import Mock, patch
from backend.cloudant_client import CloudantClient
from backend.cos_client import COSClient
from backend.watsonx_client import WatsonxClient

# ============================================================================
# Property Tests
# ============================================================================


class TestProperty20RetryLogic:
    """
    Property 20: Retry Logic Execution

    For any transient error, retry logic should execute up to max_retries times
    with exponential backoff.
    """

    @given(
        max_retries=st.integers(min_value=1, max_value=5),
        retry_delay=st.floats(min_value=0.1, max_value=1.0, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=10, deadline=None)
    def test_cloudant_retry_executes_correct_number_of_times(self, max_retries, retry_delay):
        """
        Property: Cloudant client retries transient errors up to max_retries times
        """
        # Create mock operation that always fails
        mock_operation = Mock(side_effect=Exception("Transient error"))

        # Create client with test retry settings
        with patch.dict(
            "os.environ",
            {
                "CLOUDANT_URL": "https://test.cloudant.com",
                "CLOUDANT_API_KEY": "test_key",
            },
        ):
            with patch("backend.cloudant_client.CloudantV1"):
                with patch("time.sleep"):  # Mock sleep to speed up test
                    client = CloudantClient(max_retries=max_retries, retry_delay=retry_delay)

                    # Attempt operation (should fail after retries)
                    with pytest.raises(Exception, match="Transient error"):
                        client._retry_operation(mock_operation)

                    # Verify operation was called max_retries times
                    assert (
                        mock_operation.call_count == max_retries
                    ), f"Operation should be called {max_retries} times, was called {mock_operation.call_count}"

    @given(
        max_retries=st.integers(min_value=2, max_value=5),
        retry_delay=st.floats(min_value=0.1, max_value=0.5, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=10, deadline=10000)
    def test_cloudant_retry_uses_exponential_backoff(self, max_retries, retry_delay):
        """
        Property: Retry delays follow exponential backoff pattern
        """
        # Track sleep calls
        sleep_calls = []

        def mock_sleep(duration):
            sleep_calls.append(duration)

        # Create mock operation that always fails
        mock_operation = Mock(side_effect=Exception("Transient error"))

        with patch.dict(
            "os.environ",
            {
                "CLOUDANT_URL": "https://test.cloudant.com",
                "CLOUDANT_API_KEY": "test_key",
            },
        ):
            with patch("backend.cloudant_client.CloudantV1"):
                with patch("time.sleep", side_effect=mock_sleep):
                    client = CloudantClient(max_retries=max_retries, retry_delay=retry_delay)

                    # Attempt operation
                    with pytest.raises(Exception):
                        client._retry_operation(mock_operation)

                    # Verify exponential backoff
                    # Should have max_retries - 1 sleep calls (no sleep after last attempt)
                    assert (
                        len(sleep_calls) == max_retries - 1
                    ), f"Should have {max_retries - 1} sleep calls, got {len(sleep_calls)}"

                    # Verify each delay is approximately 2x the previous
                    for i in range(len(sleep_calls)):
                        expected_delay = retry_delay * (2**i)
                        actual_delay = sleep_calls[i]

                        # Allow small floating point error
                        assert (
                            abs(actual_delay - expected_delay) < 0.01
                        ), f"Sleep {i} should be ~{expected_delay}s, was {actual_delay}s"

    def test_cloudant_retry_succeeds_on_second_attempt(self):
        """
        Test that retry succeeds if operation succeeds on retry
        """
        # Create mock that fails once then succeeds
        mock_operation = Mock(side_effect=[Exception("Transient error"), "Success"])

        with patch.dict(
            "os.environ",
            {
                "CLOUDANT_URL": "https://test.cloudant.com",
                "CLOUDANT_API_KEY": "test_key",
            },
        ):
            with patch("backend.cloudant_client.CloudantV1"):
                with patch("time.sleep"):  # Mock sleep to speed up test
                    client = CloudantClient(max_retries=3, retry_delay=0.1)

                    # Should succeed on second attempt
                    result = client._retry_operation(mock_operation)

                    assert result == "Success"
                    assert mock_operation.call_count == 2  # Failed once, succeeded once

    def test_cloudant_retry_does_not_retry_non_retryable_errors(self):
        """
        Test that certain errors are not retried
        """
        # Create mock that raises "not found" error (should not retry)
        mock_operation = Mock(side_effect=Exception("not found"))

        with patch.dict(
            "os.environ",
            {
                "CLOUDANT_URL": "https://test.cloudant.com",
                "CLOUDANT_API_KEY": "test_key",
            },
        ):
            with patch("backend.cloudant_client.CloudantV1"):
                client = CloudantClient(max_retries=3, retry_delay=0.1)

                # Should fail immediately without retries
                with pytest.raises(Exception, match="not found"):
                    client._retry_operation(mock_operation)

                # Should only be called once (no retries)
                assert mock_operation.call_count == 1

    @given(
        max_retries=st.integers(min_value=1, max_value=5),
        retry_delay=st.floats(min_value=0.1, max_value=1.0, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=10, deadline=None)
    def test_cos_retry_executes_correct_number_of_times(self, max_retries, retry_delay):
        """
        Property: COS client retries transient errors up to max_retries times
        """
        # Create mock operation that always fails
        mock_operation = Mock(side_effect=Exception("Transient error"))

        with patch.dict(
            "os.environ",
            {
                "COS_API_KEY": "test_key",
                "COS_INSTANCE_ID": "test_instance",
                "COS_ENDPOINT": "test.endpoint.com",
                "COS_BUCKET_NAME": "test_bucket",
            },
        ):
            with patch("ibm_boto3.client"):
                with patch("time.sleep"):  # Mock sleep to speed up test
                    client = COSClient(max_retries=max_retries, retry_delay=retry_delay)

                    # Attempt operation
                    with pytest.raises(Exception, match="Transient error"):
                        client._retry_operation(mock_operation)

                    # Verify operation was called max_retries times
                    assert mock_operation.call_count == max_retries

    @given(
        max_retries=st.integers(min_value=1, max_value=5),
        retry_delay=st.floats(min_value=0.1, max_value=1.0, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=10, deadline=None)
    def test_watsonx_retry_executes_correct_number_of_times(self, max_retries, retry_delay):
        """
        Property: watsonx.ai client retries transient errors up to max_retries times
        """
        # Create mock operation that always fails
        mock_operation = Mock(side_effect=Exception("Transient error"))

        with patch.dict(
            "os.environ",
            {"WATSONX_API_KEY": "test_key", "WATSONX_PROJECT_ID": "test_project"},
        ):
            with patch("backend.watsonx_client.APIClient"):
                with patch("time.sleep"):  # Mock sleep to speed up test
                    client = WatsonxClient(max_retries=max_retries, retry_delay=retry_delay)

                    # Attempt operation
                    with pytest.raises(Exception, match="Transient error"):
                        client._retry_operation(mock_operation)

                    # Verify operation was called max_retries times
                    assert mock_operation.call_count == max_retries

    def test_watsonx_retry_does_not_retry_auth_errors(self):
        """
        Test that authentication errors are not retried
        """
        # Create mock that raises auth error (should not retry)
        mock_operation = Mock(side_effect=Exception("unauthorized"))

        with patch.dict(
            "os.environ",
            {"WATSONX_API_KEY": "test_key", "WATSONX_PROJECT_ID": "test_project"},
        ):
            with patch("backend.watsonx_client.APIClient"):
                client = WatsonxClient(max_retries=3, retry_delay=0.1)

                # Should fail immediately without retries
                with pytest.raises(Exception, match="unauthorized"):
                    client._retry_operation(mock_operation)

                # Should only be called once (no retries)
                assert mock_operation.call_count == 1


# ============================================================================
# Integration Tests
# ============================================================================


class TestRetryLogicIntegration:
    """Integration tests for retry logic across all clients"""

    def test_all_clients_have_retry_logic(self):
        """Verify all clients implement retry logic"""
        with patch.dict(
            "os.environ",
            {
                "CLOUDANT_URL": "https://test.cloudant.com",
                "CLOUDANT_API_KEY": "test_key",
                "COS_API_KEY": "test_key",
                "COS_INSTANCE_ID": "test_instance",
                "COS_ENDPOINT": "test.endpoint.com",
                "COS_BUCKET_NAME": "test_bucket",
                "WATSONX_API_KEY": "test_key",
                "WATSONX_PROJECT_ID": "test_project",
            },
        ):
            with patch("backend.cloudant_client.CloudantV1"):
                with patch("ibm_boto3.client"):
                    with patch("backend.watsonx_client.APIClient"):
                        # Create clients
                        cloudant_client = CloudantClient()
                        cos_client = COSClient()
                        watsonx_client = WatsonxClient()

                        # Verify they all have _retry_operation method
                        assert hasattr(cloudant_client, "_retry_operation")
                        assert callable(cloudant_client._retry_operation)

                        assert hasattr(cos_client, "_retry_operation")
                        assert callable(cos_client._retry_operation)

                        assert hasattr(watsonx_client, "_retry_operation")
                        assert callable(watsonx_client._retry_operation)

    def test_retry_parameters_configurable(self):
        """Verify retry parameters can be configured"""
        with patch.dict(
            "os.environ",
            {
                "CLOUDANT_URL": "https://test.cloudant.com",
                "CLOUDANT_API_KEY": "test_key",
            },
        ):
            with patch("backend.cloudant_client.CloudantV1"):
                # Create client with custom retry settings
                client = CloudantClient(max_retries=5, retry_delay=2.0)

                assert client.max_retries == 5
                assert client.retry_delay == 2.0

    def test_exponential_backoff_timing(self):
        """
        Test that exponential backoff timing is correct
        """
        sleep_calls = []

        def mock_sleep(duration):
            sleep_calls.append(duration)

        mock_operation = Mock(side_effect=Exception("Transient error"))

        with patch.dict(
            "os.environ",
            {
                "CLOUDANT_URL": "https://test.cloudant.com",
                "CLOUDANT_API_KEY": "test_key",
            },
        ):
            with patch("backend.cloudant_client.CloudantV1"):
                with patch("time.sleep", side_effect=mock_sleep):
                    client = CloudantClient(max_retries=4, retry_delay=1.0)

                    with pytest.raises(Exception):
                        client._retry_operation(mock_operation)

                    # Verify delays: 1.0, 2.0, 4.0 (no sleep after 4th attempt)
                    assert len(sleep_calls) == 3
                    assert abs(sleep_calls[0] - 1.0) < 0.01
                    assert abs(sleep_calls[1] - 2.0) < 0.01
                    assert abs(sleep_calls[2] - 4.0) < 0.01
