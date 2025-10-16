#!/usr/bin/env python3
"""
Robots Meta Tag Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class RobotsMetaTest(SEOTest):
    """Test for robots meta tag"""
    
    @property
    def test_id(self) -> str:
        return "robots_meta"
    
    @property
    def test_name(self) -> str:
        return "Robots Meta Tag"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the robots meta tag test"""
        soup = content.rendered_soup or content.static_soup
        robots = soup.find('meta', attrs={'name': 'robots'})
        
        if robots:
            robots_content = robots.get('content', '').lower()
            if 'noindex' in robots_content or 'nofollow' in robots_content:
                return TestResult(
                    url=content.url,
                    test_id='robots_meta_tag',
                    test_name='Robots Meta Tag',
                    category='Meta Tags',
                    status=TestStatus.WARNING,
                    severity='Medium',
                    issue_description=f'Robots tag restricts indexing: {robots_content}',
                    recommendation='Review if this page should be restricted from search engines',
                    score=robots_content
                )
        
        return TestResult(
            url=content.url,
            test_id='robots_meta_tag',
            test_name='Robots Meta Tag',
            category='Meta Tags',
            status=TestStatus.PASS,
            severity='Medium',
            issue_description='Page allows indexing and following',
            recommendation='Continue allowing search engine access',
            score='No restrictions'
        )
    
