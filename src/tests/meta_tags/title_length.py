#!/usr/bin/env python3
"""
Title Length Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class TitleLengthTest(SEOTest):
    """Test for title length"""
    
    @property
    def test_id(self) -> str:
        return "title_length"
    
    @property
    def test_name(self) -> str:
        return "Title Length"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the title length test"""
        soup = content.rendered_soup or content.static_soup
        title = soup.find('title')
        
        if not title:
            return None
        
        title_text = title.text.strip()
        length = len(title_text)
        
        # Estimate pixel width (rough calculation)
        pixel_width = length * 10  # Approximate
        
        if 30 <= length <= 60:
            status = TestStatus.PASS
            issue = f'Title length is optimal ({length} characters, ~{pixel_width}px)'
            recommendation = 'Title length is well optimized'
        elif length < 30:
            status = TestStatus.WARNING
            issue = f'Title is too short ({length} characters)'
            recommendation = 'Expand title to 30-60 characters for better SEO'
        else:
            status = TestStatus.WARNING
            issue = f'Title is too long ({length} characters, ~{pixel_width}px)'
            recommendation = 'Shorten title to prevent truncation in search results'
        
        return TestResult(
            url=content.url,
            test_id='meta_title_length',
            test_name='Title Length',
            category='Meta Tags',
            status=status,
            severity='High',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{length} chars / ~{pixel_width}px'
        )
    
