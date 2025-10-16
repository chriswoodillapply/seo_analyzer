#!/usr/bin/env python3
"""
Header Hierarchy Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class HeaderHierarchyTest(SEOTest):
    """Test for header hierarchy"""
    
    @property
    def test_id(self) -> str:
        return "header_hierarchy"
    
    @property
    def test_name(self) -> str:
        return "Header Hierarchy"
    
    @property
    def category(self) -> str:
        return TestCategory.HEADER_STRUCTURE
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the header hierarchy test"""
        soup = content.rendered_soup or content.static_soup
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headers:
            return TestResult(
                url=content.url,
                test_id='header_hierarchy',
                test_name='Header Hierarchy',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No header tags found',
                recommendation='Add proper header structure for content organization',
                score='No headers'
            )
        
        # Check for proper hierarchy
        header_levels = [int(h.name[1]) for h in headers]
        has_h1 = 1 in header_levels
        
        if has_h1:
            return TestResult(
                url=content.url,
                test_id='header_hierarchy',
                test_name='Header Hierarchy',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Found proper header structure with {len(headers)} headers',
                recommendation='Maintain logical header hierarchy',
                score=f'{len(headers)} total headers'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='header_hierarchy',
                test_name='Header Hierarchy',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Header hierarchy missing H1',
                recommendation='Add H1 tag for proper content structure',
                score=f'{len(headers)} headers without H1'
            )
    
