#!/usr/bin/env python3
"""
Setup Cloud Object Storage Buckets and Upload Regulatory Documents
IBM Dev Day AI Demystified Hackathon 2026
Team: AI Kings 👑

This script:
1. Creates the COS bucket: watsonx-hackathon-regulations
2. Creates folder structure: EU/, UK/, US/, templates/
3. Creates regulatory_mappings in Cloudant linking to COS URLs
4. Provides instructions for uploading regulatory PDFs
"""

import os
import sys
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
import ibm_boto3
from ibm_botocore.client import Config
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables
load_dotenv()


class COSBucketSetup:
    """Setup Cloud Object Storage buckets and regulatory mappings"""

    def __init__(self):
        """Initialize COS and Cloudant clients"""
        # COS credentials
        self.cos_api_key = os.getenv("COS_API_KEY")
        self.cos_instance_id = os.getenv("COS_INSTANCE_ID")
        self.cos_endpoint = os.getenv(
            "COS_ENDPOINT", "s3.us-south.cloud-object-storage.appdomain.cloud"
        )
        self.cos_auth_endpoint = os.getenv(
            "COS_AUTH_ENDPOINT", "https://iam.cloud.ibm.com/identity/token"
        )
        self.bucket_name = os.getenv("COS_BUCKET_NAME", "watsonx-hackathon-regulations")

        # Cloudant credentials
        self.cloudant_url = os.getenv("CLOUDANT_URL")
        self.cloudant_api_key = os.getenv("CLOUDANT_API_KEY")
        self.mappings_db = os.getenv("CLOUDANT_DB_REGULATORY_MAPPINGS", "regulatory_mappings")

        if not all(
            [
                self.cos_api_key,
                self.cos_instance_id,
                self.cloudant_url,
                self.cloudant_api_key,
            ]
        ):
            raise ValueError(
                "Missing credentials. Please set COS_API_KEY, COS_INSTANCE_ID, "
                "CLOUDANT_URL, and CLOUDANT_API_KEY in your .env file"
            )

        # Initialize COS client
        self.cos_client = ibm_boto3.client(
            "s3",
            ibm_api_key_id=self.cos_api_key,
            ibm_service_instance_id=self.cos_instance_id,
            ibm_auth_endpoint=self.cos_auth_endpoint,
            config=Config(signature_version="oauth"),
            endpoint_url=f"https://{self.cos_endpoint}",
        )

        # Initialize Cloudant client
        authenticator = IAMAuthenticator(self.cloudant_api_key)
        self.cloudant_client = CloudantV1(authenticator=authenticator)
        self.cloudant_client.set_service_url(self.cloudant_url)

        print(f"✓ Connected to COS: {self.cos_endpoint}")
        print(f"✓ Connected to Cloudant: {self.cloudant_url}")

    def create_bucket(self) -> bool:
        """Create COS bucket if it doesn't exist"""
        print(f"\n🪣 Creating bucket: {self.bucket_name}...")

        try:
            # Check if bucket exists
            self.cos_client.head_bucket(Bucket=self.bucket_name)
            print(f"  Bucket '{self.bucket_name}' already exists")
            return False
        except Exception:
            # Bucket doesn't exist, create it
            try:
                self.cos_client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": "us-south-standard"},
                )
                print(f"✓ Created bucket: {self.bucket_name}")
                return True
            except Exception as e:
                print(f"✗ Failed to create bucket: {e}")
                raise

    def create_folder_structure(self):
        """Create folder structure in COS bucket"""
        print("\n📁 Creating folder structure...")

        folders = ["EU/", "UK/", "US/", "templates/"]

        for folder in folders:
            try:
                # Create empty object to represent folder
                self.cos_client.put_object(Bucket=self.bucket_name, Key=folder, Body=b"")
                print(f"✓ Created folder: {folder}")
            except Exception as e:
                print(f"✗ Failed to create folder '{folder}': {e}")

    def get_regulatory_mappings(self) -> List[Dict]:
        """Get regulatory document mappings"""
        base_url = f"https://{self.cos_endpoint}/{self.bucket_name}"

        return [
            # EU Regulations
            {
                "_id": "reg_eu_gdpr",
                "regulation_id": "reg_eu_gdpr",
                "regulation_name": "General Data Protection Regulation (GDPR)",
                "regulation_type": "Data Protection",
                "jurisdiction": "EU",
                "effective_date": "2018-05-25",
                "cos_url": f"{base_url}/EU/GDPR_Regulation_2016_679.pdf",
                "cos_key": "EU/GDPR_Regulation_2016_679.pdf",
                "description": "EU regulation on data protection and privacy",
                "key_requirements": [
                    "Data breach notification within 72 hours",
                    "Right to erasure (right to be forgotten)",
                    "Data protection by design and by default",
                    "Consent requirements for data processing",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["gdpr", "data-protection", "privacy", "eu"],
            },
            {
                "_id": "reg_eu_ai_act",
                "regulation_id": "reg_eu_ai_act",
                "regulation_name": "EU Artificial Intelligence Act",
                "regulation_type": "AI Regulation",
                "jurisdiction": "EU",
                "effective_date": "2024-08-01",
                "cos_url": f"{base_url}/EU/EU_AI_Act_2024.pdf",
                "cos_key": "EU/EU_AI_Act_2024.pdf",
                "description": "EU regulation on artificial intelligence systems",
                "key_requirements": [
                    "Risk-based approach to AI systems",
                    "Transparency and explainability requirements",
                    "Human oversight for high-risk AI",
                    "Prohibited AI practices",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["ai-act", "artificial-intelligence", "eu", "regulation"],
            },
            {
                "_id": "reg_eu_dma",
                "regulation_id": "reg_eu_dma",
                "regulation_name": "Digital Markets Act (DMA)",
                "regulation_type": "Competition",
                "jurisdiction": "EU",
                "effective_date": "2023-05-02",
                "cos_url": f"{base_url}/EU/Digital_Markets_Act_2022.pdf",
                "cos_key": "EU/Digital_Markets_Act_2022.pdf",
                "description": "EU regulation on digital platform gatekeepers",
                "key_requirements": [
                    "Gatekeeper obligations",
                    "Interoperability requirements",
                    "Data portability",
                    "Fair competition practices",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["dma", "competition", "digital-markets", "eu"],
            },
            # UK Regulations
            {
                "_id": "reg_uk_dpa",
                "regulation_id": "reg_uk_dpa",
                "regulation_name": "UK Data Protection Act 2018",
                "regulation_type": "Data Protection",
                "jurisdiction": "UK",
                "effective_date": "2018-05-25",
                "cos_url": f"{base_url}/UK/UK_Data_Protection_Act_2018.pdf",
                "cos_key": "UK/UK_Data_Protection_Act_2018.pdf",
                "description": "UK implementation of GDPR and additional provisions",
                "key_requirements": [
                    "GDPR compliance requirements",
                    "UK-specific data protection provisions",
                    "ICO enforcement powers",
                    "Data subject rights",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["dpa", "data-protection", "gdpr", "uk"],
            },
            {
                "_id": "reg_uk_online_safety",
                "regulation_id": "reg_uk_online_safety",
                "regulation_name": "Online Safety Act 2023",
                "regulation_type": "Online Safety",
                "jurisdiction": "UK",
                "effective_date": "2023-10-26",
                "cos_url": f"{base_url}/UK/Online_Safety_Act_2023.pdf",
                "cos_key": "UK/Online_Safety_Act_2023.pdf",
                "description": "UK regulation on online content and platform safety",
                "key_requirements": [
                    "Duty of care for users",
                    "Content moderation requirements",
                    "Age verification",
                    "Transparency reporting",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["online-safety", "content-moderation", "uk"],
            },
            # US Regulations
            {
                "_id": "reg_us_ccpa",
                "regulation_id": "reg_us_ccpa",
                "regulation_name": "California Consumer Privacy Act (CCPA)",
                "regulation_type": "Data Protection",
                "jurisdiction": "US",
                "effective_date": "2020-01-01",
                "cos_url": f"{base_url}/US/CCPA_California_Civil_Code_1798.pdf",
                "cos_key": "US/CCPA_California_Civil_Code_1798.pdf",
                "description": "California state law on consumer data privacy",
                "key_requirements": [
                    "Right to know what data is collected",
                    "Right to delete personal information",
                    "Right to opt-out of data sale",
                    "Non-discrimination for exercising rights",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["ccpa", "data-protection", "privacy", "california", "us"],
            },
            {
                "_id": "reg_us_cpra",
                "regulation_id": "reg_us_cpra",
                "regulation_name": "California Privacy Rights Act (CPRA)",
                "regulation_type": "Data Protection",
                "jurisdiction": "US",
                "effective_date": "2023-01-01",
                "cos_url": f"{base_url}/US/CPRA_Amendment_2020.pdf",
                "cos_key": "US/CPRA_Amendment_2020.pdf",
                "description": "Amendment to CCPA with enhanced privacy protections",
                "key_requirements": [
                    "Sensitive personal information protections",
                    "Right to correct inaccurate data",
                    "Data minimization requirements",
                    "California Privacy Protection Agency enforcement",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["cpra", "ccpa", "data-protection", "california", "us"],
            },
            {
                "_id": "reg_us_hipaa",
                "regulation_id": "reg_us_hipaa",
                "regulation_name": "Health Insurance Portability and Accountability Act (HIPAA)",
                "regulation_type": "Healthcare Privacy",
                "jurisdiction": "US",
                "effective_date": "1996-08-21",
                "cos_url": f"{base_url}/US/HIPAA_Privacy_Rule.pdf",
                "cos_key": "US/HIPAA_Privacy_Rule.pdf",
                "description": "US federal law on healthcare data privacy and security",
                "key_requirements": [
                    "Protected Health Information (PHI) safeguards",
                    "Business Associate Agreements",
                    "Breach notification requirements",
                    "Patient rights to access records",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["hipaa", "healthcare", "phi", "privacy", "us"],
            },
            {
                "_id": "reg_us_sox",
                "regulation_id": "reg_us_sox",
                "regulation_name": "Sarbanes-Oxley Act (SOX)",
                "regulation_type": "Financial Compliance",
                "jurisdiction": "US",
                "effective_date": "2002-07-30",
                "cos_url": f"{base_url}/US/Sarbanes_Oxley_Act_2002.pdf",
                "cos_key": "US/Sarbanes_Oxley_Act_2002.pdf",
                "description": "US federal law on corporate financial reporting",
                "key_requirements": [
                    "Internal controls over financial reporting",
                    "CEO/CFO certification of financial statements",
                    "Audit committee independence",
                    "Document retention requirements",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["sox", "financial", "compliance", "audit", "us"],
            },
            {
                "_id": "reg_us_ftc_act",
                "regulation_id": "reg_us_ftc_act",
                "regulation_name": "Federal Trade Commission Act Section 5",
                "regulation_type": "Consumer Protection",
                "jurisdiction": "US",
                "effective_date": "1914-09-26",
                "cos_url": f"{base_url}/US/FTC_Act_Section_5.pdf",
                "cos_key": "US/FTC_Act_Section_5.pdf",
                "description": "US federal law prohibiting unfair or deceptive practices",
                "key_requirements": [
                    "Prohibition of unfair practices",
                    "Prohibition of deceptive practices",
                    "Data security requirements",
                    "Privacy policy enforcement",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["ftc", "consumer-protection", "unfair-practices", "us"],
            },
            # Multi-Jurisdiction
            {
                "_id": "reg_multi_iso27001",
                "regulation_id": "reg_multi_iso27001",
                "regulation_name": "ISO/IEC 27001:2022",
                "regulation_type": "Information Security",
                "jurisdiction": "Multi-Jurisdiction",
                "effective_date": "2022-10-25",
                "cos_url": f"{base_url}/templates/ISO_27001_2022_Standard.pdf",
                "cos_key": "templates/ISO_27001_2022_Standard.pdf",
                "description": "International standard for information security management",
                "key_requirements": [
                    "Information security management system (ISMS)",
                    "Risk assessment and treatment",
                    "Security controls implementation",
                    "Continuous improvement",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["iso27001", "information-security", "isms", "international"],
            },
            {
                "_id": "reg_multi_iso27701",
                "regulation_id": "reg_multi_iso27701",
                "regulation_name": "ISO/IEC 27701:2019",
                "regulation_type": "Privacy Management",
                "jurisdiction": "Multi-Jurisdiction",
                "effective_date": "2019-08-06",
                "cos_url": f"{base_url}/templates/ISO_27701_2019_Standard.pdf",
                "cos_key": "templates/ISO_27701_2019_Standard.pdf",
                "description": "International standard for privacy information management",
                "key_requirements": [
                    "Privacy information management system (PIMS)",
                    "PII controller requirements",
                    "PII processor requirements",
                    "GDPR mapping",
                ],
                "last_updated": datetime.now().isoformat(),
                "tags": ["iso27701", "privacy", "pims", "pii", "international"],
            },
        ]

    def populate_regulatory_mappings(self) -> bool:
        """Populate regulatory mappings in Cloudant"""
        print(f"\n⚖️  Populating regulatory mappings in '{self.mappings_db}'...")

        mappings = self.get_regulatory_mappings()
        success_count = 0
        error_count = 0

        for mapping in mappings:
            try:
                # Check if mapping already exists
                try:
                    self.cloudant_client.get_document(db=self.mappings_db, doc_id=mapping["_id"])
                    print(f"  Mapping '{mapping['regulation_id']}' already exists, skipping...")
                    continue
                except Exception:
                    pass

                # Create document
                document = Document(**mapping)
                self.cloudant_client.post_document(db=self.mappings_db, document=document)
                print(f"✓ Added mapping: {mapping['regulation_name']} ({mapping['jurisdiction']})")
                success_count += 1
            except Exception as e:
                print(f"✗ Failed to add mapping '{mapping['regulation_id']}': {e}")
                error_count += 1

        print(f"\n✅ Successfully added {success_count} regulatory mappings")
        if error_count > 0:
            print(f"⚠️  {error_count} mappings failed to add")

        return error_count == 0

    def print_upload_instructions(self):
        """Print instructions for uploading regulatory PDFs"""
        print("\n" + "=" * 70)
        print("📄 REGULATORY PDF UPLOAD INSTRUCTIONS")
        print("=" * 70)
        print("\nTo complete the setup, you need to upload regulatory PDF documents.")
        print("\nOption 1: Upload via IBM Cloud Console")
        print("  1. Go to: https://cloud.ibm.com/objectstorage")
        print(f"  2. Select bucket: {self.bucket_name}")
        print("  3. Upload PDFs to the appropriate folders (EU/, UK/, US/, templates/)")
        print("\nOption 2: Upload via AWS CLI (S3-compatible)")
        print("  1. Install AWS CLI: https://aws.amazon.com/cli/")
        print("  2. Configure credentials:")
        print(f"     aws configure set aws_access_key_id {self.cos_api_key[:10]}...")
        print("  3. Upload files:")
        print(
            f"     aws s3 cp local_file.pdf s3://{self.bucket_name}/EU/ --endpoint-url https://{self.cos_endpoint}"
        )
        print("\nOption 3: Use the provided upload script")
        print("  python scripts/upload_regulatory_pdfs.py --folder /path/to/pdfs")
        print("\n" + "=" * 70)
        print("\n📋 Required Documents (13 total):")
        print("\nEU/ (3 documents):")
        print("  - GDPR_Regulation_2016_679.pdf")
        print("  - EU_AI_Act_2024.pdf")
        print("  - Digital_Markets_Act_2022.pdf")
        print("\nUK/ (2 documents):")
        print("  - UK_Data_Protection_Act_2018.pdf")
        print("  - Online_Safety_Act_2023.pdf")
        print("\nUS/ (5 documents):")
        print("  - CCPA_California_Civil_Code_1798.pdf")
        print("  - CPRA_Amendment_2020.pdf")
        print("  - HIPAA_Privacy_Rule.pdf")
        print("  - Sarbanes_Oxley_Act_2002.pdf")
        print("  - FTC_Act_Section_5.pdf")
        print("\ntemplates/ (2 documents):")
        print("  - ISO_27001_2022_Standard.pdf")
        print("  - ISO_27701_2019_Standard.pdf")
        print("\n" + "=" * 70)
        print("\n💡 TIP: You can use publicly available regulatory documents from:")
        print("  - EUR-Lex: https://eur-lex.europa.eu/")
        print("  - UK Legislation: https://www.legislation.gov.uk/")
        print("  - US Government Publishing Office: https://www.govinfo.gov/")
        print("  - ISO: https://www.iso.org/ (standards may require purchase)")
        print("\n" + "=" * 70)

    def verify_setup(self):
        """Verify COS bucket and mappings"""
        print("\n🔍 Verifying setup...")

        try:
            # Verify bucket exists
            self.cos_client.head_bucket(Bucket=self.bucket_name)
            print(f"✓ Bucket '{self.bucket_name}' exists")

            # List objects in bucket
            response = self.cos_client.list_objects_v2(Bucket=self.bucket_name)
            object_count = response.get("KeyCount", 0)
            print(f"✓ Bucket contains {object_count} objects")

            # Verify mappings database
            db_info = self.cloudant_client.get_database_information(
                db=self.mappings_db
            ).get_result()
            doc_count = db_info.get("doc_count", 0)
            print(f"✓ Regulatory mappings database contains {doc_count} documents")

            print("\n✅ Setup verification complete!")
            return True
        except Exception as e:
            print(f"✗ Verification failed: {e}")
            return False

    def run_setup(self):
        """Run complete COS setup"""
        print("=" * 70)
        print("LexConductor - Cloud Object Storage Setup")
        print("IBM Dev Day AI Demystified Hackathon 2026")
        print("=" * 70)

        try:
            # Create bucket
            self.create_bucket()

            # Create folder structure
            self.create_folder_structure()

            # Populate regulatory mappings
            self.populate_regulatory_mappings()

            # Verify setup
            self.verify_setup()

            # Print upload instructions
            self.print_upload_instructions()

            print("\n" + "=" * 70)
            print("✅ COS setup complete!")
            print("=" * 70)
            print("\nNext steps:")
            print("1. Upload regulatory PDFs (see instructions above)")
            print("2. Run: python scripts/populate_historical_decisions.py")
            print("3. Verify all data: python scripts/verify_data_layer.py")
            print("=" * 70)

            return True
        except Exception as e:
            print(f"\n✗ Setup failed: {e}")
            return False


def main():
    """Main entry point"""
    try:
        setup = COSBucketSetup()
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
