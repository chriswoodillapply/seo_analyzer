#!/usr/bin/env python3
"""
Image Alt Text Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ImageAltTextTest(SEOTest):
    """Test for image alt text"""
    
    @property
    def test_id(self) -> str:
        return "image_alt_text"
    
    @property
    def test_name(self) -> str:
        return "Image Alt Text"
    
    @property
    def category(self) -> str:
        return TestCategory.IMAGES
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the image alt text test"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return TestResult(
                url=content.url,
                test_id='img_alt_text',
                test_name='Image Alt Text',
                category='Images',
                status=TestStatus.INFO,
                severity='High',
                issue_description='No images found on page',
                recommendation='N/A - No images present',
                score='0 images'
            )
        
        missing_alt = [img for img in images if not img.get('alt')]
        
        if len(missing_alt) == 0:
            return TestResult(
                url=content.url,
                test_id='img_alt_text',
                test_name='Image Alt Text',
                category='Images',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'All {len(images)} images have alt text',
                recommendation='Continue providing descriptive alt text',
                score=f'{len(images)}/{len(images)} images with alt'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_alt_text',
                test_name='Image Alt Text',
                category='Images',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{len(missing_alt)} of {len(images)} images missing alt text',
                recommendation='Add descriptive alt text to all images for accessibility',
                score=f'{len(images)-len(missing_alt)}/{len(images)} images with alt'
            )
    
