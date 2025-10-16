#!/usr/bin/env python3
"""
Twitter Card Tags Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class TwitterCardTagsTest(SEOTest):
    """Test for twitter card tags"""
    
    @property
    def test_id(self) -> str:
        return "twitter_card_tags"
    
    @property
    def test_name(self) -> str:
        return "Twitter Card Tags"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the twitter card tags test"""
        soup = content.rendered_soup or content.static_soup
        twitter_tags = {
            'twitter:card': soup.find('meta', attrs={'name': 'twitter:card'}),
            'twitter:site': soup.find('meta', attrs={'name': 'twitter:site'}),
            'twitter:title': soup.find('meta', attrs={'name': 'twitter:title'}),
            'twitter:description': soup.find('meta', attrs={'name': 'twitter:description'}),
            'twitter:image': soup.find('meta', attrs={'name': 'twitter:image'}),
        }
        
        found_tags = {k: v for k, v in twitter_tags.items() if v is not None}
        found_count = len(found_tags)
        
        if found_count >= 3:
            return [TestResult(
                url=content.url,
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Found {found_count}/5 Twitter Card tags',
                recommendation='Continue maintaining Twitter Cards for social sharing',
                score=f'{found_count}/5 tags present'
            )
        elif found_count >= 1:
            return [TestResult(
                url=content.url,
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Incomplete Twitter Card implementation ({found_count}/5)',
                recommendation='Add twitter:card, twitter:title, twitter:description, twitter:image',
                score=f'{found_count}/5 tags present'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No Twitter Card tags found',
                recommendation='Add Twitter Card tags to improve Twitter sharing appearance',
                score='0/5 tags present'
            )
    
