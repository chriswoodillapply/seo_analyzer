#!/usr/bin/env python3
"""
Page Load Time Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class PageLoadTimeTest(SEOTest):
    """Test for page load time"""
    
    @property
    def test_id(self) -> str:
        return "page_load_time"
    
    @property
    def test_name(self) -> str:
        return "Page Load Time"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the page load time test"""
        load_time = content.rendered_load_time or content.static_load_time
        
        if load_time < 3:
            status = TestStatus.PASS
            issue = f'Page loads in {load_time:.2f} seconds'
            recommendation = 'Page load time is good'
        elif load_time < 5:
            status = TestStatus.WARNING
            issue = f'Page loads in {load_time:.2f} seconds'
            recommendation = 'Consider optimizing for faster load times'
        else:
            status = TestStatus.FAIL
            issue = f'Page loads slowly ({load_time:.2f} seconds)'
            recommendation = 'Optimize images, scripts, and server response for faster loading'
        
        return [TestResult(
            url=content.url,
            test_id='page_load_time',
            test_name='Page Load Time',
            category='Performance',
            status=status,
            severity='High',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{load_time:.2f}s'
        )
    
