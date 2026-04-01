#!/usr/bin/env python3
"""
Azure DevOps Compliance Evaluator
Evaluates repositories and pipelines against GitOps and trunk-based development best practices
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from enum import Enum

class ComplianceLevel(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    FAILURE = "failure"

class DevOpsEvaluator:
    """Main evaluator class for Azure DevOps assessment"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.findings = []
        self.scores = {}
        
    def _default_config(self) -> Dict[str, Any]:
        """Default evaluation thresholds"""
        return {
            "code_coverage_web": 70,
            "code_coverage_backend": 80,
            "code_coverage_critical": 100,
            "sast_critical_threshold": 5,
            "sast_high_threshold": 15,
            "dast_high_threshold": 10,
            "required_approvers": 2,
            "pr_review_sla_hours": 24,
            "performance_lcp_ms": 2500,
            "performance_cls": 0.1,
            "performance_ttfb_ms": 600,
            "branch_max_age_days": 2,
            "deployment_frequency_daily": True,
            "lead_time_hours": 24
        }
    
    # ==================== REPOSITORY EVALUATION ====================
    
    def evaluate_branch_strategy(self, branches: List[Dict]) -> Tuple[int, List[Dict]]:
        """
        Evaluate trunk-based development compliance
        
        Criteria:
        - Healthy: daily commits to main, feature branches < 48h old
        - Warning: some stale branches, commits < 2x/week
        - Failure: many stale branches, no activity
        """
        findings = []
        score = 100
        current_time = datetime.now()
        
        main_branches = [b for b in branches if b.get('name') in ['main', 'master']]
        if not main_branches:
            findings.append({
                "severity": "CRITICAL",
                "category": "branch_strategy",
                "finding": "No main branch found",
                "description": "Repository should have 'main' or 'master' as primary branch",
                "evidence": f"Branches found: {[b.get('name') for b in branches[:5]]}",
                "remediation": "Rename or create 'main' branch as default branch"
            })
            return 30, findings
        
        main_branch = main_branches[0]
        last_commit = main_branch.get('last_commit_date')
        
        if last_commit:
            days_since_commit = (current_time - datetime.fromisoformat(last_commit)).days
            
            if days_since_commit > 7:
                score -= 30
                findings.append({
                    "severity": "CRITICAL",
                    "category": "branch_strategy",
                    "finding": "No recent commits on main",
                    "description": f"Main branch has no commits for {days_since_commit} days (healthy: daily)",
                    "evidence": f"Last commit: {last_commit}",
                    "remediation": "Increase merge frequency to main branch (trunk-based dev practice)"
                })
            elif days_since_commit > 2:
                score -= 10
                findings.append({
                    "severity": "WARNING",
                    "category": "branch_strategy",
                    "finding": "Commit frequency lower than ideal",
                    "description": f"Main branch commits every {days_since_commit} days (healthy: daily)",
                    "evidence": f"Last commit: {last_commit}",
                    "remediation": "Merge feature branches more frequently to main"
                })
        
        # Check for stale feature branches
        stale_branches = []
        for branch in branches:
            if branch.get('name') not in ['main', 'master']:
                last_commit = branch.get('last_commit_date')
                if last_commit:
                    age = (current_time - datetime.fromisoformat(last_commit)).days
                    if age > self.config['branch_max_age_days']:
                        stale_branches.append({
                            'name': branch.get('name'),
                            'age_days': age
                        })
        
        if stale_branches:
            score -= min(20, len(stale_branches) * 5)
            findings.append({
                "severity": "WARNING",
                "category": "branch_strategy",
                "finding": f"{len(stale_branches)} stale feature branches",
                "description": "Feature branches should be merged or deleted within 48 hours",
                "evidence": json.dumps([b['name'] for b in stale_branches[:10]]),
                "remediation": "Delete stale branches or rebase and merge to main"
            })
        
        return max(0, score), findings
    
    def evaluate_pr_standards(self, pull_requests: List[Dict]) -> Tuple[int, List[Dict]]:
        """
        Evaluate PR creation and review standards
        
        Checks:
        - Title format (conventional commits)
        - Required approvers
        - Review time SLA
        - Code owner enforcement
        - Description quality
        """
        findings = []
        score = 100
        
        if not pull_requests:
            findings.append({
                "severity": "INFO",
                "category": "pr_standards",
                "finding": "No PRs to evaluate",
                "description": "Repository has no pull requests yet",
                "evidence": "Empty PR list",
                "remediation": "N/A - expected for new repositories"
            })
            return score, findings
        
        # Conventional commits check
        conventional_pattern = r'^(feat|fix|docs|style|refactor|perf|test|chore|ci|build)(\(.+\))?:\s.+'
        conventional_prs = sum(1 for pr in pull_requests 
                              if re.match(conventional_pattern, pr.get('title', '')))
        conventional_rate = (conventional_prs / len(pull_requests)) * 100 if pull_requests else 0
        
        if conventional_rate < 50:
            score -= 20
            findings.append({
                "severity": "WARNING",
                "category": "pr_standards",
                "finding": f"Low conventional commit compliance ({conventional_rate:.0f}%)",
                "description": "Only {:.0f}% of PR titles follow feat/fix/docs/refactor pattern".format(conventional_rate),
                "evidence": "Sample titles: " + ", ".join([pr.get('title', '')[:50] for pr in pull_requests[:3]]),
                "remediation": "Enforce conventional commits via branch protection rules or pre-commit hooks"
            })
        
        # Reviewer compliance check
        insufficient_approvals = []
        slow_reviews = []
        
        for pr in pull_requests:
            approvers = pr.get('approvers', [])
            if len(approvers) < self.config['required_approvers']:
                insufficient_approvals.append(pr.get('id'))
            
            if pr.get('created_date') and pr.get('completed_date'):
                review_time = (datetime.fromisoformat(pr['completed_date']) - 
                              datetime.fromisoformat(pr['created_date'])).total_seconds() / 3600
                if review_time > self.config['pr_review_sla_hours']:
                    slow_reviews.append({
                        'id': pr.get('id'),
                        'hours': review_time
                    })
        
        if insufficient_approvals:
            score -= 25
            findings.append({
                "severity": "HIGH",
                "category": "pr_standards",
                "finding": f"{len(insufficient_approvals)} PRs with < {self.config['required_approvers']} approvals",
                "description": f"Best practice requires {self.config['required_approvers']}+ approvers",
                "evidence": ", ".join(str(id) for id in insufficient_approvals[:5]),
                "remediation": f"Enable branch protection rule: Require {self.config['required_approvers']} approvals"
            })
        
        if slow_reviews:
            score -= 10
            findings.append({
                "severity": "WARNING",
                "category": "pr_standards",
                "finding": f"{len(slow_reviews)} PRs exceeded {self.config['pr_review_sla_hours']}h review SLA",
                "description": "Code reviews should complete within 24 hours",
                "evidence": json.dumps([(r['id'], f"{r['hours']:.1f}h") for r in slow_reviews[:3]]),
                "remediation": "Set team SLA expectations and automate notifications for slow reviews"
            })
        
        return max(0, score), findings
    
    def evaluate_code_quality_gating(self, quality_metrics: Dict) -> Tuple[int, List[Dict]]:
        """Evaluate code quality gates and coverage"""
        findings = []
        score = 100
        
        # Code coverage evaluation
        coverage = quality_metrics.get('code_coverage', {})
        app_type = quality_metrics.get('app_type', 'web')
        threshold = self.config['code_coverage_web'] if app_type == 'web' else self.config['code_coverage_backend']
        
        if coverage.get('overall'):
            overall_coverage = coverage['overall']
            if overall_coverage < threshold - 10:
                score -= 30
                findings.append({
                    "severity": "HIGH",
                    "category": "code_quality",
                    "finding": f"Code coverage {overall_coverage}% below threshold {threshold}%",
                    "description": f"{app_type.capitalize()} apps should maintain > {threshold}% coverage",
                    "evidence": json.dumps(coverage),
                    "remediation": "Increase test coverage: write unit tests for uncovered paths"
                })
            elif overall_coverage < threshold:
                score -= 10
                findings.append({
                    "severity": "WARNING",
                    "category": "code_quality",
                    "finding": f"Code coverage {overall_coverage}% below recommended {threshold}%",
                    "description": f"Current coverage is close to minimum threshold",
                    "evidence": json.dumps(coverage),
                    "remediation": "Aim for > {threshold}% coverage in new PRs"
                })
        
        return max(0, score), findings
    
    # ==================== PIPELINE EVALUATION ====================
    
    def evaluate_pipeline_stages(self, pipeline: Dict, app_type: str = 'web') -> Tuple[int, List[Dict]]:
        """
        Evaluate CI/CD pipeline stages for required checks
        
        Web apps: Build → Lint → Secret Check → SAST → DAST → Unit/E2E Tests → Perf Tests → Deploy
        Backend: Build → Lint → Secret Check → SAST → DAST → TDD → API Tests → Deploy
        """
        findings = []
        score = 100
        
        stages = pipeline.get('stages', [])
        stage_names = [s.get('name', '').lower() for s in stages]
        
        # Define required stages
        required_stages = {
            'build': ('BUILD', 'Compilation'),
            'lint': ('LINT', 'Code style enforcement'),
            'secret': ('SECRET CHECKING', 'Credential detection'),
            'sast': ('SAST', 'Static security analysis'),
            'dast': ('DAST', 'Dynamic security testing'),
            'deploy': ('DEPLOY', 'Production deployment')
        }
        
        if app_type == 'web':
            required_stages.update({
                'test': ('UNIT/E2E TESTS', 'Test execution'),
                'perf': ('PERFORMANCE TESTS', 'Performance validation')
            })
        else:
            required_stages.update({
                'tdd': ('TDD/UNIT TESTS', 'Test-driven development'),
                'api': ('API TESTS', 'Contract/integration testing')
            })
        
        # Check for missing stages
        missing_stages = []
        for key, (stage_name, description) in required_stages.items():
            if not any(key in name for name in stage_names):
                missing_stages.append((stage_name, description))
                score -= 10
        
        if missing_stages:
            findings.append({
                "severity": "HIGH",
                "category": "pipeline",
                "finding": f"{len(missing_stages)} required pipeline stages missing",
                "description": "Pipeline is missing security or quality gates",
                "evidence": json.dumps([(s[0], s[1]) for s in missing_stages]),
                "remediation": f"Add missing stages: {', '.join([s[0] for s in missing_stages])}"
            })
        
        # Check stage ordering (security before deploy)
        security_stages_idx = []
        deploy_idx = None
        
        for i, name in enumerate(stage_names):
            if any(sec in name for sec in ['sast', 'dast', 'secret']):
                security_stages_idx.append(i)
            if 'deploy' in name:
                deploy_idx = i
        
        if security_stages_idx and deploy_idx and max(security_stages_idx) > deploy_idx:
            score -= 25
            findings.append({
                "severity": "CRITICAL",
                "category": "pipeline",
                "finding": "Security stages run after deployment",
                "description": "SAST/DAST must execute before production deployment",
                "evidence": f"Security at index {max(security_stages_idx)}, Deploy at {deploy_idx}",
                "remediation": "Reorder pipeline: move SAST/DAST before Deploy stage"
            })
        
        return max(0, score), findings
    
    def evaluate_security_scanning(self, sast_findings: Dict, dast_findings: Dict) -> Tuple[int, List[Dict]]:
        """Evaluate SAST and DAST results against thresholds"""
        findings = []
        score = 100
        
        # SAST evaluation
        sast_critical = sast_findings.get('critical', 0)
        sast_high = sast_findings.get('high', 0)
        
        if sast_critical > 0:
            score -= 40
            findings.append({
                "severity": "CRITICAL",
                "category": "security",
                "finding": f"{sast_critical} critical SAST vulnerabilities",
                "description": "Critical security vulnerabilities must be remediated immediately",
                "evidence": json.dumps(sast_findings),
                "remediation": "Fix critical vulnerabilities before deploying to production"
            })
        elif sast_high > self.config['sast_critical_threshold']:
            score -= 20
            findings.append({
                "severity": "HIGH",
                "category": "security",
                "finding": f"{sast_high} high-severity SAST findings (threshold: {self.config['sast_critical_threshold']})",
                "description": "High-severity issues should be reviewed and prioritized",
                "evidence": json.dumps(sast_findings),
                "remediation": "Create tickets for high-severity findings, implement fixes in upcoming sprints"
            })
        
        # DAST evaluation
        dast_high = dast_findings.get('high', 0)
        
        if dast_high > self.config['dast_high_threshold']:
            score -= 20
            findings.append({
                "severity": "HIGH",
                "category": "security",
                "finding": f"{dast_high} high-severity DAST findings (threshold: {self.config['dast_high_threshold']})",
                "description": "Dynamic security tests found runtime vulnerabilities",
                "evidence": json.dumps(dast_findings),
                "remediation": "Address high-severity API vulnerabilities in staging environment"
            })
        
        return max(0, score), findings
    
    def evaluate_test_coverage(self, test_metrics: Dict, app_type: str = 'web') -> Tuple[int, List[Dict]]:
        """Evaluate unit test, E2E, and API test coverage"""
        findings = []
        score = 100
        
        unit_coverage = test_metrics.get('unit_test_coverage')
        e2e_pass_rate = test_metrics.get('e2e_pass_rate')
        api_pass_rate = test_metrics.get('api_test_pass_rate')
        
        if app_type == 'web':
            threshold = self.config['code_coverage_web']
            if unit_coverage and unit_coverage < threshold:
                score -= 20
                findings.append({
                    "severity": "HIGH",
                    "category": "testing",
                    "finding": f"Unit test coverage {unit_coverage}% below {threshold}%",
                    "description": "Web app unit tests should cover > {threshold}% of code",
                    "evidence": f"Coverage: {unit_coverage}%",
                    "remediation": "Write unit tests for new features and refactorings"
                })
            
            if e2e_pass_rate and e2e_pass_rate < 95:
                score -= 15
                findings.append({
                    "severity": "WARNING",
                    "category": "testing",
                    "finding": f"E2E test pass rate {e2e_pass_rate}% below 95%",
                    "description": "E2E tests should have > 95% pass rate",
                    "evidence": f"Pass rate: {e2e_pass_rate}%",
                    "remediation": "Investigate flaky E2E tests and fix root causes"
                })
        else:  # backend
            threshold = self.config['code_coverage_backend']
            if unit_coverage and unit_coverage < threshold:
                score -= 20
                findings.append({
                    "severity": "HIGH",
                    "category": "testing",
                    "finding": f"Unit test coverage {unit_coverage}% below {threshold}%",
                    "description": "Backend APIs should maintain > {threshold}% test coverage",
                    "evidence": f"Coverage: {unit_coverage}%",
                    "remediation": "Practice TDD: write tests before implementing API endpoints"
                })
            
            if api_pass_rate and api_pass_rate < 95:
                score -= 15
                findings.append({
                    "severity": "WARNING",
                    "category": "testing",
                    "finding": f"API test pass rate {api_pass_rate}% below 95%",
                    "description": "API contract tests should have > 95% pass rate",
                    "evidence": f"Pass rate: {api_pass_rate}%",
                    "remediation": "Review failing contract tests and update API contracts"
                })
        
        return max(0, score), findings
    
    # ==================== ARTIFACTS & METRICS EVALUATION ====================
    
    def evaluate_performance_metrics(self, performance: Dict) -> Tuple[int, List[Dict]]:
        """Evaluate web performance metrics"""
        findings = []
        score = 100
        
        metrics = {
            'lcp': (self.config['performance_lcp_ms'], 'Largest Contentful Paint'),
            'ttfb': (self.config['performance_ttfb_ms'], 'Time to First Byte'),
            'cls': (self.config['performance_cls'], 'Cumulative Layout Shift')
        }
        
        for key, (threshold, name) in metrics.items():
            value = performance.get(key)
            if value and value > threshold:
                score -= 15
                findings.append({
                    "severity": "WARNING",
                    "category": "performance",
                    "finding": f"{name}: {value}ms (threshold: {threshold}ms)",
                    "description": f"Web performance metric exceeds acceptable threshold",
                    "evidence": json.dumps(performance),
                    "remediation": f"Optimize for {name}: implement code splitting, lazy loading, caching"
                })
        
        return max(0, score), findings
    
    def evaluate_deployment_metrics(self, metrics: Dict) -> Tuple[int, List[Dict]]:
        """Evaluate deployment frequency and success metrics"""
        findings = []
        score = 100
        
        deploy_freq = metrics.get('deployments_per_day', 0)
        deployment_success = metrics.get('success_rate', 100)
        lead_time = metrics.get('lead_time_hours', 0)
        
        if deploy_freq < 1 and self.config['deployment_frequency_daily']:
            score -= 20
            findings.append({
                "severity": "WARNING",
                "category": "deployment",
                "finding": f"Deployment frequency {deploy_freq}/day (target: 1+/day)",
                "description": "DORA metrics recommend daily deployments",
                "evidence": f"Deployments per day: {deploy_freq}",
                "remediation": "Increase deployment frequency through CI/CD improvements"
            })
        
        if deployment_success < 99:
            score -= 15
            findings.append({
                "severity": "WARNING",
                "category": "deployment",
                "finding": f"Deployment success rate {deployment_success}% (target: > 99%)",
                "description": "Deployments should have high reliability",
                "evidence": f"Success rate: {deployment_success}%",
                "remediation": "Improve testing coverage and automated validations"
            })
        
        if lead_time > self.config['lead_time_hours']:
            score -= 10
            findings.append({
                "severity": "WARNING",
                "category": "deployment",
                "finding": f"Lead time {lead_time}h (target: < {self.config['lead_time_hours']}h)",
                "description": "Lead time from commit to production should be < 24 hours",
                "evidence": f"Lead time: {lead_time}h",
                "remediation": "Streamline CI/CD pipeline, implement continuous deployment"
            })
        
        return max(0, score), findings
    
    # ==================== REPORT GENERATION ====================
    
    def generate_report(self, evaluation_data: Dict) -> Dict:
        """Generate comprehensive evaluation report"""
        
        # Evaluate each dimension
        repo_score, repo_findings = self.evaluate_repository(evaluation_data.get('repository', {}))
        pipeline_score, pipeline_findings = self.evaluate_pipeline(evaluation_data.get('pipeline', {}))
        artifacts_score, artifacts_findings = self.evaluate_artifacts(evaluation_data.get('artifacts', {}))
        
        # Calculate overall score
        overall_score = (repo_score + pipeline_score + artifacts_score) / 3
        
        return {
            "evaluation_date": datetime.now().isoformat(),
            "project": evaluation_data.get('project_name'),
            "repository": evaluation_data.get('repository_name'),
            "app_type": evaluation_data.get('app_type', 'web'),
            "overall_compliance_score": round(overall_score, 1),
            "dimensions": {
                "repository": {
                    "score": round(repo_score, 1),
                    "findings": repo_findings
                },
                "pipeline": {
                    "score": round(pipeline_score, 1),
                    "findings": pipeline_findings
                },
                "artifacts": {
                    "score": round(artifacts_score, 1),
                    "findings": artifacts_findings
                }
            },
            "summary": self._generate_summary(overall_score),
            "recommendations": self._prioritize_recommendations(repo_findings + pipeline_findings + artifacts_findings)
        }
    
    def evaluate_repository(self, repo_data: Dict) -> Tuple[int, List[Dict]]:
        """Comprehensive repository evaluation"""
        all_findings = []
        scores = []
        
        score, findings = self.evaluate_branch_strategy(repo_data.get('branches', []))
        scores.append(score)
        all_findings.extend(findings)
        
        score, findings = self.evaluate_pr_standards(repo_data.get('pull_requests', []))
        scores.append(score)
        all_findings.extend(findings)
        
        score, findings = self.evaluate_code_quality_gating(repo_data.get('quality_metrics', {}))
        scores.append(score)
        all_findings.extend(findings)
        
        avg_score = sum(scores) / len(scores) if scores else 100
        return round(avg_score, 1), all_findings
    
    def evaluate_pipeline(self, pipeline_data: Dict) -> Tuple[int, List[Dict]]:
        """Comprehensive pipeline evaluation"""
        all_findings = []
        scores = []
        
        app_type = pipeline_data.get('app_type', 'web')
        
        score, findings = self.evaluate_pipeline_stages(pipeline_data.get('definition', {}), app_type)
        scores.append(score)
        all_findings.extend(findings)
        
        score, findings = self.evaluate_security_scanning(
            pipeline_data.get('sast_results', {}),
            pipeline_data.get('dast_results', {})
        )
        scores.append(score)
        all_findings.extend(findings)
        
        score, findings = self.evaluate_test_coverage(pipeline_data.get('test_metrics', {}), app_type)
        scores.append(score)
        all_findings.extend(findings)
        
        avg_score = sum(scores) / len(scores) if scores else 100
        return round(avg_score, 1), all_findings
    
    def evaluate_artifacts(self, artifacts_data: Dict) -> Tuple[int, List[Dict]]:
        """Comprehensive artifacts & metrics evaluation"""
        all_findings = []
        scores = []
        
        score, findings = self.evaluate_performance_metrics(artifacts_data.get('performance', {}))
        scores.append(score)
        all_findings.extend(findings)
        
        score, findings = self.evaluate_deployment_metrics(artifacts_data.get('deployment_metrics', {}))
        scores.append(score)
        all_findings.extend(findings)
        
        avg_score = sum(scores) / len(scores) if scores else 100
        return round(avg_score, 1), all_findings
    
    def _generate_summary(self, score: float) -> str:
        """Generate text summary based on score"""
        if score >= 90:
            return "Excellent DevOps maturity. Strong GitOps practices and trunk-based development compliance."
        elif score >= 75:
            return "Good DevOps practices with some areas for improvement. Address critical findings to improve compliance."
        elif score >= 60:
            return "DevOps practices need improvement. Multiple gaps in security, testing, and deployment processes."
        else:
            return "DevOps practices require significant improvement. Address critical findings immediately."
    
    def _prioritize_recommendations(self, all_findings: List[Dict]) -> List[Dict]:
        """Sort recommendations by severity and impact"""
        priority_map = {"CRITICAL": 0, "HIGH": 1, "WARNING": 2, "INFO": 3}
        
        sorted_findings = sorted(
            all_findings,
            key=lambda x: (priority_map.get(x.get('severity', 'INFO'), 3), -len(x.get('remediation', '')))
        )
        
        return sorted_findings[:10]  # Return top 10 recommendations


if __name__ == "__main__":
    # Example usage
    evaluator = DevOpsEvaluator()
    
    example_data = {
        "project_name": "WebApp",
        "repository_name": "webapp-repo",
        "app_type": "web",
        "repository": {
            "branches": [
                {"name": "main", "last_commit_date": (datetime.now() - timedelta(hours=12)).isoformat()}
            ],
            "pull_requests": [],
            "quality_metrics": {"code_coverage": {"overall": 75}}
        },
        "pipeline": {
            "definition": {"stages": [{"name": "build"}, {"name": "lint"}, {"name": "sast"}, {"name": "deploy"}]},
            "app_type": "web",
            "sast_results": {"critical": 0, "high": 2},
            "dast_results": {"high": 3},
            "test_metrics": {"unit_test_coverage": 75, "e2e_pass_rate": 96}
        },
        "artifacts": {
            "performance": {"lcp": 2000, "ttfb": 400, "cls": 0.08},
            "deployment_metrics": {"deployments_per_day": 0.5, "success_rate": 99.5, "lead_time_hours": 18}
        }
    }
    
    report = evaluator.generate_report(example_data)
    print(json.dumps(report, indent=2))
