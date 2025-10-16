#!/usr/bin/env python3
"""
Geographic Targeting Test
"""

from typing import Optional, List, TYPE_CHECKING
import re
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class GeoTargetingMetaTest(SEOTest):
    """Test for geographic targeting"""
    
    @property
    def test_id(self) -> str:
        return "geo_targeting_meta"
    
    @property
    def test_name(self) -> str:
        return "Geographic Targeting"
    
    @property
    def category(self) -> str:
        return TestCategory.INTERNATIONAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the geographic targeting test"""
        soup = content.rendered_soup or content.static_soup
        
        geo_tags = soup.find_all('meta', attrs={'name': re.compile(r'^geo\.', re.I)})
        
        if geo_tags:
            tag_names = [tag.get('name') for tag in geo_tags]
            return [TestResult(
                url=content.url,
                test_id='geo_targeting_meta',
                test_name='Geographic Targeting',
                category='International SEO',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Geographic meta tags found: {", ".join(tag_names)}',
                recommendation='Continue using geo tags for local targeting',
                score=f'{len(geo_tags)} geo tags'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='geo_targeting_meta',
                test_name='Geographic Targeting',
                category='International SEO',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No geographic targeting meta tags',
                recommendation='If targeting local areas, add geo.region/geo.placename tags',
                score='No geo tags'
            )
    
