#!/usr/bin/env python3
"""
GS009: SSR No-JS Fallback Test

Checks if meaningful content is available without JavaScript execution
to ensure Googlebot can access content even if JS fails.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re


class SSRNoscriptFallbackTest(SEOTest):
    """Test to check SSR fallback without JavaScript"""
    
    @property
    def test_id(self) -> str:
        return "GS009"
    
    @property
    def test_name(self) -> str:
        return "SSR No-JS Fallback"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the SSR no-JS fallback test"""
        results = []
        
        # Check static HTML content quality
        static_result = self._check_static_content_quality(content)
        results.append(static_result)
        
        # Check for noscript fallbacks
        noscript_result = self._check_noscript_fallbacks(content)
        results.append(noscript_result)
        
        # Check for critical content in static HTML
        critical_result = self._check_critical_content_static(content)
        results.append(critical_result)
        
        # Check for JavaScript dependencies
        js_dependency_result = self._check_javascript_dependencies(content)
        results.append(js_dependency_result)
        
        return results
    
    def _check_static_content_quality(self, content: PageContent) -> TestResult:
        """Check quality of static HTML content"""
        static_soup = content.static_soup
        if not static_soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No static content available for analysis",
                "Ensure static HTML is properly fetched",
                "0/100"
            )
        
        # Extract main content from static HTML
        main_content = self._extract_main_content(static_soup)
        word_count = len(main_content.split())
        
        # Check for H1 in static HTML
        h1_tags = static_soup.find_all('h1')
        h1_count = len(h1_tags)
        h1_text = h1_tags[0].get_text().strip() if h1_tags else ""
        
        # Check for paragraphs in static HTML
        p_tags = static_soup.find_all('p')
        p_count = len(p_tags)
        
        if word_count < 50:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Static content is too thin ({word_count} words)",
                "Implement server-side rendering to provide meaningful static content",
                "0/100"
            )
        
        if h1_count == 0:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "No H1 tag found in static HTML",
                "Add H1 tag to server-side rendered content",
                "0/100"
            )
        
        if p_count < 3:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Few paragraphs in static HTML ({p_count})",
                "Add more content to server-side rendered HTML",
                "60/100"
            )
        
        if word_count < 200:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Static content may be insufficient ({word_count} words)",
                "Consider improving server-side rendering",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Static content is adequate ({word_count} words, {h1_count} H1, {p_count} paragraphs)",
            "Server-side rendering provides meaningful content",
            "100/100"
        )
    
    def _check_noscript_fallbacks(self, content: PageContent) -> TestResult:
        """Check for noscript fallback content"""
        static_soup = content.static_soup
        if not static_soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No static content available for analysis",
                "Ensure static HTML is properly fetched",
                "0/100"
            )
        
        noscript_tags = static_soup.find_all('noscript')
        
        if not noscript_tags:
            return self._create_result(
                content,
                TestStatus.INFO,
                "No noscript tags found",
                "Consider adding noscript fallbacks for critical content",
                "80/100"
            )
        
        # Check noscript content quality
        noscript_content = ""
        for noscript in noscript_tags:
            noscript_content += noscript.get_text().strip() + " "
        
        noscript_word_count = len(noscript_content.split())
        
        if noscript_word_count < 20:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Noscript content is minimal ({noscript_word_count} words)",
                "Add more meaningful content to noscript tags",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Noscript fallbacks found with adequate content ({noscript_word_count} words)",
            "Noscript fallbacks provide good content",
            "100/100"
        )
    
    def _check_critical_content_static(self, content: PageContent) -> TestResult:
        """Check if critical content is available in static HTML"""
        static_soup = content.static_soup
        if not static_soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No static content available for analysis",
                "Ensure static HTML is properly fetched",
                "0/100"
            )
        
        # Check for critical elements in static HTML
        critical_elements = {
            'title': static_soup.find('title'),
            'h1': static_soup.find('h1'),
            'meta_description': static_soup.find('meta', attrs={'name': 'description'}),
            'canonical': static_soup.find('link', rel='canonical'),
            'main': static_soup.find('main') or static_soup.find('article')
        }
        
        missing_elements = []
        for element_name, element in critical_elements.items():
            if not element:
                missing_elements.append(element_name)
        
        if missing_elements:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Critical elements missing from static HTML: {', '.join(missing_elements)}",
                "Ensure critical SEO elements are server-side rendered",
                "0/100"
            )
        
        # Check if main content has meaningful text
        main_element = critical_elements['main']
        if main_element:
            main_text = main_element.get_text().strip()
            main_word_count = len(main_text.split())
            
            if main_word_count < 50:
                return self._create_result(
                    content,
                    TestStatus.WARNING,
                    f"Main content in static HTML is thin ({main_word_count} words)",
                    "Improve server-side rendering of main content",
                    "60/100"
                )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "All critical elements present in static HTML",
            "Server-side rendering includes critical SEO elements",
            "100/100"
        )
    
    def _check_javascript_dependencies(self, content: PageContent) -> TestResult:
        """Check for JavaScript dependencies that might block content"""
        static_soup = content.static_soup
        if not static_soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No static content available for analysis",
                "Ensure static HTML is properly fetched",
                "0/100"
            )
        
        # Count script tags
        script_tags = static_soup.find_all('script')
        external_scripts = [s for s in script_tags if s.get('src')]
        inline_scripts = [s for s in script_tags if not s.get('src')]
        
        # Check for blocking scripts
        blocking_scripts = []
        for script in external_scripts:
            src = script.get('src', '')
            # Check for scripts that might block rendering
            if any(indicator in src.lower() for indicator in ['analytics', 'gtag', 'ga', 'facebook', 'twitter']):
                blocking_scripts.append(src)
        
        if len(external_scripts) > 10:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"High number of external scripts ({len(external_scripts)})",
                "Consider reducing JavaScript dependencies",
                "60/100"
            )
        
        if blocking_scripts:
            return self._create_result(
                content,
                TestStatus.INFO,
                f"Third-party scripts detected: {', '.join(blocking_scripts[:3])}",
                "Monitor script loading impact on content visibility",
                "80/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"JavaScript usage is reasonable ({len(external_scripts)} external, {len(inline_scripts)} inline)",
            "JavaScript dependencies appear manageable",
            "100/100"
        )
    
    def _extract_main_content(self, soup) -> str:
        """Extract main content from soup"""
        # Try to find main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'main|content'))
        
        if main_content:
            return main_content.get_text().strip()
        
        # Fallback to body content
        body = soup.find('body')
        if body:
            return body.get_text().strip()
        
        return soup.get_text().strip()
