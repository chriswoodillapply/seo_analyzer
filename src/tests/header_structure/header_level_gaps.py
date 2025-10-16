#!/usr/bin/env python3
"""
Header Level Gaps Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class HeaderLevelGapsTest(SEOTest):
    """Test for header level gaps"""
    
    @property
    def test_id(self) -> str:
        return "header_level_gaps"
    
    @property
    def test_name(self) -> str:
        return "Header Level Gaps"
    
    @property
    def category(self) -> str:
        return TestCategory.HEADER_STRUCTURE
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the header level gaps test"""
        soup = content.rendered_soup or content.static_soup
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headers:
            return []
        
        header_levels = [int(h.name[1]) for h in headers]
        
        gaps = []
        for i in range(len(header_levels) - 1):
            current = header_levels[i]
            next_level = header_levels[i + 1]
            
            if next_level > current + 1:
                gaps.append(f'H{current} → H{next_level}')
        
        if not gaps:
            return [TestResult(
                url=content.url,
                test_id='header_level_gaps',
                test_name='Header Level Gaps',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No header level gaps detected',
                recommendation='Continue maintaining proper header hierarchy',
                score='No gaps'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='header_level_gaps',
                test_name='Header Level Gaps',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Header level gaps found: {", ".join(gaps)}',
                recommendation='Use sequential header levels (H1→H2→H3) for proper document structure',
                score=f'{len(gaps)} gap(s)'
            )
    
    # =========================================================================
    # ADDITIONAL IMAGE TESTS - PHASE 1
    # =========================================================================
    
