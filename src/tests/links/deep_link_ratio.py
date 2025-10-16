#!/usr/bin/env python3
"""
Deep Link Ratio Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class DeepLinkRatioTest(SEOTest):
    """Test for distribution of internal links to deep pages"""
    
    @property
    def test_id(self) -> str:
        return "deep_link_ratio"
    
    @property
    def test_name(self) -> str:
        return "Deep Link Distribution"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    @property
    def requires_site_context(self) -> bool:
        return True
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the deep link ratio test"""
        
        # If no crawl context, return INFO
        if not crawl_context:
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='Requires site-wide analysis for link distribution',
                recommendation='Run with --crawl to analyze link patterns',
                score='Crawl required'
            )
        
        # Get outbound link count
        outbound_count = crawl_context.get_outbound_link_count(content.url)
        
        if outbound_count == 0:
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.WARNING,
                severity=self.severity,
                issue_description='Page has no outbound internal links',
                recommendation='Add relevant internal links to improve site navigation and link equity distribution',
                score='0 outbound links'
            )
        
        # Count deep links (pages at depth 3+)
        deep_links = 0
        for target_url in crawl_context.internal_links.get(content.url, []):
            target_depth = crawl_context.get_page_depth(target_url)
            if target_depth >= 3:
                deep_links += 1
        
        deep_ratio = (deep_links / outbound_count * 100) if outbound_count > 0 else 0
        
        if deep_ratio >= 30:
            status = TestStatus.PASS
            issue = f'Good deep link distribution: {deep_ratio:.1f}% of links go to deeper pages'
            recommendation = 'Continue linking to deep content'
        elif deep_ratio >= 15:
            status = TestStatus.WARNING
            issue = f'Moderate deep link distribution: {deep_ratio:.1f}% of links go to deeper pages'
            recommendation = 'Consider adding more links to deep content pages'
        else:
            status = TestStatus.INFO
            issue = f'Low deep link distribution: {deep_ratio:.1f}% of links go to deeper pages'
            recommendation = 'Add more links to deep pages to improve discoverability'
        
        return [TestResult(
            url=content.url,
            test_id=self.test_id,
            test_name=self.test_name,
            category=self.category,
            status=status,
            severity=self.severity,
            issue_description=issue,
            recommendation=recommendation,
            score=f'{deep_links}/{outbound_count} deep links ({deep_ratio:.1f}%)'
        )
