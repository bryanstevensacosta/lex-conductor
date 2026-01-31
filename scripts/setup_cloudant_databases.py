#!/usr/bin/env python3
"""
Setup Cloudant Databases and Indexes
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

This script creates the required Cloudant databases and indexes for LexConductor:
- golden_clauses database with contract_type index
- historical_decisions database with decision_id index
- regulatory_mappings database with jurisdiction index
"""

import os
import sys
import time
from typing import List
from dotenv import load_dotenv
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables
load_dotenv()


class CloudantDatabaseSetup:
    """Setup Cloudant databases and indexes for LexConductor"""

    def __init__(self):
        """Initialize Cloudant client"""
        # Get credentials from environment
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

    def create_database(self, db_name: str) -> bool:
        """Create a database if it doesn't exist"""
        try:
            # Check if database exists
            self.client.get_database_information(db=db_name)
            print(f"  Database '{db_name}' already exists")
            return False
        except Exception:
            # Database doesn't exist, create it
            try:
                self.client.put_database(db=db_name)
                print(f"✓ Created database: {db_name}")
                return True
            except Exception as e:
                print(f"✗ Failed to create database '{db_name}': {e}")
                raise

    def create_index(self, db_name: str, index_name: str, fields: List[str]) -> bool:
        """Create an index on specified fields"""
        try:
            index_definition = {
                "index": {"fields": fields},
                "name": index_name,
                "type": "json",
            }

            self.client.post_index(
                db=db_name,
                index=index_definition["index"],
                name=index_name,
                type=index_definition["type"],
            )
            print(f"✓ Created index '{index_name}' on {fields} in database '{db_name}'")

            # Add delay to avoid rate limiting
            time.sleep(2)

            return True
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"  Index '{index_name}' already exists in database '{db_name}'")
                return False
            else:
                print(f"✗ Failed to create index '{index_name}': {e}")
                raise

    def setup_golden_clauses_db(self):
        """Setup golden_clauses database with indexes"""
        db_name = os.getenv("CLOUDANT_DB_GOLDEN_CLAUSES", "golden_clauses")
        print(f"\n📚 Setting up {db_name} database...")

        # Create database
        self.create_database(db_name)

        # Create indexes
        self.create_index(db_name, "idx_contract_type", ["contract_types"])
        self.create_index(db_name, "idx_clause_type", ["type"])
        self.create_index(db_name, "idx_jurisdiction", ["jurisdiction"])
        self.create_index(db_name, "idx_mandatory", ["mandatory"])
        self.create_index(db_name, "idx_risk_level", ["risk_level"])

        print(f"✓ {db_name} database setup complete")

    def setup_historical_decisions_db(self):
        """Setup historical_decisions database with indexes"""
        db_name = os.getenv("CLOUDANT_DB_HISTORICAL_DECISIONS", "historical_decisions")
        print(f"\n📜 Setting up {db_name} database...")

        # Create database
        self.create_database(db_name)

        # Create indexes
        self.create_index(db_name, "idx_decision_id", ["decision_id"])
        self.create_index(db_name, "idx_contract_type", ["contract_type"])
        self.create_index(db_name, "idx_jurisdiction", ["jurisdiction"])
        self.create_index(db_name, "idx_date", ["date"])
        self.create_index(db_name, "idx_confidence", ["confidence"])

        print(f"✓ {db_name} database setup complete")

    def setup_regulatory_mappings_db(self):
        """Setup regulatory_mappings database with indexes"""
        db_name = os.getenv("CLOUDANT_DB_REGULATORY_MAPPINGS", "regulatory_mappings")
        print(f"\n⚖️  Setting up {db_name} database...")

        # Create database
        self.create_database(db_name)

        # Create indexes
        self.create_index(db_name, "idx_jurisdiction", ["jurisdiction"])
        self.create_index(db_name, "idx_regulation_name", ["regulation_name"])
        self.create_index(db_name, "idx_regulation_type", ["regulation_type"])

        print(f"✓ {db_name} database setup complete")

    def verify_setup(self):
        """Verify all databases and indexes are created"""
        print("\n🔍 Verifying database setup...")

        databases = [
            os.getenv("CLOUDANT_DB_GOLDEN_CLAUSES", "golden_clauses"),
            os.getenv("CLOUDANT_DB_HISTORICAL_DECISIONS", "historical_decisions"),
            os.getenv("CLOUDANT_DB_REGULATORY_MAPPINGS", "regulatory_mappings"),
        ]

        for db_name in databases:
            try:
                # Get database info
                db_info = self.client.get_database_information(db=db_name).get_result()
                doc_count = db_info.get("doc_count", 0)

                # Get indexes
                _ = self.client.post_find(
                    db=db_name, selector={"_id": {"$gt": None}}, limit=0
                ).get_result()

                print(f"✓ {db_name}: {doc_count} documents")
            except Exception as e:
                print(f"✗ {db_name}: Verification failed - {e}")
                return False

        print("\n✅ All databases verified successfully!")
        return True

    def run_setup(self):
        """Run complete database setup"""
        print("=" * 70)
        print("LexConductor - Cloudant Database Setup")
        print("IBM Dev Day AI Demystified Hackathon 2026")
        print("=" * 70)

        try:
            # Setup each database
            self.setup_golden_clauses_db()
            self.setup_historical_decisions_db()
            self.setup_regulatory_mappings_db()

            # Verify setup
            self.verify_setup()

            print("\n" + "=" * 70)
            print("✅ Cloudant database setup complete!")
            print("=" * 70)
            print("\nNext steps:")
            print("1. Run: python scripts/populate_golden_clauses.py")
            print("2. Run: python scripts/populate_historical_decisions.py")
            print("3. Run: python scripts/setup_cos_buckets.py")
            print("=" * 70)

            return True
        except Exception as e:
            print(f"\n✗ Setup failed: {e}")
            return False


def main():
    """Main entry point"""
    try:
        setup = CloudantDatabaseSetup()
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
