#!/usr/bin/env python3
"""
Terraform Module Validator
Validates Terraform modules against best practices.
"""
import os
import re
import sys
from pathlib import Path
from typing import Any


def extract_blocks(content: str, block_type: str) -> list[tuple[str, str]]:
    """
    Extract top-level HCL blocks of the given type, correctly handling nested braces.
    Returns a list of (name, body) tuples.
    """
    results = []
    pattern = re.compile(
        rf'{block_type}\s+"([^"]+)"\s*\{{', re.MULTILINE
    )
    for match in pattern.finditer(content):
        name = match.group(1)
        start = match.end()  # position right after the opening '{'
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            if content[i] == "{":
                depth += 1
            elif content[i] == "}":
                depth -= 1
            i += 1
        body = content[start : i - 1]
        results.append((name, body))
    return results


class ModuleValidator:
    def __init__(self, module_path: str):
        self.module_path = Path(module_path)
        self.issues: list[str] = []
        self.warnings: list[str] = []
        self.suggestions: list[str] = []

    def validate(self) -> dict[str, Any]:
        print(f"Validating module: {self.module_path}\n")

        self.check_required_files()
        self.check_variables_file()
        self.check_outputs_file()
        self.check_readme()
        self.check_versions_file()
        self.check_examples()
        self.check_naming_conventions()

        return {
            "valid": len(self.issues) == 0,
            "issues": self.issues,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
        }

    def check_required_files(self):
        for f in ["main.tf", "variables.tf", "outputs.tf"]:
            if not (self.module_path / f).exists():
                self.issues.append(f"Missing required file: {f}")

    def check_variables_file(self):
        vars_file = self.module_path / "variables.tf"
        if not vars_file.exists():
            return

        content = vars_file.read_text()
        blocks = extract_blocks(content, "variable")

        for var_name, body in blocks:
            if "description" not in body:
                self.warnings.append(f"Variable '{var_name}' missing description")
            if "type" not in body:
                self.warnings.append(f"Variable '{var_name}' missing type constraint")
            if any(kw in var_name.lower() for kw in ["password", "secret", "key", "token"]):
                if "sensitive" not in body or "sensitive = true" not in body:
                    self.warnings.append(
                        f"Variable '{var_name}' appears sensitive but not marked as sensitive = true"
                    )

    def check_outputs_file(self):
        outputs_file = self.module_path / "outputs.tf"
        if not outputs_file.exists():
            return

        content = outputs_file.read_text()
        blocks = extract_blocks(content, "output")

        if not blocks:
            self.suggestions.append("Consider adding outputs to expose useful resource attributes")
            return

        for output_name, body in blocks:
            if "description" not in body:
                self.warnings.append(f"Output '{output_name}' missing description")
            if any(kw in output_name.lower() for kw in ["password", "secret", "key", "token"]):
                if "sensitive" not in body or "sensitive = true" not in body:
                    self.warnings.append(
                        f"Output '{output_name}' appears sensitive but not marked as sensitive = true"
                    )

    def check_readme(self):
        readme_candidates = ["README.md", "readme.md", "README.txt"]
        readme_path = next(
            (self.module_path / f for f in readme_candidates if (self.module_path / f).exists()),
            None,
        )

        if not readme_path:
            self.issues.append("Missing README.md — modules must be documented")
            return

        content = readme_path.read_text().lower()
        for section in ["usage", "inputs", "outputs"]:
            if section not in content:
                self.suggestions.append(f"README missing '{section.title()}' section")
        if "example" not in content:
            self.suggestions.append("README should include usage examples")

    def check_versions_file(self):
        versions_file = self.module_path / "versions.tf"
        if versions_file.exists():
            content = versions_file.read_text()
            if "required_version" not in content:
                self.warnings.append("versions.tf should specify required_version")
            if "required_providers" not in content:
                self.warnings.append("versions.tf should specify required_providers with versions")
        else:
            main_file = self.module_path / "main.tf"
            if main_file.exists() and "required_version" in main_file.read_text():
                pass  # version constraint found in main.tf
            else:
                self.warnings.append(
                    "Missing versions.tf — specify Terraform and provider version constraints"
                )

    def check_examples(self):
        examples_dir = self.module_path / "examples"
        if not examples_dir.exists():
            self.suggestions.append("Consider adding an examples/ directory with usage examples")
        elif not any(examples_dir.iterdir()):
            self.suggestions.append("examples/ directory is empty — add example configurations")

    def check_naming_conventions(self):
        for tf_file in self.module_path.glob("*.tf"):
            if not re.match(r"^[a-z0-9_]+\.tf$", tf_file.name):
                self.warnings.append(f"File '{tf_file.name}' should use snake_case naming")

            content = tf_file.read_text()

            # Resource names should be snake_case
            for resource_name in re.findall(r'resource\s+"[^"]+"\s+"([^"]+)"', content):
                if not re.match(r"^[a-z0-9_]+$", resource_name):
                    self.warnings.append(
                        f"Resource name '{resource_name}' should use snake_case"
                    )

            # Hardcoded region
            if re.search(r'=\s*"[a-z]+-[a-z]+-[0-9]"', content):
                self.suggestions.append(
                    f"Possible hardcoded region in {tf_file.name} — consider a variable"
                )


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_module.py <module-directory>")
        sys.exit(1)

    module_path = sys.argv[1]
    if not os.path.isdir(module_path):
        print(f"Error: {module_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("  TERRAFORM MODULE VALIDATOR")
    print("=" * 60)
    print()

    validator = ModuleValidator(module_path)
    result = validator.validate()

    if result["issues"]:
        print("ISSUES (Must Fix):")
        for issue in result["issues"]:
            print(f"  [X] {issue}")
        print()

    if result["warnings"]:
        print("WARNINGS (Should Fix):")
        for warning in result["warnings"]:
            print(f"  [!] {warning}")
        print()

    if result["suggestions"]:
        print("SUGGESTIONS (Consider):")
        for suggestion in result["suggestions"]:
            print(f"  [?] {suggestion}")
        print()

    print("=" * 60)
    if result["valid"]:
        print("  PASSED")
        if not result["warnings"] and not result["suggestions"]:
            print("  No issues, warnings, or suggestions.")
    else:
        print(f"  FAILED — {len(result['issues'])} issue(s) must be fixed")
    print("=" * 60)

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
