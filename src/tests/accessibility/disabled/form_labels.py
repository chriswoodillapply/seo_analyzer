#!/usr/bin/env python3
"""
Form Labels Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class FormLabelsTest(SEOTest):
    """Test for form labels"""
    
    @property
    def test_id(self) -> str:
        return "form_labels"
    
    @property
    def test_name(self) -> str:
        return "Form Labels"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the form labels test"""
        soup = content.rendered_soup or content.static_soup
        inputs = soup.find_all('input')
        labels = soup.find_all('label')
        
        if not inputs:
            return None
        
        if len(labels) >= len(inputs):
            return TestResult(
                url=content.url,
                test_id='form_labels',
                test_name='Form Labels',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'Form inputs have proper labels',
                recommendation='Continue providing labels for all form inputs',
                score=f'{len(labels)} labels for {len(inputs)} inputs'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='form_labels',
                test_name='Form Labels',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'Some inputs may be missing labels',
                recommendation='Associate labels with all form inputs',
                score=f'{len(labels)} labels for {len(inputs)} inputs'
            )
    
