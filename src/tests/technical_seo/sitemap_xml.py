#!/usr/bin/env python3
"""
XML Sitemap Presence Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SitemapXmlTest(SEOTest):
    """Test for xml sitemap presence"""
    
    @property
    def test_id(self) -> str:
        return "sitemap_xml"
    
    @property
    def test_name(self) -> str:
        return "XML Sitemap Presence"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the xml sitemap presence test"""
        from urllib.parse import urlparse
        parsed = urlparse(content.url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
        
        try:
            import requests
            response = requests.get(sitemap_url, timeout=5)
            if response.status_code == 200:
                return TestResult(
                    url=content.url,
                    test_id='sitemap_xml',
                    test_name='XML Sitemap Presence',
                    category='Technical SEO',
                    status=TestStatus.PASS,
                    severity='Medium',
                    issue_description='XML sitemap found',
                    recommendation='Ensure sitemap is up to date and submitted to search engines',
                    score='File exists'
                )
        except:
            pass
        
        return TestResult(
            url=content.url,
            test_id='sitemap_xml',
            test_name='XML Sitemap Presence',
            category='Technical SEO',
            status=TestStatus.WARNING,
            severity='Medium',
            issue_description='XML sitemap not found',
            recommendation='Create and submit XML sitemap to search engines',
            score='File not found'
        )
    
