#!/usr/bin/env python3
"""
GS001: Googlebot Render Visibility Test

Verifies that main content is visible to Googlebot by checking:
- Canonical tag presence and validity
- H1 tag presence and content
- Main content text length
- Overlay blocking (splash/cookie dialogs)
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re


class GooglebotRenderVisibilityTest(SEOTest):
    """Test to verify Googlebot can see main content"""
    
    @property
    def test_id(self) -> str:
        return "GS001"
    
    @property
    def test_name(self) -> str:
        return "Googlebot Render Visibility"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the Googlebot render visibility test"""
        results = []
        
        # Use rendered content if available, fallback to static
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return [self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )]
        
        # Check canonical tag
        canonical_result = self._check_canonical(content, soup)
        results.append(canonical_result)
        
        # Check H1 presence and content
        h1_result = self._check_h1_content(content, soup)
        results.append(h1_result)
        
        # Check main content text length
        content_result = self._check_main_content(content, soup)
        results.append(content_result)
        
        # Check for blocking overlays
        overlay_result = self._check_blocking_overlays(content, soup)
        results.append(overlay_result)
        
        return results
    
    def _check_canonical(self, content: PageContent, soup) -> TestResult:
        """Check canonical tag presence and validity"""
        canonical_tag = soup.find('link', rel='canonical')
        
        if not canonical_tag:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "No canonical tag found",
                "Add a canonical tag pointing to the preferred URL",
                "0/100"
            )
        
        canonical_url = canonical_tag.get('href', '')
        if not canonical_url:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "Canonical tag has no href attribute",
                "Add href attribute to canonical tag",
                "0/100"
            )
        
        # Check if canonical points to current URL or valid variant
        if canonical_url == content.url or canonical_url.rstrip('/') == content.url.rstrip('/'):
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Canonical tag correctly points to {canonical_url}",
                "Canonical tag is properly configured",
                "100/100"
            )
        else:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Canonical tag points to {canonical_url}, not current URL {content.url}",
                "Verify canonical URL is the preferred version",
                "70/100"
            )
    
    def _check_h1_content(self, content: PageContent, soup) -> TestResult:
        """Check H1 tag presence and content quality"""
        h1_tags = soup.find_all('h1')
        
        if not h1_tags:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "No H1 tag found",
                "Add an H1 tag with descriptive content",
                "0/100"
            )
        
        if len(h1_tags) > 1:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Multiple H1 tags found ({len(h1_tags)})",
                "Use only one H1 tag per page",
                "60/100"
            )
        
        h1_text = h1_tags[0].get_text().strip()
        if not h1_text:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "H1 tag is empty",
                "Add descriptive text to H1 tag",
                "0/100"
            )
        
        if len(h1_text) < 10:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"H1 text is too short: '{h1_text}'",
                "Use more descriptive H1 text",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"H1 tag found with good content: '{h1_text}'",
            "H1 tag is properly configured",
            "100/100"
        )
    
    def _check_main_content(self, content: PageContent, soup) -> TestResult:
        """Check main content text length and quality"""
        # Try to find main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'main|content'))
        
        if main_content:
            text_content = main_content.get_text().strip()
        else:
            # Fallback to body content
            body = soup.find('body')
            text_content = body.get_text().strip() if body else soup.get_text().strip()
        
        # Remove extra whitespace
        text_content = re.sub(r'\s+', ' ', text_content)
        word_count = len(text_content.split())
        
        if word_count < 50:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Main content is too short ({word_count} words)",
                "Add substantial content to the page",
                "0/100"
            )
        
        if word_count < 200:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Main content is relatively short ({word_count} words)",
                "Consider adding more substantial content",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Main content has adequate length ({word_count} words)",
            "Content length is sufficient",
            "100/100"
        )
    
    def _check_blocking_overlays(self, content: PageContent, soup) -> TestResult:
        """Check for blocking overlays (splash screens, cookie dialogs)"""
        issues = []
        
        # Check for splash screen
        splash_elements = soup.find_all(class_=re.compile(r'splash', re.I))
        if splash_elements:
            issues.append(f"Splash screen detected: {len(splash_elements)} elements")
        
        # Check for cookie dialog
        cookie_elements = soup.find_all(attrs={'data-testid': re.compile(r'cookie', re.I)})
        if not cookie_elements:
            cookie_elements = soup.find_all(class_=re.compile(r'cookie', re.I))
        
        if cookie_elements:
            issues.append(f"Cookie dialog detected: {len(cookie_elements)} elements")
        
        # Check for modal dialogs
        modal_elements = soup.find_all(attrs={'role': 'dialog'}) + soup.find_all(class_=re.compile(r'modal|dialog', re.I))
        if modal_elements:
            issues.append(f"Modal dialogs detected: {len(modal_elements)} elements")
        
        if issues:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Blocking overlays detected: {'; '.join(issues)}",
                "Ensure overlays don't block Googlebot from accessing main content",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No blocking overlays detected",
            "Page is accessible to Googlebot",
            "100/100"
        )
