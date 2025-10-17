#!/usr/bin/env python3
"""
Title/H1 Keyword Alignment Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class HeaderKeywordOptimizationTest(SEOTest):
    """Test for title/h1 keyword alignment"""
    
    @property
    def test_id(self) -> str:
        return "header_keyword_optimization"
    
    @property
    def test_name(self) -> str:
        return "Title/H1 Keyword Alignment"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the title/h1 keyword alignment test"""
        soup = content.rendered_soup or content.static_soup
        title = soup.find('title')
        h1 = soup.find('h1')
        
        if not title or not h1:
            return None
        
        title_text = title.text.strip().lower()
        h1_text = h1.text.strip().lower()
        
        # Extract words from title (simple approach)
        title_words = set([w for w in title_text.split() if len(w) > 3])
        h1_words = set([w for w in h1_text.split() if len(w) > 3])
        
        if not title_words:
            return None
        
        common_words = title_words.intersection(h1_words)
        overlap_percentage = (len(common_words) / len(title_words)) * 100 if title_words else 0
        
        if overlap_percentage >= 30:
            return TestResult(
                url=content.url,
                test_id='header_keyword_optimization',
                test_name='Title/H1 Keyword Alignment',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Good keyword alignment between title and H1 ({overlap_percentage:.0f}%)',
                recommendation='Continue aligning title and H1 keywords for relevance',
                score=f'{overlap_percentage:.0f}% overlap'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='header_keyword_optimization',
                test_name='Title/H1 Keyword Alignment',
                category='Content',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Low keyword alignment between title and H1 ({overlap_percentage:.0f}%)',
                recommendation='Use similar keywords in title and H1 for better topical relevance',
                score=f'{overlap_percentage:.0f}% overlap'
            )
    
