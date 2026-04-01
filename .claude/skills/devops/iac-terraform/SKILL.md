---
name: iac-terraform
description: Terraform and Terragrunt IaC — write modules, manage state, troubleshoot errors, review infrastructure code, set up CI/CD pipelines
---

## Runtime Context

- Terraform: !`terraform version 2>/dev/null | head -1 || echo "not installed"`
- Terragrunt: !`terragrunt --version 2>/dev/null | head -1 || echo "not installed"`
- TF files here: !`ls *.tf 2>/dev/null | tr '\n' ' ' || echo "none"`
- HCL files here: !`ls *.hcl 2>/dev/null | tr '\n' ' ' || echo "none"`

# Infrastructure as Code - Terraform & Terragrunt

Comprehensive guidance for infrastructure as code using Terraform and Terragrunt, from development through production deployment.

## When to Use This Skill

Use this skill when:
- Writing or refactoring Terraform configurations
- Creating reusable Terraform modules
- Troubleshooting Terraform/Terragrunt errors
- Managing Terraform state
- Implementing IaC best practices
- Setting up Terragrunt project structure
- Reviewing infrastructure code
- Debugging plan/apply issues

## Core Workflows

### 1. New Infrastructure Development

**Workflow Decision Tree:**

```
Is this reusable across environments/projects?
├─ Yes → Create a Terraform module
│   └─ See "Creating Terraform Modules" below
└─ No → Create environment-specific configuration
    └─ See "Environment Configuration" below
```

#### Creating Terraform Modules

When building reusable infrastructure:

1. **Scaffold new module with script:**
```bash
python3 .claude/skills/iac-terraform/scripts/init_module.py my-module-name
```

This automatically creates:
- Standard module file structure
- Template files with proper formatting
- Examples directory
- README with documentation

2. **Use module template structure:**
   - See `assets/templates/MODULE_TEMPLATE.md` for complete structure
   - Required files: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`
   - Recommended: `examples/` directory with working examples

3. **Follow module best practices:**
   - Single responsibility - one module, one purpose
   - Sensible defaults for optional variables
   - Complete descriptions for all variables and outputs
   - Input validation using `validation` blocks
   - Mark sensitive values with `sensitive = true`

4. **Validate module:**
```bash
python3 .claude/skills/iac-terraform/scripts/validate_module.py /path/to/module
```

This checks for:
- Required files present
- Variables have descriptions and types
- Outputs have descriptions
- README exists and is complete
- Naming conventions followed
- Sensitive values properly marked

5. **Test module:**
```bash
cd examples/complete
terraform init
terraform plan
```

6. **Document module:**
   - Use terraform-docs to auto-generate: `terraform-docs markdown . > README.md`
   - Include usage examples
   - Document all inputs and outputs

**Key Module Patterns:**

See `references/best_practices.md` "Module Design" section for:
- Composability patterns
- Variable organization
- Output design
- Module versioning strategies

#### Environment Configuration

For environment-specific infrastructure:

1. **Structure by environment:**
```
environments/
├── dev/
├── staging/
└── prod/
```

2. **Use consistent file organization:**
```
environment/
├── main.tf           # Resource definitions
├── variables.tf      # Variable declarations
├── terraform.tfvars  # Default values (committed)
├── secrets.auto.tfvars  # Sensitive values (.gitignore)
├── backend.tf        # State configuration
├── outputs.tf        # Output values
└── versions.tf       # Version constraints
```

3. **Reference modules:**
```hcl
module "vpc" {
  source = "git::https://github.com/company/terraform-modules.git//vpc?ref=v1.2.0"

  name        = "${var.environment}-vpc"
  vpc_cidr    = var.vpc_cidr
  environment = var.environment
}
```

### 2. State Management & Inspection

**When to inspect state:**
- Before major changes
- Investigating drift
- Debugging resource issues
- Auditing infrastructure

**Inspect state and check health:**
```bash
python3 .claude/skills/iac-terraform/scripts/inspect_state.py /path/to/terraform/directory
```

**Check for drift (WARNING: runs `terraform plan` — may be slow and requires cloud auth):**
```bash
python3 .claude/skills/iac-terraform/scripts/inspect_state.py /path/to/terraform/directory --check-drift
```

The script provides:
- Resource count and types
- Backend configuration
- Provider versions
- Issues with resources (tainted, etc.)
- Drift detection (if requested)

**Manual state operations:**
```bash
# List all resources
terraform state list

# Show specific resource
terraform state show aws_instance.web

# Remove from state (doesn't destroy)
terraform state rm aws_instance.web

# Move/rename resource
terraform state mv aws_instance.web aws_instance.web_server

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0
```

**State best practices:** See `references/best_practices.md` "State Management" section for:
- Remote backend setup (S3 + DynamoDB)
- State file organization strategies
- Encryption and security
- Backup and recovery procedures

### 3. Standard Terraform Workflow

```bash
# 1. Initialize (first time or after module changes)
terraform init

# 2. Format code
terraform fmt -recursive

# 3. Validate syntax
terraform validate

# 4. Plan changes (always review!)
terraform plan -out=tfplan

# 5. Apply changes
terraform apply tfplan

# 6. Verify outputs
terraform output
```

**With Terragrunt:**
```bash
# Run for single module
terragrunt plan
terragrunt apply

# Run for all modules in directory tree
terragrunt run-all plan
terragrunt run-all apply
```

### 4. Troubleshooting Issues

When encountering errors:

1. **Read the complete error message** - Don't skip details

2. **Check common issues:** See `references/troubleshooting.md` for:
   - State lock errors
   - State drift/corruption
   - Provider authentication failures
   - Resource errors (already exists, dependency errors, timeouts)
   - Module source issues
   - Terragrunt-specific issues (dependency cycles, hooks)
   - Performance problems

3. **Enable debug logging if needed:**
```bash
export TF_LOG=DEBUG
export TF_LOG_PATH=terraform-debug.log
terraform plan
```

4. **Isolate the problem:**
```bash
# Test specific resource
terraform plan -target=aws_instance.web
terraform apply -target=aws_instance.web
```

5. **Common quick fixes:**

**State locked:**
```bash
# Verify no one else running, then:
terraform force-unlock <lock-id>
```

**Provider cache issues:**
```bash
rm -rf .terraform
terraform init -upgrade
```

**Module cache issues:**
```bash
rm -rf .terraform/modules
terraform init
```

### 5. Code Review & Quality

**Before committing:**

1. **Format code:**
```bash
terraform fmt -recursive
```

2. **Validate syntax:**
```bash
terraform validate
```

3. **Lint with tflint:**
```bash
tflint --module
```

4. **Security scan with checkov:**
```bash
checkov -d .
```

5. **Validate modules:**
```bash
python3 .claude/skills/iac-terraform/scripts/validate_module.py modules/vpc
```

6. **Generate documentation:**
```bash
terraform-docs markdown modules/vpc > modules/vpc/README.md
```

**Review checklist:**
- [ ] All variables have descriptions
- [ ] Sensitive values marked as sensitive
- [ ] Outputs have descriptions
- [ ] Resources follow naming conventions
- [ ] No hardcoded values (use variables)
- [ ] README is complete and current
- [ ] Examples directory exists and works
- [ ] Version constraints specified
- [ ] Security best practices followed

See `references/best_practices.md` for comprehensive guidelines.

**Azure DevOps CI/CD integration:** Use `assets/workflows/azure-devops-terraform.yml` as the starting point. The pipeline runs format check, validate, TFLint, Checkov, and plan automatically on PRs. Apply requires a manual approval gate configured in ADO Environments.

### 6. Cost Review

When planning or auditing infrastructure costs:

1. **Tag all resources** for cost allocation — see `references/cost_optimization.md` "Cost Tagging" section
2. **Right-size compute** — start small, measure, scale up
3. **Use spot/preemptible instances** for non-critical workloads
4. **Apply S3 lifecycle policies** for log/archive data
5. **Add VPC endpoints** to avoid unnecessary NAT gateway charges
6. **Schedule non-prod shutdowns** — see scheduler patterns in cost_optimization.md
7. **Set budget alerts** with AWS Budgets / Azure Cost Management

See `references/cost_optimization.md` for full strategies including multi-cloud patterns.

## Terragrunt Patterns

### Project Structure

```
terragrunt-project/
├── terragrunt.hcl              # Root config
├── account.hcl                 # Account-level vars
├── region.hcl                  # Region-level vars
└── environments/
    ├── dev/
    │   ├── env.hcl            # Environment vars
    │   └── us-east-1/
    │       ├── vpc/
    │       │   └── terragrunt.hcl
    │       └── eks/
    │           └── terragrunt.hcl
    └── prod/
        └── us-east-1/
            ├── vpc/
            └── eks/
```

### Dependency Management

```hcl
# In eks/terragrunt.hcl
dependency "vpc" {
  config_path = "../vpc"

  # Mock outputs for plan/validate
  mock_outputs = {
    vpc_id         = "vpc-mock"
    subnet_ids     = ["subnet-mock"]
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

inputs = {
  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.private_subnet_ids
}
```

### Common Patterns

See `assets/templates/MODULE_TEMPLATE.md` for complete Terragrunt configuration templates including:
- Root terragrunt.hcl with provider generation
- Remote state configuration
- Module-level terragrunt.hcl patterns
- Dependency handling

## Reference Documentation

### references/best_practices.md

Comprehensive best practices covering:
- **Project Structure** - Recommended directory layouts
- **State Management** - Remote state, locking, organization
- **Module Design** - Single responsibility, composability, versioning
- **Variable Management** - Declarations, files hierarchy, secrets
- **Resource Naming** - Conventions and standards
- **Security Practices** - Least privilege, encryption, secret management
- **Testing & Validation** - Tools and approaches
- **CI/CD Integration** - Pipeline patterns

### references/troubleshooting.md

Detailed troubleshooting guide for:
- **State Issues** - Lock errors, drift, corruption
- **Provider Issues** - Version conflicts, authentication
- **Resource Errors** - Already exists, dependencies, timeouts
- **Module Issues** - Source not found, version conflicts
- **Terragrunt Specific** - Dependency cycles, hooks
- **Performance Issues** - Slow plans, optimization strategies

### references/cost_optimization.md

Cloud cost optimization strategies:
- **Right-Sizing Resources** - Compute, database, and storage optimization
- **Spot and Reserved Instances** - Cost-effective instance strategies
- **Storage Optimization** - S3 lifecycle policies, EBS volume types
- **Networking Costs** - VPC endpoints, data transfer optimization
- **Resource Lifecycle** - Scheduled shutdown, cleanup automation
- **Cost Tagging** - Comprehensive tagging for cost allocation
- **Monitoring and Alerts** - Budget alerts, anomaly detection
- **Multi-Cloud** - Azure, GCP cost optimization patterns

## CI/CD Workflows

Ready-to-use CI/CD pipeline templates in `assets/workflows/`:

### azure-devops-terraform.yml (primary)

Azure DevOps pipeline with 4 stages:
- **Validate** — `terraform fmt`, `terraform validate`, TFLint
- **Security** — Checkov scan (soft fail, non-blocking)
- **Plan** — Init + plan with artifact publishing; plan output shown in pipeline logs
- **Apply** — Manual approval gate via ADO Environment, downloads plan artifact and applies

Supports both **AWS** (via `AWSShellScript` task + service connection) and **Azure** (via `AzureCLI` task + ARM service connection) — see commented-out blocks in the file.

**Setup required in Azure DevOps:**
1. Create a variable group named `terraform-vars` with backend config values
2. Create a Service Connection for your cloud provider (AWS or Azure)
3. Create an Environment named `production` with an approval check: Project Settings → Environments → Approvals and Checks

### Other templates (reference)

- **github-actions-terraform.yml** — GitHub Actions with OIDC auth
- **github-actions-terragrunt.yml** — GitHub Actions Terragrunt with changed-module detection
- **gitlab-ci-terraform.yml** — GitLab CI multi-stage pipeline

## Scripts

### scripts/init_module.py

Scaffolds a new Terraform module with proper structure and template files.

```bash
python3 .claude/skills/iac-terraform/scripts/init_module.py my-vpc
python3 .claude/skills/iac-terraform/scripts/init_module.py my-vpc --path ./modules
python3 .claude/skills/iac-terraform/scripts/init_module.py my-vpc --json
```

### scripts/inspect_state.py

Comprehensive state inspection and health check.

**WARNING:** `--check-drift` runs `terraform plan` which contacts your cloud provider, requires valid credentials, and may take several minutes on large state files.

```bash
python3 .claude/skills/iac-terraform/scripts/inspect_state.py /path/to/terraform
python3 .claude/skills/iac-terraform/scripts/inspect_state.py /path/to/terraform --check-drift
```

### scripts/validate_module.py

Validates Terraform modules against best practices.

```bash
python3 .claude/skills/iac-terraform/scripts/validate_module.py /path/to/module
```

Returns issues (must fix), warnings (should fix), and suggestions (consider).

## Quick Reference

### Essential Commands

```bash
terraform init / init -upgrade
terraform validate
terraform fmt -recursive
terraform plan / plan -out=tfplan
terraform apply / apply tfplan
terraform destroy / destroy -target=<resource>
terraform state list / show <resource> / rm <resource> / mv <old> <new>
terraform import <address> <id>
terraform output / output <name>
```

### Terragrunt Commands

```bash
terragrunt plan / apply / destroy
terragrunt run-all plan / apply / destroy
terragrunt run-all apply --terragrunt-include-dir vpc --terragrunt-include-dir eks
```

## Best Practices Summary

**Always:** remote state with locking, plan before apply, pin versions, use modules, mark sensitive values, document, test in non-prod first.

**Never:** commit secrets, manually edit state files, use root credentials, skip review for prod, ignore security findings.
