#!/usr/bin/env python3
"""
Anchor Text Quality Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class AnchorTextQualityTest(SEOTest):
    """Test for anchor text quality"""
    
    @property
    def test_id(self) -> str:
        return "anchor_text_quality"
    
    @property
    def test_name(self) -> str:
        return "Anchor Text Quality"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the anchor text quality test"""
        soup = content.rendered_soup or content.static_soup
        links = soup.find_all('a', href=True)
        
        generic_anchors = ['click here', 'read more', 'here', 'link', 'more']
        poor_quality = [
            link for link in links
            if link.text.strip().lower() in generic_anchors
        ]
        
        if len(poor_quality) == 0:
            return TestResult(
                url=content.url,
                test_id='anchor_text_quality',
                test_name='Anchor Text Quality',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='All anchor text is descriptive',
                recommendation='Continue using descriptive anchor text',
                score=f'{len(links)} links with good anchor text'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='anchor_text_quality',
                test_name='Anchor Text Quality',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'{len(poor_quality)} links have generic anchor text',
                recommendation='Replace generic anchor text with descriptive, keyword-rich text',
                score=f'{len(poor_quality)}/{len(links)} poor quality'
            )
    
    # =========================================================================
    # CONTENT TESTS
    # =========================================================================
    
