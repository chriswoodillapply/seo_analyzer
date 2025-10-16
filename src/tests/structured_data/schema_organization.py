#!/usr/bin/env python3
"""
Organization Schema Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SchemaOrganizationTest(SEOTest):
    """Test for organization schema"""
    
    @property
    def test_id(self) -> str:
        return "schema_organization"
    
    @property
    def test_name(self) -> str:
        return "Organization Schema"
    
    @property
    def category(self) -> str:
        return TestCategory.STRUCTURED_DATA
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the organization schema test"""
        import json
        soup = content.rendered_soup or content.static_soup
        
        # Find all JSON-LD scripts
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        has_organization = False
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                # Handle both single objects and arrays
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if item.get('@type') == 'Organization':
                        has_organization = True
                        break
            except:
                continue
        
        if has_organization:
            return TestResult(
                url=content.url,
                test_id='schema_organization',
                test_name='Organization Schema',
                category='Structured Data',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Organization schema markup found',
                recommendation='Continue maintaining Organization structured data',
                score='Organization schema present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='schema_organization',
                test_name='Organization Schema',
                category='Structured Data',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No Organization schema markup found',
                recommendation='Add Organization schema to help search engines understand your business',
                score='No Organization schema'
            )
    
