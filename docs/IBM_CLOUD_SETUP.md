# IBM Cloud Services Setup Guide

**LexConductor - IBM Dev Day AI Demystified Hackathon 2026**  
**Team: AI Kings 👑**

This guide walks you through setting up all required IBM Cloud services for the LexConductor project.

## Prerequisites

- IBM Cloud account (provided by hackathon)
- $100 credits available
- Access to watsonx Orchestrate
- Python 3.11+ installed locally

## Overview

You will set up the following services:

1. **IBM Cloudant** - NoSQL database for Golden Clauses and precedents
2. **IBM Cloud Object Storage (COS)** - Storage for regulatory PDF documents
3. **IBM Code Engine** - Serverless hosting for external agents
4. **IBM watsonx Orchestrate** - Primary orchestration platform (REQUIRED)
5. **IBM watsonx.ai** - AI inference with Granite models

**Estimated Setup Time**: 30-45 minutes  
**Estimated Cost**: <$5 (well under $100 limit)

---

## Step 1: IBM Cloudant Setup

### 1.1 Create Cloudant Instance

1. Log in to [IBM Cloud Console](https://cloud.ibm.com/)
2. Click **Create resource** (top right)
3. Search for "Cloudant"
4. Click **Cloudant** from results

### 1.2 Configure Instance

- **Plan**: Lite (Free)
- **Region**: US South (Dallas)
- **Service name**: `lexconductor-cloudant`
- **Resource group**: Default
- **Authentication method**: IAM and legacy credentials

Click **Create**

### 1.3 Get Credentials

1. Go to your Cloudant instance
2. Click **Service credentials** (left sidebar)
3. Click **New credential**
4. Name: `lexconductor-credentials`
5. Role: Manager
6. Click **Add**
7. Click **View credentials** and copy:
   - `url` → `CLOUDANT_URL`
   - `apikey` → `CLOUDANT_API_KEY`
   - `username` → `CLOUDANT_USERNAME`
   - `password` → `CLOUDANT_PASSWORD`

### 1.4 Create Databases

1. Click **Launch Dashboard** (top right)
2. Click **Create Database** (top right)
3. Create three databases:
   - `golden_clauses`
   - `historical_decisions`
   - `regulatory_mappings`
4. For each database:
   - Database name: (as above)
   - Partitioning: Non-partitioned
   - Click **Create**

### 1.5 Update .env File

```bash
CLOUDANT_URL=https://your-instance.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=your_cloudant_api_key_here
CLOUDANT_USERNAME=your_cloudant_username
CLOUDANT_PASSWORD=your_cloudant_password

CLOUDANT_DB_GOLDEN_CLAUSES=golden_clauses
CLOUDANT_DB_HISTORICAL_DECISIONS=historical_decisions
CLOUDANT_DB_REGULATORY_MAPPINGS=regulatory_mappings
```

---

## Step 2: IBM Cloud Object Storage (COS) Setup

### 2.1 Create COS Instance

1. Go to [IBM Cloud Console](https://cloud.ibm.com/)
2. Click **Create resource**
3. Search for "Object Storage"
4. Click **Cloud Object Storage**

### 2.2 Configure Instance

- **Plan**: Lite (Free - 25GB)
- **Service name**: `lexconductor-cos`
- **Resource group**: Default

Click **Create**

### 2.3 Get Credentials

1. Go to your COS instance
2. Click **Service credentials** (left sidebar)
3. Click **New credential**
4. Name: `lexconductor-cos-credentials`
5. Role: Writer
6. **Include HMAC Credential**: ON (important!)
7. Click **Add**
8. Click **View credentials** and copy:
   - `apikey` → `COS_API_KEY`
   - `iam_serviceid_crn` → `COS_INSTANCE_ID`
   - `endpoints` → Find `us-south` public endpoint

### 2.4 Create Bucket

1. Click **Buckets** (left sidebar)
2. Click **Create bucket**
3. Choose **Customize your bucket**
4. Configuration:
   - **Name**: `watsonx-hackathon-regulations` (must be globally unique)
   - **Resiliency**: Regional
   - **Location**: us-south
   - **Storage class**: Standard
5. Click **Create bucket**

### 2.5 Create Folder Structure

1. Open your bucket
2. Click **Upload** → **Folder**
3. Create folders:
   - `EU/`
   - `UK/`
   - `US/`
   - `templates/`

### 2.6 Update .env File

```bash
COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY=your_cos_api_key_here
COS_INSTANCE_ID=your_cos_instance_id_here
COS_AUTH_ENDPOINT=https://iam.cloud.ibm.com/identity/token

COS_BUCKET_NAME=watsonx-hackathon-regulations
COS_REGION=us-south
```

---

## Step 3: IBM Code Engine Setup

### 3.1 Create Code Engine Project

1. Go to [IBM Cloud Console](https://cloud.ibm.com/)
2. Click **Create resource**
3. Search for "Code Engine"
4. Click **Code Engine**

### 3.2 Configure Project

- **Location**: Osaka (jp-osa) - Required by hackathon
- **Project name**: `lexconductor-agents`
- **Resource group**: Default

Click **Create**

### 3.3 Note Project Details

1. Go to your Code Engine project
2. Note the **Project ID** and **Region**
3. You'll deploy applications here later

### 3.4 Update .env File

```bash
CODE_ENGINE_PROJECT=lexconductor-agents
CODE_ENGINE_REGION=jp-osa
```

**Note**: Application URLs will be added after deployment in Task 5.

---

## Step 4: IBM watsonx Orchestrate Setup

### 4.1 Access watsonx Orchestrate

1. Go to [IBM Cloud Console](https://cloud.ibm.com/)
2. Navigate to **Resource list**
3. Under **AI / Machine Learning**, find **watsonx Orchestrate**
4. Click to open

### 4.2 Get API Credentials

1. In watsonx Orchestrate, click **Settings** (gear icon)
2. Go to **API Details**
3. Copy:
   - **Service Instance URL** → `WO_INSTANCE`
   - Click **Generate API Key** → `WO_API_KEY`

### 4.3 Update .env File

```bash
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_watsonx_orchestrate_api_key_here
```

### 4.4 Configure ADK Environment

```bash
# Activate virtual environment
source .venv/bin/activate

# Add environment
orchestrate env add prod --instance $WO_INSTANCE --api-key $WO_API_KEY

# Activate environment
orchestrate env activate prod

# Login
orchestrate auth login
```

---

## Step 5: IBM watsonx.ai Setup

### 5.1 Access watsonx.ai

1. Go to [watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
2. Create or select a project
3. Note your **Project ID** (in project settings)

### 5.2 Get API Key

1. Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
2. Click **Create**
3. Name: `lexconductor-watsonx-key`
4. Description: "LexConductor hackathon project"
5. Click **Create**
6. **Copy the API key** (you won't see it again!)

### 5.3 Verify Granite Model Access

1. In watsonx.ai, go to **Prompt Lab**
2. Search for "granite-3-8b-instruct"
3. Verify it's available

### 5.4 Update .env File

```bash
WATSONX_API_KEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
WATSONX_TEMPERATURE=0.1
WATSONX_MAX_TOKENS=2000
```

---

## Step 6: Verify Setup

### 6.1 Run Verification Script

```bash
# Activate virtual environment
source .venv/bin/activate

# Run verification
python scripts/verify_setup.py
```

Expected output:
```
✓ Python 3.12.2 detected
✓ All dependencies installed
✓ watsonx Orchestrate ADK 2.3.0 installed
✓ .env file exists
✓ All required environment variables configured
```

### 6.2 Test Connections

```bash
# Test all service connections
python scripts/test_connections.py
```

Expected output:
```
✓ watsonx.ai: CONNECTED
✓ Cloudant: CONNECTED
✓ Cloud Object Storage: CONNECTED
✓ watsonx Orchestrate: CONNECTED
```

---

## Cost Monitoring

### Set Up Alerts

1. Go to [IBM Cloud Console](https://cloud.ibm.com/)
2. Click **Manage** → **Billing and usage**
3. Click **Spending notifications**
4. Set alerts at:
   - 25% ($25)
   - 50% ($50)
   - 80% ($80)

### Monitor Usage

Check usage regularly:
```bash
# View current usage
ibmcloud billing account-usage
```

**Budget**: $100 total  
**Target**: <$5 for entire hackathon  
**Services**: All using Lite/Free tiers

---

## Troubleshooting

### Cloudant Connection Issues

**Error**: "Unauthorized"
- Verify API key is correct
- Check IAM role is "Manager"
- Ensure URL includes `https://`

### COS Connection Issues

**Error**: "Access Denied"
- Verify HMAC credentials were generated
- Check bucket name is correct
- Ensure region matches (us-south)

### watsonx.ai Connection Issues

**Error**: "Invalid API key"
- Verify API key is IBM Cloud API key (not watsonx.ai specific)
- Check project ID is correct
- Ensure you have access to the project

### Code Engine Issues

**Error**: "Region not available"
- Ensure you selected Osaka (jp-osa) region
- Check project name is unique

---

## Security Checklist

Before proceeding:

- [ ] .env file is in .gitignore
- [ ] No credentials in code
- [ ] API keys have minimal required permissions
- [ ] Spending alerts configured
- [ ] All services using Lite/Free tiers

---

## Next Steps

After completing this setup:

1. ✅ All IBM Cloud services configured
2. ✅ Credentials in .env file
3. ✅ Connections verified
4. ➡️ **Proceed to Task 2**: Populate data layer

---

## Quick Reference

### Service Endpoints

- **Cloudant**: `https://{instance}.cloudantnosqldb.appdomain.cloud`
- **COS**: `s3.us-south.cloud-object-storage.appdomain.cloud`
- **Code Engine**: `https://{app}.jp-osa.codeengine.appdomain.cloud`
- **watsonx.ai**: `https://us-south.ml.cloud.ibm.com`

### Required Databases

- `golden_clauses` - Internal policy templates
- `historical_decisions` - Past contract decisions
- `regulatory_mappings` - Regulation metadata

### Required Bucket Folders

- `EU/` - European regulations (GDPR, AI Act, etc.)
- `UK/` - UK regulations
- `US/` - US regulations (CCPA, etc.)
- `templates/` - Contract templates

---

**Setup Complete!** 🎉

You're now ready to start implementing the LexConductor system.

**Hackathon Deadline**: February 1, 2026 - 10:00 AM ET  
**Time Remaining**: ~48 hours

---

*Last Updated: January 30, 2026*  
*Document Version: 1.0*
