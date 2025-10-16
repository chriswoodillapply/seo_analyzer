#!/usr/bin/env python3
"""
Duplicate Meta Tags Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class DuplicateMetaTagsTest(SEOTest):
    """Test for duplicate meta tags"""
    
    @property
    def test_id(self) -> str:
        return "duplicate_meta_tags"
    
    @property
    def test_name(self) -> str:
        return "Duplicate Meta Tags"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the duplicate meta tags test"""
        soup = content.rendered_soup or content.static_soup
        titles = soup.find_all('title')
        descriptions = soup.find_all('meta', attrs={'name': 'description'})
        
        issues = []
        if len(titles) > 1:
            issues.append(f'{len(titles)} title tags')
        if len(descriptions) > 1:
            issues.append(f'{len(descriptions)} description tags')
        
        if issues:
            return [TestResult(
                url=content.url,
                test_id='duplicate_meta_tags',
                test_name='Duplicate Meta Tags',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'Duplicate meta tags found: {", ".join(issues)}',
                recommendation='Remove duplicate title/description tags - only one of each allowed',
                score='; '.join(issues)
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='duplicate_meta_tags',
                test_name='Duplicate Meta Tags',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No duplicate meta tags detected',
                recommendation='Continue using single title and description tags',
                score='No duplicates'
            )
    
