# Setup Guide

Complete setup instructions for Lex Conductor development environment.

## Prerequisites

Before starting, ensure you have:
- ✅ Python 3.11 or higher
- ✅ pip (Python package manager)
- ✅ Git
- ✅ IBM Cloud account (hackathon provisioned)
- ✅ watsonx Orchestrate access

See [Prerequisites](./prerequisites.md) for detailed requirements.

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/bryanstevensacosta/lex-conductor.git
cd lex-conductor
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install watsonx Orchestrate ADK
pip install ibm-watsonx-orchestrate
```

### 4. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# Use your preferred editor (nano, vim, code, etc.)
nano .env
```

Required environment variables:

```bash
# watsonx Orchestrate (REQUIRED)
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here

# watsonx.ai (OPTIONAL)
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### 5. Configure watsonx Orchestrate ADK

```bash
# Add environment
orchestrate env add prod \
  --instance $WO_INSTANCE \
  --api-key $WO_API_KEY

# Activate environment
orchestrate env activate prod

# Login
orchestrate auth login
```

### 6. Verify Installation

```bash
# Check Python version
python --version

# Check pip packages
pip list | grep ibm-watsonx-orchestrate

# Check Orchestrate connection
orchestrate auth status

# List environments
orchestrate env list
```

### 7. Install Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

## Getting IBM Cloud Credentials

### watsonx Orchestrate

1. **Access IBM Cloud**
   - Check your email for team invitation
   - Accept invitation and log in
   - Switch to the watsonx account

2. **Launch watsonx Orchestrate**
   - Go to IBM Cloud Resource List
   - Find "watsonx Orchestrate" under AI/Machine Learning
   - Click "Launch watsonx Orchestrate"

3. **Get API Credentials**
   - In watsonx Orchestrate, go to Settings
   - Navigate to API Details
   - Copy Service Instance URL
   - Generate and copy API Key

### watsonx.ai (Optional)

1. **Access watsonx.ai**
   - From IBM Cloud, launch watsonx.ai
   - Create or select a project

2. **Get Credentials**
   - Scroll to "Developer access" section
   - Copy Project ID
   - Create IBM Cloud API key:
     - Go to Manage → Access (IAM)
     - Click API keys
     - Create new API key
     - Copy and save securely

## Troubleshooting

### Python Version Issues

```bash
# Check Python version
python --version

# If version is < 3.11, install newer version
# On macOS with Homebrew:
brew install python@3.11

# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.11
```

### Virtual Environment Issues

```bash
# If venv creation fails, install venv module
python -m pip install virtualenv

# Create with virtualenv instead
virtualenv .venv
```

### Dependency Installation Issues

```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# If specific package fails, install individually
pip install ibm-watsonx-orchestrate
```

### watsonx Orchestrate Connection Issues

```bash
# Check environment variables
echo $WO_INSTANCE
echo $WO_API_KEY

# Re-add environment
orchestrate env remove prod
orchestrate env add prod --instance $WO_INSTANCE --api-key $WO_API_KEY

# Check authentication
orchestrate auth status
```

### IBM Cloud Access Issues

**Problem**: Can't access IBM Cloud account
- Check spam folder for invitation email
- Verify you're using correct email address
- Wait up to 2 hours for account activation
- Contact support@bemyapp.com if issues persist

**Problem**: watsonx Orchestrate not visible
- Ensure you've switched to the correct account
- Check Resource List under AI/Machine Learning
- Verify account has been fully activated

## Next Steps

After completing setup:

1. **Deploy Agents**
   - Navigate to [Agent Definitions](../03-agents/agent-definitions/)
   - Follow deployment instructions
   - See [Integration Guide](../05-integration/watsonx-orchestrate.md)

2. **Start Development**
   - Review [Development Guide](../04-development/)
   - Understand [Architecture](../02-project/architecture.md)
   - Read [Agent Documentation](../03-agents/)

3. **Test System**
   - Deploy all agents
   - Test end-to-end workflow
   - Verify all components working

## Quick Reference

```bash
# Activate virtual environment
source .venv/bin/activate

# Check Orchestrate status
orchestrate auth status

# List deployed agents
orchestrate agents list

# Test agent
orchestrate chat --agent conductor-agent

# View logs
orchestrate agents logs conductor-agent
```

## Support

- **Setup Issues**: See [Development Guide](../04-development/)
- **IBM Cloud Help**: IBM Cloud console support
- **watsonx Orchestrate**: https://www.ibm.com/docs/en/watson-orchestrate
- **Hackathon Support**: support@bemyapp.com

---

**Estimated Time**: 15-30 minutes  
**Difficulty**: Beginner-friendly  
**Next**: [Quick Start Guide](./quick-start.md)
