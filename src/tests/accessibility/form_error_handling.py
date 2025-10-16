#!/usr/bin/env python3
"""
Form Error Handling Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class FormErrorHandlingTest(SEOTest):
    """Test for form error handling"""
    
    @property
    def test_id(self) -> str:
        return "form_error_handling"
    
    @property
    def test_name(self) -> str:
        return "Form Error Handling"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the form error handling test"""
        soup = content.rendered_soup or content.static_soup
        forms = soup.find_all('form')
        
        if not forms:
            return []
        
        inputs_with_aria = 0
        total_inputs = 0
        
        for form in forms:
            inputs = form.find_all(['input', 'select', 'textarea'])
            total_inputs += len(inputs)
            
            for input_elem in inputs:
                if input_elem.get('aria-describedby') or input_elem.get('aria-invalid') or input_elem.get('aria-errormessage'):
                    inputs_with_aria += 1
        
        if total_inputs == 0:
            return []
        
        percentage = (inputs_with_aria / total_inputs) * 100 if total_inputs else 0
        
        if percentage >= 50:
            return [TestResult(
                url=content.url,
                test_id='form_error_handling',
                test_name='Form Error Handling',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Forms have accessibility attributes ({percentage:.0f}%)',
                recommendation='Continue providing accessible form error handling',
                score=f'{percentage:.0f}% accessible'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='form_error_handling',
                test_name='Form Error Handling',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Limited form accessibility ({percentage:.0f}%)',
                recommendation='Add aria-describedby and aria-invalid for form error handling',
                score=f'{percentage:.0f}% accessible'
            )
    
