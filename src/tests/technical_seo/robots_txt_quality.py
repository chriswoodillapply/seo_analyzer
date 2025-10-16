#!/usr/bin/env python3
"""
Robots.txt Quality Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class RobotsTxtQualityTest(SEOTest):
    """Test for robots.txt quality"""
    
    @property
    def test_id(self) -> str:
        return "robots_txt_quality"
    
    @property
    def test_name(self) -> str:
        return "Robots.txt Quality"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the robots.txt quality test"""
        from urllib.parse import urlparse
        import requests
        
        parsed = urlparse(content.url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                robots_content = response.text
                
                # Check for common issues
                issues = []
                if 'Disallow: /' in robots_content and 'Allow:' not in robots_content:
                    issues.append('Blocking entire site')
                if robots_content.count('Disallow:') > 50:
                    issues.append('Too many disallow rules')
                if 'Sitemap:' not in robots_content:
                    issues.append('No sitemap reference')
                
                if not issues:
                    return TestResult(
                        url=content.url,
                        test_id='robots_txt_quality',
                        test_name='Robots.txt Quality',
                        category='Technical SEO',
                        status=TestStatus.PASS,
                        severity='Medium',
                        issue_description='Robots.txt appears well-configured',
                        recommendation='Continue maintaining robots.txt best practices',
                        score='Well configured'
                    )
                else:
                    return TestResult(
                        url=content.url,
                        test_id='robots_txt_quality',
                        test_name='Robots.txt Quality',
                        category='Technical SEO',
                        status=TestStatus.WARNING,
                        severity='Medium',
                        issue_description=f'Robots.txt issues: {", ".join(issues)}',
                        recommendation='Review and optimize robots.txt configuration',
                        score=f'{len(issues)} issue(s)'
                    )
        except:
            pass
        
        return None
    
