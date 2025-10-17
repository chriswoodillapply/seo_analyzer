#!/usr/bin/env python3
"""
Semantic HTML5 Elements Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SemanticHtmlTest(SEOTest):
    """Test for semantic html5 elements"""
    
    @property
    def test_id(self) -> str:
        return "semantic_html"
    
    @property
    def test_name(self) -> str:
        return "Semantic HTML5 Elements"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the semantic html5 elements test"""
        soup = content.rendered_soup or content.static_soup
        
        semantic_tags = soup.find_all(['nav', 'main', 'article', 'section', 'aside', 'header', 'footer'])
        
        if len(semantic_tags) >= 3:
            return TestResult(
                url=content.url,
                test_id='semantic_html',
                test_name='Semantic HTML5 Elements',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Page uses {len(semantic_tags)} semantic HTML5 elements',
                recommendation='Continue using semantic elements for better accessibility',
                score=f'{len(semantic_tags)} semantic tags'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='semantic_html',
                test_name='Semantic HTML5 Elements',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Limited use of semantic HTML5 elements',
                recommendation='Use semantic elements (nav, main, article, etc.) instead of divs',
                score=f'{len(semantic_tags)} semantic tags'
            )
    
    # =========================================================================
    # MOBILE TESTS
    # =========================================================================
    
