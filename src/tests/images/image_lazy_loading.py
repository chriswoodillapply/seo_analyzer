#!/usr/bin/env python3
"""
Image Lazy Loading Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ImageLazyLoadingTest(SEOTest):
    """Test for image lazy loading"""
    
    @property
    def test_id(self) -> str:
        return "image_lazy_loading"
    
    @property
    def test_name(self) -> str:
        return "Image Lazy Loading"
    
    @property
    def category(self) -> str:
        return TestCategory.IMAGES
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the image lazy loading test"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return []
        
        lazy_images = [img for img in images if img.get('loading') == 'lazy']
        
        if len(lazy_images) > 0:
            return [TestResult(
                url=content.url,
                test_id='img_lazy_loading',
                test_name='Image Lazy Loading',
                category='Images',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'{len(lazy_images)} of {len(images)} images use lazy loading',
                recommendation='Consider lazy loading for below-fold images',
                score=f'{len(lazy_images)}/{len(images)} lazy loaded'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='img_lazy_loading',
                test_name='Image Lazy Loading',
                category='Images',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No images use lazy loading',
                recommendation='Implement lazy loading for below-fold images to improve performance',
                score='0 lazy loaded images'
            )
    
    # =========================================================================
    # LINK TESTS
    # =========================================================================
    
