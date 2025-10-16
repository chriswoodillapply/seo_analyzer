#!/usr/bin/env python3
"""
Mobile Font Sizes Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class MobileFontSizesTest(SEOTest):
    """Test for mobile font sizes"""
    
    @property
    def test_id(self) -> str:
        return "mobile_font_sizes"
    
    @property
    def test_name(self) -> str:
        return "Mobile Font Sizes"
    
    @property
    def category(self) -> str:
        return TestCategory.MOBILE_USABILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the mobile font sizes test"""
        if not content.rendered_soup:
            return TestResult(
                url=content.url,
                test_id='mobile_font_sizes',
                test_name='Mobile Font Sizes',
                category='Mobile Usability',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='Font size check requires JavaScript rendering',
                recommendation='Enable JavaScript rendering for mobile checks',
                score='Not measured'
            )
        
        return TestResult(
            url=content.url,
            test_id='mobile_font_sizes',
            test_name='Mobile Font Sizes',
            category='Mobile Usability',
            status=TestStatus.INFO,
            severity='Medium',
            issue_description='Mobile font size check requires CSS analysis',
            recommendation='Ensure minimum 16px font size for mobile readability',
            score='Manual check required'
        )
    
    # =========================================================================
    # SECURITY TESTS
    # =========================================================================
    
