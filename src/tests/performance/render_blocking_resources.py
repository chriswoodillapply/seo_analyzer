#!/usr/bin/env python3
"""
Render-Blocking Resources Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class RenderBlockingResourcesTest(SEOTest):
    """Test for render-blocking resources"""
    
    @property
    def test_id(self) -> str:
        return "render_blocking_resources"
    
    @property
    def test_name(self) -> str:
        return "Render-Blocking Resources"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the render-blocking resources test"""
        soup = content.rendered_soup or content.static_soup
        
        # Count render-blocking scripts and stylesheets
        blocking_scripts = [s for s in soup.find_all('script', src=True) 
                           if s.parent.name == 'head' and not s.get('async') and not s.get('defer')]
        
        blocking_styles = soup.find_all('link', rel='stylesheet')
        non_blocking_styles = [s for s in blocking_styles 
                               if s.get('media') and s.get('media') != 'all' and s.get('media') != 'screen']
        
        actual_blocking_styles = len(blocking_styles) - len(non_blocking_styles)
        total_blocking = len(blocking_scripts) + actual_blocking_styles
        
        if total_blocking == 0:
            return TestResult(
                url=content.url,
                test_id='render_blocking_resources',
                test_name='Render-Blocking Resources',
                category='Performance',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No render-blocking resources detected',
                recommendation='Excellent - all resources are async or deferred',
                score='0 blocking resources'
            )
        elif total_blocking <= 3:
            return TestResult(
                url=content.url,
                test_id='render_blocking_resources',
                test_name='Render-Blocking Resources',
                category='Performance',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'{total_blocking} render-blocking resources found',
                recommendation='Consider async/defer for scripts, critical CSS inline',
                score=f'{total_blocking} blocking'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='render_blocking_resources',
                test_name='Render-Blocking Resources',
                category='Performance',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{total_blocking} render-blocking resources (scripts: {len(blocking_scripts)}, styles: {actual_blocking_styles})',
                recommendation='Significantly reduce render-blocking resources for better FCP/LCP',
                score=f'{total_blocking} blocking'
            )
    
