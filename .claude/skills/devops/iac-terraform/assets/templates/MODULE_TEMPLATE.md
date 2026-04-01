# Terraform Module Template

Reference template for creating well-structured Terraform modules.

## Module Structure

```
module-name/
├── main.tf           # Primary resource definitions
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── versions.tf       # Version constraints
├── README.md         # Module documentation
└── examples/
    └── complete/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

---

## main.tf

```hcl
# Use locals for computed values
locals {
  common_tags = merge(
    var.tags,
    {
      Name      = var.name
      Module    = "module-name"
      ManagedBy = "Terraform"
    }
  )
}

resource "aws_example" "main" {
  name = var.name

  tags = local.common_tags
}
```

---

## variables.tf

```hcl
variable "name" {
  description = "Name to be used on all resources as prefix"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid IPv4 CIDR block."
  }
}

variable "environment" {
  description = "Environment name"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

# Sensitive variable
variable "database_password" {
  description = "Master password for the database"
  type        = string
  sensitive   = true
}

# Complex type
variable "subnets" {
  description = "Map of subnet configurations"
  type = map(object({
    cidr_block        = string
    availability_zone = string
    public            = bool
  }))
  default = {}
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}
```

---

## outputs.tf

```hcl
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs for deploying workloads"
  value       = aws_subnet.private[*].id
}

# Sensitive output
output "database_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

# Complex output
output "subnet_details" {
  description = "Detailed information about all subnets"
  value = {
    for subnet in aws_subnet.main :
    subnet.id => {
      cidr_block        = subnet.cidr_block
      availability_zone = subnet.availability_zone
      public            = subnet.map_public_ip_on_launch
    }
  }
}
```

---

## versions.tf

```hcl
terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
}
```

---

## README.md Template

```markdown
# Module Name

Brief description of what this module does.

## Usage

\`\`\`hcl
module "example" {
  source = "./modules/module-name"

  name        = "my-resource"
  vpc_cidr    = "10.0.0.0/16"
  environment = "prod"

  tags = {
    Environment = "prod"
    Project     = "example"
  }
}
\`\`\`

## Examples

- [Complete](./examples/complete) - Full example with all options

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.3.0 |
| aws | >= 5.0.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| name | Resource name | \`string\` | n/a | yes |
| vpc_cidr | VPC CIDR block | \`string\` | n/a | yes |
| environment | Environment name | \`string\` | n/a | yes |
| tags | Common tags | \`map(string)\` | \`{}\` | no |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | VPC identifier |
| private_subnet_ids | List of private subnet IDs |

## Authors

Module maintained by your team.

## License

Apache 2 Licensed.
```

---

## examples/complete/main.tf

```hcl
provider "aws" {
  region = var.region
}

module "example" {
  source = "../../"

  name        = "example"
  vpc_cidr    = "10.0.0.0/16"
  environment = "dev"

  tags = {
    Environment = "dev"
    Project     = "example"
    ManagedBy   = "Terraform"
  }
}
```

---

## Terragrunt Configuration Templates

### Root terragrunt.hcl

```hcl
locals {
  account_vars     = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars      = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  environment_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  account_name = local.account_vars.locals.account_name
  account_id   = local.account_vars.locals.account_id
  aws_region   = local.region_vars.locals.aws_region
  environment  = local.environment_vars.locals.environment
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"
  assume_role { role_arn = "arn:aws:iam::${local.account_id}:role/TerraformRole" }
  default_tags {
    tags = {
      Environment = "${local.environment}"
      ManagedBy   = "Terragrunt"
    }
  }
}
EOF
}

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "${local.account_name}-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.aws_region
    encrypt        = true
    dynamodb_table = "${local.account_name}-terraform-lock"
  }
}

inputs = {
  account_name = local.account_name
  account_id   = local.account_id
  aws_region   = local.aws_region
  environment  = local.environment
}
```

### Module-level terragrunt.hcl

```hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "git::https://github.com/company/terraform-modules.git//vpc?ref=v1.0.0"
}

dependency "iam" {
  config_path = "../iam"
  mock_outputs = {
    role_arn = "arn:aws:iam::123456789012:role/mock"
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

inputs = {
  name         = "my-vpc"
  vpc_cidr     = "10.0.0.0/16"
  iam_role_arn = dependency.iam.outputs.role_arn
  tags = {
    Component = "networking"
  }
}
```

---

## Best Practices Checklist

- [ ] Descriptions on all variables and outputs
- [ ] Validation blocks on important variables
- [ ] Sensitive values marked `sensitive = true`
- [ ] Sensible defaults where appropriate
- [ ] README with usage examples
- [ ] Working example in `examples/` directory
- [ ] Module versioned with Git tags
- [ ] `versions.tf` with version constraints
