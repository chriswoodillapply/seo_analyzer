#!/usr/bin/env python3
"""
Video Captions Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class VideoCaptionsTest(SEOTest):
    """Test for video captions"""
    
    @property
    def test_id(self) -> str:
        return "video_captions"
    
    @property
    def test_name(self) -> str:
        return "Video Captions"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the video captions test"""
        soup = content.rendered_soup or content.static_soup
        videos = soup.find_all('video')
        
        if not videos:
            return []
        
        videos_with_tracks = 0
        for video in videos:
            tracks = video.find_all('track')
            if tracks:
                videos_with_tracks += 1
        
        if videos_with_tracks == len(videos):
            return [TestResult(
                url=content.url,
                test_id='video_captions',
                test_name='Video Captions',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='High',
                issue_description='All videos have caption tracks',
                recommendation='Continue providing captions for accessibility',
                score=f'{videos_with_tracks}/{len(videos)} captioned'
            )
        elif videos_with_tracks > 0:
            return [TestResult(
                url=content.url,
                test_id='video_captions',
                test_name='Video Captions',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'Only {videos_with_tracks}/{len(videos)} videos have captions',
                recommendation='Add <track> elements with captions for all videos',
                score=f'{videos_with_tracks}/{len(videos)} captioned'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='video_captions',
                test_name='Video Captions',
                category='Accessibility',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Videos found but no captions',
                recommendation='Add caption tracks for WCAG compliance',
                score='0 captioned'
            )
    
