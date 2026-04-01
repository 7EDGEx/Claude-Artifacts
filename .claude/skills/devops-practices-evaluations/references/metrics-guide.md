# Azure DevOps Evaluator - Reference Guide

## Quick Reference: Metric Thresholds

### Code Coverage
| Metric | Web App | Backend API | Critical Path |
|--------|---------|-------------|----------------|
| Minimum | 70% | 80% | 100% |
| Target | 80% | 85%+ | 100% |
| Good | 75%+ | 82%+ | 95%+ |

### Security Findings
| Severity | Threshold | Action |
|----------|-----------|--------|
| Critical | 0 | Block deployment immediately |
| High | < 5 | Create tickets, plan fix in current sprint |
| Medium | < 15 | Track, plan fix in roadmap |
| Low | < 50 | Monitor, document decisions |

### Performance Metrics (Web Apps)
| Metric | Threshold | Good Target |
|--------|-----------|-------------|
| LCP (Largest Contentful Paint) | < 2.5s | < 1.2s |
| FCP (First Contentful Paint) | < 1.8s | < 0.9s |
| CLS (Cumulative Layout Shift) | < 0.1 | < 0.05 |
| TTFB (Time to First Byte) | < 600ms | < 300ms |
| FID (First Input Delay) | < 100ms | < 50ms |

### Deployment Metrics (DORA)
| Metric | Target | Elite |
|--------|--------|-------|
| Deployment Frequency | Daily | Multiple/day |
| Lead Time | < 24h | < 1h |
| Change Failure Rate | < 15% | < 15% |
| MTTR | < 1h | < 15m |

## Azure DevOps API Endpoints

### Get Repository Details
```
GET https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}?api-version=7.0
Headers: Authorization: Basic {PAT_base64}
```

### Get Pull Requests
```
GET https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/pullrequests?api-version=7.0&searchCriteria.status=completed
```

### Get Branches
```
GET https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}/refs?api-version=7.0
```

### Get Pipeline Runs
```
GET https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipelineId}/runs?api-version=7.0
```

### Get Pipeline Definition
```
GET https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipelineId}?api-version=7.0
```

### Get Build Results
```
GET https://dev.azure.com/{organization}/{project}/_apis/build/builds/{buildId}/timeline?api-version=7.0
```

## Web Scraping Data Sources

### Documentation Repository Structure
```
docs.{domain}/
├── reports/
│   ├── code-coverage/
│   │   ├── index.html          → Overall % in <span class="coverage">75%</span>
│   │   ├── modules.json        → Per-module breakdown
│   │   └── trends.json         → 30-day historical data
│   ├── performance/
│   │   ├── lighthouse.html     → LCP, CLS, FCP scores
│   │   ├── metrics.json        → {lcp: 2000, cls: 0.08, ...}
│   │   └── pageload-trends.csv → Time-series data
│   ├── security/
│   │   ├── sast-results.json   → {critical: 0, high: 5, medium: 12}
│   │   ├── dast-findings.html  → OWASP ZAP output
│   │   └── sbom.json           → Software Bill of Materials
│   ├── e2e-tests/
│   │   ├── results.json        → {passed: 48, failed: 2, skipped: 1}
│   │   └── flaky-tests.csv     → Test stability tracking
│   └── deployment/
│       ├── metrics.json        → {deploys_per_day: 2.5, success_rate: 99.5}
│       └── change-log.md       → Deployment history
```

### HTML Parsing Patterns

#### Code Coverage
```html
<span class="coverage-score">75%</span>
<table class="coverage-table">
  <tr><td>src/components</td><td>82%</td></tr>
  <tr><td>src/utils</td><td>65%</td></tr>
</table>
```

#### Performance Metrics
```html
<div class="metric-card">
  <h3>Largest Contentful Paint</h3>
  <span class="value">2.1s</span>
  <span class="status">good</span>
</div>
```

#### Test Results
```html
<div class="test-summary">
  <span class="passed">248</span> passed
  <span class="failed">3</span> failed
</div>
```

## Conventional Commits Pattern

Valid patterns (case-insensitive):
```
feat: Add user authentication
fix: Resolve login timeout issue
docs: Update API documentation
style: Format code with Prettier
refactor: Extract common logic
perf: Optimize database queries
test: Add unit tests for utils
chore: Update dependencies
ci: Fix GitHub Actions workflow
build: Update webpack config
```

Regex:
```regex
^(feat|fix|docs|style|refactor|perf|test|chore|ci|build)(\(.+\))?:\s.+
```

## PR Review Checklist

### Title Requirements
- ✅ Follows conventional commits
- ✅ Describes change clearly
- ✅ Lowercase for type, Title Case for subject

### Description Requirements
- ✅ Explains "what" and "why"
- ✅ Links to issue/work item
- ✅ Describes breaking changes (if any)
- ✅ Lists testing performed
- ✅ Notes for reviewer (if applicable)

### Code Review Requirements
- ✅ 2+ approvals from code owners
- ✅ All conversations resolved
- ✅ CI/CD pipeline passing
- ✅ Code coverage not declining
- ✅ No security issues (SAST passing)

## Pipeline Stage Ordering

### Web Application Pipeline (Correct Order)
```
1. Trigger (on PR/push)
2. Checkout Code
3. Build (npm install, webpack)
4. Lint (ESLint, Prettier check)
5. Secret Scan (TruffleHog, GitGuardian)
6. SAST (SonarQube, CodeQL)
7. Unit Tests (Jest, coverage > 70%)
8. E2E Tests (Cypress, Playwright)
9. DAST (OWASP ZAP, running app)
10. Performance Tests (Lighthouse CI)
11. Deploy to Staging
12. Smoke Tests (Staging)
13. Deploy to Production
14. Smoke Tests (Production)
```

### Backend API Pipeline (Correct Order)
```
1. Trigger (on PR/push)
2. Checkout Code
3. Build (gradle, maven, go build)
4. Lint (golangci-lint, pylint)
5. Secret Scan (TruffleHog)
6. SAST (SonarQube, Checkmarx)
7. Unit Tests (JUnit, pytest - TDD)
8. Integration Tests (Docker Compose)
9. API Tests (Postman, REST Assured)
10. DAST (API security testing)
11. Build Container Image
12. Push to Registry
13. Deploy to Staging
14. Smoke Tests (Staging)
15. Deploy to Production
16. Health Checks (Production)
```

## Common Findings & Fixes

### Finding: No CODEOWNERS File
**File Location**: `CODEOWNERS` or `.github/CODEOWNERS`
```
# Core team reviews all changes
* @core-team

# Frontend team reviews UI changes
src/components/ @frontend-team
src/styles/ @frontend-team

# Backend team reviews API changes
src/api/ @backend-team
src/services/ @backend-team

# Security team reviews security-critical paths
src/auth/ @security-team
src/crypto/ @security-team
```

### Finding: Stale Feature Branches
```bash
# Find branches older than 7 days
git branch -v | grep -E '\[.+/.*\]' | awk '{
  cmd = "git log --format=%cd --date=short " $1 " | head -1"
  cmd | getline date
  close(cmd)
  
  cmd2 = "date -d " date " +%s"
  cmd2 | getline branch_time
  close(cmd2)
  
  now = systime()
  age = (now - branch_time) / 86400
  
  if (age > 7) print $1, "(" age " days)"
}'

# Delete stale branches
git branch -D branch-name
```

### Finding: Low Code Coverage
**Improvement Strategy**:
1. Identify untested modules: `coverage/coverage-summary.json`
2. Write tests for highest-risk paths first
3. Set merge gate: Coverage % >= previous
4. Target: Increase 5% per sprint

### Finding: Missing Pipeline Stages
**Quick Fix Script**:
```yaml
# Add to azure-pipelines.yml
- stage: SAST
  displayName: 'Static Analysis'
  jobs:
  - job: SonarQube
    steps:
    - task: SonarCloudPrepare@1
    - task: Maven@3
    - task: SonarCloudPublish@1

- stage: DAST
  displayName: 'Dynamic Security'
  jobs:
  - job: OWASPZAP
    steps:
    - script: |
        docker run -t owasp/zap2docker-stable zap-baseline.py \
          -t https://staging.app.com
```

## Troubleshooting

### Issue: Web Scraping Returns Empty
**Solutions**:
- Check if docs site requires authentication
- Verify domain is accessible from CI/CD agent
- Use Azure DevOps artifact download API as fallback
- Request JSON API endpoint instead of HTML parsing

### Issue: Azure DevOps API 401 Unauthorized
**Solutions**:
- Verify PAT token is valid and not expired
- Check PAT scope includes "Code (full)" or "Build (read)"
- Ensure org name is correct (use dev.azure.com)
- Base64 encode PAT: `echo -n ":${PAT}" | base64`

### Issue: Pipeline Stages Not Found
**Solutions**:
- Check pipeline YAML file path is correct
- Verify stage names match exactly (case-sensitive)
- Use `Get Pipeline` API to debug
- Check for conditionals that hide stages (if conditions)

## References

- [GitOps Principles](https://opengitops.dev/)
- [Trunk-Based Development Guide](https://trunkbaseddevelopment.com/)
- [Azure DevOps REST API Docs](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- [OWASP CI/CD Security](https://owasp.org/www-project-cicd-security/)
- [DORA Metrics](https://dora.dev/)
- [Web Vitals](https://web.dev/vitals/)
