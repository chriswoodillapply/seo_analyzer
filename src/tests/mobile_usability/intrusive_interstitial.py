#!/usr/bin/env python3
"""
Intrusive Interstitials Test
"""

from typing import Optional, List, TYPE_CHECKING
import re
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class IntrusiveInterstitialTest(SEOTest):
    """Test for intrusive interstitials"""
    
    @property
    def test_id(self) -> str:
        return "intrusive_interstitial"
    
    @property
    def test_name(self) -> str:
        return "Intrusive Interstitials"
    
    @property
    def category(self) -> str:
        return TestCategory.MOBILE_USABILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the intrusive interstitials test"""
        soup = content.rendered_soup or content.static_soup
        
        # Basic check for modal/overlay indicators
        modals = soup.find_all(attrs={'class': re.compile(r'(modal|popup|overlay|interstitial)', re.I)})
        
        if len(modals) > 0:
            return [TestResult(
                url=content.url,
                test_id='intrusive_interstitial',
                test_name='Intrusive Interstitials',
                category='Mobile Usability',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'{len(modals)} potential modal/popup elements found',
                recommendation='Ensure popups are not intrusive on mobile (Google penalty risk)',
                score=f'{len(modals)} potential popups'
            )
        else:
            return [TestResult(
                url=content.url,
                test_id='intrusive_interstitial',
                test_name='Intrusive Interstitials',
                category='Mobile Usability',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No obvious intrusive popups detected',
                recommendation='Continue avoiding intrusive interstitials',
                score='No popups detected'
            )
    
