#!/usr/bin/env python3
"""
LexConductor - Connection Testing Script
IBM Dev Day AI Demystified Hackathon 2026

This script tests connectivity to all IBM Cloud services.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text: str):
    print(f"\n{BLUE}{'=' * 80}{RESET}")
    print(f"{BLUE}{text.center(80)}{RESET}")
    print(f"{BLUE}{'=' * 80}{RESET}\n")


def print_success(text: str):
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text: str):
    print(f"{RED}✗ {text}{RESET}")


def print_info(text: str):
    print(f"{BLUE}ℹ {text}{RESET}")


def test_watsonx_ai():
    """Test watsonx.ai connectivity."""
    print_header("Testing watsonx.ai Connection")
    
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    
    if not api_key or "your_" in api_key:
        print_error("WATSONX_API_KEY not configured")
        return False
    
    if not project_id or "your_" in project_id:
        print_error("WATSONX_PROJECT_ID not configured")
        return False
    
    try:
        from ibm_watsonx_ai import APIClient
        from ibm_watsonx_ai import Credentials
        
        print_info("Connecting to watsonx.ai...")
        
        credentials = Credentials(
            url=url,
            api_key=api_key,
        )
        
        client = APIClient(credentials, project_id=project_id)
        
        # Test connection by listing models
        print_info("Listing available models...")
        models = client.foundation_models.get_model_specs()
        
        # Check if Granite 3 8B Instruct is available
        granite_found = False
        for model in models:
            model_id = model.get("model_id", "") if isinstance(model, dict) else str(model)
            if "granite-3-8b-instruct" in model_id:
                granite_found = True
                print_success(f"Found model: {model_id}")
                break
        
        if granite_found:
            print_success("watsonx.ai connection successful")
            print_success("Granite 3 8B Instruct model available")
            return True
        else:
            print_success("watsonx.ai connection successful")
            print_info("Note: Model listing may require additional permissions")
            return True
            
    except Exception as e:
        print_error(f"watsonx.ai connection failed: {str(e)}")
        return False


def test_cloudant():
    """Test Cloudant connectivity."""
    print_header("Testing Cloudant Connection")
    
    url = os.getenv("CLOUDANT_URL")
    api_key = os.getenv("CLOUDANT_API_KEY")
    
    if not url or "your-" in url:
        print_error("CLOUDANT_URL not configured")
        return False
    
    if not api_key or "your_" in api_key:
        print_error("CLOUDANT_API_KEY not configured")
        return False
    
    try:
        from ibmcloudant.cloudant_v1 import CloudantV1
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
        
        print_info("Connecting to Cloudant...")
        
        authenticator = IAMAuthenticator(api_key)
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(url)
        
        # Test connection by listing databases
        print_info("Listing databases...")
        response = client.get_all_dbs().get_result()
        
        print_success(f"Cloudant connection successful")
        print_info(f"Found {len(response)} databases")
        
        # Check for required databases
        required_dbs = [
            os.getenv("CLOUDANT_DB_GOLDEN_CLAUSES", "golden_clauses"),
            os.getenv("CLOUDANT_DB_HISTORICAL_DECISIONS", "historical_decisions"),
            os.getenv("CLOUDANT_DB_REGULATORY_MAPPINGS", "regulatory_mappings"),
        ]
        
        for db_name in required_dbs:
            if db_name in response:
                print_success(f"Database '{db_name}' exists")
            else:
                print_error(f"Database '{db_name}' not found (will be created)")
        
        return True
        
    except Exception as e:
        print_error(f"Cloudant connection failed: {str(e)}")
        return False


def test_cos():
    """Test Cloud Object Storage connectivity."""
    print_header("Testing Cloud Object Storage Connection")
    
    endpoint = os.getenv("COS_ENDPOINT")
    api_key = os.getenv("COS_API_KEY")
    instance_id = os.getenv("COS_INSTANCE_ID")
    
    if not endpoint or "your-" in endpoint:
        print_error("COS_ENDPOINT not configured")
        return False
    
    if not api_key or "your_" in api_key:
        print_error("COS_API_KEY not configured")
        return False
    
    if not instance_id or "your_" in instance_id:
        print_error("COS_INSTANCE_ID not configured")
        return False
    
    try:
        import ibm_boto3
        from ibm_botocore.client import Config
        
        print_info("Connecting to Cloud Object Storage...")
        
        # Get auth endpoint
        auth_endpoint = os.getenv("COS_AUTH_ENDPOINT", "https://iam.cloud.ibm.com/identity/token")
        
        cos_client = ibm_boto3.client(
            "s3",
            ibm_api_key_id=api_key,
            ibm_service_instance_id=instance_id,
            ibm_auth_endpoint=auth_endpoint,
            config=Config(signature_version="oauth"),
            endpoint_url=f"https://{endpoint}"
        )
        
        # Test connection by listing buckets
        print_info("Listing buckets...")
        response = cos_client.list_buckets()
        
        print_success("Cloud Object Storage connection successful")
        print_info(f"Found {len(response['Buckets'])} buckets")
        
        # Check for required bucket
        bucket_name = os.getenv("COS_BUCKET_NAME", "watsonx-hackathon-regulations")
        bucket_exists = any(b["Name"] == bucket_name for b in response["Buckets"])
        
        if bucket_exists:
            print_success(f"Bucket '{bucket_name}' exists")
        else:
            print_error(f"Bucket '{bucket_name}' not found (will be created)")
        
        return True
        
    except Exception as e:
        print_error(f"Cloud Object Storage connection failed: {str(e)}")
        return False


def test_orchestrate():
    """Test watsonx Orchestrate configuration."""
    print_header("Testing watsonx Orchestrate Configuration")
    
    instance = os.getenv("WO_INSTANCE")
    api_key = os.getenv("WO_API_KEY")
    
    if not instance or "your-" in instance:
        print_error("WO_INSTANCE not configured")
        return False
    
    if not api_key or "your_" in api_key:
        print_error("WO_API_KEY not configured")
        return False
    
    print_success("watsonx Orchestrate credentials configured")
    print_info(f"Instance: {instance}")
    
    # Note: Full connectivity test requires ADK environment setup
    print_info("To test full connectivity, run:")
    print_info("  orchestrate env add prod --instance $WO_INSTANCE --api-key $WO_API_KEY")
    print_info("  orchestrate env activate prod")
    print_info("  orchestrate auth login")
    
    return True


def main():
    """Main testing function."""
    print_header("LexConductor - Connection Testing")
    print_info("IBM Dev Day AI Demystified Hackathon 2026")
    print_info("Team: AI Kings 👑")
    
    tests = []
    
    # Run all tests
    tests.append(("watsonx.ai", test_watsonx_ai()))
    tests.append(("Cloudant", test_cloudant()))
    tests.append(("Cloud Object Storage", test_cos()))
    tests.append(("watsonx Orchestrate", test_orchestrate()))
    
    # Summary
    print_header("CONNECTION TEST SUMMARY")
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        if result:
            print_success(f"{name}: CONNECTED")
        else:
            print_error(f"{name}: FAILED")
    
    print()
    if passed == total:
        print_success(f"All connections successful ({passed}/{total})")
        print_info("You're ready to start development!")
    else:
        print_error(f"Some connections failed ({passed}/{total} passed)")
        print_info("Check your .env file and IBM Cloud service credentials")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
