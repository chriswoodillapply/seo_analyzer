#!/usr/bin/env python3
"""
Pagination Tags Test
"""

from typing import Optional, List, TYPE_CHECKING
import re
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class PaginationTagsTest(SEOTest):
    """Test for pagination tags"""
    
    @property
    def test_id(self) -> str:
        return "pagination_tags"
    
    @property
    def test_name(self) -> str:
        return "Pagination Tags"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the pagination tags test"""
        soup = content.rendered_soup or content.static_soup
        rel_prev = soup.find('link', attrs={'rel': 'prev'})
        rel_next = soup.find('link', attrs={'rel': 'next'})
        
        is_paginated = bool(re.search(r'[?&]page=|[?&]p=|/page/\d+', content.url))
        
        if rel_prev or rel_next:
            tags_found = []
            if rel_prev:
                tags_found.append('prev')
            if rel_next:
                tags_found.append('next')
            
            return [TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Pagination tags present: {", ".join(tags_found)}',
                recommendation='Continue using rel=prev/next for paginated content',
                score=f'{len(tags_found)} tag(s)'
            )
        elif is_paginated:
            return [TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Paginated URL but no rel=prev/next tags',
                recommendation='Add rel=prev/next tags to help search engines understand pagination',
                score='Missing pagination tags'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='No pagination detected',
                recommendation='N/A - Not a paginated page',
                score='Not applicable'
            )
    
