#!/usr/bin/env python3
"""
Touch Target Sizes Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class TouchTargetSizesTest(SEOTest):
    """Test for minimum touch target sizes (mobile usability)"""
    
    @property
    def test_id(self) -> str:
        return "touch_target_sizes"
    
    @property
    def test_name(self) -> str:
        return "Touch Target Sizes"
    
    @property
    def category(self) -> str:
        return TestCategory.MOBILE_USABILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the touch target sizes test"""
        
        soup = content.rendered_soup or content.static_soup
        
        # Find interactive elements
        interactive_selectors = ['a', 'button', 'input', 'select', 'textarea']
        interactive_elements = []
        
        for selector in interactive_selectors:
            elements = soup.find_all(selector)
            interactive_elements.extend(elements)
        
        if not interactive_elements:
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='No interactive elements found',
                recommendation='N/A',
                score='0 interactive elements'
            )
        
        # Check for elements with explicit size attributes
        # (Full implementation would need browser to get computed dimensions)
        small_targets = []
        checked_count = 0
        
        for element in interactive_elements[:50]:  # Check first 50 elements
            # Check for explicit width/height in style
            style = element.get('style', '')
            if style:
                # Simple check for small explicit sizes
                if 'width' in style.lower() or 'height' in style.lower():
                    if any(size in style for size in ['width:2', 'width:3', 'height:2', 'height:3', 
                                                       'width: 2', 'width: 3', 'height: 2', 'height: 3']):
                        small_targets.append(element.name)
            checked_count += 1
        
        # This is a basic check - full implementation would use Playwright to measure actual rendered sizes
        if len(small_targets) > 0:
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.WARNING,
                severity=self.severity,
                issue_description=f'Found {len(small_targets)} potentially small touch targets',
                recommendation='Ensure interactive elements are minimum 48x48px (WCAG 2.5.5)',
                score=f'{len(small_targets)}/{checked_count} may be too small'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.PASS,
                severity=self.severity,
                issue_description=f'No obviously undersized touch targets found in {checked_count} elements',
                recommendation='Continue following mobile touch target guidelines',
                score=f'{checked_count} elements checked'
            )
