#!/usr/bin/env python3
"""
Web Font Optimization Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class WebFontOptimizationTest(SEOTest):
    """Test for web font optimization"""
    
    @property
    def test_id(self) -> str:
        return "web_font_optimization"
    
    @property
    def test_name(self) -> str:
        return "Web Font Optimization"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the web font optimization test"""
        soup = content.rendered_soup or content.static_soup
        
        # Check for preconnect to font providers
        preconnects = soup.find_all('link', rel='preconnect')
        font_preconnect = any('fonts.' in str(link.get('href', '')) for link in preconnects)
        
        # Check for preload of fonts
        preloads = soup.find_all('link', rel='preload', as_='font')
        
        # Check stylesheets for font-display property (would need CSS parsing)
        # For now, just check if fonts are being loaded
        font_links = [link for link in soup.find_all('link', href=True) 
                     if 'fonts.' in link.get('href', '') or '.woff' in link.get('href', '')]
        
        optimizations_found = []
        if font_preconnect:
            optimizations_found.append('preconnect')
        if preloads:
            optimizations_found.append('preload')
        
        if not font_links:
            return []  # No fonts, no need to check
        
        if len(optimizations_found) >= 1:
            return [TestResult(
                url=content.url,
                test_id='web_font_optimization',
                test_name='Web Font Optimization',
                category='Performance',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Font optimization detected: {", ".join(optimizations_found)}',
                recommendation='Continue optimizing font loading with preload/preconnect',
                score=f'{len(optimizations_found)} optimization(s)'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='web_font_optimization',
                test_name='Web Font Optimization',
                category='Performance',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='Web fonts found but no optimization detected',
                recommendation='Add font-display: swap and preconnect to font providers',
                score='Not optimized'
            )
    
