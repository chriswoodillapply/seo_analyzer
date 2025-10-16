#!/usr/bin/env python3
"""
Largest Contentful Paint (LCP) Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class LcpTest(SEOTest):
    """Test for largest contentful paint (lcp)"""
    
    @property
    def test_id(self) -> str:
        return "lcp"
    
    @property
    def test_name(self) -> str:
        return "Largest Contentful Paint (LCP)"
    
    @property
    def category(self) -> str:
        return TestCategory.CORE_WEB_VITALS
    
    @property
    def severity(self) -> str:
        return TestSeverity.CRITICAL
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the largest contentful paint (lcp) test"""
        if not content.core_web_vitals or 'lcp' not in content.core_web_vitals:
            return TestResult(
                url=content.url,
                test_id='largest_contentful_paint',
                test_name='Largest Contentful Paint (LCP)',
                category='Core Web Vitals',
                status=TestStatus.INFO,
                severity='Critical',
                issue_description='LCP measurement not available',
                recommendation='Enable JavaScript rendering for Core Web Vitals',
                score='Not measured'
            )
        
        lcp = content.core_web_vitals['lcp']
        
        if lcp <= 2500:
            status = TestStatus.PASS
            issue = f'LCP is good ({lcp:.0f}ms)'
            recommendation = 'LCP is within recommended threshold'
        elif lcp <= 4000:
            status = TestStatus.WARNING
            issue = f'LCP needs improvement ({lcp:.0f}ms)'
            recommendation = 'Optimize largest content element loading'
        else:
            status = TestStatus.FAIL
            issue = f'LCP is poor ({lcp:.0f}ms)'
            recommendation = 'Significantly optimize largest element loading'
        
        return TestResult(
            url=content.url,
            test_id='largest_contentful_paint',
            test_name='Largest Contentful Paint (LCP)',
            category='Core Web Vitals',
            status=status,
            severity='Critical',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{lcp:.0f}ms'
        )
    
