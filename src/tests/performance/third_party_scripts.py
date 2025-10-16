#!/usr/bin/env python3
"""
Third-Party Scripts Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ThirdPartyScriptsTest(SEOTest):
    """Test for third-party scripts"""
    
    @property
    def test_id(self) -> str:
        return "third_party_scripts"
    
    @property
    def test_name(self) -> str:
        return "Third-Party Scripts"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the third-party scripts test"""
        from urllib.parse import urlparse
        soup = content.rendered_soup or content.static_soup
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        all_scripts = soup.find_all('script', src=True)
        third_party = [s for s in all_scripts 
                      if s['src'].startswith('http') and domain not in s['src']]
        
        if len(third_party) == 0:
            return [TestResult(
                url=content.url,
                test_id='third_party_scripts',
                test_name='Third-Party Scripts',
                category='Performance',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No third-party scripts detected',
                recommendation='Great - minimal external dependencies',
                score='0 third-party scripts'
            )
        elif len(third_party) <= 5:
            return [TestResult(
                url=content.url,
                test_id='third_party_scripts',
                test_name='Third-Party Scripts',
                category='Performance',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description=f'{len(third_party)} third-party scripts found',
                recommendation='Monitor third-party script impact on performance',
                score=f'{len(third_party)} scripts'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='third_party_scripts',
                test_name='Third-Party Scripts',
                category='Performance',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Many third-party scripts ({len(third_party)})',
                recommendation='Reduce third-party scripts or load them asynchronously',
                score=f'{len(third_party)} scripts'
            )
    
