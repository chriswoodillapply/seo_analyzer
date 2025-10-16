#!/usr/bin/env python3
"""
Content Structure Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ContentStructureTest(SEOTest):
    """Test for content structure"""
    
    @property
    def test_id(self) -> str:
        return "content_structure"
    
    @property
    def test_name(self) -> str:
        return "Content Structure"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the content structure test"""
        soup = content.rendered_soup or content.static_soup
        
        paragraphs = len(soup.find_all('p'))
        lists = len(soup.find_all(['ul', 'ol']))
        headers = len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
        
        structure_score = paragraphs + lists + headers
        
        if structure_score >= 10:
            return [TestResult(
                url=content.url,
                test_id='content_structure',
                test_name='Content Structure',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='Content is well-structured',
                recommendation='Continue using proper HTML formatting',
                score=f'P:{paragraphs} Lists:{lists} Headers:{headers}'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='content_structure',
                test_name='Content Structure',
                category='Content',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='Limited content structure',
                recommendation='Add more paragraphs, lists, and headers for better structure',
                score=f'P:{paragraphs} Lists:{lists} Headers:{headers}'
            )
    
    # =========================================================================
    # TECHNICAL SEO TESTS
    # =========================================================================
    
