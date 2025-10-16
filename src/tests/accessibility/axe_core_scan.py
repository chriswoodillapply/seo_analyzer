#!/usr/bin/env python3
"""
axe-core Accessibility Scan Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class AxeCoreScanTest(SEOTest):
    """Run axe-core accessibility testing"""
    
    @property
    def test_id(self) -> str:
        return "axe_core_scan"
    
    @property
    def test_name(self) -> str:
        return "axe-core Accessibility Scan"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.CRITICAL
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute axe-core accessibility scan"""
        
        # Check if we have rendered content (indicates Playwright was used)
        if not content.rendered_html:
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='axe-core requires JavaScript rendering (Playwright)',
                recommendation='Enable JavaScript rendering with --javascript flag',
                score='Requires JS rendering'
            )
        
        # Try to run axe-core if available
        try:
            from src.integrations.axe_core import AxeCoreIntegration
            
            # Note: This requires access to the Playwright page object
            # For now, we'll need to modify ContentFetcher to store the page reference
            # or run axe during the rendering phase
            
            # Placeholder: Check if we have axe results stored in content
            if hasattr(content, 'axe_results') and content.axe_results:
                results = content.axe_results
                summary = AxeCoreIntegration.format_axe_results(results)
                
                total_violations = summary.get('total_violations', 0)
                critical = summary.get('severity_breakdown', {}).get('critical', 0)
                serious = summary.get('severity_breakdown', {}).get('serious', 0)
                
                if total_violations == 0:
                    return [TestResult(
                        url=content.url,
                        test_id=self.test_id,
                        test_name=self.test_name,
                        category=self.category,
                        status=TestStatus.PASS,
                        severity=self.severity,
                        issue_description='No accessibility violations detected by axe-core',
                        recommendation='Continue following WCAG 2.1 guidelines',
                        score=f'0 violations, {summary.get("total_passes", 0)} checks passed'
                    )
                
                elif critical > 0 or serious > 0:
                    top_issues = ', '.join([v['id'] for v in summary.get('top_violations', [])[:3]])
                    return [TestResult(
                        url=content.url,
                        test_id=self.test_id,
                        test_name=self.test_name,
                        category=self.category,
                        status=TestStatus.FAIL,
                        severity=self.severity,
                        issue_description=f'{total_violations} accessibility violations found (Critical: {critical}, Serious: {serious})',
                        recommendation=f'Fix critical issues immediately. Top issues: {top_issues}',
                        score=f'{total_violations} violations ({critical} critical, {serious} serious)'
                    )
                else:
                    return [TestResult(
                        url=content.url,
                        test_id=self.test_id,
                        test_name=self.test_name,
                        category=self.category,
                        status=TestStatus.WARNING,
                        severity=self.severity,
                        issue_description=f'{total_violations} minor/moderate accessibility issues',
                        recommendation='Review and fix accessibility issues for better compliance',
                        score=f'{total_violations} violations (minor/moderate)'
                    )
            
            # If axe hasn't been run yet, return INFO
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='axe-core not run yet - requires ContentFetcher integration',
                recommendation='Run axe-core manually: npm install -g @axe-core/cli && axe ' + content.url,
                score='Integration pending'
            )
            
        except ImportError:
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='axe-core integration module not available',
                recommendation='Use https://www.deque.com/axe/ for comprehensive accessibility testing',
                score='Manual test recommended'
            )

