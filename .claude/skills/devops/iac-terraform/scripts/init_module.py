#!/usr/bin/env python3
"""
Terraform Module Scaffolding Tool
Creates a standardized Terraform module structure with template files.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TEMPLATES = {
    "main.tf": """\
# {module_title} Module
# TODO: Add resource definitions

# locals {{
#   common_tags = merge(var.tags, {{
#     Module = "{module_name}"
#   }})
# }}

# Example resource (replace with actual resources):
# resource "aws_example" "main" {{
#   name = var.name
#   tags = local.common_tags
# }}
""",

    "variables.tf": """\
variable "name" {{
  description = "Name to be used on all resources as a prefix"
  type        = string
}}

variable "environment" {{
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {{
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }}
}}

variable "tags" {{
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {{}}
}}

# Example: sensitive variable
# variable "secret_value" {{
#   description = "A sensitive value"
#   type        = string
#   sensitive   = true
# }}
""",

    "outputs.tf": """\
# output "id" {{
#   description = "The ID of the primary resource"
#   value       = aws_example.main.id
# }}

# output "arn" {{
#   description = "The ARN of the primary resource"
#   value       = aws_example.main.arn
# }}
""",

    "versions.tf": """\
terraform {{
  required_version = ">= 1.3.0"

  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }}
  }}
}}
""",

    "README.md": """\
# {module_title} Module

Brief description of what this module does.

## Usage

```hcl
module "{module_name}" {{
  source = "./modules/{module_name}"

  name        = "my-resource"
  environment = "prod"

  tags = {{
    Project = "example"
  }}
}}
```

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
| name | Resource name prefix | `string` | n/a | yes |
| environment | Environment name | `string` | n/a | yes |
| tags | Common resource tags | `map(string)` | `{{}}` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | ID of the primary resource |

## Authors

Module maintained by your team.

## License

Apache 2 Licensed.
""",

    "examples/complete/main.tf": """\
provider "aws" {{
  region = var.region
}}

module "{module_name}" {{
  source = "../../"

  name        = "example-{module_name}"
  environment = "dev"

  tags = {{
    Environment = "dev"
    Project     = "example"
    ManagedBy   = "Terraform"
  }}
}}
""",

    "examples/complete/variables.tf": """\
variable "region" {{
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}}
""",

    "examples/complete/outputs.tf": """\
# output "id" {{
#   description = "ID of the created resource"
#   value       = module.{module_name}.id
# }}
""",
}


def validate_module_name(name: str) -> bool:
    return bool(re.match(r"^[a-z0-9][a-z0-9_-]*$", name))


def module_title(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def create_module_structure(module_name: str, base_path: Path) -> dict:
    module_path = base_path / module_name
    created_files = []
    errors = []

    if module_path.exists():
        return {
            "success": False,
            "error": f"Directory already exists: {module_path}",
            "files": [],
        }

    title = module_title(module_name)
    context = {"module_name": module_name, "module_title": title}

    for relative_path, template in TEMPLATES.items():
        file_path = module_path / relative_path
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(template.format(**context))
            created_files.append(str(file_path))
        except Exception as e:
            errors.append(f"{relative_path}: {e}")

    return {
        "success": len(errors) == 0,
        "module_path": str(module_path),
        "files": created_files,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new Terraform module with standardized structure"
    )
    parser.add_argument("module_name", help="Module name (lowercase, hyphens/underscores allowed)")
    parser.add_argument("--path", default=".", help="Base directory to create the module in")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    if not validate_module_name(args.module_name):
        msg = f"Invalid module name '{args.module_name}'. Use lowercase letters, numbers, hyphens, and underscores only."
        if args.json:
            print(json.dumps({"success": False, "error": msg}))
        else:
            print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)

    base_path = Path(args.path).resolve()
    if not base_path.exists():
        msg = f"Base path does not exist: {base_path}"
        if args.json:
            print(json.dumps({"success": False, "error": msg}))
        else:
            print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)

    result = create_module_structure(args.module_name, base_path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(f"Module '{args.module_name}' created at: {result['module_path']}")
            print(f"\nCreated {len(result['files'])} files:")
            for f in result["files"]:
                print(f"  {f}")
            print("\nNext steps:")
            print(f"  python3 .claude/skills/iac-terraform/scripts/validate_module.py {result['module_path']}")
            print(f"  cd {result['module_path']}/examples/complete && terraform init && terraform plan")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}", file=sys.stderr)
            for e in result.get("errors", []):
                print(f"  {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
