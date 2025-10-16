#!/usr/bin/env python3
"""
Video Schema Markup Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class VideoSchemaMarkupTest(SEOTest):
    """Test for video schema markup"""
    
    @property
    def test_id(self) -> str:
        return "video_schema_markup"
    
    @property
    def test_name(self) -> str:
        return "Video Schema Markup"
    
    @property
    def category(self) -> str:
        return TestCategory.STRUCTURED_DATA
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the video schema markup test"""
        import json
        soup = content.rendered_soup or content.static_soup
        
        # Check if page has video elements
        videos = soup.find_all(['video', 'iframe'])
        video_iframes = [v for v in videos if v.name == 'iframe' and ('youtube' in str(v.get('src', '')) or 'vimeo' in str(v.get('src', '')))]
        has_video_elements = len(soup.find_all('video')) > 0 or len(video_iframes) > 0
        
        if not has_video_elements:
            return []  # No video, no need to check
        
        # Check for VideoObject schema
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        has_video_schema = False
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if item.get('@type') == 'VideoObject':
                        has_video_schema = True
                        break
            except:
                continue
        
        if has_video_schema:
            return [TestResult(
                url=content.url,
                test_id='video_schema_markup',
                test_name='Video Schema Markup',
                category='Structured Data',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='VideoObject schema found for video content',
                recommendation='Continue using video schema for rich snippets',
                score='Video schema present'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='video_schema_markup',
                test_name='Video Schema Markup',
                category='Structured Data',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Video content found but no VideoObject schema',
                recommendation='Add VideoObject schema to enable video rich snippets',
                score='Missing video schema'
            )
    
