#!/usr/bin/env python3
"""
DOM Complexity Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class DomComplexityTest(SEOTest):
    """Test for dom complexity"""
    
    @property
    def test_id(self) -> str:
        return "dom_complexity"
    
    @property
    def test_name(self) -> str:
        return "DOM Complexity"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the dom complexity test"""
        soup = content.rendered_soup or content.static_soup
        dom_elements = len(soup.find_all())
        
        if dom_elements < 1500:
            status = TestStatus.PASS
            issue = f'DOM has {dom_elements} elements (good)'
            recommendation = 'DOM complexity is well managed'
        elif dom_elements < 3000:
            status = TestStatus.WARNING
            issue = f'DOM has {dom_elements} elements (moderate)'
            recommendation = 'Consider simplifying page structure'
        else:
            status = TestStatus.FAIL
            issue = f'DOM has {dom_elements} elements (excessive)'
            recommendation = 'Reduce DOM complexity for better performance'
        
        return TestResult(
            url=content.url,
            test_id='dom_complexity',
            test_name='DOM Complexity',
            category='Performance',
            status=status,
            severity='Low',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{dom_elements} elements'
        )
    
    # =========================================================================
    # CORE WEB VITALS TESTS
    # =========================================================================
    
