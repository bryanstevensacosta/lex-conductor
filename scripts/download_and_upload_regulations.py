#!/usr/bin/env python3
"""
Download and Upload Regulatory Documents
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

This script downloads public regulatory documents and uploads them to COS.
For the hackathon, we create simplified text-based PDFs with key information.
"""

import os
import sys
from dotenv import load_dotenv
import ibm_boto3
from ibm_botocore.client import Config

# Load environment variables
load_dotenv()


class RegulatoryDocumentUploader:
    """Download and upload regulatory documents to COS"""

    def __init__(self):
        """Initialize COS client"""
        cos_api_key = os.getenv("COS_API_KEY")
        cos_instance_id = os.getenv("COS_INSTANCE_ID")
        cos_endpoint = os.getenv("COS_ENDPOINT", "s3.us-south.cloud-object-storage.appdomain.cloud")
        cos_auth_endpoint = os.getenv(
            "COS_AUTH_ENDPOINT", "https://iam.cloud.ibm.com/identity/token"
        )
        self.bucket_name = os.getenv("COS_BUCKET_NAME", "watsonx-hackathon-regulations")

        if not all([cos_api_key, cos_instance_id]):
            raise ValueError("Missing COS credentials. Please set COS_API_KEY and COS_INSTANCE_ID")

        # Initialize COS client
        self.cos_client = ibm_boto3.client(
            "s3",
            ibm_api_key_id=cos_api_key,
            ibm_service_instance_id=cos_instance_id,
            ibm_auth_endpoint=cos_auth_endpoint,
            config=Config(signature_version="oauth"),
            endpoint_url=f"https://{cos_endpoint}",
        )

        print(f"✓ Connected to COS: {cos_endpoint}")
        print(f"✓ Target bucket: {self.bucket_name}")

    def create_placeholder_document(
        self, regulation_name: str, jurisdiction: str, url: str, key_points: list
    ) -> bytes:
        """Create a simple text document as placeholder for actual PDF"""
        content = f"""
{'=' * 80}
{regulation_name}
{'=' * 80}

Jurisdiction: {jurisdiction}
Official Source: {url}

IMPORTANT NOTE FOR HACKATHON:
This is a placeholder document for demonstration purposes.
In production, this would be replaced with the actual regulatory PDF.

KEY REQUIREMENTS:
"""
        for i, point in enumerate(key_points, 1):
            content += f"\n{i}. {point}"

        content += f"""

{'=' * 80}
COMPLIANCE INFORMATION
{'=' * 80}

This document serves as a reference for the LexConductor system to identify
relevant regulatory requirements during contract analysis.

For actual legal compliance, please refer to the official regulatory text
at the URL provided above.

{'=' * 80}
Document generated for: IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑
{'=' * 80}
"""
        return content.encode("utf-8")

    def get_regulatory_documents(self) -> list:
        """Get list of regulatory documents to upload"""
        return [
            # EU Regulations
            {
                "key": "EU/GDPR_Regulation_2016_679.pdf",
                "name": "General Data Protection Regulation (GDPR)",
                "jurisdiction": "EU",
                "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679",
                "key_points": [
                    "Data breach notification within 72 hours (Article 33)",
                    "Right to erasure / right to be forgotten (Article 17)",
                    "Data protection by design and by default (Article 25)",
                    "Consent requirements for data processing (Article 7)",
                    "Data Protection Impact Assessments for high-risk processing (Article 35)",
                    "Appointment of Data Protection Officer when required (Article 37)",
                    "Cross-border data transfer restrictions (Chapter V)",
                    "Maximum fines: €20 million or 4% of global annual turnover",
                ],
            },
            {
                "key": "EU/EU_AI_Act_2024.pdf",
                "name": "EU Artificial Intelligence Act",
                "jurisdiction": "EU",
                "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52021PC0206",
                "key_points": [
                    "Risk-based approach: Unacceptable, High, Limited, Minimal risk",
                    "Prohibited AI practices (social scoring, manipulation, etc.)",
                    "Transparency requirements for AI systems",
                    "Human oversight for high-risk AI systems",
                    "Technical documentation and record-keeping obligations",
                    "Conformity assessments for high-risk AI",
                    "Post-market monitoring requirements",
                    "Penalties up to €30 million or 6% of global turnover",
                ],
            },
            {
                "key": "EU/Digital_Markets_Act_2022.pdf",
                "name": "Digital Markets Act (DMA)",
                "jurisdiction": "EU",
                "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925",
                "key_points": [
                    "Gatekeeper designation criteria and obligations",
                    "Interoperability requirements for messaging services",
                    "Data portability and access requirements",
                    "Prohibition of self-preferencing practices",
                    "Restrictions on combining personal data across services",
                    "Business user access to platform data",
                    "Transparency in ranking and advertising",
                    "Fines up to 10% of worldwide turnover",
                ],
            },
            # UK Regulations
            {
                "key": "UK/UK_Data_Protection_Act_2018.pdf",
                "name": "UK Data Protection Act 2018",
                "jurisdiction": "UK",
                "url": "https://www.legislation.gov.uk/ukpga/2018/12/contents",
                "key_points": [
                    "UK implementation of GDPR principles",
                    "Additional provisions for law enforcement processing",
                    "Intelligence services data processing rules",
                    "ICO enforcement powers and penalties",
                    "Data subject rights (access, rectification, erasure)",
                    "Lawful basis for processing requirements",
                    "Special category data protections",
                    "International data transfer mechanisms",
                ],
            },
            {
                "key": "UK/Online_Safety_Act_2023.pdf",
                "name": "Online Safety Act 2023",
                "jurisdiction": "UK",
                "url": "https://www.legislation.gov.uk/ukpga/2023/50/contents",
                "key_points": [
                    "Duty of care for user-generated content platforms",
                    "Illegal content removal requirements",
                    "Child safety measures and age verification",
                    "Content moderation transparency obligations",
                    "Risk assessment and mitigation duties",
                    "Ofcom regulatory oversight and enforcement",
                    "Transparency reporting requirements",
                    "Senior management liability provisions",
                ],
            },
            # US Regulations
            {
                "key": "US/CCPA_California_Civil_Code_1798.pdf",
                "name": "California Consumer Privacy Act (CCPA)",
                "jurisdiction": "US",
                "url": "https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5",
                "key_points": [
                    "Right to know what personal information is collected (§1798.100)",
                    "Right to delete personal information (§1798.105)",
                    "Right to opt-out of sale of personal information (§1798.120)",
                    "Right to non-discrimination for exercising rights (§1798.125)",
                    "Privacy policy disclosure requirements (§1798.130)",
                    "Do Not Sell My Personal Information link requirement (§1798.135)",
                    "Private right of action for data breaches (§1798.150)",
                    "Civil penalties up to $7,500 per violation (§1798.155)",
                ],
            },
            {
                "key": "US/CPRA_Amendment_2020.pdf",
                "name": "California Privacy Rights Act (CPRA)",
                "jurisdiction": "US",
                "url": "https://oag.ca.gov/privacy/ccpa",
                "key_points": [
                    "Sensitive personal information protections",
                    "Right to correct inaccurate personal information",
                    "Right to limit use of sensitive personal information",
                    "Data minimization and purpose limitation requirements",
                    "California Privacy Protection Agency (CPPA) creation",
                    "Enhanced penalties for violations involving minors",
                    "Risk assessment requirements for high-risk processing",
                    "Automated decision-making opt-out rights",
                ],
            },
            {
                "key": "US/HIPAA_Privacy_Rule.pdf",
                "name": "Health Insurance Portability and Accountability Act (HIPAA)",
                "jurisdiction": "US",
                "url": "https://www.hhs.gov/hipaa/for-professionals/privacy/index.html",
                "key_points": [
                    "Protected Health Information (PHI) safeguards",
                    "Minimum necessary standard for PHI use and disclosure",
                    "Patient rights to access and amend health records",
                    "Business Associate Agreement (BAA) requirements",
                    "Breach notification requirements (within 60 days)",
                    "Administrative, physical, and technical safeguards",
                    "Privacy policies and procedures requirements",
                    "Civil penalties up to $1.5 million per violation type per year",
                ],
            },
            {
                "key": "US/Sarbanes_Oxley_Act_2002.pdf",
                "name": "Sarbanes-Oxley Act (SOX)",
                "jurisdiction": "US",
                "url": "https://www.govinfo.gov/content/pkg/PLAW-107publ204/pdf/PLAW-107publ204.pdf",
                "key_points": [
                    "Internal controls over financial reporting (Section 404)",
                    "CEO/CFO certification of financial statements (Section 302)",
                    "Audit committee independence requirements (Section 301)",
                    "Auditor independence and rotation (Section 201-203)",
                    "Document retention requirements (Section 802)",
                    "Whistleblower protections (Section 806)",
                    "Real-time disclosure of material changes (Section 409)",
                    "Criminal penalties for securities fraud",
                ],
            },
            {
                "key": "US/FTC_Act_Section_5.pdf",
                "name": "Federal Trade Commission Act Section 5",
                "jurisdiction": "US",
                "url": "https://www.ftc.gov/legal-library/browse/statutes/federal-trade-commission-act",
                "key_points": [
                    "Prohibition of unfair or deceptive acts or practices",
                    "Reasonable data security requirements",
                    "Privacy policy enforcement and compliance",
                    "Deceptive advertising prohibitions",
                    "Unfairness standard: substantial injury, unavoidable, not outweighed by benefits",
                    "FTC enforcement authority and consent orders",
                    "Civil penalties for violations of FTC orders",
                    "Consumer redress and disgorgement remedies",
                ],
            },
            # International Standards
            {
                "key": "templates/ISO_27001_2022_Standard.pdf",
                "name": "ISO/IEC 27001:2022 Information Security Management",
                "jurisdiction": "Multi-Jurisdiction",
                "url": "https://www.iso.org/standard/27001",
                "key_points": [
                    "Information Security Management System (ISMS) framework",
                    "Risk assessment and treatment methodology",
                    "Annex A: 93 security controls across 4 themes",
                    "Context of the organization analysis",
                    "Leadership and commitment requirements",
                    "Planning and operational controls",
                    "Performance evaluation and measurement",
                    "Continual improvement through PDCA cycle",
                ],
            },
            {
                "key": "templates/ISO_27701_2019_Standard.pdf",
                "name": "ISO/IEC 27701:2019 Privacy Information Management",
                "jurisdiction": "Multi-Jurisdiction",
                "url": "https://www.iso.org/standard/71670.html",
                "key_points": [
                    "Privacy Information Management System (PIMS) extension to ISO 27001",
                    "PII controller requirements and controls",
                    "PII processor requirements and controls",
                    "GDPR mapping and compliance support",
                    "Privacy by design and by default principles",
                    "Data subject rights implementation",
                    "Cross-border data transfer controls",
                    "Privacy impact assessment guidance",
                ],
            },
        ]

    def upload_document(self, key: str, content: bytes) -> bool:
        """Upload document to COS"""
        try:
            # Check if document already exists
            try:
                self.cos_client.head_object(Bucket=self.bucket_name, Key=key)
                print(f"  Document '{key}' already exists, skipping...")
                return False
            except Exception:
                pass

            # Upload document
            self.cos_client.put_object(
                Bucket=self.bucket_name, Key=key, Body=content, ContentType="text/plain"
            )
            print(f"✓ Uploaded: {key}")
            return True
        except Exception as e:
            print(f"✗ Failed to upload '{key}': {e}")
            return False

    def run_upload(self):
        """Run complete upload process"""
        print("=" * 70)
        print("LexConductor - Regulatory Documents Upload")
        print("IBM Dev Day AI Demystified Hackathon 2026")
        print("=" * 70)
        print("\nℹ️  NOTE: For hackathon purposes, we're creating placeholder documents")
        print("   with key regulatory information. In production, these would be")
        print("   replaced with actual regulatory PDFs.")
        print()

        documents = self.get_regulatory_documents()
        success_count = 0
        skip_count = 0
        error_count = 0

        for doc in documents:
            print(f"\n📄 Processing: {doc['name']}")

            # Create placeholder document
            content = self.create_placeholder_document(
                doc["name"], doc["jurisdiction"], doc["url"], doc["key_points"]
            )

            # Upload to COS
            result = self.upload_document(doc["key"], content)
            if result:
                success_count += 1
            elif result is False:
                skip_count += 1
            else:
                error_count += 1

        # Summary
        print("\n" + "=" * 70)
        print("UPLOAD SUMMARY")
        print("=" * 70)
        print(f"✅ Successfully uploaded: {success_count} documents")
        print(f"⏭️  Skipped (already exist): {skip_count} documents")
        if error_count > 0:
            print(f"❌ Failed: {error_count} documents")

        print("\n📊 Documents by jurisdiction:")
        jurisdictions = {}
        for doc in documents:
            jur = doc["jurisdiction"]
            jurisdictions[jur] = jurisdictions.get(jur, 0) + 1

        for jur, count in jurisdictions.items():
            print(f"  {jur}: {count} documents")

        print("\n" + "=" * 70)
        print("✅ Regulatory documents upload complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Verify data layer: python scripts/verify_data_layer.py")
        print("2. Start implementing agents: Task 3 in tasks.md")
        print("=" * 70)

        return error_count == 0


def main():
    """Main entry point"""
    try:
        uploader = RegulatoryDocumentUploader()
        success = uploader.run_upload()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
