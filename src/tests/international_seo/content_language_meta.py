#!/usr/bin/env python3
"""
Content Language Test
"""

from typing import Optional, TYPE_CHECKING
import re
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ContentLanguageMetaTest(SEOTest):
    """Test for content language"""
    
    @property
    def test_id(self) -> str:
        return "content_language_meta"
    
    @property
    def test_name(self) -> str:
        return "Content Language"
    
    @property
    def category(self) -> str:
        return TestCategory.INTERNATIONAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the content language test"""
        headers = content.static_headers
        soup = content.rendered_soup or content.static_soup
        
        # Check HTTP header
        http_lang = headers.get('Content-Language', '')
        
        # Check HTML lang attribute
        html_tag = soup.find('html')
        html_lang = html_tag.get('lang') if html_tag else ''
        
        # Check meta tag
        meta_lang = soup.find('meta', attrs={'http-equiv': re.compile(r'content-language', re.I)})
        
        if http_lang or html_lang:
            return TestResult(
                url=content.url,
                test_id='content_language_meta',
                test_name='Content Language',
                category='International SEO',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Language specified: {html_lang or http_lang}',
                recommendation='Continue specifying content language',
                score=html_lang or http_lang
            )
        else:
            return TestResult(
                url=content.url,
                test_id='content_language_meta',
                test_name='Content Language',
                category='International SEO',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='No language specification found',
                recommendation='Add lang attribute to HTML tag',
                score='No language specified'
            )
    
    # =========================================================================
    # PHASE 4 TESTS - INFO/PLACEHOLDER IMPLEMENTATIONS
    # =========================================================================
    
