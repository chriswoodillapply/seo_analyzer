#!/usr/bin/env python3
"""
Mobile Content Width Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class MobileContentWidthTest(SEOTest):
    """Test for mobile content width"""
    
    @property
    def test_id(self) -> str:
        return "mobile_content_width"
    
    @property
    def test_name(self) -> str:
        return "Mobile Content Width"
    
    @property
    def category(self) -> str:
        return TestCategory.MOBILE_USABILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the mobile content width test"""
        soup = content.rendered_soup or content.static_soup
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        
        if not viewport:
            return [TestResult(
                url=content.url,
                test_id='mobile_content_width',
                test_name='Mobile Content Width',
                category='Mobile Usability',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='No viewport meta tag',
                recommendation='Add viewport meta tag for mobile responsiveness',
                score='No viewport'
            )
        
        viewport_content = viewport.get('content', '').lower()
        
        # Check for proper configuration
        has_width = 'width=device-width' in viewport_content
        has_no_max_scale = 'maximum-scale' not in viewport_content or 'maximum-scale=1' not in viewport_content
        
        if has_width and has_no_max_scale:
            return [TestResult(
                url=content.url,
                test_id='mobile_content_width',
                test_name='Mobile Content Width',
                category='Mobile Usability',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Proper mobile viewport configuration',
                recommendation='Continue maintaining responsive design',
                score='Well configured'
            )
        elif has_width:
            return [TestResult(
                url=content.url,
                test_id='mobile_content_width',
                test_name='Mobile Content Width',
                category='Mobile Usability',
                status=TestStatus.WARNING,
                severity='High',
                issue_description='Viewport configured but may restrict zooming',
                recommendation='Avoid maximum-scale=1 to allow user zooming',
                score='Viewport with restrictions'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='mobile_content_width',
                test_name='Mobile Content Width',
                category='Mobile Usability',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Viewport not properly configured',
                recommendation='Set viewport width=device-width for responsive design',
                score='Misconfigured'
            )
    
