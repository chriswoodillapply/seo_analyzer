#!/usr/bin/env python3
"""
Orphan Page Check Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class OrphanPageCheckTest(SEOTest):
    """Test for orphan pages - pages with no inbound internal links"""
    
    @property
    def test_id(self) -> str:
        return "orphan_page_check"
    
    @property
    def test_name(self) -> str:
        return "Orphan Page Check"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    @property
    def requires_site_context(self) -> bool:
        return True
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the orphan page check test"""
        
        # If no crawl context, return INFO
        if not crawl_context:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='Requires site-wide crawl to detect orphan pages',
                recommendation='Run with --crawl to enable site-wide analysis',
                score='Crawl required'
            )
        
        # Check if this page is an orphan
        is_orphan = crawl_context.is_orphan_page(content.url)
        inbound_count = crawl_context.get_inbound_link_count(content.url)
        
        if is_orphan and content.url != crawl_context.root_url:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.FAIL,
                severity=self.severity,
                issue_description=f'Orphan page detected: No internal links pointing to this page',
                recommendation='Add internal links from other pages to improve discoverability and crawlability',
                score=f'{inbound_count} inbound links'
            )
        else:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.PASS,
                severity=self.severity,
                issue_description=f'Page has {inbound_count} inbound internal link(s)',
                recommendation='Continue maintaining internal link structure',
                score=f'{inbound_count} inbound links'
            )
