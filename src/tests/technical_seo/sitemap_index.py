#!/usr/bin/env python3
"""
Sitemap Index Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SitemapIndexTest(SEOTest):
    """Test for sitemap index"""
    
    @property
    def test_id(self) -> str:
        return "sitemap_index"
    
    @property
    def test_name(self) -> str:
        return "Sitemap Index"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the sitemap index test"""
        from urllib.parse import urlparse
        import requests
        
        parsed = urlparse(content.url)
        sitemap_index_url = f"{parsed.scheme}://{parsed.netloc}/sitemap_index.xml"
        
        try:
            response = requests.head(sitemap_index_url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                return TestResult(
                    url=content.url,
                    test_id='sitemap_index_presence',
                    test_name='Sitemap Index',
                    category='Technical SEO',
                    status=TestStatus.PASS,
                    severity='Low',
                    issue_description='Sitemap index file found',
                    recommendation='Sitemap index is useful for large sites with multiple sitemaps',
                    score='Index file exists'
                )
        except:
            pass
        
        return TestResult(
            url=content.url,
            test_id='sitemap_index_presence',
            test_name='Sitemap Index',
            category='Technical SEO',
            status=TestStatus.INFO,
            severity='Low',
            issue_description='No sitemap index file found',
            recommendation='For sites with 50,000+ URLs, consider using sitemap index',
            score='No index file'
        )
    
