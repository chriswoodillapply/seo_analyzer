#!/usr/bin/env python3
"""
Responsive Image Strategy Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ResponsiveImageStrategyTest(SEOTest):
    """Test for responsive image strategy"""
    
    @property
    def test_id(self) -> str:
        return "responsive_image_strategy"
    
    @property
    def test_name(self) -> str:
        return "Responsive Image Strategy"
    
    @property
    def category(self) -> str:
        return TestCategory.MOBILE_USABILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the responsive image strategy test"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return []
        
        with_srcset = len([img for img in images if img.get('srcset')])
        with_sizes = len([img for img in images if img.get('sizes')])
        picture_elements = len(soup.find_all('picture'))
        
        responsive_count = with_srcset + picture_elements
        responsive_percentage = (responsive_count / len(images)) * 100 if images else 0
        
        if responsive_percentage >= 50:
            return [TestResult(
                url=content.url,
                test_id='responsive_image_strategy',
                test_name='Responsive Image Strategy',
                category='Mobile Usability',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Good responsive image implementation ({responsive_percentage:.0f}%)',
                recommendation='Continue using srcset/picture for responsive images',
                score=f'{responsive_percentage:.0f}% responsive'
            )
        elif responsive_count > 0:
            return [TestResult(
                url=content.url,
                test_id='responsive_image_strategy',
                test_name='Responsive Image Strategy',
                category='Mobile Usability',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Partial responsive images ({responsive_percentage:.0f}%)',
                recommendation='Implement srcset for more images to serve appropriate sizes',
                score=f'{responsive_percentage:.0f}% responsive'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='responsive_image_strategy',
                test_name='Responsive Image Strategy',
                category='Mobile Usability',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No responsive images detected',
                recommendation='Implement responsive images with srcset/picture elements',
                score='Not responsive'
            )
    
