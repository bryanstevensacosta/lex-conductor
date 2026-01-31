# Environment Configuration

Complete guide to configuring environment variables for Lex Conductor.

## Environment File

Lex Conductor uses a `.env` file to store configuration and credentials.

### Create Environment File

```bash
# Copy template
cp .env.example .env

# Edit with your preferred editor
nano .env
# or
code .env
# or
vim .env
```

## Required Variables

### watsonx Orchestrate (MANDATORY)

```bash
# watsonx Orchestrate Instance URL
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com

# watsonx Orchestrate API Key
WO_API_KEY=your_api_key_here
```

**How to Get:**
1. Log in to IBM Cloud
2. Go to Resource List → AI/Machine Learning
3. Launch watsonx Orchestrate
4. Navigate to Settings → API Details
5. Copy Instance URL
6. Generate and copy API Key

## Optional Variables

### watsonx.ai (Optional)

```bash
# IBM Cloud API Key
WATSONX_API_KEY=your_ibm_cloud_api_key

# watsonx.ai Project ID
WATSONX_PROJECT_ID=your_project_id

# watsonx.ai API URL
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**How to Get:**
1. Go to watsonx.ai home page
2. Select or create a project
3. Scroll to "Developer access" section
4. Copy Project ID
5. Create IBM Cloud API key:
   - Manage → Access (IAM) → API keys
   - Create new API key
   - Copy and save securely

### Application Settings (Optional)

```bash
# Application environment
APP_ENV=development  # or production

# Log level
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# API port (if running local API)
API_PORT=8000

# Enable debug mode
DEBUG=false
```

## Complete .env Example

```bash
# ============================================
# watsonx Orchestrate (REQUIRED)
# ============================================
WO_INSTANCE=https://us-south.watson-orchestrate.ibm.com
WO_API_KEY=abc123def456ghi789jkl012mno345pqr678stu901

# ============================================
# watsonx.ai (OPTIONAL)
# ============================================
WATSONX_API_KEY=xyz789abc123def456ghi789jkl012mno345
WATSONX_PROJECT_ID=12345678-1234-1234-1234-123456789012
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# ============================================
# Application Settings (OPTIONAL)
# ============================================
APP_ENV=development
LOG_LEVEL=INFO
API_PORT=8000
DEBUG=false
```

## Security Best Practices

### Never Commit Secrets

```bash
# Verify .env is in .gitignore
cat .gitignore | grep .env

# Should show:
# .env
# .env.local
# .env.*.local
```

### Use .env.example for Templates

```bash
# .env.example (safe to commit)
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_project_id
```

### Separate Environments

```bash
# Development
.env.development

# Production
.env.production

# Testing
.env.test
```

### Rotate Keys Regularly

- Change API keys every 30-90 days
- Revoke unused keys immediately
- Use separate keys for dev/prod
- Monitor key usage in IBM Cloud

## Loading Environment Variables

### Python

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access variables
wo_instance = os.getenv('WO_INSTANCE')
wo_api_key = os.getenv('WO_API_KEY')
```

### Shell Scripts

```bash
# Load .env file
set -a
source .env
set +a

# Use variables
echo $WO_INSTANCE
```

### watsonx Orchestrate ADK

```bash
# ADK automatically uses environment variables
orchestrate env add prod \
  --instance $WO_INSTANCE \
  --api-key $WO_API_KEY
```

## Validation

### Check Required Variables

```bash
# Check if variables are set
if [ -z "$WO_INSTANCE" ]; then
    echo "Error: WO_INSTANCE not set"
    exit 1
fi

if [ -z "$WO_API_KEY" ]; then
    echo "Error: WO_API_KEY not set"
    exit 1
fi

echo "✅ All required variables are set"
```

### Test Connection

```bash
# Test watsonx Orchestrate connection
orchestrate auth status

# Should show:
# ✅ Authenticated
# Instance: https://your-instance.watson-orchestrate.ibm.com
```

## Troubleshooting

### Variables Not Loading

```bash
# Check .env file exists
ls -la .env

# Check file permissions
chmod 600 .env

# Verify content
cat .env | grep -v "^#" | grep -v "^$"
```

### Invalid Credentials

```bash
# Verify API key format
echo $WO_API_KEY | wc -c
# Should be ~40-50 characters

# Test authentication
orchestrate auth login
```

### Wrong Instance URL

```bash
# Correct format:
https://us-south.watson-orchestrate.ibm.com
https://eu-de.watson-orchestrate.ibm.com

# Incorrect formats:
http://... (missing 's')
.../api/v1 (don't include path)
```

## Environment-Specific Configuration

### Development

```bash
APP_ENV=development
LOG_LEVEL=DEBUG
DEBUG=true
```

### Production

```bash
APP_ENV=production
LOG_LEVEL=WARNING
DEBUG=false
```

### Testing

```bash
APP_ENV=test
LOG_LEVEL=INFO
DEBUG=true
```

## IBM Cloud Regions

Choose the correct URL for your region:

```bash
# US South
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# EU Germany
WATSONX_URL=https://eu-de.ml.cloud.ibm.com

# EU United Kingdom
WATSONX_URL=https://eu-gb.ml.cloud.ibm.com

# Japan
WATSONX_URL=https://jp-tok.ml.cloud.ibm.com
```

## Related Documentation

- [Setup Guide](./setup.md) - Complete setup instructions
- [Prerequisites](./prerequisites.md) - Required tools and accounts
- [Security Guide](../07-infrastructure/security.md) - Security best practices

---

**Security Level**: 🔒 High - Contains sensitive credentials  
**Never Commit**: .env files to version control  
**Always Use**: .env.example for templates
