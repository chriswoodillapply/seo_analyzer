#!/usr/bin/env python3
"""
Thin Content Detection Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ThinContentDetectionTest(SEOTest):
    """Test for thin/boilerplate content detection"""
    
    @property
    def test_id(self) -> str:
        return "thin_content_detection"
    
    @property
    def test_name(self) -> str:
        return "Thin Content Detection"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    @property
    def requires_site_context(self) -> bool:
        return True
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the thin content detection test"""
        
        # Basic word count check (works without crawl context)
        soup = content.rendered_soup or content.static_soup
        text = soup.get_text()
        words = len([w for w in text.split() if len(w) > 2])
        
        # If no crawl context, do basic check only
        if not crawl_context:
            if words < 300:
                return TestResult(
                    url=content.url,
                    test_id=self.test_id,
                    test_name=self.test_name,
                    category=self.category,
                    status=TestStatus.WARNING,
                    severity=self.severity,
                    issue_description=f'Thin content: {words} words (site-wide analysis requires crawl)',
                    recommendation='Aim for 300+ unique words. Run with --crawl for duplicate detection',
                    score=f'{words} words'
                )
            else:
                return TestResult(
                    url=content.url,
                    test_id=self.test_id,
                    test_name=self.test_name,
                    category=self.category,
                    status=TestStatus.PASS,
                    severity=self.severity,
                    issue_description=f'Sufficient content: {words} words',
                    recommendation='Continue providing valuable content',
                    score=f'{words} words'
                )
        
        # With crawl context, check for duplicate/boilerplate content
        # This is a simplified version - could use content hashing for better detection
        similar_pages = []
        if crawl_context.content_hashes:
            # Find pages with similar word counts (±50 words) as a proxy for duplicates
            for url, metadata in crawl_context.all_pages.items():
                if url != content.url and abs(metadata.word_count - words) < 50:
                    similar_pages.append(url)
        
        duplicate_count = len(similar_pages)
        
        if words < 200:
            status = TestStatus.FAIL
            issue = f'Very thin content: {words} words'
            recommendation = 'Add substantial unique content (aim for 500+ words)'
        elif words < 300:
            status = TestStatus.WARNING
            issue = f'Thin content: {words} words'
            recommendation = 'Expand content to 300+ words with unique value'
        elif duplicate_count > 5:
            status = TestStatus.WARNING
            issue = f'Potential duplicate content: {duplicate_count} similar pages found'
            recommendation = 'Ensure each page has unique, valuable content'
        else:
            status = TestStatus.PASS
            issue = f'Good content length: {words} words'
            recommendation = 'Continue providing substantial unique content'
        
        return TestResult(
            url=content.url,
            test_id=self.test_id,
            test_name=self.test_name,
            category=self.category,
            status=status,
            severity=self.severity,
            issue_description=issue,
            recommendation=recommendation,
            score=f'{words} words, {duplicate_count} similar pages'
        )
