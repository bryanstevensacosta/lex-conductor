# LexConductor - Terraform Variables
# IBM Dev Day AI Demystified Hackathon 2026

variable "github_token" {
  description = "GitHub Personal Access Token with repo and admin:repo_hook permissions"
  type        = string
  sensitive   = true
}

variable "github_owner" {
  description = "GitHub organization or username that owns the repository"
  type        = string
}

variable "repository_name" {
  description = "Name of the GitHub repository"
  type        = string
  default     = "lex-conductor"
}

variable "required_status_checks" {
  description = "List of status checks that must pass before merging"
  type        = list(string)
  default = [
    "pre-commit",
    "black",
    "ruff",
    "mypy"
  ]
}
