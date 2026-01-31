# LexConductor - GitHub Branch Protection Rules
# IBM Dev Day AI Demystified Hackathon 2026

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

# GitHub Provider Configuration
provider "github" {
  token = var.github_token
  owner = var.github_owner
}

# Branch Protection Rule for master
resource "github_branch_protection" "master" {
  repository_id = var.repository_name
  pattern       = "master"

  # Require pull request reviews before merging
  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 1
    require_last_push_approval      = false
  }

  # Require status checks to pass before merging
  required_status_checks {
    strict   = true
    contexts = var.required_status_checks
  }

  # Enforce restrictions for administrators
  enforce_admins = false

  # Require signed commits
  require_signed_commits = false

  # Require linear history
  require_linear_history = true

  # Allow force pushes
  allows_force_pushes = false

  # Allow deletions
  allows_deletions = false

  # Require conversation resolution before merging
  require_conversation_resolution = true

  # Lock branch (read-only)
  lock_branch = false
}
