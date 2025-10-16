#!/usr/bin/env python3
"""
Potentially Oversized Images Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class OversizedImagesTest(SEOTest):
    """Test for potentially oversized images"""
    
    @property
    def test_id(self) -> str:
        return "oversized_images"
    
    @property
    def test_name(self) -> str:
        return "Potentially Oversized Images"
    
    @property
    def category(self) -> str:
        return TestCategory.IMAGES
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the potentially oversized images test"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img', src=True)
        
        if not images:
            return []
        
        # Look for images without optimization indicators
        potentially_large = []
        for img in images:
            src = img.get('src', '')
            # Check for lack of optimization indicators
            if not any(indicator in src.lower() for indicator in ['thumb', 'small', 'compressed', 'optimized', 'webp', 'avif']):
                # Check if it's a full-size image indicator
                if any(size in src.lower() for size in ['full', 'original', 'large', 'hires', 'hi-res']):
                    potentially_large.append(src[:50])
        
        if len(potentially_large) > 0:
            return [TestResult(
                url=content.url,
                test_id='img_oversized_files',
                test_name='Potentially Oversized Images',
                category='Images',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'{len(potentially_large)} potentially oversized images detected',
                recommendation='Optimize and compress images to improve page load speed',
                score=f'{len(potentially_large)} potentially large'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='img_oversized_files',
                test_name='Potentially Oversized Images',
                category='Images',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No obvious oversized images detected',
                recommendation='Continue optimizing images for web delivery',
                score='Images appear optimized'
            )
    
