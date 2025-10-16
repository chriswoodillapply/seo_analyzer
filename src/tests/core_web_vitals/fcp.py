#!/usr/bin/env python3
"""
First Contentful Paint (FCP) Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class FcpTest(SEOTest):
    """Test for first contentful paint (fcp)"""
    
    @property
    def test_id(self) -> str:
        return "fcp"
    
    @property
    def test_name(self) -> str:
        return "First Contentful Paint (FCP)"
    
    @property
    def category(self) -> str:
        return TestCategory.CORE_WEB_VITALS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the first contentful paint (fcp) test"""
        if not content.core_web_vitals or 'fcp' not in content.core_web_vitals:
            return TestResult(
                url=content.url,
                test_id='first_contentful_paint',
                test_name='First Contentful Paint (FCP)',
                category='Core Web Vitals',
                status=TestStatus.INFO,
                severity='High',
                issue_description='FCP measurement not available',
                recommendation='Enable JavaScript rendering for Core Web Vitals',
                score='Not measured'
            )
        
        fcp = content.core_web_vitals['fcp']
        
        if fcp <= 1800:
            status = TestStatus.PASS
            issue = f'FCP is good ({fcp:.0f}ms)'
            recommendation = 'First paint is within recommended threshold'
        elif fcp <= 3000:
            status = TestStatus.WARNING
            issue = f'FCP needs improvement ({fcp:.0f}ms)'
            recommendation = 'Optimize critical rendering path'
        else:
            status = TestStatus.FAIL
            issue = f'FCP is poor ({fcp:.0f}ms)'
            recommendation = 'Significantly optimize initial page rendering'
        
        return TestResult(
            url=content.url,
            test_id='first_contentful_paint',
            test_name='First Contentful Paint (FCP)',
            category='Core Web Vitals',
            status=status,
            severity='High',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{fcp:.0f}ms'
        )
    
    # =========================================================================
    # ACCESSIBILITY TESTS
    # =========================================================================
    
