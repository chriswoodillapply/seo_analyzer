#!/usr/bin/env python3
"""
Cumulative Layout Shift (CLS) Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ClsTest(SEOTest):
    """Test for cumulative layout shift (cls)"""
    
    @property
    def test_id(self) -> str:
        return "cls"
    
    @property
    def test_name(self) -> str:
        return "Cumulative Layout Shift (CLS)"
    
    @property
    def category(self) -> str:
        return TestCategory.CORE_WEB_VITALS
    
    @property
    def severity(self) -> str:
        return TestSeverity.CRITICAL
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the cumulative layout shift (cls) test"""
        if not content.core_web_vitals or 'cls' not in content.core_web_vitals:
            return [TestResult(
                url=content.url,
                test_id='cumulative_layout_shift',
                test_name='Cumulative Layout Shift (CLS)',
                category='Core Web Vitals',
                status=TestStatus.INFO,
                severity='Critical',
                issue_description='CLS measurement not available',
                recommendation='Enable JavaScript rendering for Core Web Vitals',
                score='Not measured'
            )
        
        cls = content.core_web_vitals['cls']
        
        if cls <= 0.1:
            status = TestStatus.PASS
            issue = f'CLS is good ({cls:.3f})'
            recommendation = 'Visual stability is excellent'
        elif cls <= 0.25:
            status = TestStatus.WARNING
            issue = f'CLS needs improvement ({cls:.3f})'
            recommendation = 'Reduce layout shifts by reserving space for dynamic content'
        else:
            status = TestStatus.FAIL
            issue = f'CLS is poor ({cls:.3f})'
            recommendation = 'Significantly reduce layout shifts for better user experience'
        
        return [TestResult(
            url=content.url,
            test_id='cumulative_layout_shift',
            test_name='Cumulative Layout Shift (CLS)',
            category='Core Web Vitals',
            status=status,
            severity='Critical',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{cls:.3f}'
        )
    
