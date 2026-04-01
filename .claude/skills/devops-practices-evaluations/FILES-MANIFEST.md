# Azure DevOps Evaluator Skill - Files Manifest

## Complete Package Contents

### Root Files
```
/mnt/user-data/outputs/azure-devops-evaluator/
├── INDEX.md                           [⭐ START HERE - Navigation Guide]
├── SKILL.md                           [Skill Definition & Specification]
├── README.md                          [User Guide with Examples]
├── VISUAL-GUIDE.md                    [Architecture & Diagrams]
├── config-template.json               [Configuration Template]
├── test-cases.json                    [5 Example Test Prompts]
│
├── scripts/
│   └── evaluator.py                   [Python Evaluation Engine]
│
└── references/
    ├── metrics-guide.md               [Technical Reference]
    └── sample-outputs.md              [Example Outputs & Data]
```

## File Descriptions

### Navigation & Getting Started

**INDEX.md** (Navigation Guide)
- File size: ~15 KB
- Purpose: Complete navigation, quick start, FAQ
- Read time: 5 minutes
- ⭐ **START HERE** before anything else
- Contains: Learning path, file guide, troubleshooting

**SKILL.md** (Skill Definition)
- File size: 12 KB
- Purpose: Complete skill specification
- Read time: 15 minutes
- Contains: Overview, evaluation dimensions, detailed criteria, output formats, examples

**README.md** (User Guide)
- File size: 11 KB
- Purpose: User-friendly guide with examples
- Read time: 15 minutes
- Contains: Installation, 5 usage examples, configuration, troubleshooting

**VISUAL-GUIDE.md** (Architecture & Diagrams)
- File size: 21 KB
- Purpose: Visual understanding of the skill
- Read time: 10 minutes
- Contains: Flowcharts, diagrams, scoring breakdown, pipeline stages, checklists

### Technical Reference

**references/metrics-guide.md** (Comprehensive Reference)
- File size: 12 KB
- Purpose: Detailed technical reference
- Read time: 15 minutes (as needed)
- Contains: 
  - Metric thresholds (code coverage, security, performance)
  - Azure DevOps API endpoints
  - Web scraping patterns
  - Conventional commits regex
  - PR checklist
  - Pipeline ordering
  - Common findings & fixes
  - Troubleshooting

**references/sample-outputs.md** (Example Outputs)
- File size: 20 KB
- Purpose: See what outputs look like
- Read time: 10 minutes (as needed)
- Contains:
  - Complete input data structure (JSON)
  - Full JSON report example
  - HTML dashboard mockup
  - Markdown report format
  - Field-by-field documentation

### Implementation Files

**scripts/evaluator.py** (Python Engine)
- File size: 15 KB
- Lines of code: 440
- Purpose: Evaluation engine implementation
- Use when: Need to integrate with external systems
- Contains:
  - DevOpsEvaluator class
  - Repository evaluation methods
  - Pipeline evaluation methods
  - Artifacts evaluation methods
  - Report generation
  - Configurable thresholds

**config-template.json** (Configuration)
- File size: 4.5 KB
- Purpose: All customizable thresholds
- Use for: Setting up your organization's specific requirements
- Contains:
  - Organization settings
  - All metric thresholds (20+)
  - Artifact sources
  - Report formats
  - Notification settings
  - Advanced options

**test-cases.json** (Test Examples)
- File size: 3.2 KB
- Purpose: Example evaluation prompts
- Use for: Testing the skill
- Contains:
  - Full audit example
  - PR compliance check
  - Pipeline security validation
  - Metrics extraction
  - Trunk-based dev verification

## File Dependencies & Reading Order

### For First-Time Users
1. **INDEX.md** (5 min) - Start here!
2. **VISUAL-GUIDE.md** (10 min) - Understand architecture
3. **SKILL.md** (15 min) - Learn details
4. **README.md** (15 min) - See examples
5. Ask Claude to evaluate!

### For Configuration
1. **config-template.json** - Template
2. **references/metrics-guide.md** - Understand metrics
3. **SKILL.md** § Configuration - Details
4. Customize and save as config.json

### For Implementation
1. **scripts/evaluator.py** - Engine
2. **references/metrics-guide.md** - API reference
3. **references/sample-outputs.md** - Output format

### For Troubleshooting
1. **INDEX.md** § FAQ - Common questions
2. **README.md** § Troubleshooting - Known issues
3. **references/metrics-guide.md** § Troubleshooting - Detailed help

## File Statistics

| File | Size | Lines | Type | Purpose |
|------|------|-------|------|---------|
| INDEX.md | 15 KB | 500+ | Markdown | Navigation |
| SKILL.md | 12 KB | 400+ | Markdown | Specification |
| README.md | 11 KB | 350+ | Markdown | User Guide |
| VISUAL-GUIDE.md | 21 KB | 700+ | Markdown | Architecture |
| evaluator.py | 15 KB | 440 | Python | Engine |
| metrics-guide.md | 12 KB | 400+ | Markdown | Reference |
| sample-outputs.md | 20 KB | 600+ | Markdown | Examples |
| config-template.json | 4.5 KB | 100+ | JSON | Config |
| test-cases.json | 3.2 KB | 50+ | JSON | Tests |
| **TOTAL** | **~113 KB** | **~3500+** | - | - |

## What's in Each File

### Evaluation Criteria (Where to Find)
- Repository assessment → SKILL.md § Repository Assessment
- Pipeline assessment → SKILL.md § Pipeline Assessment
- Artifacts assessment → SKILL.md § Artifacts Assessment
- All details → references/metrics-guide.md

### Configuration (Where to Find)
- Default thresholds → config-template.json
- Threshold meanings → references/metrics-guide.md
- How to customize → SKILL.md § Configuration & Customization

### Examples (Where to Find)
- Usage examples → README.md § Usage Examples
- Test prompts → test-cases.json
- Sample outputs → references/sample-outputs.md
- Data structures → references/sample-outputs.md § Input Data Structure

### Troubleshooting (Where to Find)
- Common issues → INDEX.md § Common Questions
- Detailed help → README.md § Troubleshooting
- Technical issues → references/metrics-guide.md § Troubleshooting

### API Reference (Where to Find)
- Azure DevOps endpoints → references/metrics-guide.md § Azure DevOps API
- Web scraping → references/metrics-guide.md § Web Scraping
- Conventional commits → references/metrics-guide.md § Conventional Commits

## File Checklist

- ✅ INDEX.md (Navigation)
- ✅ SKILL.md (Specification)
- ✅ README.md (User Guide)
- ✅ VISUAL-GUIDE.md (Architecture)
- ✅ scripts/evaluator.py (Engine)
- ✅ references/metrics-guide.md (Reference)
- ✅ references/sample-outputs.md (Examples)
- ✅ config-template.json (Configuration)
- ✅ test-cases.json (Test Cases)

## Quick Access by Need

### "I want to start using this skill"
→ INDEX.md (5 min) + ask Claude

### "I want to understand how it works"
→ VISUAL-GUIDE.md + SKILL.md + README.md

### "I want to customize thresholds"
→ config-template.json + references/metrics-guide.md

### "I want to see example output"
→ references/sample-outputs.md + test-cases.json

### "I need to troubleshoot"
→ INDEX.md § FAQ + README.md § Troubleshooting + references/metrics-guide.md § Troubleshooting

### "I want to integrate with external systems"
→ scripts/evaluator.py + references/metrics-guide.md § API

## Installation & Organization

Recommended directory structure:
```
your-org/
├── azure-devops-evaluator/       (This skill package)
│   ├── INDEX.md                   (⭐ Start here)
│   ├── SKILL.md
│   ├── README.md
│   ├── VISUAL-GUIDE.md
│   ├── config.json                (Your customized config)
│   ├── scripts/
│   │   └── evaluator.py
│   └── references/
│       ├── metrics-guide.md
│       └── sample-outputs.md
└── evaluation-reports/            (Your evaluation results)
    ├── 2024-03-26-report.json
    ├── 2024-03-26-report.html
    └── 2024-03-26-report.md
```

## Version Information

- **Version**: 1.0
- **Release Date**: 2024-03-26
- **Status**: Production Ready
- **Total Files**: 9
- **Total Size**: ~113 KB
- **Documentation**: 100+ KB
- **Code**: 15 KB
- **Configuration**: 8 KB

## Next Steps

1. **Download** all files from `/mnt/user-data/outputs/azure-devops-evaluator/`
2. **Read** INDEX.md first
3. **Copy** config-template.json → config.json
4. **Customize** config.json for your organization
5. **Ask Claude** to evaluate your project

---

**All files are ready to use. Start with INDEX.md! 🚀**
