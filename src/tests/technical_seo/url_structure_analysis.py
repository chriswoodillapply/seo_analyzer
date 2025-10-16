#!/usr/bin/env python3
"""
URL Structure Quality Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class UrlStructureAnalysisTest(SEOTest):
    """Test for url structure quality"""
    
    @property
    def test_id(self) -> str:
        return "url_structure_analysis"
    
    @property
    def test_name(self) -> str:
        return "URL Structure Quality"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the url structure quality test"""
        from urllib.parse import urlparse
        
        parsed = urlparse(content.url)
        path = parsed.path
        
        # Analyze URL characteristics
        issues = []
        url_length = len(content.url)
        
        if url_length > 100:
            issues.append(f'Long URL ({url_length} chars)')
        
        if '_' in path:
            issues.append('Underscores in URL (hyphens preferred)')
        
        if path.count('/') > 5:
            issues.append('Deep URL structure')
        
        if any(char in path for char in ['%', '&', '=', '?']) and parsed.query:
            issues.append('Special characters in path')
        
        # Check for descriptive words
        path_parts = [p for p in path.split('/') if p and not p.isdigit()]
        if len(path_parts) == 0:
            issues.append('No descriptive words in URL')
        
        if not issues:
            return [TestResult(
                url=content.url,
                test_id='url_structure_analysis',
                test_name='URL Structure Quality',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='URL structure is SEO-friendly',
                recommendation='Continue using clean, descriptive URLs',
                score='Well structured'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='url_structure_analysis',
                test_name='URL Structure Quality',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'URL structure issues: {", ".join(issues[:3])}',
                recommendation='Use short, descriptive URLs with hyphens',
                score=f'{len(issues)} issue(s)'
            )
    
