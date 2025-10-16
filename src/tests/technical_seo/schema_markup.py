#!/usr/bin/env python3
"""
Schema Markup Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SchemaMarkupTest(SEOTest):
    """Test for schema markup"""
    
    @property
    def test_id(self) -> str:
        return "schema_markup"
    
    @property
    def test_name(self) -> str:
        return "Schema Markup"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the schema markup test"""
        soup = content.rendered_soup or content.static_soup
        
        # Check for JSON-LD
        json_ld = soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        # Check for microdata
        microdata = soup.find_all(attrs={'itemscope': True})
        
        schema_count = len(json_ld) + len(microdata)
        
        if schema_count > 0:
            return [TestResult(
                url=content.url,
                test_id='schema_markup',
                test_name='Schema Markup',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Found {schema_count} schema markup instances',
                recommendation='Continue implementing relevant structured data',
                score=f'{schema_count} schema blocks'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='schema_markup',
                test_name='Schema Markup',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No schema markup found',
                recommendation='Implement structured data for rich snippets',
                score='No schema found'
            )
    
    # =========================================================================
    # PERFORMANCE TESTS
    # =========================================================================
    
