#!/usr/bin/env python3
"""
Content Freshness Indicators Test
"""

from typing import Optional, List, TYPE_CHECKING
import re
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ContentFreshnessDateTest(SEOTest):
    """Test for content freshness indicators"""
    
    @property
    def test_id(self) -> str:
        return "content_freshness_date"
    
    @property
    def test_name(self) -> str:
        return "Content Freshness Indicators"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the content freshness indicators test"""
        import json
        soup = content.rendered_soup or content.static_soup
        
        # Check for schema datePublished/dateModified
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        has_date_schema = False
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if 'datePublished' in item or 'dateModified' in item:
                        has_date_schema = True
                        break
            except:
                continue
        
        # Check for common date meta tags
        date_meta = soup.find('meta', attrs={'property': re.compile(r'(article:published_time|article:modified_time)', re.I)})
        
        if has_date_schema or date_meta:
            return [TestResult(
                url=content.url,
                test_id='content_freshness_date',
                test_name='Content Freshness Indicators',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='Content date metadata found',
                recommendation='Continue maintaining date metadata for content freshness signals',
                score='Date metadata present'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='content_freshness_date',
                test_name='Content Freshness Indicators',
                category='Content',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No date metadata found',
                recommendation='Consider adding publication/modified dates for content freshness',
                score='No date metadata'
            )
    
