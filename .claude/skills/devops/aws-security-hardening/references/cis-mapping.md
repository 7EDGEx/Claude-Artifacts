# CIS AWS Foundations Benchmark v2.0 — Control Mapping

Reference table for mapping findings to CIS controls. Use the Control ID
in every finding in the security report.

---

## Section 1 — IAM

| Control ID | Title | Key Check |
|------------|-------|-----------|
| CIS 1.1 | Maintain current contact details | Account metadata |
| CIS 1.2 | Ensure security contact info is registered | Account metadata |
| CIS 1.4 | Ensure no root account access key exists | IAM root user |
| CIS 1.5 | Ensure MFA is enabled for root account | IAM root MFA |
| CIS 1.6 | Ensure hardware MFA for root | IAM root hardware MFA |
| CIS 1.7 | Eliminate use of root for daily tasks | CloudTrail root usage |
| CIS 1.8 | Ensure min password length ≥ 14 | IAM password policy |
| CIS 1.9 | Ensure password reuse prevention | IAM password policy (24) |
| CIS 1.10 | Ensure MFA enabled for IAM users with console access | IAM users |
| CIS 1.11 | Do not setup access keys during initial user setup | IAM users |
| CIS 1.12 | Ensure credentials unused for 45+ days are disabled | IAM credential report |
| CIS 1.13 | Ensure only one active access key per user | IAM users |
| CIS 1.14 | Ensure access keys are rotated every 90 days | IAM credential report |
| CIS 1.15 | Ensure IAM users receive permissions only through groups | IAM structure |
| CIS 1.16 | Ensure no custom IAM policies allow full `*:*` privileges | IAM policies |
| CIS 1.17 | Ensure a support role has been created | IAM roles |
| CIS 1.18 | Ensure instance profiles are attached only to necessary instances | EC2/IAM |
| CIS 1.19 | Ensure expired SSL/TLS certificates are removed | IAM/ACM |
| CIS 1.20 | Ensure IAM Access Analyzer is enabled | IAM Access Analyzer |
| CIS 1.21 | Ensure IAM users are managed centrally via IdP | IAM federation |
| CIS 1.22 | Ensure CloudShell access is restricted | IAM policy |

---

## Section 2 — Storage (S3)

| Control ID | Title | Key Check |
|------------|-------|-----------|
| CIS 2.1.1 | Ensure S3 bucket versioning is enabled | `versioning { enabled = true }` |
| CIS 2.1.2 | Ensure S3 bucket SSE is enabled | `server_side_encryption_configuration` |
| CIS 2.1.3 | Ensure MFA delete is enabled on S3 | `versioning { mfa_delete = "Enabled" }` |
| CIS 2.1.4 | Ensure all S3 buckets employ public access block | `aws_s3_bucket_public_access_block` |
| CIS 2.1.5 | Ensure S3 bucket access logging is enabled | `logging {}` block |
| CIS 2.1.6 | Ensure S3 bucket object-level logging via CloudTrail | CloudTrail data events |

---

## Section 3 — Logging

| Control ID | Title | Key Check |
|------------|-------|-----------|
| CIS 3.1 | Ensure CloudTrail is enabled in all regions | `is_multi_region_trail = true` |
| CIS 3.2 | Ensure CloudTrail log file validation is enabled | `enable_log_file_validation = true` |
| CIS 3.3 | Ensure CloudTrail S3 bucket is not publicly accessible | S3 ACL/policy on trail bucket |
| CIS 3.4 | Ensure CloudTrail trails are integrated with CloudWatch Logs | `cloud_watch_logs_group_arn` |
| CIS 3.5 | Ensure AWS Config is enabled | `aws_config_configuration_recorder` |
| CIS 3.6 | Ensure S3 bucket access logging for CloudTrail bucket | Logging on trail bucket |
| CIS 3.7 | Ensure CloudTrail logs are encrypted at rest using KMS | `kms_key_id` on trail |
| CIS 3.8 | Ensure rotation for customer-created KMS CMKs is enabled | `enable_key_rotation = true` |
| CIS 3.9 | Ensure VPC flow logging is enabled | `aws_flow_log` resource |
| CIS 3.10 | Ensure object-level logging for write events on CloudTrail S3 bucket | Data events |
| CIS 3.11 | Ensure object-level logging for read events on CloudTrail S3 bucket | Data events |

---

## Section 4 — Monitoring (CloudWatch Alarms)

| Control ID | Title |
|------------|-------|
| CIS 4.1 | Unauthorized API calls |
| CIS 4.2 | Management Console sign-in without MFA |
| CIS 4.3 | Root account usage |
| CIS 4.4 | IAM policy changes |
| CIS 4.5 | CloudTrail configuration changes |
| CIS 4.6 | AWS Management Console authentication failures |
| CIS 4.7 | Disabling or scheduled deletion of KMS CMKs |
| CIS 4.8 | S3 bucket policy changes |
| CIS 4.9 | AWS Config configuration changes |
| CIS 4.10 | Security group changes |
| CIS 4.11 | Changes to NACLs |
| CIS 4.12 | Changes to network gateways |
| CIS 4.13 | Route table changes |
| CIS 4.14 | VPC changes |
| CIS 4.15 | AWS Organizations changes |

---

## Section 5 — Networking

| Control ID | Title | Key Check |
|------------|-------|-----------|
| CIS 5.1 | Ensure no network ACLs allow ingress from `0.0.0.0/0` to remote admin ports | NACLs port 22/3389 |
| CIS 5.2 | Ensure no security groups allow ingress from `0.0.0.0/0` to remote admin ports | SGs port 22/3389 |
| CIS 5.3 | Ensure no security groups allow ingress from `::/0` to remote admin ports | SGs IPv6 |
| CIS 5.4 | Ensure default security group restricts all traffic | Default SG |
| CIS 5.5 | Ensure routing tables for VPC peering are least-access | VPC peering routes |
| CIS 5.6 | Ensure VPC flow logging is enabled in all VPCs | `aws_flow_log` |

---

## Section 6 — (Not in CIS v2 core — Additional AWS Best Practices)

These are commonly referenced alongside CIS in AWS hardening engagements:

| Reference | Title | Key Check |
|-----------|-------|-----------|
| AWS-BP-EC2-1 | Enforce IMDSv2 on all EC2 instances | `http_tokens = "required"` |
| AWS-BP-EC2-2 | Encrypt all EBS volumes | `encrypted = true` |
| AWS-BP-KMS-1 | Use KMS CMK over SSE-S3 for sensitive data | `sse_algorithm = "aws:kms"` |
| AWS-BP-RDS-1 | Enable encryption at rest for RDS | `storage_encrypted = true` |
| AWS-BP-RDS-2 | Disable public accessibility on RDS | `publicly_accessible = false` |
| AWS-BP-ALB-1 | Enforce TLS 1.2+ on ALB listeners | `ssl_policy` |
| AWS-BP-LAMBDA-1 | Avoid wildcard resource in Lambda execution roles | IAM role |
| AWS-BP-SECRET-1 | No hardcoded credentials in IaC | Scan for keys/passwords |