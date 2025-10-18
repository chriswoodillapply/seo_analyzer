#!/usr/bin/env python3
"""
GS014: Robots Meta Headers Test

Checks robots.txt allow, meta robots, and x-robots-tag headers to ensure
pages are not blocked from indexing.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re
from urllib.parse import urlparse, urljoin


class RobotsMetaHeadersTest(SEOTest):
    """Test to check robots meta headers and blocking"""
    
    @property
    def test_id(self) -> str:
        return "GS014"
    
    @property
    def test_name(self) -> str:
        return "Robots Meta Headers"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the robots meta headers test"""
        results = []
        
        # Check meta robots tag
        meta_result = self._check_meta_robots(content)
        results.append(meta_result)
        
        # Check x-robots-tag headers
        header_result = self._check_x_robots_headers(content)
        results.append(header_result)
        
        # Check for noindex directives
        noindex_result = self._check_noindex_directives(content)
        results.append(noindex_result)
        
        # Check for follow/nofollow directives
        follow_result = self._check_follow_directives(content)
        results.append(follow_result)
        
        return results
    
    def _check_meta_robots(self, content: PageContent) -> TestResult:
        """Check meta robots tag"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        
        if not meta_robots:
            return self._create_result(
                content,
                TestStatus.PASS,
                "No meta robots tag found (defaults to index, follow)",
                "Page is not blocked by meta robots tag",
                "100/100"
            )
        
        content_value = meta_robots.get('content', '').lower()
        
        if 'noindex' in content_value:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Meta robots tag blocks indexing: {content_value}",
                "Remove noindex directive to allow indexing",
                "0/100"
            )
        
        if 'nofollow' in content_value:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Meta robots tag blocks following links: {content_value}",
                "Consider removing nofollow directive to allow link following",
                "70/100"
            )
        
        if 'index' in content_value and 'follow' in content_value:
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Meta robots tag allows indexing: {content_value}",
                "Page is properly configured for indexing",
                "100/100"
            )
        
        return self._create_result(
            content,
            TestStatus.INFO,
            f"Meta robots tag found: {content_value}",
            "Monitor meta robots tag configuration",
            "80/100"
        )
    
    def _check_x_robots_headers(self, content: PageContent) -> TestResult:
        """Check x-robots-tag headers"""
        headers = content.static_headers or {}
        x_robots = headers.get('x-robots-tag', '')
        
        if not x_robots:
            return self._create_result(
                content,
                TestStatus.PASS,
                "No x-robots-tag header found",
                "Page is not blocked by x-robots-tag header",
                "100/100"
            )
        
        x_robots_lower = x_robots.lower()
        
        if 'noindex' in x_robots_lower:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"x-robots-tag header blocks indexing: {x_robots}",
                "Remove noindex directive from x-robots-tag header",
                "0/100"
            )
        
        if 'nofollow' in x_robots_lower:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"x-robots-tag header blocks following links: {x_robots}",
                "Consider removing nofollow directive from x-robots-tag header",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.INFO,
            f"x-robots-tag header found: {x_robots}",
            "Monitor x-robots-tag header configuration",
            "80/100"
        )
    
    def _check_noindex_directives(self, content: PageContent) -> TestResult:
        """Check for noindex directives"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Check for noindex in meta robots
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        meta_noindex = False
        if meta_robots and 'noindex' in meta_robots.get('content', '').lower():
            meta_noindex = True
        
        # Check for noindex in x-robots-tag headers
        headers = content.static_headers or {}
        x_robots = headers.get('x-robots-tag', '')
        header_noindex = 'noindex' in x_robots.lower()
        
        if meta_noindex or header_noindex:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "Noindex directive found (blocks indexing)",
                "Remove noindex directive to allow Google to index the page",
                "0/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No noindex directives found",
            "Page is not blocked from indexing",
            "100/100"
        )
    
    def _check_follow_directives(self, content: PageContent) -> TestResult:
        """Check for follow/nofollow directives"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Check meta robots for nofollow
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        meta_nofollow = False
        if meta_robots and 'nofollow' in meta_robots.get('content', '').lower():
            meta_nofollow = True
        
        # Check x-robots-tag for nofollow
        headers = content.static_headers or {}
        x_robots = headers.get('x-robots-tag', '')
        header_nofollow = 'nofollow' in x_robots.lower()
        
        if meta_nofollow or header_nofollow:
            return self._create_result(
                content,
                TestStatus.WARNING,
                "Nofollow directive found (blocks link following)",
                "Consider removing nofollow directive to allow Google to follow links",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            "No nofollow directives found",
            "Page allows Google to follow links",
            "100/100"
        )
