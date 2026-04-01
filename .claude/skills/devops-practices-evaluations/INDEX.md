# Azure DevOps GitOps & Trunk-Based Development Evaluator Skill - Complete Index

## 📋 Skill Package Contents

```
azure-devops-evaluator/
│
├── 📄 SKILL.md (12 KB)
│   └─ **START HERE** - Complete skill documentation
│     • Quick start guide
│     • Overview of all evaluation dimensions
│     • Detailed evaluation criteria
│     • Output report structure
│     • Usage examples
│     • Common findings & remediation
│     • Advanced features & limitations
│
├── 📄 README.md (11 KB)
│   └─ User-friendly guide
│     • Installation instructions
│     • Quick start usage
│     • Comprehensive examples (5 use cases)
│     • Configuration details
│     • Evaluation dimensions breakdown
│     • Troubleshooting guide
│     • Integration information
│
├── 📄 VISUAL-GUIDE.md (21 KB)
│   └─ Quick reference visual diagrams
│     • Architecture diagrams
│     • Evaluation flow charts
│     • Scoring breakdowns
│     • Pipeline stage ordering (web + backend)
│     • Data sources map
│     • Common findings checklist
│     • Success criteria checklist
│
├── 📁 scripts/ (Python evaluation engine)
│   └── evaluator.py (440 lines)
│       • DevOpsEvaluator class
│       • Repository evaluation methods
│       • Pipeline evaluation methods
│       • Artifacts evaluation methods
│       • Report generation logic
│       • Configurable thresholds
│       • JSON report output
│
├── 📁 references/ (Detailed technical reference)
│   │
│   ├── metrics-guide.md (COMPREHENSIVE - 400+ lines)
│   │   • Metric thresholds reference (code coverage, security, performance)
│   │   • Azure DevOps API endpoints
│   │   • Web scraping data sources & structure
│   │   • HTML/JSON parsing patterns
│   │   • Conventional commits regex
│   │   • PR review checklist
│   │   • Pipeline stage ordering (detailed)
│   │   • Common findings & fixes with code samples
│   │   • Troubleshooting guide
│   │
│   └── sample-outputs.md (EXTENSIVE - 600+ lines)
│       • Complete input data structure (JSON)
│       • Full JSON report example
│       • HTML dashboard output mockup
│       • Markdown report format
│       • Field-by-field documentation
│
├── 📋 test-cases.json (5 example test prompts)
│   • Full audit example
│   • PR compliance check
│   • Pipeline security validation
│   • Metrics extraction
│   • Trunk-based dev verification
│
├── ⚙️ config-template.json (Customizable configuration)
│   • Organization settings
│   • All configurable thresholds
│   • Artifact sources
│   • Report format options
│   • Notification settings
│   • Advanced options
│
└── THIS FILE: INDEX.md (Navigation guide)
```

---

## 🚀 Getting Started (3 Steps)

### Step 1: Understand the Skill
**Read these first** (in order):
1. This INDEX.md (you are here)
2. VISUAL-GUIDE.md (10 min) - See diagrams and architecture
3. SKILL.md (15 min) - Full skill description

### Step 2: Configure
1. Copy `config-template.json` → `config.json`
2. Customize thresholds for your organization
3. Set up Azure DevOps PAT token (optional, for better API access)

### Step 3: Use the Skill
Ask Claude:
```
Evaluate our DevOps practices for the CoreAPI project.
Check trunk-based development, PR standards, and pipeline security.
Our docs are at docs.acme.com/reports/
```

---

## 📚 File Guide

### Core Documentation (Read in This Order)

| File | Size | Purpose | Read Time |
|------|------|---------|-----------|
| **VISUAL-GUIDE.md** | 21 KB | Architecture, diagrams, quick reference | 10 min |
| **SKILL.md** | 12 KB | Complete skill specification | 15 min |
| **README.md** | 11 KB | Usage guide with examples | 15 min |

### Technical References (As Needed)

| File | Size | Purpose | When to Read |
|------|------|---------|--------------|
| **references/metrics-guide.md** | 12 KB | Thresholds, APIs, patterns | Need metric details |
| **references/sample-outputs.md** | 20 KB | Example data & reports | Want to see output format |
| **test-cases.json** | 3.2 KB | Example prompts | Testing the skill |
| **config-template.json** | 4.5 KB | Configuration template | Need to customize |

### Implementation (For Developers)

| File | Size | Purpose | When Needed |
|------|------|---------|------------|
| **scripts/evaluator.py** | 15 KB | Evaluation engine | Integrating with external systems |

---

## 🎯 Quick Navigation by Use Case

### "I just want to use the skill"
→ **README.md** - Jump to "Quick Start" section
→ **test-cases.json** - See example prompts

### "I want to understand how it works"
→ **VISUAL-GUIDE.md** - Diagrams
→ **SKILL.md** - Full details
→ **references/metrics-guide.md** - Threshold details

### "I need to customize thresholds"
→ **config-template.json** - Copy and modify
→ **references/metrics-guide.md** - See what metrics mean
→ **SKILL.md** - "Configuration & Customization" section

### "I want to see example output"
→ **references/sample-outputs.md** - Complete examples
→ **test-cases.json** - Test prompts that generate output

### "I need to troubleshoot something"
→ **README.md** - "Troubleshooting" section
→ **references/metrics-guide.md** - "Troubleshooting" section

### "I want to integrate with external systems"
→ **scripts/evaluator.py** - Evaluation engine
→ **references/metrics-guide.md** - Azure DevOps API endpoints

---

## 📊 Evaluation Dimensions Summary

### 1. Repository Assessment (33%)
```
Branch Strategy       (25 pts) - Trunk-based development
├─ Daily commits on main
├─ Feature branches < 48h old  
└─ Branches deleted after merge

PR Standards          (35 pts) - Code review process
├─ Conventional commits (feat/fix/docs/refactor)
├─ 2+ approvers required
└─ Review SLA < 24 hours

Code Quality Gating   (40 pts) - Coverage & gates
├─ Coverage > 70% (web) / > 80% (backend)
└─ Quality gates enforced
```

### 2. Pipeline Architecture (33%)
```
Required Stages       (30 pts) - CI/CD steps
├─ Build, Lint, Secret Check (mandatory)
├─ SAST, DAST (security)
└─ Tests, Deploy

Security Scanning     (40 pts) - Vulnerability detection
├─ SAST: Critical=0, High<5
└─ DAST: High<10

Test Coverage         (30 pts) - Quality assurance
├─ Unit tests: >95% pass rate
└─ E2E tests: >95% pass rate
```

### 3. Artifacts & Metrics (34%)
```
Performance           (40 pts) - Web Vitals (web apps)
├─ LCP < 2.5s
├─ CLS < 0.1
└─ Lighthouse > 80

Deployment            (60 pts) - DORA metrics
├─ Frequency: 1+/day
├─ Success rate: >99%
├─ Lead time: <24h
└─ MTTR: <1h
```

---

## 🔍 Key Features at a Glance

| Feature | Details | Reference |
|---------|---------|-----------|
| **Repository Audit** | Branch strategy, PR standards, reviewer compliance | SKILL.md § Repository Assessment |
| **Pipeline Validation** | Stage ordering, security placement, test coverage | SKILL.md § Pipeline Assessment |
| **Security Analysis** | SAST/DAST findings, secret scanning, vulnerability counts | SKILL.md § Security Scanning |
| **Performance Metrics** | Web Vitals, Lighthouse, deployment frequency, lead time | SKILL.md § Artifacts Assessment |
| **Web Scraping** | Extract metrics from docs.{domain}/reports/ | README.md § Advanced Usage |
| **Multi-Format Reports** | JSON, HTML dashboard, Markdown, CSV | SKILL.md § Output Report Structure |
| **Trend Analysis** | 30-day compliance trends, improvement tracking | references/sample-outputs.md |
| **Customizable Thresholds** | All metrics configurable per organization | config-template.json |

---

## 🛠️ Configuration Quick Reference

### Most Common Customizations

```json
// Code Coverage Thresholds
{
  "code_coverage": {
    "web_app": 70,           // ← Change if needed
    "backend_api": 80,       // ← Change if needed
    "critical_paths": 100
  }
}

// Security Findings Thresholds  
{
  "security": {
    "sast": {
      "critical_threshold": 0,    // ← No critical allowed
      "high_threshold": 5,        // ← Max 5 high findings
      "block_deployment_on_critical": true
    }
  }
}

// Required Approvers
{
  "pr_standards": {
    "required_approvers": 2,  // ← Change if needed
    "review_sla_hours": 24    // ← Change if needed
  }
}

// Performance Targets
{
  "performance": {
    "web_app": {
      "lcp_ms": 2500,         // ← Change if needed
      "cls": 0.1              // ← Change if needed
    }
  }
}
```

See **config-template.json** for all options.

---

## 📞 Common Questions Answered

### Q: How do I get started?
A: Read SKILL.md (15 min), then ask Claude to evaluate your project.

### Q: Can I customize the thresholds?
A: Yes! Copy config-template.json and modify all values. See SKILL.md § Configuration.

### Q: What data sources does it use?
A: Azure DevOps API + web scraping from docs.{domain}/reports/. See VISUAL-GUIDE.md.

### Q: How long does an evaluation take?
A: ~30 seconds per repo. Multi-repo scan with 10 repos: ~5 minutes.

### Q: Can it block deployments?
A: No, it reports findings. Use pipeline gates to block based on these findings.

### Q: Does it support GitHub/GitLab?
A: Primarily built for Azure DevOps. GitHub/GitLab integration in future versions.

### Q: Can I integrate it with Slack/email?
A: Yes! See references/sample-outputs.md § Notification Integration.

### Q: What if I don't have public docs?
A: Use Azure DevOps artifact API instead of web scraping. Fall back to API.

### Q: Is the Python script required?
A: No, Claude handles evaluation via the SKILL.md. Python script is optional for standalone use.

---

## 🔐 Security & Privacy

- **No credential storage**: PAT token used for API calls only
- **No data transmission**: All evaluation local to your DevOps instance
- **Web scraping**: Only public documentation URLs
- **Sensitive data**: Code coverage, security findings treated as sensitive

---

## 📈 Success Metrics

After implementing recommendations, you should see:

| Metric | Target | Timeline |
|--------|--------|----------|
| Code Coverage | 80%+ | 2-4 sprints |
| Security Findings | 0 critical, <5 high | 1-2 weeks |
| PR Review SLA | <24 hours | Immediate |
| Deployment Frequency | 1+/day | 2-4 weeks |
| Lead Time | <24 hours | 1-2 months |
| Compliance Score | 90%+ | 3-6 months |

---

## 📖 Detailed Topic References

### If you want to learn about...

| Topic | Primary | Secondary | Tertiary |
|-------|---------|-----------|----------|
| **Trunk-Based Development** | SKILL.md | VISUAL-GUIDE.md | references/metrics-guide.md |
| **GitOps Best Practices** | SKILL.md § Overview | README.md | references/metrics-guide.md |
| **Pipeline Security** | SKILL.md § Pipeline | VISUAL-GUIDE.md | references/metrics-guide.md |
| **Code Coverage** | config-template.json | SKILL.md | references/metrics-guide.md |
| **Performance Metrics** | SKILL.md § Artifacts | VISUAL-GUIDE.md | references/sample-outputs.md |
| **DORA Metrics** | SKILL.md | README.md | references/metrics-guide.md |
| **API Integration** | references/metrics-guide.md | scripts/evaluator.py | README.md |
| **Web Scraping** | references/metrics-guide.md | references/sample-outputs.md | config-template.json |

---

## 🚦 Skill Maturity Levels

```
LEVEL 1: BASIC (Start here)
├─ Repository audit only
├─ Manual configuration
└─ JSON report output

LEVEL 2: INTERMEDIATE (After 1 week)
├─ Full pipeline evaluation
├─ Web scraping for metrics
└─ HTML dashboard + recommendations

LEVEL 3: ADVANCED (After 1 month)
├─ Multi-repository scanning
├─ Trend analysis & comparison
├─ Integration with ticketing systems
└─ Automated remediation suggestions

LEVEL 4: EXPERT (3+ months)
├─ Team benchmarking
├─ Custom metric plugins
├─ Continuous compliance monitoring
└─ Slack/email automation
```

---

## 📦 What's Included

✅ Complete skill documentation (SKILL.md)
✅ User guide with examples (README.md)
✅ Visual architecture diagrams (VISUAL-GUIDE.md)
✅ Technical reference (references/)
✅ Python evaluation engine (scripts/evaluator.py)
✅ Configuration template (config-template.json)
✅ Example test cases (test-cases.json)
✅ Sample output formats (references/sample-outputs.md)

## 🎓 Learning Path

**Day 1** (30 min):
- Read VISUAL-GUIDE.md
- Run first evaluation with test-cases.json

**Week 1** (2-3 hours):
- Read SKILL.md and README.md
- Configure config-template.json
- Evaluate your main repository
- Review findings and recommendations

**Month 1**:
- Implement high-priority recommendations
- Set up multi-repository scanning
- Integrate with Slack/dashboards
- Track 30-day trend improvements

**Quarter 1+**:
- Achieve 90%+ compliance score
- Establish continuous evaluation
- Benchmark against industry standards
- Mentor team on best practices

---

## 🤝 Integration Checklist

Before deploying to production, ensure:

- [ ] Azure DevOps API access (PAT token or public repos)
- [ ] Documentation domain accessible & structured
- [ ] SAST/DAST tools integrated into pipeline
- [ ] Code coverage reporting configured
- [ ] Performance metrics collection setup
- [ ] Deployment metrics tracked
- [ ] Config customized for your org
- [ ] Test evaluation on sample repo
- [ ] Review sample outputs
- [ ] Plan remediation for findings

---

## 📞 Support & Next Steps

### For help, consult:
1. **README.md** § Troubleshooting
2. **references/metrics-guide.md** § Troubleshooting
3. Review test-cases.json for examples
4. Check sample-outputs.md for expected format

### To extend the skill:
1. See scripts/evaluator.py for evaluation logic
2. Read references/metrics-guide.md for metrics definitions
3. Modify config-template.json for custom thresholds

---

## 📋 Version & Changelog

**Version**: 1.0  
**Release Date**: 2024-03-26  
**Status**: Production Ready

### Included Components:
- Core Evaluator: ✅
- Repository Assessment: ✅
- Pipeline Validation: ✅
- Security Analysis: ✅
- Artifacts & Metrics: ✅
- Multi-Format Reports: ✅
- Web Scraping: ✅
- Trend Analysis: ✅
- Config Template: ✅
- Test Cases: ✅
- Documentation: ✅

---

**Last Updated**: 2024-03-26  
**Maintained By**: DevOps Evaluation Team  
**License**: Internal Use

---

## 🎉 You're Ready!

Start with VISUAL-GUIDE.md, then SKILL.md, then use the skill with Claude.

Good luck evaluating your DevOps practices! 🚀
