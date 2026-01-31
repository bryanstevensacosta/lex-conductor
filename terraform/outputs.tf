# LexConductor - Terraform Outputs
# IBM Dev Day AI Demystified Hackathon 2026

output "branch_protection_id" {
  description = "The ID of the branch protection rule"
  value       = github_branch_protection.master.id
}

output "protected_branch" {
  description = "The name of the protected branch"
  value       = github_branch_protection.master.pattern
}

output "repository" {
  description = "The repository name"
  value       = var.repository_name
}
