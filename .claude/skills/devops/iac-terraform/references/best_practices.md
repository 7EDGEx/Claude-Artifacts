# Terraform Best Practices

Comprehensive guide to Terraform best practices for infrastructure as code.

## Table of Contents

1. [Project Structure](#project-structure)
2. [State Management](#state-management)
3. [Module Design](#module-design)
4. [Variable Management](#variable-management)
5. [Resource Naming](#resource-naming)
6. [Security Practices](#security-practices)
7. [Testing & Validation](#testing--validation)
8. [CI/CD Integration](#cicd-integration)

---

## Project Structure

### Recommended Directory Layout

```
terraform-project/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   └── README.md
│   ├── compute/
│   └── database/
├── global/
│   ├── iam/
│   └── dns/
└── README.md
```

### Key Principles

**Separate Environments** — Use directories for each environment (dev, staging, prod). Each environment has its own state file to prevent accidental cross-environment changes.

**Reusable Modules** — Common infrastructure patterns in `modules/`. Modules are versioned and tested, used across multiple environments.

**Global Resources** — Resources shared across environments (IAM, DNS) kept in a separate state with extra review scrutiny.

---

## State Management

### Remote State is Essential

**Recommended Backend: S3 + DynamoDB**

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/networking/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    kms_key_id     = "arn:aws:kms:us-east-1:ACCOUNT:key/KEY_ID"
  }
}
```

**State Best Practices:**
1. Enable encryption at rest
2. Enable S3 versioning for state recovery
3. Use DynamoDB locking to prevent concurrent modifications
4. Restrict IAM access to state files
5. Use separate state files per component (reduced blast radius)
6. Automate state backups

### State File Organization

**Bad:** Single `terraform.tfstate` containing everything.

**Good:** Separate state files per logical component:
```
networking/terraform.tfstate
compute/terraform.tfstate
database/terraform.tfstate
```

### State Management Commands

```bash
terraform state list
terraform state show aws_instance.example
terraform state mv aws_instance.old aws_instance.new
terraform state rm aws_instance.example
terraform import aws_instance.example i-1234567890abcdef0
terraform state pull > state.json  # Read-only inspection
```

---

## Module Design

### Module Structure

```
module-name/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── README.md
└── examples/
    └── complete/
        ├── main.tf
        └── variables.tf
```

### Module Best Practices

**Single Responsibility** — Each module does one thing well.

**Composability** — Modules work together via outputs/inputs:
```hcl
module "vpc" { source = "./modules/vpc"; cidr = "10.0.0.0/16" }
module "eks" { source = "./modules/eks"; vpc_id = module.vpc.vpc_id; subnet_ids = module.vpc.private_subnet_ids }
```

**Sensible Defaults:**
```hcl
variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t3.micro"
}
```

**Complete Documentation with Validation:**
```hcl
variable "vpc_cidr" {
  type        = string
  description = "CIDR block for VPC. Must be a valid IPv4 CIDR."
  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid IPv4 CIDR block."
  }
}
```

**Useful Outputs:**
```hcl
output "private_subnet_ids" {
  description = "List of private subnet IDs for deploying workloads"
  value       = aws_subnet.private[*].id
}
```

### Module Versioning

```hcl
module "vpc" {
  source = "git::https://github.com/company/terraform-modules.git//vpc?ref=v1.2.3"
}
```

Use semantic versioning: `v1.0.0` (initial), `v1.1.0` (new features), `v1.1.1` (bug fixes), `v2.0.0` (breaking changes).

---

## Variable Management

### Variable Declaration

Always include type, description, and validation where relevant:
```hcl
variable "environment" {
  type        = string
  description = "Environment name (dev, staging, prod)"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Variable Files Hierarchy

```
terraform.tfvars        # Default values (committed, no secrets)
dev.tfvars             # Dev overrides
prod.tfvars            # Prod overrides
secrets.auto.tfvars    # Auto-loaded (in .gitignore)
```

### Sensitive Variables

```hcl
variable "database_password" {
  type        = string
  description = "Master password for database"
  sensitive   = true
}
```

**Better: Use External Secret Management**
```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/master-password"
}
resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

---

## Resource Naming

**Terraform Resources (snake_case):**
```hcl
resource "aws_vpc" "main_vpc" { }
resource "aws_instance" "web_server_01" { }
```

**AWS Resource Names (kebab-case):**
```
company-prod-api-alb
company-dev-workers-asg
company-staging-database-rds
```

**Pattern:** `{company}-{environment}-{service}-{resource_type}`

---

## Security Practices

### Least Privilege IAM
```hcl
resource "aws_iam_policy" "good" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "arn:aws:s3:::my-bucket/*"
    }]
  })
}
```

### Encryption Everywhere
```hcl
# S3 — server-side encryption with KMS
resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.secure.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.bucket.arn
    }
  }
}

# EBS — encrypted root volume
resource "aws_instance" "secure" {
  root_block_device { encrypted = true }
}

# RDS — encrypted storage
resource "aws_db_instance" "secure" {
  storage_encrypted = true
  kms_key_id       = aws_kms_key.rds.arn
}
```

### Secret Management

```hcl
# NEVER DO THIS:
resource "aws_db_instance" "bad" { password = "MySecretPassword123" }

# CORRECT:
data "aws_secretsmanager_secret_version" "db" { secret_id = var.db_secret_arn }
resource "aws_db_instance" "good" { password = data.aws_secretsmanager_secret_version.db.secret_string }
```

### Consistent Tagging
```hcl
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Owner       = "platform-team"
    Project     = var.project_name
    CostCenter  = var.cost_center
  }
}
resource "aws_instance" "web" {
  tags = merge(local.common_tags, { Name = "web-server" })
}
```

---

## Testing & Validation

```bash
terraform validate          # Syntax check
terraform plan -out=tfplan  # Review before apply
tflint --module             # Lint
checkov -d .                # Security scanning
terraform-docs markdown . > README.md  # Auto-docs
```

**Terratest (Go) for automated testing:**
```go
func TestVPCCreation(t *testing.T) {
    opts := terraform.WithDefaultRetryableErrors(t, &terraform.Options{TerraformDir: "../examples/complete"})
    defer terraform.Destroy(t, opts)
    terraform.InitAndApply(t, opts)
    vpcId := terraform.Output(t, opts, "vpc_id")
    assert.NotEmpty(t, vpcId)
}
```

---

## CI/CD Integration

**Best Practices:**
1. Always run plan on PRs — review before merge
2. Require approvals for production
3. Use workspaces/directories — separate pipeline per environment
4. Use OIDC or IAM roles — never store credentials
5. Run security scans (checkov, tfsec) in pipeline
6. Enable S3 state versioning for recovery

---

## Common Pitfalls to Avoid

| Pitfall | Fix |
|---------|-----|
| Local state | Use remote backend |
| Hardcoded values | Use variables and locals |
| Copying code between envs | Create reusable modules |
| Manual infra changes | All changes through Terraform |
| Poor resource names | Follow naming conventions |
| No documentation | Document everything |
| Single giant state file | Split into logical components |
| Deploy directly to prod | Test in dev/staging first |
