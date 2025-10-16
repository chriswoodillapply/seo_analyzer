#!/usr/bin/env python3
"""
Meta Refresh Detection Test
"""

from typing import Optional, TYPE_CHECKING
import re
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class MetaRefreshRedirectTest(SEOTest):
    """Test for meta refresh detection"""
    
    @property
    def test_id(self) -> str:
        return "meta_refresh_redirect"
    
    @property
    def test_name(self) -> str:
        return "Meta Refresh Detection"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the meta refresh detection test"""
        soup = content.rendered_soup or content.static_soup
        meta_refresh = soup.find('meta', attrs={'http-equiv': re.compile(r'refresh', re.I)})
        
        if meta_refresh:
            refresh_content = meta_refresh.get('content', '')
            return TestResult(
                url=content.url,
                test_id='meta_refresh_redirect',
                test_name='Meta Refresh Detection',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'Meta refresh redirect detected: {refresh_content}',
                recommendation='Replace meta refresh with 301/302 HTTP redirect for better SEO',
                score='Meta refresh found'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='meta_refresh_redirect',
                test_name='Meta Refresh Detection',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No meta refresh redirects detected',
                recommendation='Continue using proper HTTP redirects',
                score='No meta refresh'
            )
    
