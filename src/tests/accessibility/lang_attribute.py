#!/usr/bin/env python3
"""
Language Attribute Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class LangAttributeTest(SEOTest):
    """Test for language attribute"""
    
    @property
    def test_id(self) -> str:
        return "lang_attribute"
    
    @property
    def test_name(self) -> str:
        return "Language Attribute"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the language attribute test"""
        soup = content.rendered_soup or content.static_soup
        html_tag = soup.find('html')
        
        if html_tag and html_tag.get('lang'):
            return [TestResult(
                url=content.url,
                test_id='lang_attribute',
                test_name='Language Attribute',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='High',
                issue_description='HTML lang attribute is set',
                recommendation='Continue maintaining proper lang attribute',
                score=f'Lang: {html_tag["lang"]}'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='lang_attribute',
                test_name='Language Attribute',
                category='Accessibility',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Missing HTML lang attribute',
                recommendation='Add lang attribute to HTML element for accessibility',
                score='No lang attribute'
            )
    
