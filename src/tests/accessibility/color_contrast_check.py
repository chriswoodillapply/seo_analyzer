#!/usr/bin/env python3
"""
Color Contrast Check Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ColorContrastCheckTest(SEOTest):
    """Test for WCAG color contrast ratios"""
    
    @property
    def test_id(self) -> str:
        return "color_contrast_check"
    
    @property
    def test_name(self) -> str:
        return "Color Contrast"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the color contrast check test"""
        
        soup = content.rendered_soup or content.static_soup
        
        # Check for inline styles with color definitions
        # Full implementation would need browser to get computed styles
        elements_with_color = []
        potential_issues = []
        
        # Find elements with inline color styles
        for element in soup.find_all(style=True):
            style = element.get('style', '').lower()
            if 'color:' in style or 'background' in style:
                elements_with_color.append(element)
                
                # Very basic check for potentially low contrast combinations
                # (light gray text, white backgrounds, etc.)
                if any(x in style for x in ['color:#eee', 'color:#ddd', 'color:#ccc', 
                                            'color:#f', 'color: #f', 'color:white',
                                            'color: white', 'color:rgb(255']):
                    if 'background' not in style or 'background:#fff' in style or 'background:white' in style:
                        potential_issues.append(element.name)
        
        # Check for common low-contrast color classes
        low_contrast_classes = ['text-gray-300', 'text-gray-400', 'text-light', 'text-muted']
        for class_name in low_contrast_classes:
            elements = soup.find_all(class_=lambda x: x and class_name in str(x))
            if elements:
                potential_issues.extend([e.name for e in elements[:5]])
        
        if len(potential_issues) > 0:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.WARNING,
                severity=self.severity,
                issue_description=f'Found {len(potential_issues)} elements with potentially low contrast',
                recommendation='Check color contrast ratios: 4.5:1 for normal text, 3:1 for large text (WCAG AA)',
                score=f'{len(potential_issues)} potential issues'
            )
        elif len(elements_with_color) > 0:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.PASS,
                severity=self.severity,
                issue_description=f'No obvious contrast issues found in {len(elements_with_color)} styled elements',
                recommendation='Use browser DevTools or axe to verify WCAG compliance',
                score=f'{len(elements_with_color)} elements checked'
            )
        else:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='No inline color styles found (colors may be in CSS)',
                recommendation='Use automated tools like axe or Lighthouse for full contrast analysis',
                score='Manual check recommended'
            )
