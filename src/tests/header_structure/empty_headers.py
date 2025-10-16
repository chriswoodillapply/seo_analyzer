#!/usr/bin/env python3
"""
Empty Headers Check Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class EmptyHeadersTest(SEOTest):
    """Test for empty headers check"""
    
    @property
    def test_id(self) -> str:
        return "empty_headers"
    
    @property
    def test_name(self) -> str:
        return "Empty Headers Check"
    
    @property
    def category(self) -> str:
        return TestCategory.HEADER_STRUCTURE
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the empty headers check test"""
        soup = content.rendered_soup or content.static_soup
        all_headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        empty_headers = [h for h in all_headers if not h.text.strip()]
        
        if len(empty_headers) == 0:
            return TestResult(
                url=content.url,
                test_id='empty_headers',
                test_name='Empty Headers Check',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='High',
                issue_description='All header tags contain text',
                recommendation='Continue using meaningful header text',
                score=f'0/{len(all_headers)} empty'
            )
        else:
            header_types = [h.name.upper() for h in empty_headers]
            return TestResult(
                url=content.url,
                test_id='empty_headers',
                test_name='Empty Headers Check',
                category='Header Structure',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{len(empty_headers)} empty header tag(s): {", ".join(header_types)}',
                recommendation='Remove empty headers or add descriptive text',
                score=f'{len(empty_headers)}/{len(all_headers)} empty'
            )
    
