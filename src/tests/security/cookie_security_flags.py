#!/usr/bin/env python3
"""
Cookie Security Flags Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class CookieSecurityFlagsTest(SEOTest):
    """Test for cookie security flags"""
    
    @property
    def test_id(self) -> str:
        return "cookie_security_flags"
    
    @property
    def test_name(self) -> str:
        return "Cookie Security Flags"
    
    @property
    def category(self) -> str:
        return TestCategory.SECURITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the cookie security flags test"""
        headers = content.static_headers
        
        # Get Set-Cookie headers (might be multiple)
        set_cookie = headers.get('Set-Cookie', '')
        
        if not set_cookie:
            return [TestResult(
                url=content.url,
                test_id='cookie_security_flags',
                test_name='Cookie Security Flags',
                category='Security',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='No cookies set',
                recommendation='N/A - No cookies detected',
                score='No cookies'
            )
        
        # Check for security flags
        has_secure = 'Secure' in set_cookie
        has_httponly = 'HttpOnly' in set_cookie
        has_samesite = 'SameSite' in set_cookie
        
        flags_count = sum([has_secure, has_httponly, has_samesite])
        
        if flags_count >= 2:
            return [TestResult(
                url=content.url,
                test_id='cookie_security_flags',
                test_name='Cookie Security Flags',
                category='Security',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Cookies have {flags_count}/3 security flags',
                recommendation='Continue using Secure, HttpOnly, and SameSite flags',
                score=f'{flags_count}/3 flags'
            )
        else:
            missing = []
            if not has_secure:
                missing.append('Secure')
            if not has_httponly:
                missing.append('HttpOnly')
            if not has_samesite:
                missing.append('SameSite')
            
            return [TestResult(
                url=content.url,
                test_id='cookie_security_flags',
                test_name='Cookie Security Flags',
                category='Security',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Cookies missing flags: {", ".join(missing)}',
                recommendation='Add Secure, HttpOnly, and SameSite flags to cookies',
                score=f'{flags_count}/3 flags'
            )
    
