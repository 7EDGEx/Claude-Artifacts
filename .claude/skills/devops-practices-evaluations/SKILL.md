---
name: azure-devops-evaluator
description: |
  Evaluate Azure DevOps repositories and CI/CD pipelines for GitOps best practices, trunk-based development compliance, and security/quality standards. Use this skill when auditing DevOps processes, assessing pipeline maturity, validating PR standards, evaluating code quality metrics, checking security scanning (SAST/DAST), and measuring compliance with trunk-based development workflows. Triggers include: "evaluate our DevOps", "audit pipeline stages", "check PR compliance", "verify GitOps practices", "assess trunk-based dev", "validate security scanning", "review code coverage", or any request to systematically evaluate Azure DevOps repositories, pipelines, and compliance metrics against industry best practices.
compatibility: |
  - Azure DevOps API access (PAT token recommended)
  - Requires web scraping capability for artifact repositories
  - Dependencies: requests, beautifulsoup4, json, csv libraries
---

# Azure DevOps GitOps & Trunk-Based Development Evaluator

## Overview

This skill systematically evaluates Azure DevOps repositories and CI/CD pipelines against GitOps best practices and trunk-based development standards. It provides comprehensive assessment across three dimensions:

1. **Repository Standards** - Git practices, PR workflows, reviewer compliance
2. **Pipeline Architecture** - CI/CD stage execution, security scanning, testing coverage
3. **Artifacts & Quality Metrics** - Code coverage, performance benchmarks, security findings

## Quick Start

Provide Claude with:
- **Azure DevOps Organization**: `{org_name}`
- **Project**: `{project_name}`
- **Repository**: `{repo_name}` (or leave for multi-repo scan)
- **Documentation Domain**: `docs.{domain}.com` (fixed pattern for artifact scraping)
- **Required Approvers Count**: Number (e.g., 2 or 3)
- **PAT Token** (optional, for API access - uses public endpoint if not provided)

Example prompt:
```
Evaluate our DevOps practices for project "CoreAPI" in Azure DevOps. 
Check trunk-based development compliance and PR reviewer compliance 
(focus: number of approvers required).

For pipeline: Verify all stages exist (Build, Lint, Secret Check, SAST, DAST, Tests, Deploy) 
AND validate results against thresholds:
- Code coverage: 70%+
- SAST findings: 0 critical, <5 high
- DAST findings: <10 high
- E2E test pass rate: >95%

Extract metrics from docs.mycompany.com/reports/

Format: JSON report with compliance scores
```

---

## Evaluation Dimensions

### 1. Repository Assessment

#### Git Workflow Compliance
- **Trunk-Based Development**
  - Primary branch naming convention (main/master)
  - Short-lived feature branches (< 48 hours old)
  - Branch deletion after merge
  - Commit frequency on main (healthy: daily commits)

#### Pull Request Standards
- **PR Creation Quality**
  - Title format compliance (conventional commits: feat/fix/docs/refactor)
  - Description completeness (linked work items, changelog, breaking changes)
  - Scope analysis (files changed, complexity assessment)
  - Test coverage indicators (test files included)

- **Reviewer Compliance** ⭐ Primary Focus
  - **Required approvers count** (configurable: default 2+)
  - % of PRs meeting approver requirement
  - Approval rate across recent PRs
  - Approval distribution (single approver vs. multiple)
  - Enforcement of requirement (branch protection rules)

#### Code Quality Gating
- **Static Analysis Integration**
  - SonarQube/CodeQL integration
  - Code coverage enforcement (threshold compliance)
  - Complexity metrics
  - Code smell tracking

---

### 2. Pipeline Assessment

#### Web Application Pipeline Stages

| Stage | Check | Compliance Indicator |
|-------|-------|---------------------|
| **Build** | Compilation success, artifact creation | Build time < 5m |
| **Lint** | Code style enforcement (ESLint, Prettier, StyleLint) | 0 errors policy |
| **Secret Checking** | Credential detection (GitGuardian, TruffleHog) | 0 secrets policy |
| **SAST** | Static Application Security Testing (CodeQL, SonarQube, Checkmarx) | Critical findings < 5 |
| **DAST** | Dynamic Application Security Testing (OWASP ZAP, Burp) | High severity < 10 |
| **Unit/Component Testing** | Jest, Mocha, Jasmine coverage | Coverage > 70% |
| **Performance Testing** | Lighthouse, WebPageTest, custom benchmarks | LCP < 2.5s, CLS < 0.1 |
| **E2E Testing** | Cypress, Playwright, Selenium test execution | Pass rate > 95% |
| **Deploy** | Staging → Production promotion | Deployment log validation |

#### Backend API Pipeline Stages

| Stage | Check | Compliance Indicator |
|-------|-------|---------------------|
| **Build** | Compilation/packaging success | Build time < 3m |
| **Lint** | Code style (golangci-lint, ESLint, pylint) | 0 errors policy |
| **Secret Checking** | Credential detection | 0 secrets policy |
| **SAST** | Security code analysis | Critical < 5 |
| **DAST** | API security testing | High findings < 10 |
| **TDD/Unit Tests** | Test-driven development validation | Coverage > 80% |
| **API Testing** | Contract tests, integration tests (Postman, REST Assured) | Pass rate > 95% |
| **Deploy** | Service deployment & health checks | Deployment success rate > 99% |

#### Pipeline Quality Gates
- **Stage Order Enforcement**: Security stages before deployment
- **Stage Execution Validation**: Each stage must execute AND produce passing results
- **Result Threshold Validation** ⭐ Primary Focus
  - Build: Compilation success + build time < 5m
  - Lint: 0 errors policy (enforced)
  - Secret Check: 0 secrets allowed (block on any found)
  - SAST: Critical=0, High<5, Medium<15 (configurable)
  - DAST: High<10, Medium<25 (configurable)
  - Unit Tests: Coverage >70% (web) / >80% (backend), >95% pass rate
  - E2E Tests: >95% pass rate (configurable)
  - Performance Tests: LCP<2.5s, CLS<0.1 (configurable)
- **Artifacts Retention**: Build logs, test results, SBOM stored > 30 days
- **Deployment Approval Workflow**: Manual approval on high severity findings
- **Concurrent Run Limits**: Prevent excessive resource consumption
- **Deployment Strategy**: Blue-green, canary, or rolling deployment validation

---

### 3. Artifacts & Quality Metrics Assessment

#### Web Scraping Artifact Sources

The skill scrapes documentation repositories for quantitative metrics:

```
docs.{domain}/reports/
├── code-coverage/       → Extract coverage % by module
├── performance/         → LCP, FCP, CLS, TTL metrics
├── security/           → SAST/DAST findings, CVE count
├── e2e-tests/          → Test execution results
└── deployment-metrics/ → Deployment frequency, lead time
```

**Extraction Strategy**:
- Parse HTML tables for metric values
- Extract JSON endpoints when available
- Support markdown-embedded data blocks
- Fallback to Azure DevOps artifact downloads

#### Quality Thresholds

**Code Coverage**
- Web Apps: > 70%
- Backend APIs: > 80%
- Critical Paths: 100%

**Security Findings**
- Critical: 0 allowed
- High: < 5
- Medium: < 15
- Low: < 50

**Performance (Web Apps)**
- Largest Contentful Paint (LCP): < 2.5s
- Cumulative Layout Shift (CLS): < 0.1
- First Input Delay (FID): < 100ms
- Time to First Byte (TTFB): < 600ms

**Deployment Metrics**
- Deployment Frequency: Daily+
- Lead Time: < 24 hours
- Change Failure Rate: < 15%
- Mean Time to Recovery: < 1 hour

---

## Output Report Structure

The evaluator generates findings in JSON format as the primary output:

### JSON Report ⭐ Primary Format
```json
{
  "evaluation_date": "2024-03-26",
  "project": "ProjectName",
  "repository": "RepoName",
  "overall_compliance_score": 82,
  "required_approvers": 2,
  "dimensions": {
    "repository": {
      "score": 85,
      "approver_compliance_rate": 95,
      "findings": [...]
    },
    "pipeline": {
      "score": 78,
      "stages_present": true,
      "results_validated": true,
      "findings": [...]
    },
    "artifacts": {
      "score": 83,
      "findings": [...]
    }
  },
  "recommendations": [...],
  "metrics": {
    "code_coverage": 75,
    "sast_findings": {"critical": 0, "high": 2},
    "dast_findings": {"high": 3},
    "e2e_pass_rate": 96.5
  }
}
```

### Optional Output Formats
- **HTML Dashboard**: Visual compliance gauges, trend analysis, risk heat map
- **Markdown Report**: Human-readable with findings and recommendations
- **CSV Export**: For tracking across multiple evaluations

---

## Usage Examples

### Example 1: Full Pipeline Audit
```
Evaluate project "WebApp" for trunk-based dev + security compliance.
Include code coverage metrics from docs.acme.com/reports/coverage/
and performance data from docs.acme.com/dashboards/perf/
```

### Example 2: PR Standard Check
```
Audit the last 20 PRs in repo "api-service" for:
- Title format compliance
- Required approvers
- Code coverage % improvement
- SAST/DAST results inclusion
```

### Example 3: Pipeline Stage Validation
```
Check if backend pipeline includes all required stages:
Build → Lint → Secret Check → SAST → TDD → API Tests → Deploy
Verify stage order and failure policies.
```

---

## Configuration & Customization

### Environment Variables
```bash
AZURE_DEVOPS_ORG=your-org
AZURE_DEVOPS_PROJECT=your-project
AZURE_DEVOPS_PAT=your-pat-token
DOCS_DOMAIN=docs.yourcompany.com
```

### Configurable Thresholds
All metrics support custom thresholds. Example:
```json
{
  "code_coverage_threshold": 75,
  "sast_critical_threshold": 3,
  "performance_lcp_threshold": 3000,
  "required_approvers": 3
}
```

---

## Detailed Evaluation Criteria

### Repository Evaluation Logic

**Branch Strategy**
- ✅ Healthy: Commits daily to main, feature branches < 48h old
- ⚠️ Warning: > 5 branches > 1 week old, commits < 2x/week
- ❌ Failure: Stale branches > 2 weeks, no activity on main

**PR Review Process**
- ✅ Healthy: 2+ approvals, < 24h review time, CODEOWNERS enforced
- ⚠️ Warning: Single approver, > 48h review time occasionally
- ❌ Failure: No approval requirement, no CODEOWNERS file

**Conventional Commits**
- ✅ Healthy: > 85% titles follow feat/fix/docs/refactor pattern
- ⚠️ Warning: 50-85% compliance
- ❌ Failure: < 50% compliance

### Pipeline Evaluation Logic

**Security Stage Placement**
- ✅ Must run before deployment
- ⚠️ Running in parallel with other stages (okay if pre-deployment)
- ❌ After deployment or optional

**Test Coverage Validation**
- ✅ Coverage increasing over time
- ⚠️ Stable coverage
- ❌ Declining coverage or below threshold

**SAST/DAST Integration**
- ✅ Blocking on critical/high, reporting on medium/low
- ⚠️ Reporting only (non-blocking)
- ❌ Not integrated

---

## Common Findings & Remediation

| Finding | Issue | Fix |
|---------|-------|-----|
| No CODEOWNERS | Undefined review responsibility | Create `.github/CODEOWNERS` or `CODEOWNERS` |
| Feature branch > 2w | Violates trunk-based dev | Rebase and merge, enforce merge deadlines |
| SAST not blocking | Security issues not caught early | Add gate: critical findings = fail |
| Code coverage declining | Quality regression | Add merge gate: coverage % >= previous |
| Manual deployment steps | Not GitOps-compliant | Move all steps into pipeline YAML |
| No secret scanning | Credential exposure risk | Integrate TruffleHog or GitGuardian |

---

## Advanced Features

### Multi-Repository Scanning
Evaluate multiple repos against a template:
```
Audit all repos in project "Platform" 
against trunk-based dev checklist
```

### Historical Trend Analysis
Track compliance scores over time:
- 30-day trend graph
- Improvement areas
- Regressions

### Team Benchmarking
Compare your project against:
- Industry standards (DORA metrics)
- Internal team baselines
- Peer projects

### Automated Remediation Suggestions
Generate:
- Terraform/IaC configs for missing pipeline stages
- GitHub Actions/Azure Pipelines YAML snippets
- Git hooks for pre-commit security checks

---

## Limitations & Edge Cases

1. **Private Documentation**: Web scraping requires public docs. For private docs, use Azure DevOps API artifacts endpoint.
2. **Custom Metrics**: Non-standard metric formats may require regex patterns or custom parsing.
3. **Legacy Pipelines**: YAML-based evaluation works best; legacy UI-only pipelines have limited assessment.
4. **Multi-Language Repos**: Language-specific linters identified automatically.

---

## References

- [GitOps Best Practices](https://opengitops.dev/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [DORA Metrics](https://dora.dev/)
- [OWASP Top 10 - CI/CD](https://owasp.org/www-project-cicd-security/)
- [Azure DevOps REST API](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
