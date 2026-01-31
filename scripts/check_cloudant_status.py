#!/usr/bin/env python3
"""
Check Cloudant Database Status
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

This script checks the current status of Cloudant databases and indexes
WITHOUT making any changes. Use this to verify what exists before running setup.
"""

import os
import sys
from dotenv import load_dotenv
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables
load_dotenv()


class CloudantStatusChecker:
    """Check Cloudant database and index status"""

    def __init__(self):
        """Initialize Cloudant client"""
        self.cloudant_url = os.getenv("CLOUDANT_URL")
        self.cloudant_api_key = os.getenv("CLOUDANT_API_KEY")

        if not self.cloudant_url or not self.cloudant_api_key:
            raise ValueError(
                "Missing Cloudant credentials. Please set CLOUDANT_URL and CLOUDANT_API_KEY "
                "in your .env file"
            )

        # Initialize authenticator and client
        authenticator = IAMAuthenticator(self.cloudant_api_key)
        self.client = CloudantV1(authenticator=authenticator)
        self.client.set_service_url(self.cloudant_url)

        print(f"✓ Connected to Cloudant: {self.cloudant_url}")

    def check_database(self, db_name: str) -> dict:
        """Check if database exists and get info"""
        try:
            db_info = self.client.get_database_information(db=db_name).get_result()
            return {
                "exists": True,
                "doc_count": db_info.get("doc_count", 0),
                "disk_size": db_info.get("sizes", {}).get("file", 0),
                "update_seq": db_info.get("update_seq", "unknown"),
            }
        except Exception as e:
            return {"exists": False, "error": str(e)}

    def check_indexes(self, db_name: str) -> dict:
        """Check indexes for a database"""
        try:
            # Get all indexes using the _index endpoint
            _ = self.client.post_find(
                db=db_name,
                selector={"_id": {"$gt": None}},
                limit=1,
                execution_stats=True,
            ).get_result()

            # Try to get index information
            indexes_info = []
            try:
                # List all indexes
                all_indexes = self.client.get_indexes_information(db=db_name).get_result()
                indexes = all_indexes.get("indexes", [])

                for idx in indexes:
                    if idx.get("type") == "json":  # Skip special indexes
                        indexes_info.append(
                            {
                                "name": idx.get("name", "unnamed"),
                                "fields": idx.get("def", {}).get("fields", []),
                                "type": idx.get("type", "unknown"),
                            }
                        )
            except Exception as e:
                indexes_info = [{"error": f"Could not list indexes: {str(e)}"}]

            return {"exists": True, "indexes": indexes_info, "count": len(indexes_info)}
        except Exception as e:
            return {"exists": False, "error": str(e)}

    def check_all_databases(self):
        """Check all required databases"""
        print("\n" + "=" * 70)
        print("CLOUDANT DATABASE STATUS CHECK")
        print("=" * 70)

        databases = {
            "golden_clauses": os.getenv("CLOUDANT_DB_GOLDEN_CLAUSES", "golden_clauses"),
            "historical_decisions": os.getenv(
                "CLOUDANT_DB_HISTORICAL_DECISIONS", "historical_decisions"
            ),
            "regulatory_mappings": os.getenv(
                "CLOUDANT_DB_REGULATORY_MAPPINGS", "regulatory_mappings"
            ),
        }

        results = {}

        for db_type, db_name in databases.items():
            print(f"\n📊 Checking database: {db_name}")
            print("-" * 70)

            # Check database
            db_status = self.check_database(db_name)
            results[db_type] = {"database": db_status}

            if db_status["exists"]:
                print("  ✅ Database EXISTS")
                print(f"     Documents: {db_status['doc_count']}")
                print(f"     Disk size: {db_status['disk_size']:,} bytes")

                # Check indexes
                print("\n  🔍 Checking indexes...")
                idx_status = self.check_indexes(db_name)
                results[db_type]["indexes"] = idx_status

                if idx_status.get("exists"):
                    if idx_status["count"] > 0:
                        print(f"     Found {idx_status['count']} custom indexes:")
                        for idx in idx_status["indexes"]:
                            if "error" in idx:
                                print(f"       ⚠️  {idx['error']}")
                            else:
                                fields_str = ", ".join([str(f) for f in idx["fields"]])
                                print(f"       • {idx['name']}: [{fields_str}]")
                    else:
                        print("     ⚠️  NO custom indexes found (only default _all_docs)")
                else:
                    print(
                        f"     ❌ Could not check indexes: {idx_status.get('error', 'Unknown error')}"
                    )
            else:
                print("  ❌ Database DOES NOT EXIST")
                print(f"     Error: {db_status.get('error', 'Unknown error')}")
                results[db_type]["indexes"] = {"exists": False}

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)

        all_dbs_exist = all(r["database"]["exists"] for r in results.values())
        all_have_indexes = all(
            r["indexes"].get("exists") and r["indexes"].get("count", 0) > 0
            for r in results.values()
            if r["database"]["exists"]
        )

        print("\n📊 Databases:")
        for db_type, status in results.items():
            db_name = databases[db_type]
            if status["database"]["exists"]:
                doc_count = status["database"]["doc_count"]
                idx_count = status["indexes"].get("count", 0)
                print(f"  ✅ {db_name}: {doc_count} docs, {idx_count} indexes")
            else:
                print(f"  ❌ {db_name}: Does not exist")

        print("\n📋 Recommendations:")

        if not all_dbs_exist:
            print("  1. ⚠️  Some databases are missing")
            print("     Run: python scripts/setup_cloudant_databases.py")

        if all_dbs_exist and not all_have_indexes:
            print("  1. ⚠️  Databases exist but indexes are missing")
            print("     Run: python scripts/setup_cloudant_databases.py")
            print("     (Script will skip existing databases and only create indexes)")

        if all_dbs_exist and all_have_indexes:
            print("  ✅ All databases and indexes exist!")
            print("     You can proceed to populate data:")
            print("     - python scripts/populate_golden_clauses.py")
            print("     - python scripts/populate_historical_decisions.py")
            print("     - python scripts/setup_cos_buckets.py")

        # Check if databases have data
        empty_dbs = [
            databases[db_type]
            for db_type, status in results.items()
            if status["database"]["exists"] and status["database"]["doc_count"] == 0
        ]

        if empty_dbs:
            print(f"\n  ℹ️  Empty databases found: {', '.join(empty_dbs)}")
            print("     These databases need to be populated with data")

        print("\n" + "=" * 70)

        return results


def main():
    """Main entry point"""
    try:
        checker = CloudantStatusChecker()
        results = checker.check_all_databases()

        # Exit with appropriate code
        all_ready = all(
            r["database"]["exists"]
            and r["indexes"].get("exists")
            and r["indexes"].get("count", 0) > 0
            for r in results.values()
        )

        sys.exit(0 if all_ready else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
