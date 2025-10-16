#!/usr/bin/env python3
"""
Responsive Images Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ResponsiveImagesSrcsetTest(SEOTest):
    """Test for responsive images"""
    
    @property
    def test_id(self) -> str:
        return "responsive_images_srcset"
    
    @property
    def test_name(self) -> str:
        return "Responsive Images"
    
    @property
    def category(self) -> str:
        return TestCategory.IMAGES
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the responsive images test"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        picture_elements = soup.find_all('picture')
        
        if not images:
            return None
        
        images_with_srcset = [img for img in images if img.get('srcset')]
        responsive_count = len(images_with_srcset) + len(picture_elements)
        
        if responsive_count > 0:
            return TestResult(
                url=content.url,
                test_id='img_responsive_srcset',
                test_name='Responsive Images',
                category='Images',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{responsive_count} responsive image implementations found',
                recommendation='Continue using srcset/picture for different screen sizes',
                score=f'{responsive_count} responsive images'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_responsive_srcset',
                test_name='Responsive Images',
                category='Images',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No responsive images detected',
                recommendation='Implement srcset or picture elements for better mobile performance',
                score='No srcset/picture'
            )
    
    # =========================================================================
    # ADDITIONAL LINK TESTS - PHASE 1
    # =========================================================================
    
