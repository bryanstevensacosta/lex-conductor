# Security Guide

Security best practices and guidelines for Lex Conductor.

## Security Overview

Security is critical for protecting credentials, data, and system integrity.

## Credential Management

### API Keys

**Never Commit Secrets:**
```bash
# ❌ NEVER do this
git add .env
git commit -m "add config"

# ✅ Always use .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "!.env.example" >> .gitignore
```

**Use Environment Variables:**
```bash
# ✅ Good - Environment variables
export WO_API_KEY=your_key_here

# ✅ Good - .env file (not committed)
WO_API_KEY=your_key_here

# ❌ Bad - Hardcoded in code
api_key = "abc123def456"  # NEVER DO THIS
```

**Provide Templates:**
```bash
# .env.example (safe to commit)
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_api_key_here
WATSONX_API_KEY=your_ibm_cloud_api_key
```

### Key Rotation

**Rotation Schedule:**
- Development keys: Every 30 days
- Production keys: Every 90 days
- Compromised keys: Immediately

**Rotation Process:**
```bash
# 1. Generate new key
ibmcloud iam api-key-create lex-conductor-new

# 2. Update .env file
nano .env

# 3. Test with new key
orchestrate auth login

# 4. Revoke old key
ibmcloud iam api-key-delete lex-conductor-old
```

### Key Storage

**Local Development:**
```bash
# Store in .env file
WO_API_KEY=your_key_here

# Load in code
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('WO_API_KEY')
```

**Production:**
- Use secret management service
- IBM Cloud Secrets Manager
- HashiCorp Vault
- AWS Secrets Manager

## Access Control

### Principle of Least Privilege

Grant minimum necessary permissions.

**IAM Roles:**
- **Viewer**: Read-only (for monitoring)
- **Operator**: Execute operations (for CI/CD)
- **Editor**: Modify resources (for developers)
- **Administrator**: Full access (for leads only)

**Example:**
```bash
# Grant operator role for CI/CD
ibmcloud iam user-policy-create ci-cd-user \
  --roles Operator \
  --service-name watson-orchestrate
```

### Multi-Factor Authentication

**Enable MFA:**
1. Go to Manage → Access (IAM)
2. Click "Settings"
3. Enable "MFA for all users"
4. Configure MFA method

**MFA Methods:**
- Time-based OTP (TOTP)
- SMS verification
- Security keys (U2F)

## Data Security

### Data Classification

**Public**: Can be shared openly
- Documentation
- Open-source code
- Public datasets

**Internal**: Within organization only
- Architecture diagrams
- Internal processes
- Non-sensitive configs

**Confidential**: Restricted access
- API keys
- User data
- Business logic

**Restricted**: Highest protection
- Credentials
- PII/PHI
- Financial data

### Data Encryption

**In Transit:**
```python
# Always use HTTPS
import requests

# ✅ Good
response = requests.get('https://api.example.com')

# ❌ Bad
response = requests.get('http://api.example.com')
```

**At Rest:**
- Use encrypted storage
- Enable encryption for databases
- Encrypt backups
- Use encrypted file systems

### PII Handling

**Prohibited Data (Hackathon):**
- ❌ Personal information (PI/PII)
- ❌ Client data
- ❌ Social media data without permission
- ❌ Company confidential data

**If Handling PII:**
- Minimize collection
- Encrypt storage
- Implement access controls
- Follow GDPR/CCPA requirements
- Document data flows

## Network Security

### API Security

**Authentication:**
```python
# ✅ Good - API key in header
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
response = requests.post(url, headers=headers, json=data)
```

**Rate Limiting:**
```python
# Implement rate limiting
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)  # 10 calls per minute
def call_api():
    return requests.get(api_url)
```

**Input Validation:**
```python
# Validate all inputs
def process_query(query: str) -> dict:
    # Validate
    if not query or len(query) > 1000:
        raise ValueError("Invalid query")
    
    # Sanitize
    query = query.strip()
    
    # Process
    return process(query)
```

### HTTPS/TLS

**Always Use HTTPS:**
```bash
# ✅ Good
WO_INSTANCE=https://us-south.watson-orchestrate.ibm.com

# ❌ Bad
WO_INSTANCE=http://us-south.watson-orchestrate.ibm.com
```

**Verify Certificates:**
```python
import requests

# ✅ Good - Verify SSL
response = requests.get(url, verify=True)

# ❌ Bad - Skip verification
response = requests.get(url, verify=False)  # NEVER DO THIS
```

## Code Security

### Dependency Management

**Keep Dependencies Updated:**
```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated
```

**Use Dependency Scanning:**
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: pypa/gh-action-pip-audit@v1
```

### Code Scanning

**Static Analysis:**
```bash
# Run security linters
bandit -r src/

# Check for secrets
trufflehog filesystem .

# Scan dependencies
safety check
```

**Pre-commit Hooks:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', 'src/']
  
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

### Secure Coding Practices

**Input Validation:**
```python
# ✅ Good - Validate inputs
def process_user_input(data: dict) -> dict:
    # Validate required fields
    required = ['query', 'user_id']
    if not all(k in data for k in required):
        raise ValueError("Missing required fields")
    
    # Validate types
    if not isinstance(data['query'], str):
        raise TypeError("Query must be string")
    
    # Sanitize
    data['query'] = data['query'].strip()[:1000]
    
    return data
```

**Error Handling:**
```python
# ✅ Good - Don't expose internals
try:
    result = process_query(query)
except Exception as e:
    logger.error(f"Error processing query: {e}")
    return {"error": "An error occurred"}  # Generic message

# ❌ Bad - Exposes internals
except Exception as e:
    return {"error": str(e)}  # May expose sensitive info
```

## Monitoring & Auditing

### Logging

**What to Log:**
- ✅ Authentication attempts
- ✅ API calls
- ✅ Errors and exceptions
- ✅ Configuration changes
- ✅ Access to sensitive data

**What NOT to Log:**
- ❌ Passwords
- ❌ API keys
- ❌ PII
- ❌ Credit card numbers
- ❌ Session tokens

**Example:**
```python
import logging

# ✅ Good - Log without sensitive data
logger.info("User authenticated", extra={
    "user_id": user_id,
    "timestamp": datetime.now(),
    "ip_address": request.ip
})

# ❌ Bad - Logs sensitive data
logger.info(f"User {user_id} logged in with password {password}")
```

### Audit Trail

**Track Important Events:**
```python
def audit_log(event: str, user: str, details: dict):
    """Log security-relevant events."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "user": user,
        "details": details,
        "ip_address": get_client_ip()
    }
    audit_logger.info(json.dumps(log_entry))

# Usage
audit_log("agent_deployed", user_id, {
    "agent": "conductor-agent",
    "version": "1.0.0"
})
```

## Incident Response

### Security Incident Plan

**1. Detection**
- Monitor logs for anomalies
- Set up alerts
- Review access logs

**2. Containment**
- Revoke compromised credentials
- Block suspicious IPs
- Isolate affected systems

**3. Investigation**
- Review audit logs
- Identify scope of breach
- Document findings

**4. Recovery**
- Rotate all credentials
- Patch vulnerabilities
- Restore from backups

**5. Post-Incident**
- Document lessons learned
- Update security procedures
- Implement preventive measures

### Compromised Credentials

**If API Key Exposed:**
```bash
# 1. Immediately revoke key
ibmcloud iam api-key-delete compromised-key

# 2. Generate new key
ibmcloud iam api-key-create new-key

# 3. Update all systems
# Update .env files
# Update CI/CD secrets
# Update production configs

# 4. Review access logs
orchestrate agents logs --since 24h | grep "unauthorized"

# 5. Document incident
```

## Compliance

### Hackathon Requirements

**Must Comply With:**
- ✅ No prohibited data (PII, client data)
- ✅ No exposed credentials in public repos
- ✅ Follow code of conduct
- ✅ Respect IBM Cloud terms of service

**Verification:**
```bash
# Check for exposed secrets
git secrets --scan

# Check .gitignore
cat .gitignore | grep -E "\.env|api.*key|secret"

# Scan repository
trufflehog filesystem . --only-verified
```

### Data Privacy

**GDPR Principles:**
- Lawfulness, fairness, transparency
- Purpose limitation
- Data minimization
- Accuracy
- Storage limitation
- Integrity and confidentiality

**Implementation:**
- Document data processing
- Implement data retention policies
- Provide data access/deletion
- Encrypt sensitive data
- Maintain audit logs

## Security Checklist

### Development
- [ ] No secrets in code
- [ ] .env in .gitignore
- [ ] .env.example provided
- [ ] Input validation implemented
- [ ] Error handling doesn't expose internals
- [ ] Dependencies up to date
- [ ] Security linters passing

### Deployment
- [ ] HTTPS only
- [ ] API keys rotated
- [ ] Access controls configured
- [ ] Monitoring enabled
- [ ] Logging configured
- [ ] Backups enabled

### Operations
- [ ] Monitor logs regularly
- [ ] Review access logs
- [ ] Update dependencies
- [ ] Rotate credentials
- [ ] Test incident response
- [ ] Document security procedures

## Related Documentation

- [IBM Cloud Setup](./ibm-cloud.md)
- [Terraform Setup](./terraform.md)
- [Environment Configuration](../01-getting-started/environment-config.md)

---

**Security Level**: High  
**Compliance**: Hackathon rules + IBM Cloud ToS  
**Review Frequency**: Weekly during development
