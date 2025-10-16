#!/usr/bin/env python3
"""
Breadcrumb Schema Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SchemaBreadcrumbTest(SEOTest):
    """Test for breadcrumb schema"""
    
    @property
    def test_id(self) -> str:
        return "schema_breadcrumb"
    
    @property
    def test_name(self) -> str:
        return "Breadcrumb Schema"
    
    @property
    def category(self) -> str:
        return TestCategory.STRUCTURED_DATA
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the breadcrumb schema test"""
        import json
        soup = content.rendered_soup or content.static_soup
        
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        has_breadcrumb = False
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if item.get('@type') == 'BreadcrumbList':
                        has_breadcrumb = True
                        break
            except:
                continue
        
        if has_breadcrumb:
            return [TestResult(
                url=content.url,
                test_id='schema_breadcrumb',
                test_name='Breadcrumb Schema',
                category='Structured Data',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='BreadcrumbList schema found',
                recommendation='Continue using breadcrumb markup for better SERP display',
                score='Breadcrumb schema present'
            )
        else:
            return []  # Not all pages need breadcrumbs
    
