# Terraform Troubleshooting Guide

Common Terraform and Terragrunt issues with solutions.

## Table of Contents

1. [State Issues](#state-issues)
2. [Provider Issues](#provider-issues)
3. [Resource Errors](#resource-errors)
4. [Module Issues](#module-issues)
5. [Terragrunt Specific](#terragrunt-specific)
6. [Performance Issues](#performance-issues)

---

## State Issues

### State Lock Error

**Symptom:**
```
Error locking state: Error acquiring the state lock
Lock Info:
  ID: abc123...
  Operation: OperationTypeApply
  Who: user@hostname
```

**Resolution:**
1. Verify no one else is running terraform first
2. Force unlock (use with caution):
```bash
terraform force-unlock abc123
```
3. Check DynamoDB lock table:
```bash
aws dynamodb get-item \
  --table-name terraform-state-lock \
  --key '{"LockID": {"S": "path/to/state/terraform.tfstate-md5"}}'
```

**Prevention:** Use S3 + DynamoDB backend with proper timeout in CI/CD pipelines.

---

### State Drift Detected

**Symptom:**
```
Note: Objects have changed outside of Terraform
Terraform detected the following changes made outside of Terraform
```

**Resolution:**
1. Review the drift: `terraform plan -detailed-exitcode`
2. Options:
   - **Accept changes:** `terraform apply -refresh-only`
   - **Revert to desired state:** `terraform apply`
   - **Update config to match reality:** edit `.tf` files then plan

**Prevention:** Implement policy preventing manual console changes. Run regular `terraform plan` in CI to detect drift early.

---

### State Corruption / Version Mismatch

**Symptom:**
```
Error: state snapshot was created by Terraform v1.5.0,
which is newer than current v1.3.0
```

**Resolution:**
1. Upgrade Terraform to matching version: `tfenv install 1.5.0 && tfenv use 1.5.0`
2. Restore from S3 backup:
```bash
aws s3api list-object-versions --bucket terraform-state --prefix prod/terraform.tfstate
aws s3api get-object --bucket terraform-state --key prod/terraform.tfstate --version-id VERSION_ID terraform.tfstate
```
3. Last resort — rebuild state:
```bash
terraform state rm aws_instance.example
terraform import aws_instance.example i-1234567890abcdef0
```

**Prevention:** Pin Terraform version in `versions.tf`. Enable S3 versioning. Never manually edit state files.

---

## Provider Issues

### Provider Version Conflict

**Symptom:**
```
Error: Incompatible provider version
Provider registry.terraform.io/hashicorp/aws v5.0.0 does not have a package available
```

**Resolution:**
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.67.0"
    }
  }
}
```
Then: `rm -rf .terraform && terraform init -upgrade`

Lock multi-platform:
```bash
terraform providers lock -platform=darwin_amd64 -platform=linux_amd64
```

---

### Authentication Failures

**Symptom:**
```
Error: no valid credential sources found
```

**Resolution:**
1. Verify credentials: `aws sts get-caller-identity`
2. Check credential chain order: env vars → `~/.aws/credentials` → IAM role
3. Configure provider with role assumption:
```hcl
provider "aws" {
  region = "us-east-1"
  assume_role { role_arn = "arn:aws:iam::ACCOUNT:role/TerraformRole" }
}
```

**Prevention:** Use OIDC for GitHub Actions, IAM roles for CI/CD, AWS SSO for developers.

---

## Resource Errors

### Resource Already Exists

**Symptom:**
```
Error: EntityAlreadyExists: Resource with id 'i-1234567890abcdef0' already exists
```

**Resolution:**
```bash
terraform import aws_instance.web i-1234567890abcdef0
terraform plan  # Should show no changes after import
```

---

### Dependency Errors

**Symptom:**
```
Error: resource depends on resource that is not declared in the configuration
```

**Resolution:**
```hcl
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.main.id
  depends_on = [aws_internet_gateway.main]
}
```

Or use data sources for pre-existing resources:
```hcl
data "aws_vpc" "existing" { id = "vpc-12345678" }
resource "aws_subnet" "new" { vpc_id = data.aws_vpc.existing.id }
```

---

### Timeout Errors

**Symptom:**
```
Error: timeout while waiting for state to become 'available' (timeout: 10m0s)
```

**Resolution:**
```hcl
resource "aws_db_instance" "main" {
  timeouts {
    create = "60m"
    update = "60m"
    delete = "60m"
  }
}
```

---

## Module Issues

### Module Source Not Found

**Symptom:**
```
Error: Failed to download module
Could not download module "vpc" source
```

**Resolution:**
1. Verify source URL is correct and accessible
2. For private repos, configure Git auth:
```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```
3. Clear module cache: `rm -rf .terraform/modules && terraform init`

---

### Module Version Conflicts

**Symptom:**
```
Error: Inconsistent dependency lock file
```

**Resolution:**
```bash
terraform init -upgrade
```
Pin module version explicitly:
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"
}
```

---

## Terragrunt Specific

### Dependency Cycle Detected

**Symptom:**
```
Error: Dependency cycle detected
```

**Resolution:**
1. Review `dependency` blocks in terragrunt.hcl files
2. Refactor to remove the cycle — split modules or use data sources instead
3. Use mock outputs for planning:
```hcl
dependency "vpc" {
  config_path = "../vpc"
  mock_outputs = { vpc_id = "vpc-mock" }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}
```

---

### Hook Failures

**Symptom:**
```
Error: Hook execution failed
Command: pre_apply_hook.sh
Exit code: 1
```

**Resolution:**
1. Run hook manually to debug: `bash .terragrunt-cache/.../pre_apply_hook.sh`
2. Ensure hook is executable: `chmod +x hooks/pre_apply_hook.sh`
3. Add proper error handling in the hook script

---

### Include Path Issues

**Symptom:**
```
Error: Cannot include file — Path does not exist: ../common.hcl
```

**Resolution:**
```hcl
include "root" {
  path = find_in_parent_folders()
}
include "common" {
  path = "${get_terragrunt_dir()}/../common.hcl"
}
```

---

## Performance Issues

### Slow Plans/Applies

**Causes:** Too many resources in single state, slow provider API calls, many data sources, complex interpolations.

**Resolution:**
1. Split into multiple state files
2. Use targeted operations: `terraform plan -target=module.vpc`
3. Minimize data sources — pin AMI IDs instead of querying each plan
4. Increase parallelism: `terraform apply -parallelism=20`
5. Terragrunt: add `skip_credentials_validation = true` for faster init

---

## Quick Diagnostic Steps

When encountering any error:

1. **Read the full error** — don't skip the details
2. **Check recent changes** — what changed since last success?
3. **Verify versions** — Terraform, providers, modules
4. **Check state** — locked? corrupted?
5. **Test auth** — `aws sts get-caller-identity`
6. **Enable debug logging:**
```bash
export TF_LOG=DEBUG
export TF_LOG_PATH=terraform-debug.log
terraform plan
```
7. **Isolate:** use `-target` to test specific resources

---

## Prevention Checklist

- [ ] Remote state with locking
- [ ] Pinned Terraform and provider versions
- [ ] Pre-commit hooks (fmt, validate)
- [ ] Plan before every apply
- [ ] State versioning/backups enabled
- [ ] CI/CD with proper review gates
- [ ] Regular drift detection in CI
