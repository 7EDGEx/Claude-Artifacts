# Azure DevOps Evaluator - Quick Visual Guide

## Skill Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER PROMPT TO CLAUDE                       │
│   "Evaluate our DevOps for trunk-based dev and security..."     │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   SKILL.md TRIGGERED    │
                    │  (This Documentation)   │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼─────────────────────────┐
        │                        │                         │
        ▼                        ▼                         ▼
   ┌─────────────┐      ┌──────────────────┐      ┌──────────────┐
   │  REPOSITORY │      │    PIPELINE      │      │  ARTIFACTS   │
   │ ASSESSMENT  │      │  ASSESSMENT      │      │ & METRICS    │
   └─────────────┘      └──────────────────┘      └──────────────┘
        │                        │                         │
        ├─Branch Strategy        ├─Stage Validation       ├─Performance
        ├─PR Standards           ├─Security Scanning      ├─Deployment
        ├─Reviewer Compliance    ├─Test Coverage          ├─Coverage
        └─Code Quality Gating    └─Stage Ordering         └─Metrics
        
        │                        │                         │
        └────────────────────────┼─────────────────────────┘
                                 │
                    ┌────────────▼──────────────┐
                    │  SCORING ENGINE          │
                    │  (evaluator.py script)   │
                    └────────────┬──────────────┘
                                 │
        ┌────────────────────────┼─────────────────────────┐
        │                        │                         │
        ▼                        ▼                         ▼
   ┌─────────────┐      ┌──────────────────┐      ┌──────────────┐
   │    JSON     │      │      HTML        │      │   MARKDOWN   │
   │   REPORT    │      │   DASHBOARD      │      │    REPORT    │
   │  (Machine   │      │   (Visual        │      │  (Human      │
   │ Readable)   │      │   Interactive)   │      │ Readable)    │
   └─────────────┘      └──────────────────┘      └──────────────┘
```

## Evaluation Flow

```
STEP 1: REPOSITORY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Input: Azure DevOps REST API calls
  
  ├─ Get Branches
  │  └─ Check main branch activity & feature branch age
  │
  ├─ Get Pull Requests
  │  ├─ Validate title format (conventional commits)
  │  ├─ Check approver count (2+ required)
  │  └─ Measure review time SLA
  │
  └─ Get Code Quality Metrics
     └─ Extract coverage %, complexity, code smells
  
  Output: Repository score (0-100)


STEP 2: PIPELINE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Input: Pipeline definition + execution results
  
  ├─ Validate Required Stages
  │  ├─ Build, Lint, Secret Check (mandatory)
  │  ├─ SAST, DAST (security)
  │  ├─ Unit Tests, E2E Tests (quality)
  │  └─ Deploy stage
  │
  ├─ Check Stage Ordering
  │  └─ Security stages MUST run before deploy
  │
  ├─ Evaluate Security Scan Results
  │  ├─ SAST: Critical=0, High<5, Medium<15
  │  └─ DAST: High<10, Medium<25
  │
  └─ Validate Test Coverage
     ├─ Unit tests: Web>70%, Backend>80%
     └─ E2E/API tests: >95% pass rate
  
  Output: Pipeline score (0-100)


STEP 3: ARTIFACTS & METRICS ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Input: Web scraping + Azure DevOps APIs
  
  ├─ Extract Performance Metrics (Web Vitals)
  │  ├─ LCP < 2.5s, CLS < 0.1, TTFB < 600ms
  │  └─ Lighthouse score > 80
  │
  ├─ Extract Code Coverage
  │  ├─ Per-module breakdown
  │  └─ Trend analysis (30-day)
  │
  └─ Extract Deployment Metrics
     ├─ Deployment frequency (target: 1+/day)
     ├─ Success rate (target: >99%)
     ├─ Lead time (target: <24h)
     └─ MTTR (target: <1h)
  
  Output: Artifacts score (0-100)


STEP 4: AGGREGATION & REPORTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  Overall Score = (Repository × 0.33) + (Pipeline × 0.33) + (Artifacts × 0.34)
  
  Generate Reports:
  ├─ JSON: Machine readable, programmatic access
  ├─ HTML: Interactive dashboard, charts
  ├─ Markdown: Human readable, GitHub-compatible
  └─ Recommendations: Prioritized by severity & impact
```

## Scoring Breakdown

```
OVERALL COMPLIANCE SCORE
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  Repository Standards (33%)     Pipeline (33%)  Artifacts (34%)│
│  ┌──────────────────┐          ┌───────────┐  ┌─────────────┐ │
│  │ ████████░ 85%    │          │ ███████░░ │  │ ████████░░ 83%│
│  └──────────────────┘          └───────────┘  └─────────────┘ │
│                                                                │
│       × 0.33 = 28.05              × 0.33 = 25.74              │
│                                    × 0.34 = 28.22             │
│                                                                │
│                                                                │
│  Overall = 28.05 + 25.74 + 28.22 = 82.0% SCORE               │
│                                                                │
│  ├─ 90-100%: EXCELLENT (all practices strong)                 │
│  ├─ 75-89%:  GOOD (areas for improvement)                     │
│  ├─ 60-74%:  FAIR (significant gaps)                          │
│  └─ <60%:    POOR (critical issues)                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Pipeline Stage Requirements

### Web Application Pipeline
```
CORRECT ORDER (Required)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Checkout Code
   ↓
2. Build (npm install, webpack, compile)
   ↓
3. Lint (ESLint, Prettier, StyleLint)
   ↓
4. Secret Scanning (TruffleHog, GitGuardian)
   ↓
5. SAST (SonarQube, CodeQL) ←─── SECURITY GATES ───┐
   ↓                                                │
6. Unit & Component Tests (Jest, Mocha)            │
   ↓                                                │
7. E2E Tests (Cypress, Playwright)                 │
   ↓                                                │
8. DAST (OWASP ZAP) ◄─────────────────────────────┘
   ↓
9. Performance Tests (Lighthouse CI)
   ↓
10. Deploy to Staging (manual approval if findings)
    ↓
11. Smoke Tests (Staging)
    ↓
12. Deploy to Production
    ↓
13. Health Checks (Production)

⚠️  CRITICAL: Security stages MUST execute before deployment!
```

### Backend API Pipeline
```
1. Checkout Code
   ↓
2. Build (gradle/maven/go build)
   ↓
3. Lint (golangci-lint, pylint)
   ↓
4. Secret Scanning
   ↓
5. SAST (SonarQube, Checkmarx) ←─── SECURITY ───┐
   ↓                                             │
6. Unit Tests / TDD (JUnit, pytest)             │
   ↓                                             │
7. Integration Tests (Docker Compose)          │
   ↓                                             │
8. API Tests (Postman, REST Assured)           │
   ↓                                             │
9. DAST (API security testing) ◄────────────────┘
   ↓
10. Build Container Image
    ↓
11. Push to Registry
    ↓
12. Deploy to Staging
    ↓
13. Smoke Tests (Staging)
    ↓
14. Deploy to Production
    ↓
15. Health Checks (Production)
```

## Data Sources

```
EVALUATOR DATA SOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────┐
│  AZURE DEVOPS API                       │
├─────────────────────────────────────────┤
│  ✓ Repositories & Branches              │
│  ✓ Pull Requests & Reviews              │
│  ✓ Pipeline Definitions                 │
│  ✓ Build Runs & Results                 │
│  ✓ Test Results                         │
│  ✓ Artifacts & Attachments              │
└─────────────────────────────────────────┘
              │
              ▼
        (Requires: PAT Token)


┌─────────────────────────────────────────┐
│  DOCUMENTATION DOMAIN (Web Scraping)    │
├─────────────────────────────────────────┤
│  docs.yourcompany.com/reports/          │
│  ├─ code-coverage/      → Coverage %    │
│  ├─ performance/        → Web Vitals    │
│  ├─ security/           → SAST/DAST     │
│  ├─ e2e-tests/          → Test results  │
│  └─ deployment/         → Deploy metrics│
└─────────────────────────────────────────┘
              │
              ▼
        (Requires: Public access)


┌─────────────────────────────────────────┐
│  QUALITY TOOL INTEGRATIONS              │
├─────────────────────────────────────────┤
│  ✓ SonarQube (SAST)                     │
│  ✓ CodeQL (SAST)                        │
│  ✓ OWASP ZAP (DAST)                     │
│  ✓ TruffleHog (Secret Scanning)         │
│  ✓ Lighthouse (Performance)             │
│  ✓ Jest/Mocha/pytest (Test Coverage)    │
│  ✓ Cypress/Playwright (E2E Tests)       │
└─────────────────────────────────────────┘
```

## Common Findings Quick Reference

```
FINDING → SEVERITY → IMPACT → REMEDIATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. No CODEOWNERS File
   Severity: HIGH | Impact: Team accountability unclear
   Fix: Create .github/CODEOWNERS with code owner assignments
   Time: 15 min

2. Stale Feature Branches (>2 days old)
   Severity: MEDIUM | Impact: Repository clutter, slow CI
   Fix: Delete branches or rebase & merge to main
   Time: 30 min

3. Low Code Coverage (<70%)
   Severity: HIGH | Impact: Untested code reaches production
   Fix: Write unit tests targeting low-coverage modules
   Time: 8-16 hours

4. SAST Critical Findings
   Severity: CRITICAL | Impact: Security vulnerability
   Fix: Fix vulnerability immediately, re-scan
   Time: Varies

5. DAST High Findings (>10)
   Severity: HIGH | Impact: Runtime vulnerabilities
   Fix: Implement security controls (CORS, auth, etc.)
   Time: 4-8 hours

6. Slow PR Reviews (>24h)
   Severity: MEDIUM | Impact: Slower development cycle
   Fix: Set team SLA, assign to backup reviewers
   Time: Ongoing

7. Security Stages After Deploy
   Severity: CRITICAL | Impact: Vulnerabilities in production
   Fix: Reorder pipeline stages, move security before deploy
   Time: 1-2 hours

8. No API Testing
   Severity: HIGH | Impact: API contract breaks go unnoticed
   Fix: Add Postman/REST Assured tests
   Time: 4-8 hours

9. Declining Coverage Trend
   Severity: MEDIUM | Impact: Code quality regression
   Fix: Add merge gate: coverage% >= previous
   Time: 1 hour to configure

10. Deployment Success Rate <99%
    Severity: MEDIUM | Impact: Unreliable deployments
    Fix: Improve test coverage, add pre-deployment checks
    Time: 8-16 hours
```

## Success Criteria Checklist

```
✅ REPOSITORY BEST PRACTICES
┌──────────────────────────────────────────────┐
│ ☐ Main branch with daily commits             │
│ ☐ Feature branches < 2 days old              │
│ ☐ Branches deleted after merge               │
│ ☐ CODEOWNERS file configured                 │
│ ☐ 2+ approvers required on main              │
│ ☐ PR titles follow conventional commits      │
│ ☐ PR reviews completed < 24 hours            │
│ ☐ Code coverage > 70% (target: 80%+)         │
│ ☐ No declining coverage trend                │
└──────────────────────────────────────────────┘

✅ PIPELINE SECURITY & QUALITY
┌──────────────────────────────────────────────┐
│ ☐ All required stages present                │
│ ☐ Security stages before deployment          │
│ ☐ SAST blocking on critical findings         │
│ ☐ No critical security findings              │
│ ☐ SAST high severity < 5                     │
│ ☐ DAST high severity < 10                    │
│ ☐ Secret scanning enabled & blocking         │
│ ☐ Linting enforced (0 errors policy)         │
│ ☐ Unit tests > 95% pass rate                 │
│ ☐ E2E tests > 95% pass rate                  │
└──────────────────────────────────────────────┘

✅ DEPLOYMENT & PERFORMANCE
┌──────────────────────────────────────────────┐
│ ☐ 1+ deployments per day                     │
│ ☐ > 99% deployment success rate              │
│ ☐ Lead time < 24 hours                       │
│ ☐ MTTR < 1 hour                              │
│ ☐ LCP < 2.5s (web apps)                      │
│ ☐ CLS < 0.1 (web apps)                       │
│ ☐ TTFB < 600ms (web apps)                    │
│ ☐ Lighthouse score > 80 (web apps)           │
│ ☐ Test coverage not declining                │
│ ☐ Performance metrics improving              │
└──────────────────────────────────────────────┘
```

## Integration Map

```
This Skill Integrates With:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────┐
│ Azure DevOps                                                │
│  ├─ Repository Management (Git)                            │
│  ├─ Pull Request Workflows                                 │
│  ├─ Pipeline/CI-CD                                         │
│  └─ Build Artifacts                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Security Tools                                              │
│  ├─ SonarQube / CodeQL (SAST)                              │
│  ├─ OWASP ZAP (DAST)                                       │
│  ├─ TruffleHog / GitGuardian (Secrets)                     │
│  └─ Checkmarx / Veracode (Advanced SAST)                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Testing Frameworks                                          │
│  ├─ Jest / Mocha / Jasmine (JavaScript)                    │
│  ├─ JUnit / pytest (Java/Python)                           │
│  ├─ Cypress / Playwright (E2E)                             │
│  └─ Postman / REST Assured (API)                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Performance & Monitoring                                    │
│  ├─ Lighthouse (Web Vitals)                                │
│  ├─ DataDog / New Relic (APM)                              │
│  └─ CloudWatch / Application Insights (Cloud)              │
└─────────────────────────────────────────────────────────────┘
```

---

This visual guide helps understand how the skill works at a glance. Refer to SKILL.md and README.md for detailed information.
