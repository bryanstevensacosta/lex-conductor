# Quick Start Guide

**LexConductor - IBM Dev Day AI Demystified Hackathon 2026**  
**Team: AI Kings 👑**

Get up and running with LexConductor in 15 minutes.

## Prerequisites

- ✅ Python 3.11+ installed
- ✅ IBM Cloud account (hackathon provided)
- ✅ Git installed
- ✅ Terminal/command line access

## Step 1: Clone and Setup (5 minutes)

```bash
# Clone the repository (if not already done)
cd lexconductor

# Run setup script
./setup.sh

# Activate virtual environment
source .venv/bin/activate

# Verify installation
python scripts/verify_setup.py
```

Expected output:
```
✓ All checks passed (6/6)
⚠ Some environment variables have placeholder values
```

## Step 2: Configure IBM Cloud Services (20 minutes)

Follow the detailed guide: [IBM Cloud Setup](./IBM_CLOUD_SETUP.md)

Quick checklist:
- [ ] Create Cloudant instance (Lite, US-South)
- [ ] Create COS instance (Lite, US-South)
- [ ] Create Code Engine project (Osaka)
- [ ] Get watsonx Orchestrate credentials
- [ ] Get watsonx.ai credentials

## Step 3: Update Environment Variables (5 minutes)

Edit `.env` file with your credentials:

```bash
# Open .env in your editor
nano .env  # or vim, code, etc.
```

Update these values:
```bash
# watsonx Orchestrate
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_actual_api_key

# watsonx.ai
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id

# Cloudant
CLOUDANT_URL=https://your-instance.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=your_cloudant_api_key

# Cloud Object Storage
COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY=your_cos_api_key
COS_INSTANCE_ID=your_cos_instance_id
```

## Step 4: Test Connections (2 minutes)

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

## Step 5: Configure watsonx Orchestrate ADK (3 minutes)

```bash
# Add environment
orchestrate env add prod --instance $WO_INSTANCE --api-key $WO_API_KEY

# Activate environment
orchestrate env activate prod

# Login
orchestrate auth login

# Verify
orchestrate agents list
```

## You're Ready! 🎉

Your development environment is now fully configured.

### Next Steps

1. **Populate Data Layer** (Task 2)
   - Create Golden Clauses
   - Upload regulatory documents
   - Seed historical precedents

2. **Implement Core Models** (Task 3)
   - Data models (Pydantic)
   - Client wrappers (Cloudant, COS, watsonx.ai)

3. **Build External Agents** (Task 4)
   - FastAPI backend
   - Agent implementations

4. **Deploy to Code Engine** (Task 5)
   - Docker containerization
   - Code Engine deployment

5. **Create Orchestrate Agents** (Task 6)
   - YAML definitions
   - Import and deploy

### Useful Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run verification
python scripts/verify_setup.py

# Test connections
python scripts/test_connections.py

# Check Orchestrate status
orchestrate agents list

# View logs
orchestrate agents logs <agent-name>

# Run tests (when implemented)
pytest tests/

# Format code
black backend/
ruff check backend/
```

### Troubleshooting

**Issue**: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: "Connection failed"
```bash
# Check .env file
cat .env | grep -v "^#" | grep "="

# Verify credentials in IBM Cloud Console
```

**Issue**: "Orchestrate command not found"
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall ADK
pip install --upgrade ibm-watsonx-orchestrate
```

### Getting Help

- **Documentation**: See `docs/` folder
- **IBM Cloud Setup**: `docs/IBM_CLOUD_SETUP.md`
- **Hackathon Guide**: `docs/06-hackathon/`
- **Steering Files**: `.kiro/steering/`

### Important Reminders

- ⏰ **Deadline**: February 1, 2026 - 10:00 AM ET
- 💰 **Budget**: $100 credits (target <$5)
- 🔒 **Security**: Never commit .env file
- 📹 **Demo**: Video must show watsonx Orchestrate (≥90s)

---

**Happy Hacking!** 👑

*Last Updated: January 30, 2026*
