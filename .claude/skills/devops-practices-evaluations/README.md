# Azure DevOps GitOps & Trunk-Based Development Evaluator Skill

A comprehensive Claude skill for auditing and evaluating Azure DevOps repositories and CI/CD pipelines against GitOps best practices, trunk-based development standards, and security/quality benchmarks.

## Features

✅ **Repository Assessment**
- Git workflow compliance (trunk-based development)
- Pull request standards and conventions
- Reviewer compliance tracking
- Code quality gating

✅ **Pipeline Evaluation**
- CI/CD stage validation
- Security scanning (SAST/DAST) results analysis
- Test coverage assessment (unit, E2E, API)
- Stage ordering compliance

✅ **Artifacts & Metrics**
- Web scraping of performance reports
- Code coverage extraction
- Deployment metrics (DORA)
- Security findings aggregation

✅ **Comprehensive Reporting**
- JSON compliance reports
- HTML compliance dashboards
- Markdown reports with recommendations
- CSV export for tracking

## Quick Start

### Prerequisites
- Azure DevOps organization access (public or with PAT token)
- Documentation domain with publicly accessible reports (optional)
- Python 3.8+ (for local script execution)

### Installation

1. **Extract the skill to your skills directory**:
```bash
cp -r azure-devops-evaluator /path/to/claude/skills/
```

2. **Install Python dependencies** (if using scripts):
```bash
pip install requests beautifulsoup4 lxml
```

### Basic Usage

Ask Claude with the skill enabled:

```
Evaluate our Azure DevOps project "WebApp" for GitOps compliance.
Check trunk-based development, PR standards, and pipeline security.
Our docs are at docs.acme.com/reports/
```

## Usage Examples

### Example 1: Full Audit
```
Complete audit of our DevOps practices for project "CoreAPI" in Azure DevOps.

Evaluate:
- Trunk-based development compliance (main branch activity, feature branch age)
- PR standards (titles, approvers, review time)
- Pipeline stages (build, lint, secret check, SAST, DAST, tests, deploy)
- Code coverage from docs.acme.com/reports/coverage/
- Performance metrics from docs.acme.com/reports/performance/
- Security findings from docs.acme.com/reports/security/

Generate a comprehensive compliance report with recommendations.
```

### Example 2: PR Standards Check
```
Audit our PR review process for the "api-service" repository:
- Check last 20 merged PRs
- Verify conventional commit titles (feat/fix/docs/refactor)
- Validate 2+ required approvers
- Check review time SLA (< 24 hours)
- Score reviewer compliance

Recommend process improvements.
```

### Example 3: Pipeline Security Validation
```
Evaluate our backend API pipeline for security compliance.

Pipeline stages: Build → Lint → Secret Scan → SAST → API Tests → Deploy

Check:
- Are security stages (SAST, secret scan) before deploy? ✓
- Latest SAST results: 0 critical, 3 high, 12 medium findings
- Latest DAST results: 5 high, 15 medium findings
- Are findings blocking deployment?
- Is deployment success rate > 99%?

Provide compliance score and fix recommendations.
```

### Example 4: Metrics Extraction
```
Extract and analyze metrics from our documentation:

From docs.acme.com/reports/:
- /code-coverage/index.html → Extract overall % and module breakdown
- /performance/metrics.json → LCP, CLS, TTFB, FCP
- /security/sast-results.json → SAST findings by severity
- /deployment/metrics.json → Deploy frequency, lead time

Score against web app best practices:
- Code coverage: 70%+ ✓
- LCP: < 2.5s ✓
- Deployment frequency: 1+ per day
```

### Example 5: Trend Analysis
```
Evaluate our 30-day DevOps trend:
- Is code coverage improving?
- Are deployments becoming more frequent?
- Are security findings decreasing?
- Is review time getting faster?

Generate trend analysis with recommendations.
```

## Skill Structure

```
azure-devops-evaluator/
├── SKILL.md                    # Skill definition & documentation
├── README.md                   # This file
├── test-cases.json             # Example test prompts
├── config-template.json        # Configuration template
├── scripts/
│   └── evaluator.py            # Core evaluation logic (Python)
└── references/
    └── metrics-guide.md        # Detailed metrics & API reference
```

## Configuration

Create a `config.json` based on `config-template.json`:

```json
{
  "evaluator_config": {
    "organization": "your-org",
    "project": "your-project",
    "repository": "your-repo",
    "app_type": "web",
    "documentation_domain": "docs.yourcompany.com"
  },
  "thresholds": {
    "code_coverage": {
      "web_app": 70,
      "backend_api": 80
    },
    "security": {
      "sast": {
        "critical_threshold": 0,
        "high_threshold": 5
      }
    }
  }
}
```

## Evaluation Dimensions

### 1. Repository Standards (Weight: 33%)

**Branch Strategy** (25 points)
- ✅ Healthy: Daily commits to main, feature branches < 48h
- ⚠️ Warning: Some stale branches, commits < 2x/week  
- ❌ Failure: Stale branches > 2w, no main activity

**PR Standards** (35 points)
- ✅ Healthy: 2+ approvals, < 24h review, conventional commits
- ⚠️ Warning: Single approver, slow reviews
- ❌ Failure: No approval requirement, inconsistent formats

**Code Quality Gating** (40 points)
- ✅ Healthy: Coverage > 80%, quality gates enforced
- ⚠️ Warning: Coverage 70-80%, gates partially enforced
- ❌ Failure: Coverage < 70%, no gates

### 2. Pipeline Architecture (Weight: 33%)

**Required Stages** (30 points)
- Build, Lint, Secret Check, SAST required
- DAST, E2E Tests, Deploy required
- Stage order: Security before deploy

**Security Scanning** (40 points)
- SAST: Critical findings = 0, High < 5
- DAST: High findings < 10
- Findings blocking deployment

**Testing Coverage** (30 points)
- Unit tests: > 70% (web), > 80% (backend)
- E2E/API tests: > 95% pass rate
- Coverage not declining

### 3. Artifacts & Quality Metrics (Weight: 34%)

**Performance** (40 points)
- LCP < 2.5s, CLS < 0.1, TTFB < 600ms
- Lighthouse scores > 80

**Deployment Metrics** (60 points)
- Frequency: 1+ deployments/day
- Lead time: < 24 hours
- Success rate: > 99%
- MTTR: < 1 hour

## Output Format

### JSON Report
```json
{
  "evaluation_date": "2024-03-26",
  "overall_compliance_score": 82.5,
  "dimensions": {
    "repository": {"score": 85, "findings": [...]},
    "pipeline": {"score": 78, "findings": [...]},
    "artifacts": {"score": 83, "findings": [...]}
  },
  "recommendations": [...]
}
```

### HTML Dashboard
- Visual compliance gauges per dimension
- 30-day trend charts
- Risk heat maps
- Interactive findings explorer

### Markdown Report
```markdown
# DevOps Evaluation Report

## Executive Summary
Overall Compliance Score: 82.5%

## Repository Assessment
Score: 85%

### Findings
- ⚠️ WARNING: 3 feature branches > 1 week old
- ✅ PASS: All PRs use conventional commits

## Recommendations
1. Delete stale feature branches
2. ...
```

## Common Findings & Fixes

| Finding | Severity | Fix |
|---------|----------|-----|
| No CODEOWNERS | HIGH | Create `.github/CODEOWNERS` file |
| Feature branch > 2w | HIGH | Rebase & merge, enforce deadline |
| SAST not blocking | CRITICAL | Add gate: critical = fail |
| Coverage declining | HIGH | Add merge gate with threshold |
| Manual deploy steps | HIGH | Move steps to pipeline YAML |
| Security after deploy | CRITICAL | Reorder stages |

See `references/metrics-guide.md` for detailed fixes.

## API & Data Sources

### Azure DevOps REST API
- Requires: Organization, Project, Repository IDs
- Authentication: Personal Access Token (PAT)
- Endpoints: v7.0

**Key Endpoints**:
- `GET /git/repositories/{id}/pullrequests` - PR data
- `GET /git/repositories/{id}/refs` - Branch data
- `GET /pipelines/{id}/runs` - Pipeline executions
- `GET /build/builds/{id}/timeline` - Stage details

### Documentation Web Scraping
- Parses HTML reports for metrics
- Supports JSON API endpoints
- Handles markdown-embedded data
- Fallback to Azure DevOps artifacts

**Expected Structure**:
```
docs.{domain}/reports/
├── code-coverage/
├── performance/
├── security/
├── e2e-tests/
└── deployment/
```

## Troubleshooting

### Web Scraping Returns Empty
```
→ Check docs site is publicly accessible
→ Verify domain matches configuration
→ Use Azure DevOps artifact API as fallback
→ Request JSON endpoint instead of HTML
```

### Azure DevOps API 401 Unauthorized
```
→ Verify PAT token is valid & not expired
→ Check PAT scope: "Code (full)", "Build (read)"
→ Ensure org name is correct
→ Try: echo -n ":{PAT}" | base64
```

### Pipeline Stages Not Found
```
→ Verify stage names in YAML (case-sensitive)
→ Check conditional expressions (if statements)
→ Use "Get Pipeline" API to debug
→ Ensure YAML file is committed to repo
```

## Advanced Usage

### Custom Thresholds
```
Evaluate with custom thresholds:
- Code coverage minimum: 75% (instead of 70%)
- Required approvers: 3 (instead of 2)
- Max SAST high findings: 10 (instead of 5)
- Performance LCP target: 2.0s (instead of 2.5s)
```

### Multi-Repository Scan
```
Audit all repos in project "Platform" 
against trunk-based dev checklist.
Generate comparative report.
```

### Historical Tracking
```
Retrieve 30-day compliance trend:
- Code coverage: 70% → 78%
- Deployment frequency: 0.5 → 2.1 per day
- Lead time: 36h → 18h
- MTTR: 2h → 45m
```

## Integration with Tools

### GitHub/GitLab Integration
```
# If migrating from Azure DevOps:
- CODEOWNERS → .github/CODEOWNERS
- Branch rules → GitHub branch protection
- PR templates → .github/pull_request_template.md
```

### Slack Notifications
```
Automated daily compliance reports:
- Overall score
- New critical findings
- Trend analysis
```

### CI/CD Integration
```
# Run in pipeline:
python scripts/evaluator.py --config config.json --output report.json

# Then publish report:
- Upload to artifact repository
- Post to dashboard
- Send notifications
```

## Performance & Scaling

- **Single Repository**: ~30 seconds
- **Multi-Repository (10)**: ~5 minutes
- **Web Scraping**: ~10-15 seconds per domain
- **API Caching**: Reduces repeat calls by 90%

## References

- [GitOps Best Practices](https://opengitops.dev/)
- [Trunk-Based Development](https://trunkbaseddevelopment.com/)
- [DORA Metrics](https://dora.dev/)
- [OWASP CI/CD Security](https://owasp.org/www-project-cicd-security/)
- [Azure DevOps REST API](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- [Web Vitals](https://web.dev/vitals/)

## Support & Contributing

For issues or suggestions:
1. Check `references/metrics-guide.md` for troubleshooting
2. Verify configuration in `config-template.json`
3. Test with example prompts in `test-cases.json`

## License

Internal use - adjust as needed for your organization.

---

**Version**: 1.0  
**Last Updated**: 2024-03-26  
**Maintained By**: DevOps Team
