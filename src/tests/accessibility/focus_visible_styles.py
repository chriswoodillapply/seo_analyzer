#!/usr/bin/env python3
"""
Focus Indicators Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class FocusVisibleStylesTest(SEOTest):
    """Test for focus indicators"""
    
    @property
    def test_id(self) -> str:
        return "focus_visible_styles"
    
    @property
    def test_name(self) -> str:
        return "Focus Indicators"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the focus indicators test"""
        soup = content.rendered_soup or content.static_soup
        
        # Look for CSS that might disable focus
        styles = soup.find_all('style')
        outline_none_found = False
        
        for style in styles:
            if style.string and ('outline:none' in style.string.replace(' ', '') or 'outline: none' in style.string):
                outline_none_found = True
                break
        
        if outline_none_found:
            return TestResult(
                url=content.url,
                test_id='focus_visible_styles',
                test_name='Focus Indicators',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='CSS may be removing focus outlines',
                recommendation='If removing outlines, provide alternative focus indicators',
                score='Outline removal detected'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='focus_visible_styles',
                test_name='Focus Indicators',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No obvious focus indicator removal',
                recommendation='Ensure all interactive elements have visible focus state',
                score='Focus styles intact'
            )
    
