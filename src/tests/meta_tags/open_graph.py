#!/usr/bin/env python3
"""
Open Graph Tags Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class OpenGraphTest(SEOTest):
    """Test for open graph tags"""
    
    @property
    def test_id(self) -> str:
        return "open_graph"
    
    @property
    def test_name(self) -> str:
        return "Open Graph Tags"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the open graph tags test"""
        soup = content.rendered_soup or content.static_soup
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        
        og_count = sum([bool(og_title), bool(og_desc), bool(og_image)])
        
        if og_count >= 2:
            return [TestResult(
                url=content.url,
                test_id='open_graph_tags',
                test_name='Open Graph Tags',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Found {og_count}/3 recommended Open Graph tags',
                recommendation='Continue maintaining Open Graph tags for social sharing',
                score=f'{og_count}/3 tags present'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='open_graph_tags',
                test_name='Open Graph Tags',
                category='Meta Tags',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Missing Open Graph tags ({og_count}/3 found)',
                recommendation='Add og:title, og:description, and og:image for better social sharing',
                score=f'{og_count}/3 tags present'
            )
    
    # =========================================================================
    # HEADER STRUCTURE TESTS
    # =========================================================================
    
