#!/usr/bin/env python3
"""
Populate Golden Clauses Collection
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

This script populates the golden_clauses database with 10-15 sample clauses
for common contract types (NDA, MSA, Service Agreement).
"""

import os
import sys
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables
load_dotenv()


class GoldenClausesPopulator:
    """Populate Golden Clauses in Cloudant"""

    def __init__(self):
        """Initialize Cloudant client"""
        self.cloudant_url = os.getenv("CLOUDANT_URL")
        self.cloudant_api_key = os.getenv("CLOUDANT_API_KEY")
        self.db_name = os.getenv("CLOUDANT_DB_GOLDEN_CLAUSES", "golden_clauses")

        if not self.cloudant_url or not self.cloudant_api_key:
            raise ValueError(
                "Missing Cloudant credentials. Please set CLOUDANT_URL and CLOUDANT_API_KEY"
            )

        # Initialize client
        authenticator = IAMAuthenticator(self.cloudant_api_key)
        self.client = CloudantV1(authenticator=authenticator)
        self.client.set_service_url(self.cloudant_url)

        print(f"✓ Connected to Cloudant: {self.cloudant_url}")
        print(f"✓ Target database: {self.db_name}")

    def get_golden_clauses(self) -> List[Dict]:
        """Get sample Golden Clauses for common contract types"""
        return [
            # NDA Clauses
            {
                "_id": "golden_nda_001",
                "clause_id": "golden_nda_001",
                "type": "confidentiality",
                "contract_types": ["NDA"],
                "text": "The Receiving Party agrees to hold and maintain the Confidential Information in strictest confidence for the sole and exclusive benefit of the Disclosing Party. The Receiving Party shall not, without prior written approval of the Disclosing Party, use for its own benefit, publish, copy, or otherwise disclose to others, or permit the use by others for their benefit or to the detriment of the Disclosing Party, any Confidential Information.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "High",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["confidentiality", "nda", "disclosure", "protection"],
            },
            {
                "_id": "golden_nda_002",
                "clause_id": "golden_nda_002",
                "type": "term_duration",
                "contract_types": ["NDA"],
                "text": "This Agreement shall remain in effect for a period of three (3) years from the Effective Date. The obligations of the Receiving Party under this Agreement shall survive termination and continue for a period of five (5) years from the date of disclosure of the Confidential Information.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "Medium",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["term", "duration", "nda", "survival"],
            },
            {
                "_id": "golden_nda_003",
                "clause_id": "golden_nda_003",
                "type": "return_destruction",
                "contract_types": ["NDA"],
                "text": "Upon termination of this Agreement or upon request by the Disclosing Party, the Receiving Party shall promptly return all Confidential Information and all copies, notes, or extracts thereof, or certify in writing the destruction of such materials.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "Medium",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["return", "destruction", "nda", "termination"],
            },
            # MSA Clauses
            {
                "_id": "golden_msa_001",
                "clause_id": "golden_msa_001",
                "type": "liability_cap",
                "contract_types": ["MSA", "Service Agreement"],
                "text": "Except for breaches of confidentiality obligations, intellectual property infringement, or gross negligence, each party's total liability under this Agreement shall be limited to the lesser of (i) one million dollars ($1,000,000) or (ii) the total fees paid or payable under this Agreement in the twelve (12) months preceding the claim.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "High",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["liability", "cap", "limitation", "damages"],
            },
            {
                "_id": "golden_msa_002",
                "clause_id": "golden_msa_002",
                "type": "indemnification",
                "contract_types": ["MSA", "Service Agreement"],
                "text": "Each party shall indemnify, defend, and hold harmless the other party from and against any and all claims, damages, losses, and expenses (including reasonable attorneys' fees) arising out of or resulting from (i) breach of this Agreement, (ii) negligence or willful misconduct, or (iii) violation of applicable laws or regulations.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "High",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["indemnification", "defense", "hold-harmless", "claims"],
            },
            {
                "_id": "golden_msa_003",
                "clause_id": "golden_msa_003",
                "type": "termination",
                "contract_types": ["MSA", "Service Agreement"],
                "text": "Either party may terminate this Agreement for convenience upon ninety (90) days' prior written notice. Either party may terminate this Agreement immediately upon written notice if the other party materially breaches this Agreement and fails to cure such breach within thirty (30) days after receiving written notice thereof.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "Medium",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["termination", "breach", "cure", "notice"],
            },
            {
                "_id": "golden_msa_004",
                "clause_id": "golden_msa_004",
                "type": "data_protection",
                "contract_types": ["MSA", "Service Agreement"],
                "text": "Service Provider shall implement and maintain appropriate technical and organizational measures to protect Personal Data against unauthorized or unlawful processing and against accidental loss, destruction, damage, alteration, or disclosure. Service Provider shall comply with all applicable data protection laws, including but not limited to GDPR, CCPA, and other relevant regulations.",
                "jurisdiction": "Multi-Jurisdiction",
                "mandatory": True,
                "risk_level": "High",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["data-protection", "privacy", "gdpr", "ccpa", "security"],
            },
            # Service Agreement Clauses
            {
                "_id": "golden_svc_001",
                "clause_id": "golden_svc_001",
                "type": "service_level",
                "contract_types": ["Service Agreement"],
                "text": "Service Provider shall provide the Services with an uptime guarantee of 99.9% measured on a monthly basis, excluding scheduled maintenance windows. Service Provider shall provide at least seventy-two (72) hours' advance notice for scheduled maintenance.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "Medium",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["sla", "uptime", "availability", "maintenance"],
            },
            {
                "_id": "golden_svc_002",
                "clause_id": "golden_svc_002",
                "type": "payment_terms",
                "contract_types": ["Service Agreement", "MSA"],
                "text": "Client shall pay all fees within thirty (30) days of the invoice date. Late payments shall accrue interest at the rate of 1.5% per month or the maximum rate permitted by law, whichever is less. Service Provider may suspend Services if payment is more than sixty (60) days overdue.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "Medium",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["payment", "fees", "invoice", "late-payment"],
            },
            {
                "_id": "golden_svc_003",
                "clause_id": "golden_svc_003",
                "type": "intellectual_property",
                "contract_types": ["Service Agreement", "MSA"],
                "text": "All intellectual property rights in the Services and any deliverables created by Service Provider shall remain the exclusive property of Service Provider. Client is granted a non-exclusive, non-transferable license to use the Services and deliverables solely for Client's internal business purposes during the term of this Agreement.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "High",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["intellectual-property", "ip", "ownership", "license"],
            },
            # Cross-Contract Clauses
            {
                "_id": "golden_common_001",
                "clause_id": "golden_common_001",
                "type": "governing_law",
                "contract_types": ["NDA", "MSA", "Service Agreement"],
                "text": "This Agreement shall be governed by and construed in accordance with the laws of the State of New York, without regard to its conflict of law provisions. Any disputes arising under this Agreement shall be subject to the exclusive jurisdiction of the state and federal courts located in New York County, New York.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "Low",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["governing-law", "jurisdiction", "venue", "disputes"],
            },
            {
                "_id": "golden_common_002",
                "clause_id": "golden_common_002",
                "type": "force_majeure",
                "contract_types": ["MSA", "Service Agreement"],
                "text": "Neither party shall be liable for any failure or delay in performance due to causes beyond its reasonable control, including but not limited to acts of God, war, terrorism, riots, embargoes, acts of civil or military authorities, fire, floods, accidents, pandemics, strikes, or shortages of transportation, facilities, fuel, energy, labor, or materials.",
                "jurisdiction": "US",
                "mandatory": False,
                "risk_level": "Low",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["force-majeure", "excusable-delay", "acts-of-god"],
            },
            {
                "_id": "golden_common_003",
                "clause_id": "golden_common_003",
                "type": "assignment",
                "contract_types": ["NDA", "MSA", "Service Agreement"],
                "text": "Neither party may assign or transfer this Agreement or any rights or obligations hereunder without the prior written consent of the other party, except that either party may assign this Agreement to a successor in connection with a merger, acquisition, or sale of all or substantially all of its assets.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "Low",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": ["assignment", "transfer", "succession", "merger"],
            },
            {
                "_id": "golden_common_004",
                "clause_id": "golden_common_004",
                "type": "entire_agreement",
                "contract_types": ["NDA", "MSA", "Service Agreement"],
                "text": "This Agreement constitutes the entire agreement between the parties concerning the subject matter hereof and supersedes all prior or contemporaneous agreements, understandings, negotiations, and discussions, whether oral or written. This Agreement may only be amended by a written document signed by both parties.",
                "jurisdiction": "US",
                "mandatory": True,
                "risk_level": "Low",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": [
                    "entire-agreement",
                    "integration",
                    "amendment",
                    "modification",
                ],
            },
            {
                "_id": "golden_common_005",
                "clause_id": "golden_common_005",
                "type": "data_breach_notification",
                "contract_types": ["MSA", "Service Agreement"],
                "text": "Notwithstanding any other provision of this Agreement, in the event of a data breach involving Personal Data, the party experiencing the breach shall notify the other party within seventy-two (72) hours of becoming aware of the breach. Liability for data breaches shall be governed separately under applicable data protection laws and shall not be subject to the general liability cap set forth in this Agreement.",
                "jurisdiction": "Multi-Jurisdiction",
                "mandatory": True,
                "risk_level": "High",
                "last_reviewed": datetime.now().isoformat(),
                "approved_by": "General Counsel",
                "tags": [
                    "data-breach",
                    "notification",
                    "gdpr",
                    "ccpa",
                    "liability-carve-out",
                ],
            },
        ]

    def populate_clauses(self) -> bool:
        """Populate Golden Clauses in Cloudant"""
        print(f"\n📚 Populating Golden Clauses in '{self.db_name}'...")

        clauses = self.get_golden_clauses()
        success_count = 0
        error_count = 0

        for clause in clauses:
            try:
                # Check if clause already exists
                try:
                    self.client.get_document(db=self.db_name, doc_id=clause["_id"])
                    print(f"  Clause '{clause['clause_id']}' already exists, skipping...")
                    continue
                except Exception:
                    # Clause doesn't exist, create it
                    pass

                # Create document
                document = Document(**clause)
                self.client.post_document(db=self.db_name, document=document)
                print(f"✓ Added clause: {clause['clause_id']} ({clause['type']})")
                success_count += 1
            except Exception as e:
                print(f"✗ Failed to add clause '{clause['clause_id']}': {e}")
                error_count += 1

        print(f"\n✅ Successfully added {success_count} Golden Clauses")
        if error_count > 0:
            print(f"⚠️  {error_count} clauses failed to add")

        return error_count == 0

    def verify_population(self):
        """Verify Golden Clauses were populated correctly"""
        print(f"\n🔍 Verifying Golden Clauses in '{self.db_name}'...")

        try:
            # Get database info
            db_info = self.client.get_database_information(db=self.db_name).get_result()
            doc_count = db_info.get("doc_count", 0)

            print(f"✓ Total documents in database: {doc_count}")

            # Query by contract type
            contract_types = ["NDA", "MSA", "Service Agreement"]
            for contract_type in contract_types:
                result = self.client.post_find(
                    db=self.db_name,
                    selector={"contract_types": {"$elemMatch": {"$eq": contract_type}}},
                    limit=100,
                ).get_result()

                count = len(result.get("docs", []))
                print(f"  {contract_type}: {count} clauses")

            print("\n✅ Golden Clauses verification complete!")
            return True
        except Exception as e:
            print(f"✗ Verification failed: {e}")
            return False

    def run_population(self):
        """Run complete population process"""
        print("=" * 70)
        print("LexConductor - Golden Clauses Population")
        print("IBM Dev Day AI Demystified Hackathon 2026")
        print("=" * 70)

        try:
            # Populate clauses
            success = self.populate_clauses()

            # Verify population
            self.verify_population()

            print("\n" + "=" * 70)
            print("✅ Golden Clauses population complete!")
            print("=" * 70)
            print("\nNext steps:")
            print("1. Run: python scripts/populate_historical_decisions.py")
            print("2. Run: python scripts/setup_cos_buckets.py")
            print("=" * 70)

            return success
        except Exception as e:
            print(f"\n✗ Population failed: {e}")
            return False


def main():
    """Main entry point"""
    try:
        populator = GoldenClausesPopulator()
        success = populator.run_population()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
