#!/usr/bin/env python3
"""
Hreflang Validation Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class HreflangValidationTest(SEOTest):
    """Test for hreflang validation"""
    
    @property
    def test_id(self) -> str:
        return "hreflang_validation"
    
    @property
    def test_name(self) -> str:
        return "Hreflang Validation"
    
    @property
    def category(self) -> str:
        return TestCategory.INTERNATIONAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the hreflang validation test"""
        soup = content.rendered_soup or content.static_soup
        hreflang_tags = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
        
        if not hreflang_tags:
            return None
        
        # Check for x-default
        has_x_default = any(tag.get('hreflang') == 'x-default' for tag in hreflang_tags)
        
        # Check for valid language codes (basic validation)
        invalid_codes = []
        for tag in hreflang_tags:
            hreflang = tag.get('hreflang', '')
            if hreflang != 'x-default' and not re.match(r'^[a-z]{2}(-[A-Z]{2})?$', hreflang):
                invalid_codes.append(hreflang)
        
        if has_x_default and not invalid_codes:
            return TestResult(
                url=content.url,
                test_id='hreflang_validation',
                test_name='Hreflang Validation',
                category='International SEO',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Hreflang tags properly implemented with x-default',
                recommendation='Ensure reciprocal hreflang links exist',
                score='Well configured'
            )
        elif invalid_codes:
            return TestResult(
                url=content.url,
                test_id='hreflang_validation',
                test_name='Hreflang Validation',
                category='International SEO',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'Invalid hreflang codes: {", ".join(invalid_codes[:3])}',
                recommendation='Use valid ISO language-country codes (e.g., en-US)',
                score=f'{len(invalid_codes)} invalid'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='hreflang_validation',
                test_name='Hreflang Validation',
                category='International SEO',
                status=TestStatus.WARNING,
                severity='High',
                issue_description='Hreflang tags present but missing x-default',
                recommendation='Add x-default hreflang for unmatched languages',
                score='Missing x-default'
            )
    
