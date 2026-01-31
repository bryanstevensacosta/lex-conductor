# Infrastructure Documentation

Infrastructure as code, IBM Cloud configuration, and security guidelines.

## 📋 Contents

- **[Terraform Setup](./terraform.md)** - Infrastructure as code with Terraform
- **[IBM Cloud Configuration](./ibm-cloud.md)** - IBM Cloud setup and services
- **[Security](./security.md)** - Security best practices and credential management

## 🏗️ Infrastructure Overview

Lex Conductor infrastructure includes:

```
IBM Cloud
├── watsonx Orchestrate (REQUIRED)
│   └── Native Conductor Agent
│
├── watsonx.ai (OPTIONAL)
│   └── Granite Models
│
└── Additional Services (OPTIONAL)
    ├── Code Engine
    ├── Cloudant
    └── Others
```

## 🚀 Quick Setup

### Option 1: Manual Setup (Recommended for Hackathon)

```bash
# 1. Access IBM Cloud
# - Accept team invitation email
# - Switch to watsonx account

# 2. Launch watsonx Orchestrate
# - Go to Resource List
# - Find watsonx Orchestrate
# - Click "Launch"

# 3. Get API credentials
# - Settings → API Details
# - Copy Instance URL and API Key

# 4. Configure locally
cp .env.example .env
# Edit .env with your credentials
```

### Option 2: Terraform (Optional)

```bash
# Navigate to terraform directory
cd terraform/

# Initialize Terraform
terraform init

# Review plan
terraform plan

# Apply configuration
terraform apply
```

## 🔧 IBM Cloud Services

### Required Services

**watsonx Orchestrate**
- Primary orchestration platform
- Native agent hosting
- Agent Connect Framework
- Built-in observability

### Optional Services

**watsonx.ai**
- AI inference platform
- Granite model access
- Prompt Lab
- Model experimentation

**Code Engine**
- Serverless platform
- Container deployment
- Auto-scaling
- Good for external agents

**Cloudant**
- NoSQL database
- JSON document storage
- Agent state/memory
- RESTful API

## 💰 Cost Management

### IBM Cloud Credits
- **$100 credits** per team
- Account valid during hackathon
- **Closes February 4, 2026**
- Monitor usage carefully

### Credit Alerts
- Email alerts at 25%, 50%, 80%
- Account suspended at 100%
- Plan usage carefully

### Cost Optimization
- Use smaller models when possible
- Avoid unnecessary API calls
- Test with minimal data first
- Monitor credit usage regularly

## 🔐 Security

### Credential Management

**Never Commit:**
- `.env` files
- API keys
- Access tokens
- Passwords
- Private keys

**Always Use:**
- Environment variables
- `.env.example` for templates
- `.gitignore` properly configured
- Separate keys for dev/prod

### Best Practices

```bash
# Store credentials in .env
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here

# Never commit .env
echo ".env" >> .gitignore

# Use .env.example for templates
cp .env.example .env
```

### Key Rotation

- Rotate keys regularly
- Use separate keys for different environments
- Revoke unused keys
- Monitor key usage

## 🏗️ Terraform Configuration

### Structure

```
terraform/
├── main.tf              # Main configuration
├── variables.tf         # Variable definitions
├── outputs.tf           # Output values
├── terraform.tfvars.example  # Variable values template
└── README.md           # Terraform guide
```

### Usage

```bash
# Initialize
terraform init

# Plan changes
terraform plan

# Apply configuration
terraform apply

# Destroy resources (after hackathon)
terraform destroy
```

## 📊 Infrastructure Monitoring

### watsonx Orchestrate

```bash
# Check agent status
orchestrate agents list

# View agent logs
orchestrate agents logs conductor-agent

# Monitor performance
# Use built-in IBM Telemetry
```

### IBM Cloud Dashboard

- Monitor credit usage
- View service status
- Check resource utilization
- Review audit logs

## 🐛 Troubleshooting

### Common Issues

**Account Access Denied:**
- Check invitation email
- Verify account activation
- Switch to correct account

**Credit Limit Reached:**
- Monitor usage alerts
- Optimize resource usage
- Contact support if needed

**Service Unavailable:**
- Check IBM Cloud status
- Verify service region
- Review service limits

## 📚 Infrastructure Patterns

### Pattern 1: Minimal (Recommended for Hackathon)
- watsonx Orchestrate only
- Manual configuration
- No additional services

### Pattern 2: Standard
- watsonx Orchestrate
- watsonx.ai for inference
- Manual or Terraform

### Pattern 3: Full Stack
- All IBM Cloud services
- Terraform managed
- Production-ready

## 🔄 Deployment Workflow

```
1. Configure IBM Cloud account
   ↓
2. Set up watsonx Orchestrate
   ↓
3. Deploy agent definitions
   ↓
4. Configure Agent Connect (if using external agents)
   ↓
5. Test end-to-end
   ↓
6. Monitor and optimize
```

## 📖 Related Documentation

- [Getting Started](../01-getting-started/) - Initial setup
- [Integration](../05-integration/) - watsonx integration
- [Development](../04-development/) - Development guide
- [Hackathon](../06-hackathon/) - Submission requirements

## 🆘 Support

- **IBM Cloud Support**: Via IBM Cloud console
- **watsonx Orchestrate**: https://www.ibm.com/docs/en/watson-orchestrate
- **Terraform**: https://www.terraform.io/docs
- **IBM Dev Day Slack**: #watsonx-orchestrate

---

**Infrastructure Status**: 🚧 Setup Required  
**Cloud Provider**: IBM Cloud  
**IaC Tool**: Terraform (optional)  
**Credits**: $100 per team (expires Feb 4, 2026)
