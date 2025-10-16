#!/usr/bin/env python3
"""
Robots.txt Presence Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class RobotsTxtTest(SEOTest):
    """Test for robots.txt presence"""
    
    @property
    def test_id(self) -> str:
        return "robots_txt"
    
    @property
    def test_name(self) -> str:
        return "Robots.txt Presence"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the robots.txt presence test"""
        from urllib.parse import urlparse
        parsed = urlparse(content.url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            import requests
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                return TestResult(
                    url=content.url,
                    test_id='robots_txt',
                    test_name='Robots.txt Presence',
                    category='Technical SEO',
                    status=TestStatus.PASS,
                    severity='Medium',
                    issue_description='Robots.txt file found',
                    recommendation='Ensure robots.txt is properly configured',
                    score='File exists'
                )
        except:
            pass
        
        return TestResult(
            url=content.url,
            test_id='robots_txt',
            test_name='Robots.txt Presence',
            category='Technical SEO',
            status=TestStatus.WARNING,
            severity='Medium',
            issue_description='Robots.txt file not found',
            recommendation='Create robots.txt file to guide search engines',
            score='File not found'
        )
    
