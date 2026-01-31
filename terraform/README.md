# Terraform - GitHub Branch Protection

This Terraform configuration manages branch protection rules for the LexConductor repository.

## Prerequisites

1. **Terraform installed** (>= 1.0)
   ```bash
   brew install terraform  # macOS
   ```

2. **GitHub Personal Access Token** with permissions:
   - `repo` (Full control of private repositories)
   - `admin:repo_hook` (Full control of repository hooks)
   
   Create token at: https://github.com/settings/tokens/new

## Setup

1. **Navigate to terraform directory:**
   ```bash
   cd terraform
   ```

2. **Create terraform.tfvars:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

3. **Edit terraform.tfvars with your values:**
   ```hcl
   github_token = "ghp_your_actual_token_here"
   github_owner = "your-github-username"
   repository_name = "lex-conductor"
   ```

4. **Initialize Terraform:**
   ```bash
   terraform init
   ```

## Usage

### Plan Changes
Preview what Terraform will do:
```bash
terraform plan
```

### Apply Changes
Create/update branch protection rules:
```bash
terraform apply
```

### Destroy Resources
Remove branch protection rules:
```bash
terraform destroy
```

## Branch Protection Rules

The configuration applies the following rules to the `master` branch:

### Pull Request Requirements
- ✅ Require pull request reviews before merging
- ✅ Require 1 approving review
- ✅ Dismiss stale reviews when new commits are pushed
- ✅ Require conversation resolution before merging

### Status Checks
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Required checks:
  - `pre-commit` - Pre-commit hooks
  - `black` - Code formatting
  - `ruff` - Linting
  - `mypy` - Type checking

### Branch Restrictions
- ✅ Require linear history (no merge commits)
- ❌ No force pushes allowed
- ❌ No branch deletion allowed
- ❌ Administrators not exempt from rules

### Security
- ❌ Signed commits not required (optional)
- ❌ Branch not locked (allows commits via PR)

## Customization

### Add More Status Checks

Edit `terraform.tfvars`:
```hcl
required_status_checks = [
  "pre-commit",
  "black",
  "ruff",
  "mypy",
  "pytest",           # Add unit tests
  "integration-tests" # Add integration tests
]
```

### Require More Reviewers

Edit `main.tf`:
```hcl
required_pull_request_reviews {
  required_approving_review_count = 2  # Change from 1 to 2
}
```

### Require Signed Commits

Edit `main.tf`:
```hcl
require_signed_commits = true
```

### Exempt Administrators

Edit `main.tf`:
```hcl
enforce_admins = false  # Admins can bypass rules
```

## Troubleshooting

### Error: "Resource not accessible by personal access token"
- Ensure your token has `repo` and `admin:repo_hook` permissions
- Regenerate token if needed

### Error: "Branch protection rule already exists"
- Run `terraform import` to import existing rule:
  ```bash
  terraform import github_branch_protection.master your-repo:master
  ```

### Error: "Required status check does not exist"
- Ensure CI/CD workflows are configured in `.github/workflows/`
- Status checks must run at least once before being required

## Security Notes

⚠️ **NEVER commit terraform.tfvars to git** - it contains your GitHub token

✅ The `.gitignore` file is configured to exclude:
- `*.tfvars` (except examples)
- `.terraform/` directory
- `*.tfstate` files
- Sensitive files

## CI/CD Integration

To use this in GitHub Actions:

```yaml
name: Terraform

on:
  push:
    branches: [master]
    paths: ['terraform/**']

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        
      - name: Terraform Init
        run: terraform init
        working-directory: ./terraform
        
      - name: Terraform Plan
        run: terraform plan
        working-directory: ./terraform
        env:
          TF_VAR_github_token: ${{ secrets.GH_TOKEN }}
          TF_VAR_github_owner: ${{ github.repository_owner }}
```

## Resources

- [Terraform GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest/docs)
- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Terraform Documentation](https://www.terraform.io/docs)

---

**Last Updated:** January 30, 2026  
**Project:** LexConductor - IBM Dev Day AI Demystified Hackathon  
**Team:** AI Kings 👑
