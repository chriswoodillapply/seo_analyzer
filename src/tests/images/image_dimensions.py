#!/usr/bin/env python3
"""
Image Dimensions Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ImageDimensionsTest(SEOTest):
    """Test for image dimensions"""
    
    @property
    def test_id(self) -> str:
        return "image_dimensions"
    
    @property
    def test_name(self) -> str:
        return "Image Dimensions"
    
    @property
    def category(self) -> str:
        return TestCategory.IMAGES
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the image dimensions test"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return []
        
        images_with_dimensions = [
            img for img in images 
            if img.get('width') and img.get('height')
        ]
        
        percentage = (len(images_with_dimensions) / len(images)) * 100 if images else 0
        
        if percentage >= 80:
            return [TestResult(
                url=content.url,
                test_id='img_dimensions_specified',
                test_name='Image Dimensions',
                category='Images',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{len(images_with_dimensions)}/{len(images)} images have dimensions',
                recommendation='Continue specifying image dimensions to prevent layout shifts',
                score=f'{percentage:.1f}% with dimensions'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='img_dimensions_specified',
                test_name='Image Dimensions',
                category='Images',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Only {len(images_with_dimensions)}/{len(images)} images have dimensions',
                recommendation='Add width/height attributes to images to improve CLS (Core Web Vitals)',
                score=f'{percentage:.1f}% with dimensions'
            )
    
