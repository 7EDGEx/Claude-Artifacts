# Sample Data Structures & Output Examples

## Input Data Structure

### Complete Evaluation Input
```json
{
  "project_name": "WebApp",
  "repository_name": "webapp-frontend",
  "app_type": "web",
  "organization": "acme-corp",
  "repository": {
    "branches": [
      {
        "name": "main",
        "last_commit_date": "2024-03-25T14:30:00Z",
        "last_commit_author": "dev-team",
        "commit_count_30d": 18
      },
      {
        "name": "feature/auth-redesign",
        "last_commit_date": "2024-03-24T10:15:00Z",
        "age_days": 1,
        "status": "active"
      },
      {
        "name": "feature/old-branch",
        "last_commit_date": "2024-03-10T08:00:00Z",
        "age_days": 15,
        "status": "stale"
      }
    ],
    "pull_requests": [
      {
        "id": "PR-1234",
        "title": "feat(auth): Add OAuth2 integration",
        "created_date": "2024-03-24T09:00:00Z",
        "completed_date": "2024-03-25T14:00:00Z",
        "approvers": ["alice", "bob"],
        "state": "completed",
        "files_changed": 24,
        "additions": 450,
        "deletions": 120
      },
      {
        "id": "PR-1233",
        "title": "Fix profile page styling",
        "created_date": "2024-03-23T11:00:00Z",
        "completed_date": "2024-03-25T10:00:00Z",
        "approvers": ["alice"],
        "state": "completed",
        "files_changed": 3
      }
    ],
    "quality_metrics": {
      "code_coverage": {
        "overall": 75.5,
        "statements": 76.2,
        "branches": 72.1,
        "functions": 74.8,
        "lines": 75.5,
        "by_module": {
          "src/components": 82.1,
          "src/pages": 68.5,
          "src/utils": 88.3,
          "src/styles": 0
        }
      },
      "complexity": {
        "cyclomatic": 3.2,
        "cognitive": 4.1
      }
    }
  },
  "pipeline": {
    "definition": {
      "name": "webapp-pipeline",
      "stages": [
        {"name": "Build", "display_name": "Build & Compile", "condition": "true"},
        {"name": "Lint", "display_name": "Code Style", "condition": "true"},
        {"name": "SecretScan", "display_name": "Secret Scanning", "condition": "true"},
        {"name": "SAST", "display_name": "Static Analysis", "condition": "true"},
        {"name": "UnitTests", "display_name": "Unit & Component Tests", "condition": "true"},
        {"name": "E2ETests", "display_name": "E2E Tests", "condition": "true"},
        {"name": "PerformanceTests", "display_name": "Performance Tests", "condition": "true"},
        {"name": "DeployStaging", "display_name": "Deploy to Staging", "condition": "succeeded()"},
        {"name": "SmokeTests", "display_name": "Smoke Tests", "condition": "succeeded()"}
      ]
    },
    "app_type": "web",
    "sast_results": {
      "tool": "SonarQube",
      "critical": 0,
      "high": 2,
      "medium": 8,
      "low": 15,
      "issues_by_type": {
        "code_smell": 12,
        "vulnerability": 5,
        "bug": 8
      },
      "last_scan_date": "2024-03-25T16:00:00Z"
    },
    "dast_results": {
      "tool": "OWASP ZAP",
      "high": 3,
      "medium": 8,
      "low": 12,
      "findings": [
        {"issue": "Missing CORS headers", "severity": "high"},
        {"issue": "Insecure direct object reference", "severity": "high"},
        {"issue": "Session fixation", "severity": "high"}
      ],
      "last_scan_date": "2024-03-25T18:00:00Z"
    },
    "test_metrics": {
      "unit_test_coverage": 75,
      "unit_test_pass_rate": 98.5,
      "unit_tests_total": 340,
      "unit_tests_passed": 335,
      "e2e_pass_rate": 96.5,
      "e2e_tests_total": 58,
      "e2e_tests_passed": 56,
      "performance_metrics": {
        "avg_build_time_seconds": 240,
        "avg_test_time_seconds": 180
      }
    }
  },
  "artifacts": {
    "performance": {
      "lcp": 2100,
      "fcp": 900,
      "cls": 0.085,
      "ttfb": 450,
      "fid": 65,
      "lighthouse_score": 82,
      "measurement_date": "2024-03-25T20:00:00Z",
      "by_page": {
        "home": {"lcp": 1800, "cls": 0.08},
        "product": {"lcp": 2400, "cls": 0.09},
        "checkout": {"lcp": 2200, "cls": 0.08}
      }
    },
    "deployment_metrics": {
      "deployments_per_day": 1.8,
      "deployment_success_rate": 99.2,
      "total_deployments_30d": 54,
      "successful_deployments_30d": 53,
      "failed_deployments_30d": 1,
      "lead_time_hours": 16.5,
      "lead_time_trend": [14.2, 15.8, 16.5],
      "deployment_frequency_trend": [1.5, 1.6, 1.8]
    }
  }
}
```

## Sample Evaluation Output

### Full JSON Report
```json
{
  "evaluation_date": "2024-03-26T10:30:00Z",
  "project": "WebApp",
  "repository": "webapp-frontend",
  "app_type": "web",
  "organization": "acme-corp",
  "overall_compliance_score": 82.3,
  "compliance_level": "GOOD",
  "evaluation_summary": "Good DevOps practices with some areas for improvement. Address high-priority findings to improve compliance.",
  "dimensions": {
    "repository": {
      "score": 85.0,
      "weight": 0.33,
      "weighted_score": 28.05,
      "sub_dimensions": {
        "branch_strategy": {"score": 80, "status": "WARNING"},
        "pr_standards": {"score": 85, "status": "HEALTHY"},
        "code_quality_gating": {"score": 90, "status": "HEALTHY"}
      },
      "findings": [
        {
          "id": "REPO-001",
          "severity": "WARNING",
          "category": "branch_strategy",
          "finding": "1 stale feature branch detected",
          "description": "Branch 'feature/old-branch' has not been updated for 15 days. Trunk-based development recommends branches be merged or deleted within 48 hours.",
          "evidence": {
            "branch_name": "feature/old-branch",
            "last_commit": "2024-03-10T08:00:00Z",
            "age_days": 15
          },
          "impact": "Increases merge complexity, slows development",
          "remediation": "Rebase feature/old-branch on main and merge or delete if work is complete",
          "priority": "medium"
        }
      ]
    },
    "pipeline": {
      "score": 78.0,
      "weight": 0.33,
      "weighted_score": 25.74,
      "sub_dimensions": {
        "required_stages": {"score": 85, "status": "HEALTHY"},
        "security_scanning": {"score": 75, "status": "WARNING"},
        "testing_coverage": {"score": 74, "status": "WARNING"}
      },
      "findings": [
        {
          "id": "PIPE-001",
          "severity": "HIGH",
          "category": "security_scanning",
          "finding": "2 high-severity SAST vulnerabilities detected",
          "description": "SonarQube scan found 2 high-severity issues exceeding the threshold of 0-1. These should be reviewed and prioritized for remediation.",
          "evidence": {
            "tool": "SonarQube",
            "critical": 0,
            "high": 2,
            "threshold": 1,
            "scan_date": "2024-03-25T16:00:00Z"
          },
          "issues": [
            {"title": "SQL injection vulnerability in user query", "file": "src/api/users.js", "line": 45},
            {"title": "Hardcoded API key", "file": "src/config/api.js", "line": 12}
          ],
          "impact": "Security risk if deployed to production",
          "remediation": "1. Review and fix SQL injection in users.js (parameterize queries)\n2. Move API key to environment variables\n3. Re-run SAST to verify fixes",
          "priority": "high"
        },
        {
          "id": "PIPE-002",
          "severity": "WARNING",
          "category": "testing_coverage",
          "finding": "Unit test coverage at 75% (target: 70%+ is minimum, 80%+ is recommended)",
          "description": "Current coverage is acceptable but below industry best practice for web applications. Recommend targeting 80%+.",
          "evidence": {
            "current_coverage": 75,
            "minimum_threshold": 70,
            "recommended": 80,
            "low_coverage_modules": [
              {"module": "src/pages", "coverage": 68.5},
              {"module": "src/components", "coverage": 82.1}
            ]
          },
          "impact": "Untested code paths may contain bugs that reach production",
          "remediation": "Focus test writing on src/pages module. Current tests: 335/340 passing (98.5%). Aim for 5% improvement per sprint.",
          "priority": "medium"
        },
        {
          "id": "PIPE-003",
          "severity": "WARNING",
          "category": "dast",
          "finding": "3 high-severity DAST vulnerabilities found",
          "description": "OWASP ZAP dynamic security scan found 3 high-severity issues during testing. These are runtime vulnerabilities that should be addressed.",
          "evidence": {
            "tool": "OWASP ZAP",
            "high": 3,
            "medium": 8,
            "low": 12,
            "threshold": 10
          },
          "issues": [
            "Missing CORS headers",
            "Insecure direct object reference",
            "Session fixation vulnerability"
          ],
          "remediation": "1. Add proper CORS headers to API responses\n2. Implement authorization checks for object access\n3. Use secure session tokens with HttpOnly flag",
          "priority": "high"
        }
      ]
    },
    "artifacts": {
      "score": 83.5,
      "weight": 0.34,
      "weighted_score": 28.39,
      "sub_dimensions": {
        "performance": {"score": 88, "status": "HEALTHY"},
        "deployment": {"score": 79, "status": "WARNING"}
      },
      "findings": [
        {
          "id": "PERF-001",
          "severity": "INFO",
          "category": "performance",
          "finding": "Web performance metrics are within acceptable ranges",
          "description": "Core Web Vitals are healthy for a web application.",
          "evidence": {
            "lcp": {"value": 2100, "threshold": 2500, "status": "PASS"},
            "cls": {"value": 0.085, "threshold": 0.1, "status": "PASS"},
            "ttfb": {"value": 450, "threshold": 600, "status": "PASS"},
            "lighthouse": 82
          },
          "remediation": "Continue monitoring. Optimize product and checkout pages where LCP is higher (2.2-2.4s).",
          "priority": "low"
        },
        {
          "id": "DEPLOY-001",
          "severity": "WARNING",
          "category": "deployment",
          "finding": "Deployment frequency below daily target",
          "description": "Current deployment frequency is 1.8 per day (good), but DORA metrics recommend 1+ per day as healthy minimum and multiple per day as elite.",
          "evidence": {
            "current_frequency": 1.8,
            "minimum_healthy": 1,
            "elite_target": 3,
            "trend_30d": [1.5, 1.6, 1.8]
          },
          "impact": "Slower feedback loops, longer lead time to customers",
          "remediation": "Continue current progress. Automate deployment approvals to reach 3+ deployments per day.",
          "priority": "low"
        }
      ]
    }
  },
  "risk_assessment": {
    "critical_risks": 0,
    "high_risks": 2,
    "medium_risks": 3,
    "risk_heat_map": {
      "security": "HIGH",
      "testing": "MEDIUM",
      "deployment": "LOW",
      "repo_practices": "MEDIUM"
    }
  },
  "summary": "Good DevOps practices with strong performance metrics and repository standards. Key improvements needed: resolve 2 high-severity SAST findings, address DAST vulnerabilities, and improve unit test coverage in pages module.",
  "recommendations": [
    {
      "priority": "CRITICAL",
      "finding_id": "PIPE-001",
      "category": "Security",
      "recommendation": "Fix 2 high-severity SAST vulnerabilities immediately",
      "details": "SQL injection and hardcoded API key pose production security risks. These must be resolved before next deployment.",
      "effort": "2-4 hours",
      "impact": "HIGH"
    },
    {
      "priority": "HIGH",
      "finding_id": "PIPE-003",
      "category": "Security",
      "recommendation": "Remediate DAST findings (CORS headers, authorization, session security)",
      "details": "Runtime vulnerabilities found during dynamic testing. Implement fixes in this sprint.",
      "effort": "4-8 hours",
      "impact": "HIGH"
    },
    {
      "priority": "HIGH",
      "finding_id": "PIPE-002",
      "category": "Testing",
      "recommendation": "Increase unit test coverage to 80%+ focusing on src/pages module",
      "details": "Current coverage of 68.5% in pages module is below threshold. This is high-risk area.",
      "effort": "8-16 hours",
      "impact": "MEDIUM"
    },
    {
      "priority": "MEDIUM",
      "finding_id": "REPO-001",
      "category": "Repository",
      "recommendation": "Delete or rebase stale feature branch",
      "details": "feature/old-branch is 15 days old, violating trunk-based development 48-hour guideline.",
      "effort": "0.5 hours",
      "impact": "LOW"
    }
  ],
  "trend_analysis": {
    "period_days": 30,
    "metrics_trend": {
      "code_coverage": {
        "30d_ago": 72.5,
        "14d_ago": 73.8,
        "today": 75.5,
        "trend": "IMPROVING",
        "improvement_percent": 4.1
      },
      "sast_findings": {
        "30d_ago": 15,
        "14d_ago": 18,
        "today": 10,
        "trend": "IMPROVING",
        "improvement_percent": -33.3
      },
      "deployment_frequency": {
        "30d_ago": 1.5,
        "14d_ago": 1.6,
        "today": 1.8,
        "trend": "IMPROVING"
      }
    }
  },
  "comparison": {
    "vs_team_baseline": {
      "code_coverage": "+5.5%",
      "deployment_frequency": "+0.3/day",
      "lead_time": "-2 hours"
    },
    "vs_industry_best_practices": {
      "code_coverage": "GOOD (target 80%)",
      "deployment_frequency": "GOOD (target 1+/day)",
      "lead_time": "EXCELLENT (target <24h)"
    }
  },
  "next_steps": [
    "Schedule security review for SAST and DAST findings",
    "Plan unit test improvements for pages module",
    "Delete stale feature branch",
    "Run SAST again after fixes",
    "Re-evaluate in 1 week"
  ],
  "evaluation_metadata": {
    "duration_seconds": 28,
    "data_sources": [
      "Azure DevOps API",
      "SonarQube scan results",
      "OWASP ZAP scan results",
      "Web scraping: docs.acme.com/reports/"
    ],
    "confidence_score": 0.94,
    "missing_data": []
  }
}
```

## Dashboard Output (Summary Stats)

```
╔════════════════════════════════════════════════════════════════════╗
║           AZURE DEVOPS COMPLIANCE EVALUATION REPORT                ║
║                                                                    ║
║ Project: WebApp                                                    ║
║ Repository: webapp-frontend                                        ║
║ Evaluation Date: 2024-03-26                                        ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  OVERALL COMPLIANCE SCORE: 82.3%   [████████░░]                   ║
║                                                                    ║
║  Repository Standards:        85.0%   [████████░░]  ✓ HEALTHY     ║
║  Pipeline Architecture:        78.0%   [███████░░░]  ⚠ WARNING    ║
║  Artifacts & Metrics:          83.5%   [████████░░]  ✓ HEALTHY    ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║ CRITICAL ISSUES: 0   HIGH: 2   MEDIUM: 3   LOW: 1                 ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║ BRANCH STRATEGY              ✓ HEALTHY                             ║
║ • Main branch: Active (last commit 12h ago)                        ║
║ • Feature branches: Healthy (<48h old)                             ║
║ • Stale branches: 1 (feature/old-branch - 15 days) ⚠              ║
║                                                                    ║
║ PR STANDARDS                 ✓ HEALTHY                             ║
║ • Conventional commits: 100%                                       ║
║ • Required approvers: 2+ enforced                                  ║
║ • Review time SLA: 18h avg (target: <24h) ✓                       ║
║                                                                    ║
║ CODE COVERAGE                ⚠ WARNING                             ║
║ • Overall: 75.5% (target: 70%+, recommended: 80%+)                ║
║ • Components: 82.1% ✓                                              ║
║ • Pages: 68.5% ⚠ (needs improvement)                              ║
║ • Utils: 88.3% ✓                                                   ║
║                                                                    ║
║ SECURITY SCANNING            ⚠ WARNING                             ║
║ • SAST: 2 HIGH findings (threshold: <5) ⚠                         ║
║   - SQL injection vulnerability                                   ║
║   - Hardcoded API key                                              ║
║ • DAST: 3 HIGH findings (threshold: <10)                           ║
║   - Missing CORS headers                                           ║
║   - Insecure object reference                                      ║
║   - Session fixation                                               ║
║                                                                    ║
║ TESTING                      ⚠ WARNING                             ║
║ • Unit tests: 335/340 passing (98.5%)                              ║
║ • E2E tests: 56/58 passing (96.5%) ✓                              ║
║ • Coverage: 75% (target: 80%)                                      ║
║                                                                    ║
║ PERFORMANCE (WEB VITALS)     ✓ HEALTHY                             ║
║ • LCP: 2.1s (target: <2.5s) ✓                                      ║
║ • CLS: 0.085 (target: <0.1) ✓                                      ║
║ • TTFB: 450ms (target: <600ms) ✓                                   ║
║ • Lighthouse: 82/100 ✓                                             ║
║                                                                    ║
║ DEPLOYMENT METRICS           ✓ HEALTHY                             ║
║ • Frequency: 1.8/day (target: 1+/day) ✓                            ║
║ • Success rate: 99.2% (target: 99%+) ✓                             ║
║ • Lead time: 16.5h (target: <24h) ✓                                ║
║ • MTTR: Excellent trend ✓                                          ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║ TOP RECOMMENDATIONS                                                ║
║                                                                    ║
║ 1. [CRITICAL] Fix 2 high-severity SAST vulnerabilities            ║
║    Effort: 2-4h | Impact: HIGH                                     ║
║    → Resolve SQL injection and hardcoded API key                  ║
║                                                                    ║
║ 2. [HIGH] Remediate DAST findings (CORS, authz, sessions)         ║
║    Effort: 4-8h | Impact: HIGH                                     ║
║    → Implement proper headers and security controls               ║
║                                                                    ║
║ 3. [HIGH] Increase unit test coverage to 80%+                     ║
║    Effort: 8-16h | Impact: MEDIUM                                  ║
║    → Focus on src/pages module (currently 68.5%)                  ║
║                                                                    ║
║ 4. [MEDIUM] Delete stale feature branch                            ║
║    Effort: 0.5h | Impact: LOW                                      ║
║    → Remove feature/old-branch (15 days old)                      ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║ 30-DAY TREND ANALYSIS                                              ║
║                                                                    ║
║ Code Coverage:     72.5% → 75.5%   [↗ +4.1%] IMPROVING            ║
║ SAST Findings:     15 → 10          [↘ -33%] IMPROVING             ║
║ Deploy Frequency:  1.5 → 1.8/day    [↗ +20%] IMPROVING            ║
║ Lead Time:         18h → 16.5h      [↘ -8%]  IMPROVING            ║
║                                                                    ║
║ Overall Trajectory: POSITIVE ✓                                     ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

## Markdown Report Format

```markdown
# DevOps Evaluation Report

**Project**: WebApp  
**Repository**: webapp-frontend  
**Date**: 2024-03-26  
**Overall Score**: 82.3%

## Executive Summary

✓ **Good DevOps Practices** - Strong compliance with GitOps and trunk-based development principles.

Key strengths:
- ✅ Excellent web performance (Lighthouse 82, LCP 2.1s)
- ✅ Healthy deployment metrics (1.8/day, 99.2% success rate)
- ✅ Strong PR standards and code review process
- ✅ Good trend trajectory (coverage +4.1% over 30 days)

Areas for improvement:
- ⚠️ Security findings require attention (2 SAST, 3 DAST high-severity)
- ⚠️ Unit test coverage below 80% target (75.5% current, 68.5% in pages module)
- ⚠️ 1 stale feature branch violates trunk-based dev

---

## Detailed Findings

### Repository Standards (Score: 85%)

#### ✓ Branch Strategy - HEALTHY
- Main branch: Active with 18 commits in 30 days
- Feature branches: Generally healthy (<48h)
- **Issue**: `feature/old-branch` is 15 days old (violates trunk-based dev)

#### ✓ PR Standards - HEALTHY
- Title format: 100% conventional commits compliance
- Approvers: 2+ enforced, all recent PRs have 2 approvals
- Review SLA: Average 18 hours (target: <24h) ✓

#### ⚠️ Code Quality Gating - WARNING
- Overall coverage: 75.5% (target: 70%+, recommended: 80%+)
- Module breakdown:
  - `src/components`: 82.1% ✓
  - `src/utils`: 88.3% ✓
  - `src/pages`: 68.5% ⚠️

---

### Pipeline Architecture (Score: 78%)

#### ✓ Pipeline Stages - HEALTHY
All required stages present and in correct order:
- Build → Lint → Secret Scan → SAST → UnitTests → E2E → Deploy ✓

#### ⚠️ Security Scanning - WARNING

**SAST Results** (SonarQube):
- Critical: 0 (threshold: 0) ✓
- High: 2 (threshold: <5) ⚠️
  - SQL injection in `src/api/users.js:45`
  - Hardcoded API key in `src/config/api.js:12`
- Medium: 8
- Low: 15

**DAST Results** (OWASP ZAP):
- High: 3 (threshold: <10)
  - Missing CORS headers
  - Insecure direct object reference
  - Session fixation vulnerability
- Medium: 8
- Low: 12

**Recommendation**: Schedule security review and remediation in current sprint.

#### ⚠️ Testing - WARNING
- Unit tests: 335/340 passing (98.5%)
- E2E tests: 56/58 passing (96.5%) ✓
- Coverage: 75% (target: 80%) ⚠️

**Action**: Increase test coverage by 5% targeting `src/pages` module.

---

### Artifacts & Quality Metrics (Score: 83.5%)

#### ✓ Performance - HEALTHY

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| LCP | 2.1s | <2.5s | ✓ |
| CLS | 0.085 | <0.1 | ✓ |
| TTFB | 450ms | <600ms | ✓ |
| Lighthouse | 82/100 | >80 | ✓ |

#### ✓ Deployment - HEALTHY
- Frequency: 1.8/day (target: 1+/day) ✓
- Success rate: 99.2% (target: 99%+) ✓
- Lead time: 16.5h (target: <24h) ✓
- 30-day improvement: +20% faster deployments

---

## Recommendations (Priority Order)

### 🔴 CRITICAL - Fix immediately
1. **Resolve 2 SAST vulnerabilities** (2-4 hours)
   - Parameterize SQL queries in users.js
   - Move API key to environment variables
   - Re-run SAST for verification

### 🟠 HIGH - Complete in current sprint
2. **Remediate DAST findings** (4-8 hours)
   - Implement CORS headers
   - Add authorization checks
   - Fix session management

3. **Improve unit test coverage** (8-16 hours)
   - Target: 80% (current: 75%)
   - Focus on `src/pages` (68.5% → 80%+)
   - Follow TDD practice

### 🟡 MEDIUM - Plan for next sprint
4. **Delete stale branch** (0.5 hours)
   - `feature/old-branch` is 15 days old
   - Violates trunk-based dev <48h guideline

---

## Trend Analysis (30-Day)

| Metric | 30d ago | 14d ago | Today | Trend |
|--------|---------|---------|-------|-------|
| Code Coverage | 72.5% | 73.8% | 75.5% | ↗ +4.1% |
| SAST Findings | 15 | 18 | 10 | ↘ -33% |
| Deploy Frequency | 1.5/day | 1.6/day | 1.8/day | ↗ +20% |
| Lead Time | 18h | 17h | 16.5h | ↘ -8% |

**Overall**: Positive trajectory with consistent improvement ✓

---

## Compliance vs Standards

| Dimension | Current | Target | Status |
|-----------|---------|--------|--------|
| Code Coverage | 75.5% | 80%+ | ⚠️ Near |
| SAST Critical | 0 | 0 | ✓ Pass |
| SAST High | 2 | <5 | ⚠️ Caution |
| Deploy Frequency | 1.8/day | 1+/day | ✓ Pass |
| Lead Time | 16.5h | <24h | ✓ Pass |
| PR Review SLA | 18h | <24h | ✓ Pass |

---

## Next Steps

1. Schedule security review meeting
2. Create tickets for SAST/DAST remediations
3. Plan test coverage improvements
4. Delete `feature/old-branch`
5. Re-evaluate in 1 week post-fixes

---

Generated: 2024-03-26T10:30:00Z  
Data Sources: Azure DevOps API, SonarQube, OWASP ZAP, Web Vitals  
Confidence: 94%
```

---

These examples demonstrate the comprehensive output formats that the skill produces. Customize thresholds and sections as needed for your organization.
