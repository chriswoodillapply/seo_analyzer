#!/usr/bin/env python3
"""
Content Word Count Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ContentWordCountTest(SEOTest):
    """Test for content word count"""
    
    @property
    def test_id(self) -> str:
        return "content_word_count"
    
    @property
    def test_name(self) -> str:
        return "Content Word Count"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the content word count test"""
        soup = content.rendered_soup or content.static_soup
        text = soup.get_text()
        words = len(text.split())
        
        if words >= 300:
            return TestResult(
                url=content.url,
                test_id='content_word_count',
                test_name='Content Word Count',
                category='Content',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Page has sufficient content ({words} words)',
                recommendation='Continue providing comprehensive content',
                score=f'{words} words'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='content_word_count',
                test_name='Content Word Count',
                category='Content',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Thin content detected ({words} words)',
                recommendation='Add more valuable content (target 300+ words)',
                score=f'{words} words'
            )
    
