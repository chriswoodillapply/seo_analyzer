#!/usr/bin/env python3
"""
Content Readability Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ContentReadabilityTest(SEOTest):
    """Test for content readability"""
    
    @property
    def test_id(self) -> str:
        return "content_readability"
    
    @property
    def test_name(self) -> str:
        return "Content Readability"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the content readability test"""
        soup = content.rendered_soup or content.static_soup
        text = soup.get_text()
        
        sentences = len([s for s in text.split('.') if s.strip()])
        words = len(text.split())
        
        if sentences > 0:
            avg_sentence_length = words / sentences
            
            if avg_sentence_length <= 20:
                status = TestStatus.PASS
                issue = 'Content has good readability'
                recommendation = 'Continue writing clear, concise content'
            else:
                status = TestStatus.WARNING
                issue = 'Content may be difficult to read'
                recommendation = 'Use shorter sentences for better readability'
            
            return TestResult(
                url=content.url,
                test_id='content_readability',
                test_name='Content Readability',
                category='Content',
                status=status,
                severity='Low',
                issue_description=issue,
                recommendation=recommendation,
                score=f'Avg {avg_sentence_length:.1f} words/sentence'
            )
        
        return None
    
