#!/usr/bin/env python3
"""
GS003: Static vs Rendered Content Test

Compares static HTML (curl) vs rendered DOM (Playwright) to detect
thin static content that only becomes meaningful after JavaScript execution.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re


class StaticVsRenderedContentTest(SEOTest):
    """Test to compare static vs rendered content"""
    
    @property
    def test_id(self) -> str:
        return "GS003"
    
    @property
    def test_name(self) -> str:
        return "Static vs Rendered Content"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the static vs rendered content test"""
        results = []
        
        # Compare H1 tags
        h1_result = self._compare_h1_tags(content)
        results.append(h1_result)
        
        # Compare main content
        content_result = self._compare_main_content(content)
        results.append(content_result)
        
        # Compare meta tags
        meta_result = self._compare_meta_tags(content)
        results.append(meta_result)
        
        # Check for JavaScript dependency
        js_result = self._check_javascript_dependency(content)
        results.append(js_result)
        
        return results
    
    def _compare_h1_tags(self, content: PageContent) -> TestResult:
        """Compare H1 tags between static and rendered content"""
        static_soup = content.static_soup
        rendered_soup = content.rendered_soup
        
        if not static_soup or not rendered_soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "Missing static or rendered content for comparison",
                "Ensure both static and rendered content are fetched",
                "0/100"
            )
        
        static_h1 = static_soup.find('h1')
        rendered_h1 = rendered_soup.find('h1')
        
        static_h1_text = static_h1.get_text().strip() if static_h1 else ""
        rendered_h1_text = rendered_h1.get_text().strip() if rendered_h1 else ""
        
        # Check if H1 is missing in static but present in rendered
        if not static_h1_text and rendered_h1_text:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "H1 tag missing in static HTML but present in rendered content",
                "Ensure H1 is present in server-side rendered HTML for Googlebot",
                "0/100"
            )
        
        # Check if H1 content differs significantly
        if static_h1_text and rendered_h1_text and static_h1_text != rendered_h1_text:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"H1 content differs: static='{static_h1_text}' vs rendered='{rendered_h1_text}'",
                "Ensure H1 content is consistent between static and rendered versions",
                "60/100"
            )
        
        # Check if both are empty
        if not static_h1_text and not rendered_h1_text:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "No H1 tag found in either static or rendered content",
                "Add an H1 tag to the page",
                "0/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"H1 tag consistent between static and rendered: '{rendered_h1_text}'",
            "H1 tag is properly server-side rendered",
            "100/100"
        )
    
    def _compare_main_content(self, content: PageContent) -> TestResult:
        """Compare main content between static and rendered versions"""
        static_soup = content.static_soup
        rendered_soup = content.rendered_soup
        
        if not static_soup or not rendered_soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "Missing static or rendered content for comparison",
                "Ensure both static and rendered content are fetched",
                "0/100"
            )
        
        # Extract main content from both versions
        static_main = self._extract_main_content(static_soup)
        rendered_main = self._extract_main_content(rendered_soup)
        
        static_word_count = len(static_main.split())
        rendered_word_count = len(rendered_main.split())
        
        # Calculate content ratio
        if rendered_word_count > 0:
            content_ratio = static_word_count / rendered_word_count
        else:
            content_ratio = 0
        
        # Check for thin static content
        if content_ratio < 0.3 and rendered_word_count > 100:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Static content is very thin ({static_word_count} words) compared to rendered ({rendered_word_count} words)",
                "Implement server-side rendering to provide meaningful static content",
                "0/100"
            )
        
        if content_ratio < 0.6 and rendered_word_count > 50:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Static content is thin ({static_word_count} words) compared to rendered ({rendered_word_count} words)",
                "Consider improving server-side rendering for better SEO",
                "50/100"
            )
        
        if static_word_count < 50 and rendered_word_count > 200:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Static content may be insufficient for Googlebot ({static_word_count} words)",
                "Ensure critical content is available in static HTML",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Static and rendered content are well-balanced ({static_word_count} vs {rendered_word_count} words)",
            "Content is properly server-side rendered",
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
    
    def _compare_meta_tags(self, content: PageContent) -> TestResult:
        """Compare meta tags between static and rendered content"""
        static_soup = content.static_soup
        rendered_soup = content.rendered_soup
        
        if not static_soup or not rendered_soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "Missing static or rendered content for comparison",
                "Ensure both static and rendered content are fetched",
                "0/100"
            )
        
        # Check title tag
        static_title = static_soup.find('title')
        rendered_title = rendered_soup.find('title')
        
        static_title_text = static_title.get_text().strip() if static_title else ""
        rendered_title_text = rendered_title.get_text().strip() if rendered_title else ""
        
        if static_title_text != rendered_title_text:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Title tag differs between static and rendered content",
                "Ensure title tag is consistent",
                "70/100"
            )
        
        # Check meta description
        static_desc = static_soup.find('meta', attrs={'name': 'description'})
        rendered_desc = rendered_soup.find('meta', attrs={'name': 'description'})
        
        static_desc_content = static_desc.get('content', '') if static_desc else ""
        rendered_desc_content = rendered_desc.get('content', '') if rendered_desc else ""
        
        if static_desc_content != rendered_desc_content:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Meta description differs between static and rendered content",
                "Ensure meta description is consistent",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "Meta tags are consistent between static and rendered content",
            "Meta tags are properly server-side rendered",
            "100/100"
        )
    
    def _check_javascript_dependency(self, content: PageContent) -> TestResult:
        """Check if page has heavy JavaScript dependency"""
        static_soup = content.static_soup
        rendered_soup = content.rendered_soup
        
        if not static_soup or not rendered_soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "Missing static or rendered content for comparison",
                "Ensure both static and rendered content are fetched",
                "0/100"
            )
        
        # Count script tags
        static_scripts = len(static_soup.find_all('script'))
        rendered_scripts = len(rendered_soup.find_all('script'))
        
        # Check for external script dependencies
        external_scripts = static_soup.find_all('script', src=True)
        inline_scripts = static_soup.find_all('script', src=False)
        
        if len(external_scripts) > 10:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"High number of external JavaScript dependencies ({len(external_scripts)})",
                "Consider reducing JavaScript dependencies for better SEO",
                "60/100"
            )
        
        # Check for JavaScript frameworks
        framework_indicators = ['react', 'vue', 'angular', 'svelte', 'next', 'nuxt']
        framework_detected = []
        
        for script in external_scripts:
            src = script.get('src', '').lower()
            for framework in framework_indicators:
                if framework in src:
                    framework_detected.append(framework)
        
        if framework_detected:
            return self._create_result(
                content,
                TestStatus.INFO,
                f"JavaScript framework detected: {', '.join(set(framework_detected))}",
                "Ensure framework content is server-side rendered",
                "80/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"JavaScript usage is reasonable ({len(external_scripts)} external, {len(inline_scripts)} inline)",
            "JavaScript implementation appears SEO-friendly",
            "100/100"
        )
