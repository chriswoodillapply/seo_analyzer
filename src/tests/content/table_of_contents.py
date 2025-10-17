#!/usr/bin/env python3
"""
Table of Contents Test
"""

from typing import Optional, TYPE_CHECKING
import re
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class TableOfContentsTest(SEOTest):
    """Test for table of contents"""
    
    @property
    def test_id(self) -> str:
        return "table_of_contents"
    
    @property
    def test_name(self) -> str:
        return "Table of Contents"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the table of contents test"""
        soup = content.rendered_soup or content.static_soup
        
        # Look for common TOC patterns
        toc_indicators = soup.find_all(attrs={'class': re.compile(r'(toc|table[-_]of[-_]contents)', re.I)})
        toc_nav = soup.find('nav', attrs={'aria-label': re.compile(r'table of contents', re.I)})
        
        # Also check for lists with many anchor links to headers
        header_ids = [h.get('id') for h in soup.find_all(['h2', 'h3', 'h4']) if h.get('id')]
        toc_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('#') and href[1:] in header_ids:
                toc_links.append(href)
        
        has_toc = len(toc_indicators) > 0 or toc_nav is not None or len(toc_links) >= 3
        
        if has_toc:
            return TestResult(
                url=content.url,
                test_id='table_of_contents',
                test_name='Table of Contents',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='Table of contents detected',
                recommendation='TOC improves UX and may trigger jump-to links in SERPs',
                score='TOC present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='table_of_contents',
                test_name='Table of Contents',
                category='Content',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No table of contents detected',
                recommendation='For long content, add TOC for better navigation',
                score='No TOC'
            )
    
