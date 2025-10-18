#!/usr/bin/env python3
"""
GS002: Console Network Errors Test

Captures and analyzes console warnings/errors and network failures that could
impact Googlebot's ability to properly render and index content.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re


class ConsoleNetworkErrorsTest(SEOTest):
    """Test to analyze console errors and network failures"""
    
    @property
    def test_id(self) -> str:
        return "GS002"
    
    @property
    def test_name(self) -> str:
        return "Console Network Errors"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "Medium"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the console network errors test"""
        results = []
        
        # Analyze console messages if available
        console_result = self._analyze_console_messages(content)
        results.append(console_result)
        
        # Analyze network errors from performance metrics
        network_result = self._analyze_network_errors(content)
        results.append(network_result)
        
        # Check for JavaScript errors in rendered content
        js_result = self._analyze_javascript_errors(content)
        results.append(js_result)
        
        return results
    
    def _analyze_console_messages(self, content: PageContent) -> TestResult:
        """Analyze console messages for errors and warnings"""
        # This would typically come from Playwright console logs
        # For now, we'll check if console data is available in performance_metrics
        console_data = content.performance_metrics.get('console_messages', [])
        
        if not console_data:
            return self._create_result(
                content,
                TestStatus.INFO,
                "No console message data available",
                "Console monitoring not implemented",
                "N/A"
            )
        
        error_count = 0
        warning_count = 0
        critical_errors = []
        
        for message in console_data:
            if message.get('type') == 'error':
                error_count += 1
                text = message.get('text', '')
                if any(keyword in text.lower() for keyword in ['failed', 'error', 'exception', 'blocked']):
                    critical_errors.append(text[:100])
            elif message.get('type') == 'warning':
                warning_count += 1
        
        if error_count > 10:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"High number of console errors ({error_count}) detected",
                "Fix JavaScript errors that may prevent proper rendering",
                "0/100"
            )
        
        if error_count > 5:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Multiple console errors ({error_count}) detected",
                "Review and fix JavaScript errors",
                "40/100"
            )
        
        if critical_errors:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Critical errors detected: {'; '.join(critical_errors[:3])}",
                "Address critical JavaScript errors",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Console is clean ({error_count} errors, {warning_count} warnings)",
            "No significant console issues detected",
            "100/100"
        )
    
    def _analyze_network_errors(self, content: PageContent) -> TestResult:
        """Analyze network errors and failed requests"""
        # Check performance metrics for network issues
        network_data = content.performance_metrics.get('network_requests', [])
        
        if not network_data:
            return self._create_result(
                content,
                TestStatus.INFO,
                "No network request data available",
                "Network monitoring not implemented",
                "N/A"
            )
        
        failed_requests = 0
        error_4xx = 0
        error_5xx = 0
        blocked_requests = 0
        
        for request in network_data:
            status = request.get('status', 0)
            if status >= 400:
                failed_requests += 1
                if 400 <= status < 500:
                    error_4xx += 1
                elif status >= 500:
                    error_5xx += 1
            
            if request.get('blocked', False):
                blocked_requests += 1
        
        total_requests = len(network_data)
        failure_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0
        
        if error_5xx > 0:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Server errors detected ({error_5xx} 5xx responses)",
                "Fix server-side issues that may prevent proper rendering",
                "0/100"
            )
        
        if failure_rate > 20:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"High network failure rate ({failure_rate:.1f}%)",
                "Investigate network issues affecting page resources",
                "40/100"
            )
        
        if blocked_requests > 0:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Blocked requests detected ({blocked_requests})",
                "Check robots.txt and CORS policies",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Network requests are healthy ({failure_rate:.1f}% failure rate)",
            "No significant network issues detected",
            "100/100"
        )
    
    def _analyze_javascript_errors(self, content: PageContent) -> TestResult:
        """Analyze JavaScript errors in rendered content"""
        # Check if rendered content has JavaScript errors
        rendered_html = content.rendered_html or ""
        
        # Look for common error patterns in HTML
        error_patterns = [
            r'error\s*:\s*[^<]+',
            r'exception\s*:\s*[^<]+',
            r'failed\s+to\s+load',
            r'blocked\s+by\s+robots\.txt',
            r'CORS\s+error',
            r'network\s+error'
        ]
        
        errors_found = []
        for pattern in error_patterns:
            matches = re.findall(pattern, rendered_html, re.IGNORECASE)
            if matches:
                errors_found.extend(matches[:3])  # Limit to first 3 matches
        
        if errors_found:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"JavaScript errors detected in content: {'; '.join(errors_found)}",
                "Fix JavaScript errors that may affect rendering",
                "50/100"
            )
        
        # Check for missing JavaScript dependencies
        script_tags = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', rendered_html)
        if not script_tags:
            return self._create_result(
                content,
                TestStatus.INFO,
                "No external JavaScript dependencies found",
                "Page appears to be static or uses inline JavaScript",
                "N/A"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No JavaScript errors detected in rendered content",
            "JavaScript execution appears successful",
            "100/100"
        )
