#!/usr/bin/env python3
"""
axe-core Accessibility Scan Test
"""

from typing import Optional, TYPE_CHECKING, List, Dict, Any
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
        """Execute axe-core accessibility scan and return one result per violation."""

        def map_impact_to_severity(impact: str) -> str:
            mapping = {
                'critical': TestSeverity.CRITICAL,
                'serious': TestSeverity.HIGH,
                'moderate': TestSeverity.MEDIUM,
                'minor': TestSeverity.LOW,
            }
            return mapping.get((impact or '').lower(), TestSeverity.MEDIUM)

        def map_impact_to_status(impact: str) -> TestStatus:
            impact_lower = (impact or '').lower()
            if impact_lower in ('critical', 'serious'):
                return TestStatus.FAIL
            return TestStatus.WARNING

        # Require rendered content to run axe
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
            )]

        # Use results captured during rendering in ContentFetcher
        axe = getattr(content, 'axe_results', None)
        if not axe:
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='axe-core did not produce results',
                recommendation='Verify axe-core injection and network connectivity to CDN',
                score='No results'
            )]

        violations: List[Dict[str, Any]] = axe.get('violations', []) or []
        if not violations:
            return [TestResult(
                url=content.url,
                test_id='axe_core_scan_pass',
                test_name='axe-core: All Checks Passed',
                category=self.category,
                status=TestStatus.PASS,
                severity=TestSeverity.LOW,
                issue_description='No accessibility violations detected by axe-core',
                recommendation='Continue following WCAG 2.1 guidelines',
                score='0 violations'
            )]

        results: List[TestResult] = []
        for v in violations:
            vid = v.get('id', 'unknown')
            impact = v.get('impact', 'minor')
            nodes = v.get('nodes', []) or []
            title = v.get('help') or v.get('description') or vid
            description = v.get('description') or title
            help_url = v.get('helpUrl')

            recommendation = title
            if help_url:
                recommendation = f"{title} ({help_url})"

            results.append(TestResult(
                url=content.url,
                test_id=f"axe_{vid}",
                test_name=f"axe-core: {vid}",
                category=self.category,
                status=map_impact_to_status(impact),
                severity=map_impact_to_severity(impact),
                issue_description=f"{description} | nodes affected: {len(nodes)}",
                recommendation=recommendation,
                score=f"impact: {impact}"
            ))

        return results

