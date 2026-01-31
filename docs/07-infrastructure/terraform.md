# Terraform Setup

Infrastructure as Code (IaC) setup for Lex Conductor using Terraform.

## Overview

Terraform configuration for provisioning IBM Cloud resources for Lex Conductor.

**Note**: Terraform is **optional** for the hackathon. Manual setup via IBM Cloud console is sufficient.

## Prerequisites

- Terraform 1.0+ installed
- IBM Cloud CLI installed
- IBM Cloud API key
- Basic Terraform knowledge

## Installation

### Install Terraform

```bash
# macOS (Homebrew)
brew install terraform

# Linux (Ubuntu/Debian)
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Verify installation
terraform version
```

### Install IBM Cloud CLI

```bash
# macOS
curl -fsSL https://clis.cloud.ibm.com/install/osx | sh

# Linux
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh

# Verify
ibmcloud --version
```

## Configuration

### Directory Structure

```
terraform/
├── main.tf              # Main configuration
├── variables.tf         # Variable definitions
├── outputs.tf           # Output values
├── terraform.tfvars.example  # Variable values template
├── .gitignore          # Ignore terraform state
└── README.md           # Terraform documentation
```

### Configure Variables

```bash
# Copy template
cp terraform/terraform.tfvars.example terraform/terraform.tfvars

# Edit with your values
nano terraform/terraform.tfvars
```

Example `terraform.tfvars`:

```hcl
# IBM Cloud Configuration
ibmcloud_api_key = "your_ibm_cloud_api_key"
region           = "us-south"
resource_group   = "default"

# Project Configuration
project_name = "lex-conductor"
environment  = "development"

# watsonx Orchestrate
orchestrate_plan = "lite"  # or "standard"

# watsonx.ai (optional)
watsonx_ai_enabled = false
watsonx_ai_plan    = "lite"
```

## Terraform Files

### main.tf

```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    ibm = {
      source  = "IBM-Cloud/ibm"
      version = "~> 1.60"
    }
  }
}

provider "ibm" {
  ibmcloud_api_key = var.ibmcloud_api_key
  region           = var.region
}

# Resource Group
data "ibm_resource_group" "group" {
  name = var.resource_group
}

# watsonx Orchestrate Instance
resource "ibm_resource_instance" "orchestrate" {
  name              = "${var.project_name}-orchestrate"
  service           = "watson-orchestrate"
  plan              = var.orchestrate_plan
  location          = var.region
  resource_group_id = data.ibm_resource_group.group.id

  tags = [
    "project:${var.project_name}",
    "environment:${var.environment}"
  ]
}

# watsonx.ai Instance (optional)
resource "ibm_resource_instance" "watsonx_ai" {
  count             = var.watsonx_ai_enabled ? 1 : 0
  name              = "${var.project_name}-watsonx-ai"
  service           = "watsonx-ai"
  plan              = var.watsonx_ai_plan
  location          = var.region
  resource_group_id = data.ibm_resource_group.group.id

  tags = [
    "project:${var.project_name}",
    "environment:${var.environment}"
  ]
}
```

### variables.tf

```hcl
variable "ibmcloud_api_key" {
  description = "IBM Cloud API Key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "IBM Cloud region"
  type        = string
  default     = "us-south"
}

variable "resource_group" {
  description = "IBM Cloud resource group"
  type        = string
  default     = "default"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "lex-conductor"
}

variable "environment" {
  description = "Environment (development, staging, production)"
  type        = string
  default     = "development"
}

variable "orchestrate_plan" {
  description = "watsonx Orchestrate service plan"
  type        = string
  default     = "lite"
}

variable "watsonx_ai_enabled" {
  description = "Enable watsonx.ai instance"
  type        = bool
  default     = false
}

variable "watsonx_ai_plan" {
  description = "watsonx.ai service plan"
  type        = string
  default     = "lite"
}
```

### outputs.tf

```hcl
output "orchestrate_instance_id" {
  description = "watsonx Orchestrate instance ID"
  value       = ibm_resource_instance.orchestrate.id
}

output "orchestrate_instance_url" {
  description = "watsonx Orchestrate instance URL"
  value       = ibm_resource_instance.orchestrate.dashboard_url
}

output "watsonx_ai_instance_id" {
  description = "watsonx.ai instance ID"
  value       = var.watsonx_ai_enabled ? ibm_resource_instance.watsonx_ai[0].id : null
}

output "resource_group_id" {
  description = "Resource group ID"
  value       = data.ibm_resource_group.group.id
}
```

## Usage

### Initialize Terraform

```bash
cd terraform/

# Initialize Terraform
terraform init

# Verify configuration
terraform validate
```

### Plan Infrastructure

```bash
# Preview changes
terraform plan

# Save plan to file
terraform plan -out=tfplan

# Review plan
terraform show tfplan
```

### Apply Configuration

```bash
# Apply changes
terraform apply

# Or apply saved plan
terraform apply tfplan

# Confirm with 'yes' when prompted
```

### View Outputs

```bash
# Show all outputs
terraform output

# Show specific output
terraform output orchestrate_instance_url
```

### Destroy Infrastructure

```bash
# Preview destruction
terraform plan -destroy

# Destroy all resources
terraform destroy

# Confirm with 'yes' when prompted
```

## State Management

### Local State (Default)

```bash
# State stored in terraform.tfstate
ls -la terraform.tfstate

# Never commit state files!
echo "terraform.tfstate*" >> .gitignore
```

### Remote State (Recommended for Teams)

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket = "lex-conductor-terraform-state"
    key    = "terraform.tfstate"
    region = "us-south"
  }
}
```

## Best Practices

### Security
- ✅ Never commit `terraform.tfvars`
- ✅ Use `.tfvars.example` for templates
- ✅ Store state securely
- ✅ Use remote state for teams
- ✅ Rotate API keys regularly

### Organization
- ✅ Use modules for reusability
- ✅ Keep configurations DRY
- ✅ Use consistent naming
- ✅ Tag all resources
- ✅ Document variables

### Workflow
- ✅ Always run `terraform plan` first
- ✅ Review changes before applying
- ✅ Use workspaces for environments
- ✅ Version control configurations
- ✅ Test in non-production first

## Troubleshooting

### Authentication Issues

```bash
# Verify API key
ibmcloud login --apikey $IBMCLOUD_API_KEY

# Check permissions
ibmcloud iam user-policies $USER_EMAIL
```

### Resource Creation Fails

```bash
# Check quota limits
ibmcloud resource quotas

# Verify region availability
ibmcloud regions

# Check service availability
ibmcloud catalog service watson-orchestrate
```

### State Lock Issues

```bash
# Force unlock (use with caution)
terraform force-unlock <LOCK_ID>

# Remove corrupted state
rm terraform.tfstate
terraform init
```

## Alternative: Manual Setup

For the hackathon, manual setup via IBM Cloud console is simpler:

1. Log in to IBM Cloud
2. Go to Catalog
3. Search for "watsonx Orchestrate"
4. Create instance
5. Configure and launch

See [IBM Cloud Setup Guide](./ibm-cloud.md) for details.

## Related Documentation

- [IBM Cloud Setup](./ibm-cloud.md)
- [Security Guide](./security.md)
- [Infrastructure Overview](./README.md)

---

**Tool**: Terraform  
**Provider**: IBM Cloud  
**Status**: Optional for hackathon
