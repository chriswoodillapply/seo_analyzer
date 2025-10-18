#!/usr/bin/env python3
"""
GS012: Internal Linking Strength Test

Analyzes internal linking strength to target URL by checking inlinks
from site navigation, sitemap, and other pages.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re
from urllib.parse import urlparse, urljoin


class InternalLinkingStrengthTest(SEOTest):
    """Test to analyze internal linking strength"""
    
    @property
    def test_id(self) -> str:
        return "GS012"
    
    @property
    def test_name(self) -> str:
        return "Internal Linking Strength"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "Medium"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the internal linking strength test"""
        results = []
        
        # Check internal links on current page
        internal_result = self._check_internal_links(content)
        results.append(internal_result)
        
        # Check navigation links
        nav_result = self._check_navigation_links(content)
        results.append(nav_result)
        
        # Check for orphan page indicators
        orphan_result = self._check_orphan_indicators(content)
        results.append(orphan_result)
        
        # Check link quality
        quality_result = self._check_link_quality(content)
        results.append(quality_result)
        
        return results
    
    def _check_internal_links(self, content: PageContent) -> TestResult:
        """Check internal links on the current page"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Find all links
        all_links = soup.find_all('a', href=True)
        internal_links = []
        external_links = []
        
        current_domain = urlparse(content.url).netloc
        
        for link in all_links:
            href = link.get('href', '')
            if not href:
                continue
            
            # Skip anchor links
            if href.startswith('#'):
                continue
            
            # Make absolute URL
            absolute_url = urljoin(content.url, href)
            link_domain = urlparse(absolute_url).netloc
            
            if link_domain == current_domain or not link_domain:
                internal_links.append(absolute_url)
            else:
                external_links.append(absolute_url)
        
        internal_count = len(internal_links)
        external_count = len(external_links)
        total_count = internal_count + external_count
        
        if total_count == 0:
            return self._create_result(
                content,
                TestStatus.WARNING,
                "No links found on page",
                "Add internal links to improve page connectivity",
                "40/100"
            )
        
        if internal_count == 0:
            return self._create_result(
                content,
                TestStatus.WARNING,
                "No internal links found",
                "Add internal links to other pages on the site",
                "50/100"
            )
        
        if internal_count < 3:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Few internal links ({internal_count})",
                "Add more internal links to improve page connectivity",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Good internal linking ({internal_count} internal, {external_count} external)",
            "Page has adequate internal link structure",
            "100/100"
        )
    
    def _check_navigation_links(self, content: PageContent) -> TestResult:
        """Check navigation links"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Find navigation elements
        nav_elements = soup.find_all(['nav', 'header', 'footer'])
        nav_links = []
        
        for nav in nav_elements:
            links = nav.find_all('a', href=True)
            nav_links.extend(links)
        
        if not nav_links:
            return self._create_result(
                content,
                TestStatus.WARNING,
                "No navigation links found",
                "Add navigation links to improve site structure",
                "50/100"
            )
        
        # Check for breadcrumb navigation
        breadcrumbs = soup.find_all(['nav'], class_=re.compile(r'breadcrumb', re.I))
        if not breadcrumbs:
            breadcrumbs = soup.find_all(['ol', 'ul'], class_=re.compile(r'breadcrumb', re.I))
        
        if breadcrumbs:
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Navigation found with breadcrumbs ({len(nav_links)} links)",
                "Page has good navigation structure",
                "100/100"
            )
        
        if len(nav_links) < 5:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Limited navigation links ({len(nav_links)})",
                "Add more navigation links to improve site structure",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Good navigation structure ({len(nav_links)} links)",
            "Page has adequate navigation",
            "90/100"
        )
    
    def _check_orphan_indicators(self, content: PageContent) -> TestResult:
        """Check for orphan page indicators"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Check for orphan page indicators
        orphan_indicators = [
            'orphan',
            'isolated',
            'standalone',
            'no navigation',
            'no links'
        ]
        
        page_text = soup.get_text().lower()
        found_indicators = [indicator for indicator in orphan_indicators if indicator in page_text]
        
        if found_indicators:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Potential orphan page indicators: {', '.join(found_indicators)}",
                "Add internal links to connect page to site structure",
                "60/100"
            )
        
        # Check for very few internal links
        all_links = soup.find_all('a', href=True)
        internal_links = [link for link in all_links if self._is_internal_link(link.get('href', ''), content.url)]
        
        if len(internal_links) < 2:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Very few internal links ({len(internal_links)})",
                "Add more internal links to prevent orphan page classification",
                "50/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"No orphan page indicators found ({len(internal_links)} internal links)",
            "Page appears to be well-connected",
            "100/100"
        )
    
    def _check_link_quality(self, content: PageContent) -> TestResult:
        """Check link quality and anchor text"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Find all links
        all_links = soup.find_all('a', href=True)
        
        if not all_links:
            return self._create_result(
                content,
                TestStatus.WARNING,
                "No links found",
                "Add links to improve page connectivity",
                "40/100"
            )
        
        # Check link quality
        quality_issues = []
        
        for link in all_links:
            href = link.get('href', '')
            anchor_text = link.get_text().strip()
            
            # Check for empty anchor text
            if not anchor_text:
                quality_issues.append("Empty anchor text")
            
            # Check for generic anchor text
            generic_texts = ['click here', 'read more', 'more', 'link', 'here']
            if anchor_text.lower() in generic_texts:
                quality_issues.append(f"Generic anchor text: '{anchor_text}'")
            
            # Check for broken links (basic check)
            if href.startswith('#') and not soup.find(id=href[1:]):
                quality_issues.append(f"Broken anchor link: {href}")
        
        if quality_issues:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Link quality issues: {'; '.join(quality_issues[:3])}",
                "Improve anchor text and fix broken links",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Good link quality ({len(all_links)} links analyzed)",
            "Links have good anchor text and structure",
            "100/100"
        )
    
    def _is_internal_link(self, href: str, current_url: str) -> bool:
        """Check if link is internal"""
        if not href:
            return False
        
        # Skip anchor links
        if href.startswith('#'):
            return False
        
        # Make absolute URL
        absolute_url = urljoin(current_url, href)
        current_domain = urlparse(current_url).netloc
        link_domain = urlparse(absolute_url).netloc
        
        return link_domain == current_domain or not link_domain
