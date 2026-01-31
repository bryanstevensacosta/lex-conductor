# Deployment Guide

Complete guide for deploying Lex Conductor agents to watsonx Orchestrate.

## Deployment Overview

Lex Conductor uses IBM watsonx Orchestrate as the primary deployment platform for agent orchestration.

## Prerequisites

- ✅ IBM Cloud account with watsonx Orchestrate access
- ✅ watsonx Orchestrate ADK installed
- ✅ Agent definitions ready (YAML files)
- ✅ Environment configured

## Deployment Process

### 1. Prepare Agent Definitions

```bash
# Navigate to agent definitions
cd docs/03-agents/agent-definitions/

# Verify YAML files exist
ls -la *.yaml

# Should show:
# - conductor_agent.yaml
# - routing_agent.yaml
# - memory_agent.yaml
# - fusion_agent.yaml
# - traceability_agent.yaml
```

### 2. Configure Environment

```bash
# Set environment variables
export WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
export WO_API_KEY=your_api_key_here

# Configure ADK
orchestrate env add prod \
  --instance $WO_INSTANCE \
  --api-key $WO_API_KEY

# Activate environment
orchestrate env activate prod

# Login
orchestrate auth login
```

### 3. Validate Agent Definitions

```bash
# Validate each agent before deployment
orchestrate agents validate -f conductor_agent.yaml
orchestrate agents validate -f routing_agent.yaml
orchestrate agents validate -f memory_agent.yaml
orchestrate agents validate -f fusion_agent.yaml
orchestrate agents validate -f traceability_agent.yaml
```

### 4. Deploy Agents

```bash
# Deploy conductor agent (orchestrator)
orchestrate agents import -f conductor_agent.yaml

# Deploy specialist agents
orchestrate agents import -f routing_agent.yaml
orchestrate agents import -f memory_agent.yaml
orchestrate agents import -f fusion_agent.yaml
orchestrate agents import -f traceability_agent.yaml

# Verify deployment
orchestrate agents list
```

### 5. Test Deployment

```bash
# Test conductor agent
orchestrate chat --agent conductor-agent

# Example query
> "Analyze the decision to expand into a new market"

# Check agent status
orchestrate agents get conductor-agent

# View logs
orchestrate agents logs conductor-agent --tail 50
```

## Deployment Strategies

### Strategy 1: All at Once

Deploy all agents simultaneously.

```bash
# Deploy all agents
for agent in conductor routing memory fusion traceability; do
    orchestrate agents import -f ${agent}_agent.yaml
done

# Verify all deployed
orchestrate agents list
```

**Pros**: Fast, simple
**Cons**: All-or-nothing, harder to debug

### Strategy 2: Incremental

Deploy agents one at a time, testing each.

```bash
# Deploy and test conductor
orchestrate agents import -f conductor_agent.yaml
orchestrate chat --agent conductor-agent

# Deploy and test routing
orchestrate agents import -f routing_agent.yaml
# Test...

# Continue for each agent
```

**Pros**: Easier to debug, safer
**Cons**: Slower, more manual

### Strategy 3: Blue-Green

Maintain two environments for zero-downtime updates.

```bash
# Deploy to staging
orchestrate env activate staging
orchestrate agents import -f conductor_agent.yaml

# Test in staging
orchestrate chat --agent conductor-agent

# Switch to production
orchestrate env activate prod
orchestrate agents import -f conductor_agent.yaml
```

**Pros**: Zero downtime, safe rollback
**Cons**: More complex, requires multiple environments

## Updating Agents

### Update Existing Agent

```bash
# Edit agent definition
nano conductor_agent.yaml

# Validate changes
orchestrate agents validate -f conductor_agent.yaml

# Re-import with force flag
orchestrate agents import -f conductor_agent.yaml --force

# Verify update
orchestrate agents get conductor-agent

# Test updated agent
orchestrate chat --agent conductor-agent
```

### Rollback Agent

```bash
# Get previous version
git checkout HEAD~1 -- conductor_agent.yaml

# Re-deploy previous version
orchestrate agents import -f conductor_agent.yaml --force

# Verify rollback
orchestrate agents get conductor-agent
```

## Monitoring Deployment

### Check Agent Status

```bash
# List all agents
orchestrate agents list

# Get specific agent details
orchestrate agents get conductor-agent

# Check agent health
orchestrate agents health conductor-agent
```

### View Logs

```bash
# Follow logs in real-time
orchestrate agents logs conductor-agent --follow

# View last 100 lines
orchestrate agents logs conductor-agent --tail 100

# View logs from last hour
orchestrate agents logs conductor-agent --since 1h

# Filter by log level
orchestrate agents logs conductor-agent --level error
```

### Monitor Performance

```bash
# View agent metrics
orchestrate agents metrics conductor-agent

# Check response times
orchestrate agents metrics conductor-agent --metric response_time

# View error rates
orchestrate agents metrics conductor-agent --metric error_rate
```

## Deployment Checklist

### Pre-Deployment
- [ ] All agent YAML files validated
- [ ] Environment variables configured
- [ ] Authentication successful
- [ ] Backup of current deployment
- [ ] Rollback plan prepared

### Deployment
- [ ] Agents deployed successfully
- [ ] All agents listed in Orchestrate
- [ ] No deployment errors
- [ ] Agent status shows "active"

### Post-Deployment
- [ ] All agents tested
- [ ] Logs reviewed for errors
- [ ] Performance metrics acceptable
- [ ] End-to-end workflow tested
- [ ] Documentation updated

## Troubleshooting

### Deployment Fails

```bash
# Check validation
orchestrate agents validate -f conductor_agent.yaml

# Check authentication
orchestrate auth status

# Check environment
orchestrate env list

# View detailed error
orchestrate agents import -f conductor_agent.yaml --verbose
```

### Agent Not Responding

```bash
# Check agent status
orchestrate agents get conductor-agent

# View recent logs
orchestrate agents logs conductor-agent --tail 100

# Restart agent
orchestrate agents restart conductor-agent
```

### Performance Issues

```bash
# Check metrics
orchestrate agents metrics conductor-agent

# View slow queries
orchestrate agents logs conductor-agent --filter "duration>5000"

# Check resource usage
orchestrate agents resources conductor-agent
```

## Environment Management

### Multiple Environments

```bash
# Development
orchestrate env add dev \
  --instance $DEV_INSTANCE \
  --api-key $DEV_KEY

# Staging
orchestrate env add staging \
  --instance $STAGING_INSTANCE \
  --api-key $STAGING_KEY

# Production
orchestrate env add prod \
  --instance $PROD_INSTANCE \
  --api-key $PROD_KEY

# Switch environments
orchestrate env activate dev
orchestrate env activate prod
```

### Environment-Specific Configuration

```yaml
# conductor_agent.yaml
name: conductor-agent
version: 1.0.0
environment:
  dev:
    log_level: DEBUG
    timeout: 30
  prod:
    log_level: INFO
    timeout: 10
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to watsonx Orchestrate

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install ADK
        run: pip install ibm-watsonx-orchestrate
      
      - name: Configure Environment
        run: |
          orchestrate env add prod \
            --instance ${{ secrets.WO_INSTANCE }} \
            --api-key ${{ secrets.WO_API_KEY }}
          orchestrate env activate prod
      
      - name: Deploy Agents
        run: |
          cd docs/03-agents/agent-definitions/
          for agent in *.yaml; do
            orchestrate agents import -f $agent --force
          done
      
      - name: Verify Deployment
        run: orchestrate agents list
```

## Best Practices

### Deployment
- ✅ Always validate before deploying
- ✅ Test in staging first
- ✅ Deploy during low-traffic periods
- ✅ Have rollback plan ready
- ✅ Monitor after deployment
- ✅ Document changes

### Version Control
- ✅ Tag releases in git
- ✅ Keep YAML files in version control
- ✅ Document breaking changes
- ✅ Maintain changelog

### Security
- ✅ Never commit API keys
- ✅ Use environment variables
- ✅ Rotate keys regularly
- ✅ Limit access to production
- ✅ Audit deployments

## Related Documentation

- [Local Setup](./local-setup.md)
- [Testing Guide](./testing.md)
- [Integration Guide](../05-integration/watsonx-orchestrate.md)
- [Agent Architecture](../03-agents/agent-architecture.md)

---

**Deployment Platform**: IBM watsonx Orchestrate  
**Deployment Tool**: watsonx Orchestrate ADK  
**Deployment Strategy**: Incremental (recommended)
