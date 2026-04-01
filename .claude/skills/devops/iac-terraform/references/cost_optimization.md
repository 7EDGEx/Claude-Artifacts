# Terraform Cost Optimization Guide

Strategies for optimizing cloud infrastructure costs when using Terraform.

## Table of Contents

1. [Right-Sizing Resources](#right-sizing-resources)
2. [Spot and Reserved Instances](#spot-and-reserved-instances)
3. [Storage Optimization](#storage-optimization)
4. [Networking Costs](#networking-costs)
5. [Resource Lifecycle](#resource-lifecycle)
6. [Cost Tagging](#cost-tagging)
7. [Monitoring and Alerts](#monitoring-and-alerts)
8. [Multi-Cloud Considerations](#multi-cloud-considerations)

---

## Right-Sizing Resources

**Start small, scale with auto-scaling:**
```hcl
resource "aws_autoscaling_group" "app" {
  min_size         = 2
  desired_capacity = 2
  max_size         = 10
}
```

**Database right-sizing:**
```hcl
resource "aws_db_instance" "main" {
  instance_class        = var.environment == "prod" ? "db.t3.medium" : "db.t3.micro"
  allocated_storage     = 20
  max_allocated_storage = 100  # Auto-scale storage
  storage_type          = var.environment == "prod" ? "io1" : "gp3"
}
```

---

## Spot and Reserved Instances

**Mixed instance policy (80% spot, 20% on-demand):**
```hcl
resource "aws_autoscaling_group" "spot" {
  mixed_instances_policy {
    instances_distribution {
      on_demand_percentage_above_base_capacity = 20
      spot_allocation_strategy                 = "capacity-optimized"
    }
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.app.id
        version            = "$Latest"
      }
      override { instance_type = "t3.medium" }
      override { instance_type = "t3.large" }
      override { instance_type = "t3a.medium" }
    }
  }
}
```

**Reserved Instances:** Purchase through AWS Portal; tag VMs consistently for reservation planning:
```hcl
locals {
  reservation_tags = {
    ReservationCandidate = var.environment == "prod" ? "true" : "false"
    UsagePattern         = "steady-state"
  }
}
```

---

## Storage Optimization

**S3 lifecycle — automatic tiering:**
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  rule {
    id     = "log-retention"
    status = "Enabled"
    transition { days = 30;  storage_class = "STANDARD_IA" }
    transition { days = 90;  storage_class = "GLACIER_IR" }
    transition { days = 180; storage_class = "DEEP_ARCHIVE" }
    expiration { days = 365 }
  }
}
```

**EBS — use gp3 (cheaper than gp2 with same baseline):**
```hcl
resource "aws_instance" "app" {
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 20
    iops                  = 3000
    throughput            = 125
    encrypted             = true
    delete_on_termination = true
  }
}
```

**EBS snapshot lifecycle:**
```hcl
resource "aws_dlm_lifecycle_policy" "snapshots" {
  description        = "EBS snapshot lifecycle"
  execution_role_arn = aws_iam_role.dlm.arn
  state              = "ENABLED"
  policy_details {
    resource_types = ["VOLUME"]
    schedule {
      name = "Daily snapshots"
      create_rule { interval = 24; interval_unit = "HOURS"; times = ["03:00"] }
      retain_rule { count = 7 }
      copy_tags = true
    }
    target_tags = { BackupEnabled = "true" }
  }
}
```

---

## Networking Costs

**VPC endpoints to avoid NAT gateway charges:**
```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id          = aws_vpc.main.id
  service_name    = "com.amazonaws.${var.region}.s3"
  route_table_ids = [aws_route_table.private.id]
  tags = { Name = "s3-endpoint"; CostSavings = "reduces-nat-charges" }
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.region}.ecr.api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private[*].id
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true
}
```

**Co-locate resources in same AZ** to minimize cross-AZ data transfer costs.

---

## Resource Lifecycle

**Schedule non-prod shutdowns (saves ~65% on compute):**
```hcl
# Stop dev instances at 7 PM weekdays
resource "aws_cloudwatch_event_rule" "stop_instances" {
  name                = "stop-dev-instances"
  schedule_expression = "cron(0 19 ? * MON-FRI *)"
}

# Start at 8 AM weekdays
resource "aws_cloudwatch_event_rule" "start_instances" {
  name                = "start-dev-instances"
  schedule_expression = "cron(0 8 ? * MON-FRI *)"
}
```

**Tag instances for scheduler:**
```hcl
resource "aws_instance" "dev" {
  tags = {
    Schedule     = "business-hours"
    AutoShutdown = "true"
  }
}
```

**Cleanup temporary data:**
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "temp" {
  bucket = aws_s3_bucket.temp.id
  rule {
    id     = "cleanup-temp"
    status = "Enabled"
    filter { prefix = "temp/" }
    expiration { days = 7 }
    abort_incomplete_multipart_upload { days_after_initiation = 1 }
  }
}
```

---

## Cost Tagging

**Comprehensive tagging strategy:**
```hcl
locals {
  common_tags = {
    CostCenter           = var.cost_center
    Project              = var.project_name
    Environment          = var.environment
    Owner                = var.team_email
    ManagedBy            = "Terraform"
    TerraformModule      = basename(abspath(path.module))
    AutoShutdown         = var.environment != "prod" ? "enabled" : "disabled"
    ReservationCandidate = var.environment == "prod" ? "true" : "false"
  }
}

resource "aws_instance" "app" {
  tags = merge(local.common_tags, { Name = "${var.environment}-app-server" })
}
```

**Enforce tagging with AWS Config:**
```hcl
resource "aws_config_config_rule" "required_tags" {
  name = "required-tags"
  source { owner = "AWS"; source_identifier = "REQUIRED_TAGS" }
  input_parameters = jsonencode({
    tag1Key = "CostCenter"
    tag2Key = "Environment"
    tag3Key = "Owner"
  })
}
```

---

## Monitoring and Alerts

**AWS Budgets:**
```hcl
resource "aws_budgets_budget" "monthly" {
  name         = "${var.environment}-monthly-budget"
  budget_type  = "COST"
  limit_amount = var.monthly_budget
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.budget_alert_email]
  }
}
```

**Cost anomaly detection:**
```hcl
resource "aws_ce_anomaly_monitor" "service" {
  name              = "${var.environment}-monitor"
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"
}

resource "aws_ce_anomaly_subscription" "alerts" {
  name      = "${var.environment}-anomaly-alerts"
  frequency = "DAILY"
  monitor_arn_list = [aws_ce_anomaly_monitor.service.arn]
  subscriber { type = "EMAIL"; address = var.cost_alert_email }
  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
      values        = ["100"]
      match_options = ["GREATER_THAN_OR_EQUAL"]
    }
  }
}
```

---

## Multi-Cloud Considerations

**Azure — Hybrid Benefit:**
```hcl
resource "azurerm_linux_virtual_machine" "main" {
  license_type = "RHEL_BYOS"
}
```

**GCP — Preemptible VMs (up to 80% cost reduction):**
```hcl
resource "google_compute_instance_template" "preemptible" {
  machine_type = "n1-standard-1"
  scheduling {
    automatic_restart   = false
    on_host_maintenance = "TERMINATE"
    preemptible         = true
  }
}
```

---

## Cost Optimization Checklist

### Before Deployment
- [ ] Right-size compute (start small)
- [ ] Use gp3 EBS volumes instead of gp2
- [ ] Enable auto-scaling instead of over-provisioning
- [ ] Implement tagging strategy
- [ ] Configure S3 lifecycle policies
- [ ] Add VPC endpoints for AWS services

### After Deployment
- [ ] Monitor usage vs. provisioned capacity
- [ ] Review cost allocation tags
- [ ] Configure budget alerts
- [ ] Enable cost anomaly detection
- [ ] Schedule non-prod shutdown

### Ongoing
- [ ] Monthly cost review
- [ ] Quarterly right-sizing analysis
- [ ] Annual reservation review
- [ ] Remove unused resources
- [ ] Optimize data transfer patterns

---

## Cost Estimation Tools

```bash
# infracost — estimate costs before applying
infracost breakdown --path .
infracost diff --path . --compare-to tfplan.json
```

Terraform Cloud also provides automatic cost estimates on every plan.
