# LexConductor - Setup Scripts

**IBM Dev Day AI Demystified Hackathon 2026**  
**Team: AI Kings 👑**

This directory contains utility scripts for setting up and verifying the LexConductor development environment.

## 🚀 Quick Start

### Option 1: Interactive Setup (Recommended)
```bash
./scripts/interactive_setup.sh
```
Guides you step-by-step through the entire IBM Cloud setup process.

### Option 2: Automated Setup (Requires IBM Cloud CLI)
```bash
./scripts/setup_ibm_cloud.sh
```
Automatically creates resources using IBM Cloud CLI.

### Option 3: Manual Setup
Follow the guides:
- English: `docs/IBM_CLOUD_SETUP.md`
- Español: `docs/GUIA_CREDENCIALES_ES.md`

---

## Scripts

### 1. verify_setup.py

**Purpose**: Comprehensive verification of local development environment setup.

**Usage**:
```bash
source .venv/bin/activate
python scripts/verify_setup.py
```

**Checks**:
- ✅ Python version (3.11+ required)
- ✅ All Python packages installed
- ✅ watsonx Orchestrate ADK installed
- ✅ Environment variables configured
- ✅ .gitignore properly configured
- ✅ Project directory structure

**Output**:
- Green ✓ for passed checks
- Red ✗ for failed checks
- Yellow ⚠ for warnings
- Blue ℹ for information

**Exit Codes**:
- `0` - All checks passed
- `1` - Some checks failed

---

### 3. setup_ibm_cloud.sh (NEW)

**Purpose**: Automated IBM Cloud resource creation using IBM Cloud CLI.

**Usage**:
```bash
./scripts/setup_ibm_cloud.sh
```

**Prerequisites**:
- IBM Cloud CLI installed
- Logged in to IBM Cloud (`ibmcloud login --sso`)
- `jq` command-line JSON processor

**What it does**:
- ✅ Creates IBM Cloud API key
- ✅ Creates Cloudant instance with credentials
- ✅ Creates Cloud Object Storage instance with HMAC credentials
- ✅ Creates Code Engine project in Osaka region
- ✅ Saves all credentials to `.env.temp`

**Output**:
- Creates `.env.temp` file with all credentials
- Displays summary of created resources

**Important**:
- Review `.env.temp` before copying to `.env`
- Delete `.env.temp` after copying for security
- watsonx Orchestrate and watsonx.ai credentials must be added manually

---

### 4. interactive_setup.sh (NEW)

**Purpose**: Interactive step-by-step guide for IBM Cloud setup.

**Usage**:
```bash
./scripts/interactive_setup.sh
```

**Prerequisites**:
- Web browser access to IBM Cloud Console
- IBM Cloud account

**What it does**:
- 📋 Guides you through each service setup
- 🔗 Provides direct links to IBM Cloud Console
- ✍️ Collects credentials interactively
- 💾 Saves all credentials to `.env.setup`
- ✅ Validates each step

**Steps**:
1. Create IBM Cloud API Key
2. Create watsonx.ai Project
3. Create Cloudant Instance
4. Create Cloud Object Storage Instance
5. Create Code Engine Project
6. Get watsonx Orchestrate Credentials

**Output**:
- Creates `.env.setup` file with all credentials
- Provides next steps instructions

**Advantages**:
- No CLI installation required
- Visual confirmation at each step
- Beginner-friendly
- Detailed instructions

---

### 2. test_connections.py

**Purpose**: Test connectivity to all IBM Cloud services.

**Usage**:
```bash
source .venv/bin/activate
python scripts/test_connections.py
```

**Tests**:
- 🔗 watsonx.ai connection and Granite model availability
- 🔗 Cloudant database connection and database existence
- 🔗 Cloud Object Storage connection and bucket existence
- 🔗 watsonx Orchestrate credentials configuration

**Prerequisites**:
- IBM Cloud services must be created
- Credentials must be in `.env` file
- Services must be accessible from your network

**Output**:
- Connection status for each service
- Detailed error messages if connection fails
- Summary of all connection tests

**Exit Codes**:
- `0` - All connections successful
- `1` - Some connections failed

---

## Typical Workflow

### Initial Setup

1. **Run setup script**:
   ```bash
   ./setup.sh
   ```

2. **Verify installation**:
   ```bash
   source .venv/bin/activate
   python scripts/verify_setup.py
   ```

3. **Create IBM Cloud services** (see `docs/IBM_CLOUD_SETUP.md`)

4. **Update .env with credentials**

5. **Test connections**:
   ```bash
   python scripts/test_connections.py
   ```

### Daily Development

Before starting work:
```bash
source .venv/bin/activate
python scripts/verify_setup.py
```

After updating dependencies:
```bash
pip install -r requirements.txt
python scripts/verify_setup.py
```

After changing credentials:
```bash
python scripts/test_connections.py
```

---

## Troubleshooting

### verify_setup.py Issues

**Error**: "Python version too old"
- Install Python 3.11 or higher
- Update PATH to use correct Python version

**Error**: "Missing packages"
- Run: `pip install -r requirements.txt`
- Ensure virtual environment is activated

**Error**: "watsonx Orchestrate ADK not found"
- Run: `pip install ibm-watsonx-orchestrate`
- Verify installation: `orchestrate --version`

**Warning**: "Placeholder values detected"
- Update `.env` with actual IBM Cloud credentials
- See `docs/IBM_CLOUD_SETUP.md` for instructions

### test_connections.py Issues

**Error**: "watsonx.ai connection failed"
- Verify `WATSONX_API_KEY` is correct IBM Cloud API key
- Verify `WATSONX_PROJECT_ID` is correct
- Check project access permissions

**Error**: "Cloudant connection failed"
- Verify `CLOUDANT_URL` includes `https://`
- Verify `CLOUDANT_API_KEY` has Manager role
- Check databases exist: `golden_clauses`, `historical_decisions`, `regulatory_mappings`

**Error**: "Cloud Object Storage connection failed"
- Verify HMAC credentials were generated
- Verify `COS_INSTANCE_ID` is correct
- Check bucket exists: `watsonx-hackathon-regulations`

**Error**: "watsonx Orchestrate connection failed"
- Verify `WO_INSTANCE` URL is correct
- Verify `WO_API_KEY` is valid
- Try regenerating API key in Orchestrate settings

---

## Script Details

### verify_setup.py

**Language**: Python 3.11+  
**Dependencies**: Standard library only  
**Runtime**: ~5 seconds  
**Network**: No network calls

**Functions**:
- `check_python_version()` - Verify Python 3.11+
- `check_env_file()` - Check .env exists and has required variables
- `check_dependencies()` - Verify all packages installed
- `check_orchestrate_adk()` - Verify ADK installation
- `check_directory_structure()` - Check project folders
- `check_gitignore()` - Verify security patterns

### test_connections.py

**Language**: Python 3.11+  
**Dependencies**: IBM Cloud SDKs  
**Runtime**: ~10-30 seconds  
**Network**: Makes API calls to IBM Cloud

**Functions**:
- `test_watsonx_ai()` - Test watsonx.ai and list models
- `test_cloudant()` - Test Cloudant and list databases
- `test_cos()` - Test COS and list buckets
- `test_orchestrate()` - Verify Orchestrate credentials

---

## Environment Variables

Both scripts read from `.env` file. Required variables:

```bash
# watsonx Orchestrate
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key

# watsonx.ai
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Cloudant
CLOUDANT_URL=https://your-instance.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=your_api_key

# Cloud Object Storage
COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY=your_api_key
COS_INSTANCE_ID=your_instance_id
```

See `.env.example` for complete list.

---

## Security Notes

- ⚠️ Never commit `.env` file to git
- ⚠️ Scripts check for placeholder values
- ⚠️ Credentials are never logged or displayed
- ⚠️ Use separate credentials for dev/test/prod

---

## Contributing

When adding new scripts:

1. Add executable permissions: `chmod +x scripts/your_script.py`
2. Add shebang: `#!/usr/bin/env python3`
3. Add docstring with purpose and usage
4. Use color codes for output (GREEN, RED, YELLOW, BLUE)
5. Return appropriate exit codes (0 = success, 1 = failure)
6. Update this README

---

## Quick Reference

```bash
# Verify setup
python scripts/verify_setup.py

# Test connections
python scripts/test_connections.py

# Both in sequence
python scripts/verify_setup.py && python scripts/test_connections.py

# With verbose output
python scripts/test_connections.py -v  # (if implemented)
```

---

**Last Updated**: January 30, 2026  
**Hackathon Deadline**: February 1, 2026 - 10:00 AM ET

---

*Team: AI Kings 👑*
