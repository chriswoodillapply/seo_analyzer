#!/usr/bin/env python3
"""
Multimedia Diversity Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class MultimediaDiversityTest(SEOTest):
    """Test for multimedia diversity"""
    
    @property
    def test_id(self) -> str:
        return "multimedia_diversity"
    
    @property
    def test_name(self) -> str:
        return "Multimedia Diversity"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the multimedia diversity test"""
        soup = content.rendered_soup or content.static_soup
        
        media_types = {
            'images': len(soup.find_all('img')),
            'videos': len(soup.find_all('video')),
            'audio': len(soup.find_all('audio')),
            'iframes': len([i for i in soup.find_all('iframe') if 'youtube' in str(i.get('src', '')) or 'vimeo' in str(i.get('src', ''))])
        }
        
        total_media = sum(media_types.values())
        media_type_count = sum(1 for v in media_types.values() if v > 0)
        
        if media_type_count >= 2:
            return TestResult(
                url=content.url,
                test_id='multimedia_diversity',
                test_name='Multimedia Diversity',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Diverse media types found ({media_type_count} types, {total_media} total)',
                recommendation='Continue using diverse media to engage users',
                score=f'{media_type_count} media types'
            )
        elif media_type_count == 1:
            return TestResult(
                url=content.url,
                test_id='multimedia_diversity',
                test_name='Multimedia Diversity',
                category='Content',
                status=TestStatus.INFO,
                severity='Low',
                issue_description=f'Limited media diversity ({total_media} items of 1 type)',
                recommendation='Consider adding varied media types (images, videos, audio)',
                score='1 media type'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='multimedia_diversity',
                test_name='Multimedia Diversity',
                category='Content',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='No multimedia content found',
                recommendation='Add images, videos, or other media to enhance engagement',
                score='No media'
            )
    
