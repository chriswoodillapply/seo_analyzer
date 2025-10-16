#!/usr/bin/env python3
"""
Security Headers Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SecurityHeadersTest(SEOTest):
    """Test for security headers"""
    
    @property
    def test_id(self) -> str:
        return "security_headers"
    
    @property
    def test_name(self) -> str:
        return "Security Headers"
    
    @property
    def category(self) -> str:
        return TestCategory.SECURITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the security headers test"""
        headers = content.static_headers
        
        security_headers = {
            'X-Frame-Options': False,
            'X-Content-Type-Options': False,
            'Strict-Transport-Security': False,
            'Content-Security-Policy': False
        }
        
        for header in security_headers.keys():
            if header in headers or header.lower() in headers:
                security_headers[header] = True
        
        found_count = sum(security_headers.values())
        
        if found_count >= 3:
            return TestResult(
                url=content.url,
                test_id='security_headers',
                test_name='Security Headers',
                category='Security',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'Found {found_count}/4 recommended security headers',
                recommendation='Continue maintaining security headers',
                score=f'{found_count}/4 headers present'
            )
        elif found_count >= 1:
            return TestResult(
                url=content.url,
                test_id='security_headers',
                test_name='Security Headers',
                category='Security',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'Only {found_count}/4 security headers found',
                recommendation='Add missing security headers for better protection',
                score=f'{found_count}/4 headers present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='security_headers',
                test_name='Security Headers',
                category='Security',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='No security headers found',
                recommendation='Implement security headers (X-Frame-Options, CSP, HSTS, etc.)',
                score='0/4 headers present'
            )
    
    # =========================================================================
    # ADDITIONAL META TAGS TESTS - PHASE 1
    # =========================================================================
    
