#!/usr/bin/env python3
"""
GS007: Duplicate Variant Detection Test

Detects duplicate URL variants that may cause canonical confusion,
including /learn/ variants, www vs non-www, trailing slashes, and locale forks.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re
from urllib.parse import urlparse, urljoin


class DuplicateVariantDetectionTest(SEOTest):
    """Test to detect duplicate URL variants"""
    
    @property
    def test_id(self) -> str:
        return "GS007"
    
    @property
    def test_name(self) -> str:
        return "Duplicate Variant Detection"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the duplicate variant detection test"""
        results = []
        
        # Check for /learn/ variants
        learn_result = self._check_learn_variants(content)
        results.append(learn_result)
        
        # Check for www vs non-www variants
        www_result = self._check_www_variants(content)
        results.append(www_result)
        
        # Check for trailing slash variants
        slash_result = self._check_trailing_slash_variants(content)
        results.append(slash_result)
        
        # Check for locale variants
        locale_result = self._check_locale_variants(content)
        results.append(locale_result)
        
        # Check for protocol variants
        protocol_result = self._check_protocol_variants(content)
        results.append(protocol_result)
        
        return results
    
    def _check_learn_variants(self, content: PageContent) -> TestResult:
        """Check for /learn/ path variants"""
        url = content.url
        parsed = urlparse(url)
        path = parsed.path
        
        # Check if URL has /learn/ in path
        if '/learn/' in path:
            # Check if there's a variant without /learn/
            variant_path = path.replace('/learn/', '/')
            variant_url = f"{parsed.scheme}://{parsed.netloc}{variant_path}"
            
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"URL contains /learn/ path: {url}",
                f"Consider canonicalizing to variant without /learn/: {variant_url}",
                "60/100"
            )
        
        # Check if there might be a /learn/ variant
        if '/insights/' in path and not '/learn/' in path:
            learn_variant = path.replace('/insights/', '/insights/learn/')
            learn_url = f"{parsed.scheme}://{parsed.netloc}{learn_variant}"
            
            return self._create_result(
                content,
                TestStatus.INFO,
                f"URL may have /learn/ variant: {learn_url}",
                "Monitor for duplicate content with /learn/ variant",
                "80/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No /learn/ variant issues detected",
            "URL path is consistent",
            "100/100"
        )
    
    def _check_www_variants(self, content: PageContent) -> TestResult:
        """Check for www vs non-www variants"""
        url = content.url
        parsed = urlparse(url)
        domain = parsed.netloc
        
        if domain.startswith('www.'):
            non_www_domain = domain[4:]
            non_www_url = f"{parsed.scheme}://{non_www_domain}{parsed.path}"
            
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"URL uses www subdomain: {url}",
                f"Consider canonicalizing to non-www version: {non_www_url}",
                "70/100"
            )
        
        if not domain.startswith('www.'):
            www_domain = f"www.{domain}"
            www_url = f"{parsed.scheme}://{www_domain}{parsed.path}"
            
            return self._create_result(
                content,
                TestStatus.INFO,
                f"URL does not use www subdomain: {url}",
                f"Monitor for www variant: {www_url}",
                "90/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No www variant issues detected",
            "URL domain is consistent",
            "100/100"
        )
    
    def _check_trailing_slash_variants(self, content: PageContent) -> TestResult:
        """Check for trailing slash variants"""
        url = content.url
        parsed = urlparse(url)
        path = parsed.path
        
        if path.endswith('/') and path != '/':
            no_slash_path = path.rstrip('/')
            no_slash_url = f"{parsed.scheme}://{parsed.netloc}{no_slash_path}"
            
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"URL has trailing slash: {url}",
                f"Consider canonicalizing to version without trailing slash: {no_slash_url}",
                "70/100"
            )
        
        if not path.endswith('/') and path != '/':
            slash_path = path + '/'
            slash_url = f"{parsed.scheme}://{parsed.netloc}{slash_path}"
            
            return self._create_result(
                content,
                TestStatus.INFO,
                f"URL does not have trailing slash: {url}",
                f"Monitor for trailing slash variant: {slash_url}",
                "90/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No trailing slash variant issues detected",
            "URL path is consistent",
            "100/100"
        )
    
    def _check_locale_variants(self, content: PageContent) -> TestResult:
        """Check for locale variants"""
        url = content.url
        parsed = urlparse(url)
        path = parsed.path
        
        # Check for locale patterns in path
        locale_patterns = [
            r'/[a-z]{2}-[A-Z]{2}/',  # en-US, es-419, etc.
            r'/[a-z]{2}/',           # en, es, etc.
            r'/[a-z]{2}_[A-Z]{2}/'   # en_US, es_ES, etc.
        ]
        
        found_locales = []
        for pattern in locale_patterns:
            matches = re.findall(pattern, path)
            found_locales.extend(matches)
        
        if found_locales:
            return self._create_result(
                content,
                TestStatus.INFO,
                f"URL contains locale indicators: {', '.join(found_locales)}",
                "Ensure proper hreflang and canonical configuration for locale variants",
                "80/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No locale variant issues detected",
            "URL does not contain locale indicators",
            "100/100"
        )
    
    def _check_protocol_variants(self, content: PageContent) -> TestResult:
        """Check for HTTP vs HTTPS variants"""
        url = content.url
        parsed = urlparse(url)
        
        if parsed.scheme == 'http':
            https_url = f"https://{parsed.netloc}{parsed.path}"
            
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"URL uses HTTP protocol: {url}",
                f"Redirect to HTTPS version: {https_url}",
                "0/100"
            )
        
        if parsed.scheme == 'https':
            http_url = f"http://{parsed.netloc}{parsed.path}"
            
            return self._create_result(
                content,
                TestStatus.INFO,
                f"URL uses HTTPS protocol: {url}",
                f"Monitor for HTTP variant: {http_url}",
                "100/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No protocol variant issues detected",
            "URL protocol is consistent",
            "100/100"
        )
