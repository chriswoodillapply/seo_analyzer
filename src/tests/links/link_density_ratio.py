#!/usr/bin/env python3
"""
Link Density Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class LinkDensityRatioTest(SEOTest):
    """Test for link density"""
    
    @property
    def test_id(self) -> str:
        return "link_density_ratio"
    
    @property
    def test_name(self) -> str:
        return "Link Density"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the link density test"""
        soup = content.rendered_soup or content.static_soup
        body = soup.find('body')
        if not body:
            return None
        
        total_text = body.get_text()
        total_text_length = len(total_text.strip())
        
        links = soup.find_all('a')
        link_text_length = sum(len(link.get_text().strip()) for link in links)
        
        if total_text_length == 0:
            return None
        
        link_density = (link_text_length / total_text_length) * 100
        
        if link_density <= 20:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Link density is {link_density:.1f}%',
                recommendation='Good balance of links to content',
                score=f'{link_density:.1f}%'
            )
        elif link_density <= 40:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Link density is {link_density:.1f}%',
                recommendation='Consider reducing number of links relative to content',
                score=f'{link_density:.1f}%'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.FAIL,
                severity='Low',
                issue_description=f'High link density: {link_density:.1f}%',
                recommendation='Too many links may dilute link value and harm SEO',
                score=f'{link_density:.1f}%'
            )
    
    # =========================================================================
    # ADDITIONAL TECHNICAL SEO TESTS - PHASE 1
    # =========================================================================
    
