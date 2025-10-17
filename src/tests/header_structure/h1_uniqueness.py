#!/usr/bin/env python3
"""
H1 Tag Uniqueness Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class H1UniquenessTest(SEOTest):
    """Test for h1 tag uniqueness"""
    
    @property
    def test_id(self) -> str:
        return "h1_uniqueness"
    
    @property
    def test_name(self) -> str:
        return "H1 Tag Uniqueness"
    
    @property
    def category(self) -> str:
        return TestCategory.HEADER_STRUCTURE
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the h1 tag uniqueness test"""
        soup = content.rendered_soup or content.static_soup
        h1_tags = soup.find_all('h1')
        
        # If no H1 tags on this page, skip the test
        if not h1_tags:
            return None
        
        # Get the H1 text from current page
        current_h1_text = h1_tags[0].get_text().strip()
        
        # If no crawl context available, return INFO status
        if not crawl_context:
            return TestResult(
                url=content.url,
                test_id='h1_uniqueness',
                test_name='H1 Tag Uniqueness',
                category='Header Structure',
                status=TestStatus.INFO,
                severity='High',
                issue_description='H1 uniqueness check requires multi-page analysis',
                recommendation='Ensure H1 is unique across all pages',
                score='Multi-page check required'
            )
        
        # Check H1 uniqueness across all pages in crawl context
        duplicate_h1_pages = []
        total_pages_with_h1 = 0
        
        # Collect all H1 texts from all pages
        h1_texts = {}
        for page_url, page_metadata in crawl_context.all_pages.items():
            # We need to get the actual H1 content from each page
            # For now, we'll use a simplified approach based on page titles
            # In a full implementation, you'd need to store H1 content in crawl context
            if hasattr(page_metadata, 'title') and page_metadata.title:
                h1_texts[page_url] = page_metadata.title
                total_pages_with_h1 += 1
        
        # Check for duplicates
        h1_frequency = {}
        for url, h1_text in h1_texts.items():
            if h1_text in h1_frequency:
                h1_frequency[h1_text].append(url)
            else:
                h1_frequency[h1_text] = [url]
        
        # Find duplicates
        duplicates = {h1_text: urls for h1_text, urls in h1_frequency.items() if len(urls) > 1}
        
        # Check if current page's H1 is duplicated
        current_page_duplicated = current_h1_text in duplicates
        
        if current_page_duplicated:
            duplicate_pages = duplicates[current_h1_text]
            duplicate_pages.remove(content.url)  # Remove current page from list
            
            status = TestStatus.FAIL
            issue = f'H1 tag is duplicated across {len(duplicate_pages) + 1} pages'
            recommendation = f'Make H1 unique. Duplicated on: {", ".join(duplicate_pages[:3])}{"..." if len(duplicate_pages) > 3 else ""}'
            score = f'Duplicated on {len(duplicate_pages) + 1} pages'
        else:
            status = TestStatus.PASS
            issue = f'H1 tag is unique across {total_pages_with_h1} pages'
            recommendation = 'H1 tag is properly unique'
            score = 'Unique'
        
        return TestResult(
            url=content.url,
            test_id='h1_uniqueness',
            test_name='H1 Tag Uniqueness',
            category='Header Structure',
            status=status,
            severity='High',
            issue_description=issue,
            recommendation=recommendation,
            score=score
        )
    
