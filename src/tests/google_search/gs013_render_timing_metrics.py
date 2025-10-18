#!/usr/bin/env python3
"""
GS013: Render Timing Metrics Test

Analyzes render timing metrics to detect late hydration that may cause
Googlebot to see thin content.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re


class RenderTimingMetricsTest(SEOTest):
    """Test to analyze render timing metrics"""
    
    @property
    def test_id(self) -> str:
        return "GS013"
    
    @property
    def test_name(self) -> str:
        return "Render Timing Metrics"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "Medium"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the render timing metrics test"""
        results = []
        
        # Check performance metrics
        performance_result = self._check_performance_metrics(content)
        results.append(performance_result)
        
        # Check for hydration markers
        hydration_result = self._check_hydration_markers(content)
        results.append(hydration_result)
        
        # Check for render blocking resources
        blocking_result = self._check_render_blocking_resources(content)
        results.append(blocking_result)
        
        # Check for timing issues
        timing_result = self._check_timing_issues(content)
        results.append(timing_result)
        
        return results
    
    def _check_performance_metrics(self, content: PageContent) -> TestResult:
        """Check performance metrics for timing issues"""
        metrics = content.performance_metrics
        
        if not metrics:
            return self._create_result(
                content,
                TestStatus.INFO,
                "No performance metrics available",
                "Enable performance monitoring for better analysis",
                "N/A"
            )
        
        # Check for key timing metrics
        dom_content_loaded = metrics.get('domContentLoaded', 0)
        load_complete = metrics.get('loadComplete', 0)
        first_paint = metrics.get('firstPaint', 0)
        first_contentful_paint = metrics.get('firstContentfulPaint', 0)
        
        if dom_content_loaded > 3000:  # 3 seconds
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Slow DOM content loaded ({dom_content_loaded}ms)",
                "Optimize page loading to improve render timing",
                "60/100"
            )
        
        if load_complete > 5000:  # 5 seconds
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Slow page load ({load_complete}ms)",
                "Optimize page loading performance",
                "60/100"
            )
        
        if first_paint > 2000:  # 2 seconds
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Slow first paint ({first_paint}ms)",
                "Optimize critical rendering path",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Good performance metrics (DOM: {dom_content_loaded}ms, Load: {load_complete}ms)",
            "Page loading performance is acceptable",
            "100/100"
        )
    
    def _check_hydration_markers(self, content: PageContent) -> TestResult:
        """Check for hydration markers in content"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Look for hydration markers
        hydration_markers = [
            'hydration',
            'hydrated',
            'client-side',
            'spa',
            'single-page',
            'javascript-framework'
        ]
        
        page_text = soup.get_text().lower()
        found_markers = [marker for marker in hydration_markers if marker in page_text]
        
        if found_markers:
            return self._create_result(
                content,
                TestStatus.INFO,
                f"Hydration markers detected: {', '.join(found_markers)}",
                "Monitor hydration timing for Googlebot compatibility",
                "80/100"
            )
        
        # Check for JavaScript framework indicators
        script_tags = soup.find_all('script')
        framework_scripts = []
        
        for script in script_tags:
            src = script.get('src', '')
            if any(framework in src.lower() for framework in ['react', 'vue', 'angular', 'svelte']):
                framework_scripts.append(src)
        
        if framework_scripts:
            return self._create_result(
                content,
                TestStatus.INFO,
                f"JavaScript framework detected: {', '.join(framework_scripts[:2])}",
                "Ensure framework content is server-side rendered",
                "80/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No hydration issues detected",
            "Page appears to render without hydration delays",
            "100/100"
        )
    
    def _check_render_blocking_resources(self, content: PageContent) -> TestResult:
        """Check for render blocking resources"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Check for render blocking resources
        blocking_resources = []
        
        # Check for blocking CSS
        css_links = soup.find_all('link', rel='stylesheet')
        for css in css_links:
            if not css.get('media') or css.get('media') == 'all':
                blocking_resources.append(f"Blocking CSS: {css.get('href', '')}")
        
        # Check for blocking JavaScript
        js_scripts = soup.find_all('script', src=True)
        for script in js_scripts:
            if not script.get('defer') and not script.get('async'):
                blocking_resources.append(f"Blocking JS: {script.get('src', '')}")
        
        if blocking_resources:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Render blocking resources found: {'; '.join(blocking_resources[:3])}",
                "Optimize resource loading to improve render timing",
                "60/100"
            )
        
        return self._create_result(
            content,
                TestStatus.PASS,
                "No render blocking resources detected",
                "Resources are properly optimized for loading",
                "100/100"
        )
    
    def _check_timing_issues(self, content: PageContent) -> TestResult:
        """Check for timing-related issues"""
        metrics = content.performance_metrics
        
        if not metrics:
            return self._create_result(
                content,
                TestStatus.INFO,
                "No performance metrics available",
                "Enable performance monitoring for better analysis",
                "N/A"
            )
        
        # Check for timing gaps
        dom_content_loaded = metrics.get('domContentLoaded', 0)
        load_complete = metrics.get('loadComplete', 0)
        
        if load_complete > 0 and dom_content_loaded > 0:
            timing_gap = load_complete - dom_content_loaded
            
            if timing_gap > 2000:  # 2 seconds
                return self._create_result(
                    content,
                    TestStatus.WARNING,
                    f"Large timing gap between DOM and load complete ({timing_gap}ms)",
                    "Investigate what's causing the delay after DOM ready",
                    "60/100"
                )
        
        # Check for slow resource loading
        resource_timing = metrics.get('resourceTiming', {})
        if resource_timing:
            slow_resources = [url for url, timing in resource_timing.items() if timing > 1000]
            if slow_resources:
                return self._create_result(
                    content,
                    TestStatus.WARNING,
                    f"Slow resources detected: {', '.join(slow_resources[:2])}",
                    "Optimize slow-loading resources",
                    "70/100"
                )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No significant timing issues detected",
            "Page timing appears to be within acceptable ranges",
            "100/100"
        )
