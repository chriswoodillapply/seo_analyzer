#!/usr/bin/env python3
"""
GS011: Hreflang Canonical Consistency Test

Checks hreflang and canonical consistency across locale pages to ensure
proper international SEO implementation.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re
from urllib.parse import urlparse


class HreflangCanonicalConsistencyTest(SEOTest):
    """Test to check hreflang and canonical consistency"""
    
    @property
    def test_id(self) -> str:
        return "GS011"
    
    @property
    def test_name(self) -> str:
        return "Hreflang Canonical Consistency"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "Medium"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the hreflang canonical consistency test"""
        results = []
        
        # Check hreflang tags
        hreflang_result = self._check_hreflang_tags(content)
        results.append(hreflang_result)
        
        # Check canonical consistency
        canonical_result = self._check_canonical_consistency(content)
        results.append(canonical_result)
        
        # Check locale detection
        locale_result = self._check_locale_detection(content)
        results.append(locale_result)
        
        return results
    
    def _check_hreflang_tags(self, content: PageContent) -> TestResult:
        """Check hreflang tags for proper implementation"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        hreflang_tags = soup.find_all('link', rel='alternate', hreflang=True)
        
        if not hreflang_tags:
            return self._create_result(
                content,
                TestStatus.INFO,
                "No hreflang tags found",
                "Add hreflang tags if page has international variants",
                "80/100"
            )
        
        # Check hreflang implementation
        issues = []
        hreflang_data = {}
        
        for tag in hreflang_tags:
            hreflang = tag.get('hreflang')
            href = tag.get('href')
            
            if not hreflang or not href:
                issues.append("Invalid hreflang tag (missing hreflang or href)")
                continue
            
            # Check for self-reference
            if href == content.url and hreflang != 'x-default':
                hreflang_data[hreflang] = href
            
            # Check for x-default
            if hreflang == 'x-default':
                if href != content.url:
                    issues.append(f"x-default should point to current URL: {href}")
        
        # Check for self-reference
        if not any(tag.get('href') == content.url for tag in hreflang_tags):
            issues.append("Missing self-reference in hreflang tags")
        
        # Check for x-default
        if not any(tag.get('hreflang') == 'x-default' for tag in hreflang_tags):
            issues.append("Missing x-default hreflang tag")
        
        if issues:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Hreflang implementation issues: {'; '.join(issues)}",
                "Fix hreflang tag implementation for proper international SEO",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Hreflang tags properly implemented ({len(hreflang_tags)} tags)",
            "Hreflang implementation follows best practices",
            "100/100"
        )
    
    def _check_canonical_consistency(self, content: PageContent) -> TestResult:
        """Check canonical consistency across locales"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        canonical_tag = soup.find('link', rel='canonical')
        if not canonical_tag:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "No canonical tag found",
                "Add canonical tag to specify preferred URL",
                "0/100"
            )
        
        canonical_url = canonical_tag.get('href', '')
        if not canonical_url:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "Canonical tag has no href",
                "Add href attribute to canonical tag",
                "0/100"
            )
        
        # Check if canonical points to current URL
        if canonical_url == content.url:
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Canonical tag correctly points to current URL: {canonical_url}",
                "Canonical tag is properly configured",
                "100/100"
            )
        
        # Check for cross-locale canonicalization
        current_parsed = urlparse(content.url)
        canonical_parsed = urlparse(canonical_url)
        
        # Check if canonical points to different locale
        current_locale = self._extract_locale_from_url(content.url)
        canonical_locale = self._extract_locale_from_url(canonical_url)
        
        if current_locale and canonical_locale and current_locale != canonical_locale:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Canonical points to different locale: {canonical_url}",
                "Ensure canonical points to same locale or use hreflang for cross-locale",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.WARNING,
            f"Canonical points to different URL: {canonical_url}",
            "Verify canonical URL is the preferred version",
            "70/100"
        )
    
    def _check_locale_detection(self, content: PageContent) -> TestResult:
        """Check locale detection from URL and content"""
        url = content.url
        parsed = urlparse(url)
        path = parsed.path
        
        # Extract locale from URL
        locale_patterns = [
            r'/([a-z]{2}-[A-Z]{2})/',  # en-US, es-419
            r'/([a-z]{2})/',           # en, es
            r'/([a-z]{2}_[A-Z]{2})/'   # en_US, es_ES
        ]
        
        detected_locales = []
        for pattern in locale_patterns:
            matches = re.findall(pattern, path)
            detected_locales.extend(matches)
        
        if not detected_locales:
            return self._create_result(
                content,
                TestStatus.INFO,
                "No locale detected in URL",
                "Consider adding locale indicators if page has international variants",
                "80/100"
            )
        
        # Check for multiple locales in URL
        if len(detected_locales) > 1:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Multiple locales detected in URL: {', '.join(detected_locales)}",
                "Use single locale per URL",
                "60/100"
            )
        
        # Check for valid locale format
        locale = detected_locales[0]
        if len(locale) == 2:  # Simple locale like 'en'
            return self._create_result(
                content,
                TestStatus.INFO,
                f"Simple locale detected: {locale}",
                "Consider using full locale format (e.g., en-US)",
                "80/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Locale properly detected: {locale}",
            "Locale implementation appears correct",
            "100/100"
        )
    
    def _extract_locale_from_url(self, url: str) -> Optional[str]:
        """Extract locale from URL"""
        parsed = urlparse(url)
        path = parsed.path
        
        locale_patterns = [
            r'/([a-z]{2}-[A-Z]{2})/',  # en-US, es-419
            r'/([a-z]{2})/',           # en, es
            r'/([a-z]{2}_[A-Z]{2})/'   # en_US, es_ES
        ]
        
        for pattern in locale_patterns:
            match = re.search(pattern, path)
            if match:
                return match.group(1)
        
        return None
