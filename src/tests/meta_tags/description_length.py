#!/usr/bin/env python3
"""
Meta Description Length Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class DescriptionLengthTest(SEOTest):
    """Test for meta description length"""
    
    @property
    def test_id(self) -> str:
        return "description_length"
    
    @property
    def test_name(self) -> str:
        return "Meta Description Length"
    
    @property
    def category(self) -> str:
        return TestCategory.META_TAGS
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the meta description length test"""
        soup = content.rendered_soup or content.static_soup
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc or not meta_desc.get('content'):
            return []
        
        desc_text = meta_desc['content'].strip()
        length = len(desc_text)
        
        if 120 <= length <= 160:
            status = TestStatus.PASS
            issue = f'Description length is optimal ({length} characters)'
            recommendation = 'Description length is well optimized'
        elif length < 120:
            status = TestStatus.WARNING
            issue = f'Description is too short ({length} characters)'
            recommendation = 'Expand description to 120-160 characters'
        else:
            status = TestStatus.WARNING
            issue = f'Description is too long ({length} characters)'
            recommendation = 'Shorten description to prevent truncation in SERPs'
        
        return [TestResult(
            url=content.url,
            test_id='meta_description_length',
            test_name='Meta Description Length',
            category='Meta Tags',
            status=status,
            severity='Medium',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{length} characters'
        )
    
