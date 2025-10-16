#!/usr/bin/env python3
"""
Heading Accessibility Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class HeadingAccessibilityGapsTest(SEOTest):
    """Test for heading accessibility"""
    
    @property
    def test_id(self) -> str:
        return "heading_accessibility_gaps"
    
    @property
    def test_name(self) -> str:
        return "Heading Accessibility"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the heading accessibility test"""
        soup = content.rendered_soup or content.static_soup
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headers:
            return [TestResult(
                url=content.url,
                test_id='heading_accessibility_gaps',
                test_name='Heading Accessibility',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No heading structure found',
                recommendation='Add proper heading hierarchy for screen reader navigation',
                score='No headings'
            )
        
        header_levels = [int(h.name[1]) for h in headers]
        
        # Check if starts with H1
        if header_levels[0] != 1:
            return [TestResult(
                url=content.url,
                test_id='heading_accessibility_gaps',
                test_name='Heading Accessibility',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Heading structure does not start with H1 (starts with H{header_levels[0]})',
                recommendation='Begin heading hierarchy with H1 for accessibility',
                score='Missing H1 first'
            )
        
        # Check for gaps
        gaps = []
        for i in range(len(header_levels) - 1):
            if header_levels[i + 1] > header_levels[i] + 1:
                gaps.append(f'H{header_levels[i]}→H{header_levels[i+1]}')
        
        if not gaps:
            return [TestResult(
                url=content.url,
                test_id='heading_accessibility_gaps',
                test_name='Heading Accessibility',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Proper heading hierarchy for screen readers',
                recommendation='Continue maintaining sequential heading levels',
                score='Proper hierarchy'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='heading_accessibility_gaps',
                test_name='Heading Accessibility',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Heading gaps affect screen reader navigation: {", ".join(gaps)}',
                recommendation='Use sequential heading levels (H1→H2→H3) for accessibility',
                score=f'{len(gaps)} gap(s)'
            )
    
