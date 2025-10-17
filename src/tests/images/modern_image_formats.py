#!/usr/bin/env python3
"""
Modern Image Formats Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ModernImageFormatsTest(SEOTest):
    """Test for modern image formats"""
    
    @property
    def test_id(self) -> str:
        return "modern_image_formats"
    
    @property
    def test_name(self) -> str:
        return "Modern Image Formats"
    
    @property
    def category(self) -> str:
        return TestCategory.IMAGES
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the modern image formats test"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        picture_sources = soup.find_all('source', attrs={'type': lambda x: x and 'image' in x})
        
        if not images and not picture_sources:
            return None
        
        modern_formats = 0
        
        for img in images:
            src = img.get('src', '')
            srcset = img.get('srcset', '')
            
            if '.webp' in src.lower() or '.avif' in src.lower():
                modern_formats += 1
            elif '.webp' in srcset.lower() or '.avif' in srcset.lower():
                modern_formats += 1
        
        for source in picture_sources:
            type_attr = source.get('type', '').lower()
            if 'webp' in type_attr or 'avif' in type_attr:
                modern_formats += 1
        
        if modern_formats > 0:
            return TestResult(
                url=content.url,
                test_id='img_modern_formats',
                test_name='Modern Image Formats',
                category='Images',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Using modern image formats (WebP/AVIF)',
                recommendation='Continue using modern formats for better performance',
                score=f'{modern_formats} modern format uses'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_modern_formats',
                test_name='Modern Image Formats',
                category='Images',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No modern image formats detected',
                recommendation='Consider using WebP or AVIF for 25-35% better compression',
                score='Using traditional formats'
            )
    
