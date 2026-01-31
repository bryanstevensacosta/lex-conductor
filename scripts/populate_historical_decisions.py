#!/usr/bin/env python3
"""
Populate Historical Decisions Collection
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

This script populates the historical_decisions database with 5-10 sample
historical decisions for common scenarios (NDA, MSA, Service Agreement).
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables
load_dotenv()


class HistoricalDecisionsPopulator:
    """Populate Historical Decisions in Cloudant"""

    def __init__(self):
        """Initialize Cloudant client"""
        self.cloudant_url = os.getenv("CLOUDANT_URL")
        self.cloudant_api_key = os.getenv("CLOUDANT_API_KEY")
        self.db_name = os.getenv("CLOUDANT_DB_HISTORICAL_DECISIONS", "historical_decisions")

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

    def get_historical_decisions(self) -> List[Dict]:
        """Get sample historical decisions"""
        # Generate dates for the past 6 months
        base_date = datetime.now()

        return [
            # NDA Decisions
            {
                "_id": "dec_2025_Q4_001",
                "decision_id": "dec_2025_Q4_001",
                "contract_type": "NDA",
                "contract_id": "NDA-2025-1215-042",
                "clause_modified": "Section 4 - Indemnification",
                "original_text": "Party A shall indemnify Party B for all claims arising from this Agreement.",
                "modified_text": "Party A shall indemnify Party B for all claims arising from this Agreement, except those arising from data breaches which shall be governed separately under Section 8 in accordance with applicable data protection laws including GDPR and CCPA.",
                "rationale": "CCPA 2026 Amendment requires separate treatment of data breach liability. Data breach indemnification must be carved out from general liability cap to ensure compliance with California privacy law requirements.",
                "approved_by": "Head of Legal",
                "date": (base_date - timedelta(days=45)).isoformat(),
                "jurisdiction": "US",
                "confidence": 0.95,
                "tags": ["data-breach", "liability-cap", "ccpa", "indemnification"],
                "regulatory_basis": ["CCPA_2026", "CPRA_2023"],
            },
            {
                "_id": "dec_2025_Q4_002",
                "decision_id": "dec_2025_Q4_002",
                "contract_type": "NDA",
                "contract_id": "NDA-2025-1201-018",
                "clause_modified": "Section 2 - Confidential Information Definition",
                "original_text": "Confidential Information means any information disclosed by one party to the other.",
                "modified_text": "Confidential Information means any information disclosed by one party to the other, excluding information that: (a) is or becomes publicly available through no breach of this Agreement; (b) was rightfully in the receiving party's possession prior to disclosure; (c) is independently developed without use of Confidential Information; or (d) is rightfully received from a third party without breach of confidentiality obligations.",
                "rationale": "Standard exclusions from confidentiality obligations are necessary to avoid overly broad restrictions that could be challenged in court. These exclusions align with industry best practices and reduce legal risk.",
                "approved_by": "General Counsel",
                "date": (base_date - timedelta(days=60)).isoformat(),
                "jurisdiction": "US",
                "confidence": 0.92,
                "tags": [
                    "confidentiality",
                    "definition",
                    "exclusions",
                    "best-practices",
                ],
                "regulatory_basis": [],
            },
            # MSA Decisions
            {
                "_id": "dec_2025_Q3_003",
                "decision_id": "dec_2025_Q3_003",
                "contract_type": "MSA",
                "contract_id": "MSA-2025-0915-127",
                "clause_modified": "Section 7 - Limitation of Liability",
                "original_text": "Each party's total liability shall be limited to the fees paid in the preceding 12 months.",
                "modified_text": "Each party's total liability shall be limited to the lesser of (i) $1,000,000 or (ii) the fees paid in the preceding 12 months, except for: (a) breaches of confidentiality; (b) intellectual property infringement; (c) data breaches involving Personal Data; (d) gross negligence or willful misconduct; and (e) indemnification obligations.",
                "rationale": "Carve-outs from liability cap are essential for high-risk scenarios. Data breach liability must be unlimited to comply with GDPR Article 82 and CCPA Section 1798.150, which allow statutory damages regardless of contractual limitations.",
                "approved_by": "General Counsel",
                "date": (base_date - timedelta(days=107)).isoformat(),
                "jurisdiction": "Multi-Jurisdiction",
                "confidence": 0.97,
                "tags": ["liability-cap", "carve-outs", "gdpr", "ccpa", "data-breach"],
                "regulatory_basis": ["GDPR_Article_82", "CCPA_1798.150"],
            },
            {
                "_id": "dec_2025_Q3_004",
                "decision_id": "dec_2025_Q3_004",
                "contract_type": "MSA",
                "contract_id": "MSA-2025-0830-089",
                "clause_modified": "Section 9 - Data Processing",
                "original_text": "Service Provider may process Client data as necessary to provide the Services.",
                "modified_text": "Service Provider shall process Personal Data only on documented instructions from Client, including with regard to transfers of Personal Data to third countries or international organizations. Service Provider shall implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk, including encryption, pseudonymization, and regular security testing. Service Provider shall notify Client without undue delay upon becoming aware of a Personal Data breach.",
                "rationale": "GDPR Article 28 requires specific data processing terms in contracts between controllers and processors. The original clause was insufficient to meet GDPR requirements for data processing agreements. Added mandatory GDPR Article 28 provisions.",
                "approved_by": "Head of Legal",
                "date": (base_date - timedelta(days=123)).isoformat(),
                "jurisdiction": "EU",
                "confidence": 0.98,
                "tags": ["data-processing", "gdpr", "article-28", "dpa", "security"],
                "regulatory_basis": ["GDPR_Article_28", "GDPR_Article_32"],
            },
            # Service Agreement Decisions
            {
                "_id": "dec_2025_Q4_005",
                "decision_id": "dec_2025_Q4_005",
                "contract_type": "Service Agreement",
                "contract_id": "SVC-2025-1110-203",
                "clause_modified": "Section 5 - Service Level Agreement",
                "original_text": "Service Provider shall use commercially reasonable efforts to maintain 99% uptime.",
                "modified_text": "Service Provider shall maintain 99.9% uptime measured monthly, excluding scheduled maintenance windows (maximum 4 hours per month with 72 hours' notice). If uptime falls below 99.9%, Client shall receive service credits: 99.0-99.9% = 10% credit; 95.0-99.0% = 25% credit; below 95.0% = 50% credit. Credits are Client's sole remedy for SLA breaches.",
                "rationale": "Vague 'commercially reasonable efforts' language creates ambiguity and potential disputes. Specific uptime targets with measurable service credits provide clear expectations and remedies. Industry standard for SaaS is 99.9% uptime.",
                "approved_by": "Head of Legal",
                "date": (base_date - timedelta(days=51)).isoformat(),
                "jurisdiction": "US",
                "confidence": 0.89,
                "tags": ["sla", "uptime", "service-credits", "remedies", "saas"],
                "regulatory_basis": [],
            },
            {
                "_id": "dec_2025_Q3_006",
                "decision_id": "dec_2025_Q3_006",
                "contract_type": "Service Agreement",
                "contract_id": "SVC-2025-0920-156",
                "clause_modified": "Section 11 - Termination for Convenience",
                "original_text": "Either party may terminate this Agreement at any time with 30 days' notice.",
                "modified_text": "Either party may terminate this Agreement for convenience upon 90 days' prior written notice. Client shall pay all fees for Services provided through the termination date plus any early termination fees specified in the applicable Statement of Work. Service Provider shall provide reasonable assistance with data export and transition for 30 days following termination.",
                "rationale": "30-day termination period is insufficient for enterprise services requiring transition planning. 90-day notice period is industry standard for B2B services. Added data export and transition assistance obligations to protect Client's business continuity.",
                "approved_by": "General Counsel",
                "date": (base_date - timedelta(days=102)).isoformat(),
                "jurisdiction": "US",
                "confidence": 0.91,
                "tags": ["termination", "notice-period", "transition", "data-export"],
                "regulatory_basis": [],
            },
            {
                "_id": "dec_2025_Q4_007",
                "decision_id": "dec_2025_Q4_007",
                "contract_type": "Service Agreement",
                "contract_id": "SVC-2025-1205-241",
                "clause_modified": "Section 6 - Intellectual Property Rights",
                "original_text": "All deliverables created under this Agreement shall be owned by Service Provider.",
                "modified_text": "All pre-existing intellectual property of each party shall remain the sole property of that party. Deliverables created specifically for Client under this Agreement shall be owned by Client upon full payment. Service Provider retains ownership of all general methodologies, tools, and know-how developed independently. Client grants Service Provider a license to use Client's trademarks solely for providing the Services.",
                "rationale": "Blanket Service Provider ownership of all deliverables is unfavorable to Client and may prevent Client from using work product paid for. Modified to provide Client ownership of custom deliverables while protecting Service Provider's pre-existing IP and general methodologies.",
                "approved_by": "Head of Legal",
                "date": (base_date - timedelta(days=26)).isoformat(),
                "jurisdiction": "US",
                "confidence": 0.94,
                "tags": [
                    "intellectual-property",
                    "ownership",
                    "deliverables",
                    "work-product",
                ],
                "regulatory_basis": [],
            },
            # Cross-Contract Decisions
            {
                "_id": "dec_2025_Q3_008",
                "decision_id": "dec_2025_Q3_008",
                "contract_type": "MSA",
                "contract_id": "MSA-2025-0905-112",
                "clause_modified": "Section 14 - Dispute Resolution",
                "original_text": "Any disputes shall be resolved in the courts of New York.",
                "modified_text": "The parties shall first attempt to resolve any dispute through good faith negotiations for 30 days. If unsuccessful, disputes shall be resolved through binding arbitration under the Commercial Arbitration Rules of the American Arbitration Association, with one arbitrator, in New York, New York. Judgment on the arbitration award may be entered in any court having jurisdiction. Notwithstanding the foregoing, either party may seek injunctive relief in court for breaches of confidentiality or intellectual property rights.",
                "rationale": "Arbitration is generally faster and less expensive than litigation for commercial disputes. Added negotiation period to encourage settlement. Preserved court access for injunctive relief where immediate action may be necessary (confidentiality breaches, IP infringement).",
                "approved_by": "General Counsel",
                "date": (base_date - timedelta(days=117)).isoformat(),
                "jurisdiction": "US",
                "confidence": 0.88,
                "tags": [
                    "dispute-resolution",
                    "arbitration",
                    "aaa",
                    "injunctive-relief",
                ],
                "regulatory_basis": [],
            },
            {
                "_id": "dec_2025_Q4_009",
                "decision_id": "dec_2025_Q4_009",
                "contract_type": "Service Agreement",
                "contract_id": "SVC-2025-1118-219",
                "clause_modified": "Section 8 - Insurance Requirements",
                "original_text": "Service Provider shall maintain general liability insurance.",
                "modified_text": "Service Provider shall maintain the following insurance coverage with insurers rated A- or better by A.M. Best: (a) Commercial General Liability: $2,000,000 per occurrence / $5,000,000 aggregate; (b) Professional Liability (E&O): $2,000,000 per claim / $5,000,000 aggregate; (c) Cyber Liability: $5,000,000 per occurrence covering data breaches and privacy violations; (d) Workers' Compensation: statutory limits. Service Provider shall name Client as additional insured and provide certificates of insurance annually.",
                "rationale": "Vague insurance requirement provides no protection. Specific coverage amounts and types are necessary to ensure adequate protection for Client. Cyber liability insurance is critical for service providers handling Client data. Coverage amounts based on industry standards for similar services.",
                "approved_by": "Head of Legal",
                "date": (base_date - timedelta(days=43)).isoformat(),
                "jurisdiction": "US",
                "confidence": 0.93,
                "tags": [
                    "insurance",
                    "liability",
                    "cyber-insurance",
                    "coverage-amounts",
                ],
                "regulatory_basis": [],
            },
            {
                "_id": "dec_2025_Q3_010",
                "decision_id": "dec_2025_Q3_010",
                "contract_type": "NDA",
                "contract_id": "NDA-2025-0910-073",
                "clause_modified": "Section 6 - Remedies",
                "original_text": "Breach of this Agreement may result in damages.",
                "modified_text": "The parties acknowledge that breach of confidentiality obligations will cause irreparable harm for which monetary damages are an inadequate remedy. Accordingly, in addition to any other remedies available at law or in equity, the non-breaching party shall be entitled to seek injunctive relief without the necessity of posting a bond. The prevailing party in any action to enforce this Agreement shall be entitled to recover reasonable attorneys' fees and costs.",
                "rationale": "Confidentiality breaches often require immediate injunctive relief to prevent further disclosure. Standard remedy language ensures the non-breaching party can obtain emergency court orders. Attorney fee provision encourages compliance and provides cost recovery for enforcement.",
                "approved_by": "General Counsel",
                "date": (base_date - timedelta(days=112)).isoformat(),
                "jurisdiction": "US",
                "confidence": 0.96,
                "tags": [
                    "remedies",
                    "injunctive-relief",
                    "attorneys-fees",
                    "enforcement",
                ],
                "regulatory_basis": [],
            },
        ]

    def populate_decisions(self) -> bool:
        """Populate historical decisions in Cloudant"""
        print(f"\n📜 Populating historical decisions in '{self.db_name}'...")

        decisions = self.get_historical_decisions()
        success_count = 0
        error_count = 0

        for decision in decisions:
            try:
                # Check if decision already exists
                try:
                    self.client.get_document(db=self.db_name, doc_id=decision["_id"])
                    print(f"  Decision '{decision['decision_id']}' already exists, skipping...")
                    continue
                except Exception:
                    pass

                # Create document
                document = Document(**decision)
                self.client.post_document(db=self.db_name, document=document)
                print(f"✓ Added decision: {decision['decision_id']} ({decision['contract_type']})")
                success_count += 1
            except Exception as e:
                print(f"✗ Failed to add decision '{decision['decision_id']}': {e}")
                error_count += 1

        print(f"\n✅ Successfully added {success_count} historical decisions")
        if error_count > 0:
            print(f"⚠️  {error_count} decisions failed to add")

        return error_count == 0

    def verify_population(self):
        """Verify historical decisions were populated correctly"""
        print(f"\n🔍 Verifying historical decisions in '{self.db_name}'...")

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
                    selector={"contract_type": contract_type},
                    limit=100,
                ).get_result()

                count = len(result.get("docs", []))
                print(f"  {contract_type}: {count} decisions")

            # Query by jurisdiction
            jurisdictions = ["US", "EU", "UK", "Multi-Jurisdiction"]
            print("\nBy jurisdiction:")
            for jurisdiction in jurisdictions:
                result = self.client.post_find(
                    db=self.db_name, selector={"jurisdiction": jurisdiction}, limit=100
                ).get_result()

                count = len(result.get("docs", []))
                if count > 0:
                    print(f"  {jurisdiction}: {count} decisions")

            # Query high confidence decisions
            result = self.client.post_find(
                db=self.db_name, selector={"confidence": {"$gte": 0.9}}, limit=100
            ).get_result()
            high_confidence_count = len(result.get("docs", []))
            print(f"\nHigh confidence (≥0.9): {high_confidence_count} decisions")

            print("\n✅ Historical decisions verification complete!")
            return True
        except Exception as e:
            print(f"✗ Verification failed: {e}")
            return False

    def run_population(self):
        """Run complete population process"""
        print("=" * 70)
        print("LexConductor - Historical Decisions Population")
        print("IBM Dev Day AI Demystified Hackathon 2026")
        print("=" * 70)

        try:
            # Populate decisions
            success = self.populate_decisions()

            # Verify population
            self.verify_population()

            print("\n" + "=" * 70)
            print("✅ Historical decisions population complete!")
            print("=" * 70)
            print("\nData layer setup complete! All databases populated:")
            print("  ✓ Golden Clauses: 15 clauses")
            print("  ✓ Historical Decisions: 10 precedents")
            print("  ✓ Regulatory Mappings: 13 regulations")
            print("\nNext steps:")
            print("1. Upload regulatory PDFs to COS (if not done)")
            print("2. Verify complete data layer: python scripts/verify_data_layer.py")
            print("3. Start implementing agents: Task 3 in tasks.md")
            print("=" * 70)

            return success
        except Exception as e:
            print(f"\n✗ Population failed: {e}")
            return False


def main():
    """Main entry point"""
    try:
        populator = HistoricalDecisionsPopulator()
        success = populator.run_population()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
