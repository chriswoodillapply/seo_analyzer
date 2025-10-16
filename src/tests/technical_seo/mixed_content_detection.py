#!/usr/bin/env python3
"""
Mixed Content Detection Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class MixedContentDetectionTest(SEOTest):
    """Test for mixed content detection"""
    
    @property
    def test_id(self) -> str:
        return "mixed_content_detection"
    
    @property
    def test_name(self) -> str:
        return "Mixed Content Detection"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the mixed content detection test"""
        if not content.url.startswith('https://'):
            return []
        
        soup = content.rendered_soup or content.static_soup
        insecure_resources = []
        
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            if script['src'].startswith('http://'):
                insecure_resources.append(f'script: {script["src"][:50]}')
        
        stylesheets = soup.find_all('link', rel='stylesheet', href=True)
        for style in stylesheets:
            if style['href'].startswith('http://'):
                insecure_resources.append(f'stylesheet: {style["href"][:50]}')
        
        images = soup.find_all('img', src=True)
        for img in images:
            if img['src'].startswith('http://'):
                insecure_resources.append(f'image: {img["src"][:50]}')
        
        iframes = soup.find_all('iframe', src=True)
        for iframe in iframes:
            if iframe['src'].startswith('http://'):
                insecure_resources.append(f'iframe: {iframe["src"][:50]}')
        
        if not insecure_resources:
            return [TestResult(
                url=content.url,
                test_id='mixed_content_detection',
                test_name='Mixed Content Detection',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No mixed content detected',
                recommendation='All resources loaded securely over HTTPS',
                score='No mixed content'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='mixed_content_detection',
                test_name='Mixed Content Detection',
                category='Technical SEO',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{len(insecure_resources)} HTTP resources on HTTPS page',
                recommendation='Update all resources to use HTTPS to avoid security warnings',
                score=f'{len(insecure_resources)} insecure resources'
            )
    
    # =========================================================================
    # ADDITIONAL PERFORMANCE TESTS - PHASE 1
    # =========================================================================
    
