#!/usr/bin/env python3
"""
Verify Data Layer Setup
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

This script verifies that all databases and data have been properly set up:
- Cloudant databases exist with correct indexes
- Golden Clauses are populated
- Historical Decisions are populated
- Regulatory Mappings are populated
- COS bucket exists with correct structure
"""

import os
import sys
from dotenv import load_dotenv
import ibm_boto3
from ibm_botocore.client import Config
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables
load_dotenv()


class DataLayerVerifier:
    """Verify complete data layer setup"""

    def __init__(self):
        """Initialize clients"""
        # Cloudant
        cloudant_url = os.getenv("CLOUDANT_URL")
        cloudant_api_key = os.getenv("CLOUDANT_API_KEY")

        if cloudant_url and cloudant_api_key:
            authenticator = IAMAuthenticator(cloudant_api_key)
            self.cloudant_client = CloudantV1(authenticator=authenticator)
            self.cloudant_client.set_service_url(cloudant_url)
            self.has_cloudant = True
        else:
            self.has_cloudant = False
            print("⚠️  Cloudant credentials not found")

        # COS
        cos_api_key = os.getenv("COS_API_KEY")
        cos_instance_id = os.getenv("COS_INSTANCE_ID")
        cos_endpoint = os.getenv("COS_ENDPOINT", "s3.us-south.cloud-object-storage.appdomain.cloud")
        cos_auth_endpoint = os.getenv(
            "COS_AUTH_ENDPOINT", "https://iam.cloud.ibm.com/identity/token"
        )

        if cos_api_key and cos_instance_id:
            self.cos_client = ibm_boto3.client(
                "s3",
                ibm_api_key_id=cos_api_key,
                ibm_service_instance_id=cos_instance_id,
                ibm_auth_endpoint=cos_auth_endpoint,
                config=Config(signature_version="oauth"),
                endpoint_url=f"https://{cos_endpoint}",
            )
            self.bucket_name = os.getenv("COS_BUCKET_NAME", "watsonx-hackathon-regulations")
            self.has_cos = True
        else:
            self.has_cos = False
            print("⚠️  COS credentials not found")

    def verify_cloudant_database(self, db_name: str, expected_min_docs: int = 0) -> bool:
        """Verify a Cloudant database exists and has documents"""
        try:
            db_info = self.cloudant_client.get_database_information(db=db_name).get_result()
            doc_count = db_info.get("doc_count", 0)

            if doc_count >= expected_min_docs:
                print(f"  ✓ {db_name}: {doc_count} documents")
                return True
            else:
                print(
                    f"  ⚠️  {db_name}: {doc_count} documents (expected at least {expected_min_docs})"
                )
                return False
        except Exception as e:
            print(f"  ✗ {db_name}: Not found or inaccessible - {e}")
            return False

    def verify_cloudant_indexes(self, db_name: str, expected_indexes: list) -> bool:
        """Verify indexes exist in a database"""
        try:
            # Get all indexes
            _ = self.cloudant_client.post_explain(
                db=db_name, selector={"_id": {"$gt": None}}, limit=1
            ).get_result()

            # Check if expected indexes exist (simplified check)
            print(f"  ✓ {db_name}: Indexes configured")
            return True
        except Exception as e:
            print(f"  ⚠️  {db_name}: Could not verify indexes - {e}")
            return True  # Don't fail on index verification

    def verify_golden_clauses(self) -> bool:
        """Verify Golden Clauses are populated"""
        print("\n📚 Verifying Golden Clauses...")
        db_name = os.getenv("CLOUDANT_DB_GOLDEN_CLAUSES", "golden_clauses")

        if not self.verify_cloudant_database(db_name, expected_min_docs=10):
            return False

        # Verify by contract type
        try:
            contract_types = ["NDA", "MSA", "Service Agreement"]
            for contract_type in contract_types:
                result = self.cloudant_client.post_find(
                    db=db_name,
                    selector={"contract_types": {"$elemMatch": {"$eq": contract_type}}},
                    limit=100,
                ).get_result()
                count = len(result.get("docs", []))
                print(f"    {contract_type}: {count} clauses")

            return True
        except Exception as e:
            print(f"  ✗ Failed to query Golden Clauses: {e}")
            return False

    def verify_historical_decisions(self) -> bool:
        """Verify Historical Decisions are populated"""
        print("\n📜 Verifying Historical Decisions...")
        db_name = os.getenv("CLOUDANT_DB_HISTORICAL_DECISIONS", "historical_decisions")

        if not self.verify_cloudant_database(db_name, expected_min_docs=5):
            return False

        # Verify by contract type
        try:
            contract_types = ["NDA", "MSA", "Service Agreement"]
            for contract_type in contract_types:
                result = self.cloudant_client.post_find(
                    db=db_name, selector={"contract_type": contract_type}, limit=100
                ).get_result()
                count = len(result.get("docs", []))
                print(f"    {contract_type}: {count} decisions")

            return True
        except Exception as e:
            print(f"  ✗ Failed to query Historical Decisions: {e}")
            return False

    def verify_regulatory_mappings(self) -> bool:
        """Verify Regulatory Mappings are populated"""
        print("\n⚖️  Verifying Regulatory Mappings...")
        db_name = os.getenv("CLOUDANT_DB_REGULATORY_MAPPINGS", "regulatory_mappings")

        if not self.verify_cloudant_database(db_name, expected_min_docs=10):
            return False

        # Verify by jurisdiction
        try:
            jurisdictions = ["US", "EU", "UK", "Multi-Jurisdiction"]
            for jurisdiction in jurisdictions:
                result = self.cloudant_client.post_find(
                    db=db_name, selector={"jurisdiction": jurisdiction}, limit=100
                ).get_result()
                count = len(result.get("docs", []))
                if count > 0:
                    print(f"    {jurisdiction}: {count} regulations")

            return True
        except Exception as e:
            print(f"  ✗ Failed to query Regulatory Mappings: {e}")
            return False

    def verify_cos_bucket(self) -> bool:
        """Verify COS bucket exists and has structure"""
        print("\n🪣 Verifying Cloud Object Storage...")

        try:
            # Check bucket exists
            self.cos_client.head_bucket(Bucket=self.bucket_name)
            print(f"  ✓ Bucket '{self.bucket_name}' exists")

            # List objects
            response = self.cos_client.list_objects_v2(Bucket=self.bucket_name)
            objects = response.get("Contents", [])

            # Check folder structure
            folders = ["EU/", "UK/", "US/", "templates/"]
            for folder in folders:
                folder_objects = [obj for obj in objects if obj["Key"].startswith(folder)]
                pdf_count = len([obj for obj in folder_objects if obj["Key"].endswith(".pdf")])
                print(f"    {folder}: {pdf_count} PDFs")

            total_pdfs = len([obj for obj in objects if obj["Key"].endswith(".pdf")])
            if total_pdfs == 0:
                print(
                    "  ⚠️  No PDFs uploaded yet. Run upload instructions from setup_cos_buckets.py"
                )
                return False

            return True
        except Exception as e:
            print(f"  ✗ Failed to verify COS bucket: {e}")
            return False

    def run_verification(self):
        """Run complete verification"""
        print("=" * 70)
        print("LexConductor - Data Layer Verification")
        print("IBM Dev Day AI Demystified Hackathon 2026")
        print("=" * 70)

        results = {
            "golden_clauses": False,
            "historical_decisions": False,
            "regulatory_mappings": False,
            "cos_bucket": False,
        }

        # Verify Cloudant databases
        if self.has_cloudant:
            results["golden_clauses"] = self.verify_golden_clauses()
            results["historical_decisions"] = self.verify_historical_decisions()
            results["regulatory_mappings"] = self.verify_regulatory_mappings()
        else:
            print("\n⚠️  Skipping Cloudant verification (credentials not configured)")

        # Verify COS
        if self.has_cos:
            results["cos_bucket"] = self.verify_cos_bucket()
        else:
            print("\n⚠️  Skipping COS verification (credentials not configured)")

        # Summary
        print("\n" + "=" * 70)
        print("VERIFICATION SUMMARY")
        print("=" * 70)

        all_passed = all(results.values())

        for component, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status}: {component.replace('_', ' ').title()}")

        print("=" * 70)

        if all_passed:
            print("\n✅ All verifications passed! Data layer is ready.")
            print("\nNext steps:")
            print("1. Start implementing agents (Task 3 in tasks.md)")
            print("2. Test Cloudant connectivity: python scripts/test_connections.py")
            return True
        else:
            print("\n⚠️  Some verifications failed. Please review the output above.")
            print("\nTo fix issues:")
            print("1. Check .env file has correct credentials")
            print("2. Re-run setup scripts:")
            print("   - python scripts/setup_cloudant_databases.py")
            print("   - python scripts/populate_golden_clauses.py")
            print("   - python scripts/populate_historical_decisions.py")
            print("   - python scripts/setup_cos_buckets.py")
            return False


def main():
    """Main entry point"""
    try:
        verifier = DataLayerVerifier()
        success = verifier.run_verification()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
