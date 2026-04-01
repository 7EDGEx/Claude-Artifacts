#!/usr/bin/env python3
"""
Terraform State Inspector & Drift Detector
Provides comprehensive analysis of Terraform state health.

WARNING: --check-drift runs `terraform plan` which contacts your cloud provider,
requires valid credentials, and may take several minutes on large state files.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: list, cwd: str) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 5 minutes"
    except FileNotFoundError:
        return 1, "", f"Command not found: {cmd[0]}"


def check_initialized(tf_dir: str) -> dict:
    if not (Path(tf_dir) / ".terraform").exists():
        return {"initialized": False, "message": "Not initialized — run `terraform init`"}
    return {"initialized": True, "message": "Initialized"}


def get_resource_list(tf_dir: str) -> dict:
    code, stdout, stderr = run_command(["terraform", "state", "list"], tf_dir)
    if code != 0:
        return {"success": False, "error": stderr.strip(), "resources": []}
    resources = [r for r in stdout.strip().splitlines() if r]
    return {"success": True, "resources": resources, "count": len(resources)}


def categorize_resources(resources: list) -> dict:
    type_counts: dict[str, int] = {}
    tainted = []
    for r in resources:
        if r.startswith("tainted."):
            tainted.append(r)
        parts = r.split(".")
        resource_type = parts[2] if parts[0] == "module" and len(parts) >= 3 else parts[0]
        type_counts[resource_type] = type_counts.get(resource_type, 0) + 1
    return {"by_type": type_counts, "tainted": tainted}


def get_versions(tf_dir: str) -> dict:
    code, stdout, _ = run_command(["terraform", "version", "-json"], tf_dir)
    if code == 0:
        try:
            data = json.loads(stdout)
            return {
                "terraform": data.get("terraform_version", "unknown"),
                "providers": data.get("provider_selections", {}),
            }
        except json.JSONDecodeError:
            pass
    code2, stdout2, _ = run_command(["terraform", "version"], tf_dir)
    first_line = stdout2.strip().splitlines()[0] if stdout2.strip() else "unknown"
    return {"terraform": first_line, "providers": {}}


def get_backend(tf_dir: str) -> dict:
    tf_state = Path(tf_dir) / ".terraform" / "terraform.tfstate"
    if not tf_state.exists():
        return {"type": "local", "note": "No backend state file found"}
    try:
        data = json.loads(tf_state.read_text())
        backend = data.get("backend", {})
        btype = backend.get("type", "local")
        config = backend.get("config") or {}
        safe_config = {
            k: ("***" if any(s in k.lower() for s in ["key", "secret", "password", "token"]) else v)
            for k, v in config.items()
        }
        return {"type": btype, "config": safe_config}
    except (json.JSONDecodeError, OSError):
        return {"type": "unknown", "error": "Could not parse backend config"}


def check_drift(tf_dir: str) -> dict:
    print("  Running terraform plan (contacting cloud provider)...")
    code, stdout, stderr = run_command(
        ["terraform", "plan", "-detailed-exitcode", "-no-color"], tf_dir
    )
    if code == 0:
        return {"drift": False, "message": "No drift — infrastructure matches configuration"}
    if code == 2:
        add = stdout.count("will be created")
        change = stdout.count("will be updated in-place") + stdout.count("will be modified")
        destroy = stdout.count("will be destroyed")
        return {
            "drift": True,
            "changes": {"add": add, "change": change, "destroy": destroy},
            "message": f"Drift detected: +{add} ~{change} -{destroy}",
        }
    return {"drift": None, "error": (stderr or stdout).strip(), "message": "Plan failed"}


def section(title: str):
    print(f"\n{'─' * 55}")
    print(f"  {title}")
    print(f"{'─' * 55}")


def main():
    parser = argparse.ArgumentParser(
        description="Inspect Terraform state health",
        epilog="WARNING: --check-drift runs terraform plan against your cloud provider.",
    )
    parser.add_argument("terraform_dir", help="Path to Terraform directory")
    parser.add_argument(
        "--check-drift",
        action="store_true",
        help="Run terraform plan to detect drift (slow, requires cloud credentials)",
    )
    args = parser.parse_args()

    tf_dir = os.path.abspath(args.terraform_dir)
    if not os.path.isdir(tf_dir):
        print(f"Error: {tf_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    print("=" * 55)
    print("  TERRAFORM STATE INSPECTOR")
    print(f"  {tf_dir}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    # Initialization
    section("Initialization")
    init = check_initialized(tf_dir)
    print(f"  {'OK  ' if init['initialized'] else 'FAIL'} {init['message']}")
    if not init["initialized"]:
        sys.exit(1)

    # Versions
    section("Versions")
    versions = get_versions(tf_dir)
    print(f"  Terraform : {versions['terraform']}")
    if versions["providers"]:
        for provider, version in versions["providers"].items():
            print(f"  {provider.split('/')[-1]:10}: {version}")
    else:
        print("  Providers : (run terraform init to lock)")

    # Backend
    section("Backend")
    backend = get_backend(tf_dir)
    print(f"  Type: {backend['type']}")
    if backend["type"] == "local":
        print("  WARNING: Local backend — not suitable for teams")
        print("  Recommend: S3 + DynamoDB remote backend")
    for k, v in backend.get("config", {}).items():
        print(f"    {k}: {v}")

    # Resources
    section("Resources")
    resource_info = get_resource_list(tf_dir)
    if not resource_info["success"]:
        print(f"  ERROR: {resource_info['error']}")
    else:
        print(f"  Total: {resource_info['count']}")
        if resource_info["count"] > 0:
            cats = categorize_resources(resource_info["resources"])
            if cats["tainted"]:
                print(f"\n  TAINTED ({len(cats['tainted'])}):")
                for t in cats["tainted"]:
                    print(f"    {t}")
            print("\n  By type:")
            for rtype, cnt in sorted(cats["by_type"].items(), key=lambda x: -x[1]):
                print(f"    {rtype}: {cnt}")

    # Drift
    section("Drift Detection")
    if args.check_drift:
        print("  WARNING: Contacting cloud provider — may take several minutes...")
        drift = check_drift(tf_dir)
        if drift.get("drift") is False:
            print(f"  OK   {drift['message']}")
        elif drift.get("drift") is True:
            c = drift.get("changes", {})
            print(f"  DRIFT: +{c.get('add',0)} ~{c.get('change',0)} -{c.get('destroy',0)}")
            print("  Run `terraform plan` for full details")
        else:
            print(f"  ERROR: {drift.get('error', drift.get('message'))}")
    else:
        print("  Skipped (use --check-drift to enable)")
        print("  Note: requires cloud credentials and may be slow")

    # Summary
    issues = []
    if backend["type"] == "local":
        issues.append("Migrate to remote state backend")
    if resource_info.get("success") and resource_info["count"] == 0:
        issues.append("No resources in state")
    if resource_info.get("success"):
        tainted = categorize_resources(resource_info.get("resources", [])).get("tainted", [])
        if tainted:
            issues.append(f"{len(tainted)} tainted resource(s) need attention")

    print("\n" + "=" * 55)
    if issues:
        print("  RECOMMENDATIONS:")
        for i in issues:
            print(f"    - {i}")
    else:
        print("  State looks healthy.")
    print("=" * 55)


if __name__ == "__main__":
    main()
