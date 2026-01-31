# IBM Cloud Configuration

Complete guide for setting up IBM Cloud services for Lex Conductor.

## Overview

Lex Conductor uses IBM Cloud services, primarily watsonx Orchestrate for agent orchestration.

## IBM Cloud Account

### Hackathon Account

For the IBM Dev Day hackathon:
- **$100 credits** provided per team
- Account valid during hackathon only
- **Closes February 4, 2026**
- Activation takes up to 2 hours

### Account Setup

1. **Check Email**
   - Look for IBM Cloud invitation email
   - Check spam folder if not found
   - Email subject: "You're invited to join an IBM Cloud account"

2. **Accept Invitation**
   - Click link in email
   - Log in or create IBM ID
   - Accept terms and conditions

3. **Switch to Hackathon Account**
   - Click account dropdown (top right)
   - Select the watsonx hackathon account
   - Verify you see the correct account name

4. **Verify Access**
   - Go to Resource List
   - Check for watsonx Orchestrate under AI/Machine Learning
   - Verify $100 credits available

## watsonx Orchestrate Setup

### Access watsonx Orchestrate

1. **Navigate to Service**
   ```
   IBM Cloud Console → Resource List → AI/Machine Learning → watsonx Orchestrate
   ```

2. **Launch Service**
   - Click on watsonx Orchestrate instance
   - Click "Launch watsonx Orchestrate" button
   - New tab opens with Orchestrate UI

3. **Verify Access**
   - You should see the Orchestrate dashboard
   - Check that you can navigate menus
   - Verify no access errors

### Get API Credentials

1. **Open Settings**
   - In watsonx Orchestrate UI
   - Click Settings icon (gear)
   - Navigate to "API Details"

2. **Copy Instance URL**
   ```
   Example: https://us-south.watson-orchestrate.ibm.com
   ```
   - Copy the full URL
   - Save to `.env` file as `WO_INSTANCE`

3. **Generate API Key**
   - Click "Generate API Key"
   - Copy the key immediately (shown only once)
   - Save to `.env` file as `WO_API_KEY`
   - Store securely (cannot be retrieved later)

4. **Test Credentials**
   ```bash
   # Set environment variables
   export WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
   export WO_API_KEY=your_api_key_here
   
   # Test with ADK
   orchestrate env add test --instance $WO_INSTANCE --api-key $WO_API_KEY
   orchestrate env activate test
   orchestrate auth login
   orchestrate auth status
   ```

## watsonx.ai Setup (Optional)

### Create watsonx.ai Instance

1. **Navigate to Catalog**
   ```
   IBM Cloud Console → Catalog → Search "watsonx.ai"
   ```

2. **Create Instance**
   - Click "watsonx.ai"
   - Select plan (Lite for hackathon)
   - Choose region (us-south recommended)
   - Click "Create"

3. **Launch watsonx.ai**
   - Go to Resource List
   - Find watsonx.ai instance
   - Click "Launch watsonx.ai"

### Get watsonx.ai Credentials

1. **Get Project ID**
   - In watsonx.ai, create or select a project
   - Go to project settings
   - Copy Project ID
   - Save as `WATSONX_PROJECT_ID`

2. **Create IBM Cloud API Key**
   - Go to Manage → Access (IAM)
   - Click "API keys"
   - Click "Create"
   - Name: "lex-conductor-watsonx"
   - Click "Create"
   - Copy and save immediately
   - Save as `WATSONX_API_KEY`

3. **Get API URL**
   ```bash
   # US South
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   
   # EU Germany
   WATSONX_URL=https://eu-de.ml.cloud.ibm.com
   ```

## Credit Management

### Monitor Usage

1. **Check Credits**
   - Go to Manage → Billing and usage
   - View "Usage" tab
   - Check remaining credits

2. **Set Up Alerts**
   - Go to Manage → Billing and usage
   - Click "Spending notifications"
   - Enable alerts at 25%, 50%, 80%
   - Add email addresses

3. **View Detailed Usage**
   - Go to Usage dashboard
   - Filter by service
   - View by time period
   - Export usage reports

### Cost Optimization

**watsonx.ai Costs:**
- Foundation model inferencing: 1,000 tokens = 1 RU = $0.0001 USD
- Notebook runtimes: $1.02 USD per CUH

**Tips to Conserve Credits:**
- ✅ Use smaller models (granite-3-2b vs granite-3-8b)
- ✅ Optimize prompts to reduce tokens
- ✅ Cache frequent queries
- ✅ Use lower runtime environments
- ✅ Stop unused notebooks
- ✅ Test with minimal data first
- ✅ Monitor usage daily

## Additional Services (Optional)

### Code Engine

Serverless platform for containerized workloads.

**Setup:**
1. Catalog → Search "Code Engine"
2. Create project
3. Deploy application or job

**Use Cases:**
- Backend API for external agents
- Scheduled jobs
- Event-driven processing

### Cloudant

NoSQL database service.

**Setup:**
1. Catalog → Search "Cloudant"
2. Create instance (Lite plan)
3. Create database
4. Get credentials

**Use Cases:**
- Agent state storage
- Conversation history
- Decision logs

### Natural Language Understanding

Text analysis and NLP.

**Setup:**
1. Catalog → Search "Natural Language Understanding"
2. Create instance
3. Get API credentials

**Use Cases:**
- Enhanced text analysis
- Entity extraction
- Sentiment analysis

## Regions and Availability

### Available Regions

- **us-south** (Dallas) - Recommended
- **us-east** (Washington DC)
- **eu-de** (Frankfurt)
- **eu-gb** (London)
- **jp-tok** (Tokyo)
- **au-syd** (Sydney)

### Service Availability

Check service availability by region:
```bash
ibmcloud catalog service watson-orchestrate --output json | jq '.geo_tags'
```

## Security Configuration

### API Key Management

**Best Practices:**
- ✅ Create separate keys for dev/prod
- ✅ Rotate keys every 30-90 days
- ✅ Revoke unused keys immediately
- ✅ Never commit keys to git
- ✅ Use environment variables
- ✅ Store in secure vault

**Create API Key:**
```bash
# Via CLI
ibmcloud iam api-key-create lex-conductor-key \
  --description "Lex Conductor API key" \
  --file key.json

# Extract key
cat key.json | jq -r '.apikey'
```

### Access Control

**IAM Roles:**
- **Viewer**: Read-only access
- **Operator**: Run operations
- **Editor**: Modify resources
- **Administrator**: Full access

**Assign Roles:**
1. Go to Manage → Access (IAM)
2. Click "Users"
3. Select user
4. Click "Access policies"
5. Assign appropriate roles

## Troubleshooting

### Cannot Access Account

**Problem**: Invitation email not received
- Check spam folder
- Verify email address
- Wait up to 2 hours for activation
- Contact support@bemyapp.com

**Problem**: Cannot switch to hackathon account
- Verify invitation accepted
- Log out and log back in
- Clear browser cache
- Try different browser

### Service Not Available

**Problem**: watsonx Orchestrate not in Resource List
- Verify correct account selected
- Check account activation status
- Verify region availability
- Contact IBM support

### Credit Issues

**Problem**: Credits not showing
- Wait for account activation (up to 2 hours)
- Verify in Billing and usage
- Contact support if still missing

**Problem**: Credits exhausted
- Monitor usage alerts
- Optimize resource usage
- Cannot add more credits (hackathon limit)

### API Authentication Fails

**Problem**: Invalid API key
- Verify key copied correctly
- Check for extra spaces
- Regenerate key if needed
- Verify key not revoked

**Problem**: Wrong instance URL
- Verify URL format (https://...)
- Check region matches
- No trailing slashes
- No /api/v1 path

## Support

### IBM Cloud Support
- **Console**: Help icon → Support Center
- **Documentation**: https://cloud.ibm.com/docs
- **Status**: https://cloud.ibm.com/status

### Hackathon Support
- **Email**: support@bemyapp.com
- **Slack**: IBM Dev Day #watsonx-orchestrate
- **Mentors**: Via BeMyApp platform

## Related Documentation

- [Terraform Setup](./terraform.md)
- [Security Guide](./security.md)
- [Infrastructure Overview](./README.md)
- [Getting Started](../01-getting-started/)

---

**Cloud Provider**: IBM Cloud  
**Primary Service**: watsonx Orchestrate  
**Credits**: $100 per team (hackathon)  
**Account Expiry**: February 4, 2026
