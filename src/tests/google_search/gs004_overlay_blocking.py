#!/usr/bin/env python3
"""
GS004: Overlay Blocking Test

Detects blocking overlays (splash screens, cookie dialogs) that may
prevent Googlebot from accessing main content.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re


class OverlayBlockingTest(SEOTest):
    """Test to detect blocking overlays"""
    
    @property
    def test_id(self) -> str:
        return "GS004"
    
    @property
    def test_name(self) -> str:
        return "Overlay Blocking"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the overlay blocking test"""
        results = []
        
        # Check for splash screens
        splash_result = self._check_splash_screens(content)
        results.append(splash_result)
        
        # Check for cookie dialogs
        cookie_result = self._check_cookie_dialogs(content)
        results.append(cookie_result)
        
        # Check for modal dialogs
        modal_result = self._check_modal_dialogs(content)
        results.append(modal_result)
        
        # Check for viewport blocking
        viewport_result = self._check_viewport_blocking(content)
        results.append(viewport_result)
        
        return results
    
    def _check_splash_screens(self, content: PageContent) -> TestResult:
        """Check for splash screens that may block content"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Look for splash screen indicators
        splash_indicators = [
            r'splash',
            r'loading',
            r'loader',
            r'spinner',
            r'overlay'
        ]
        
        splash_elements = []
        for indicator in splash_indicators:
            elements = soup.find_all(class_=re.compile(indicator, re.I))
            splash_elements.extend(elements)
        
        if not splash_elements:
            return self._create_result(
                content,
                TestStatus.PASS,
                "No splash screen detected",
                "Page is accessible without splash screen blocking",
                "100/100"
            )
        
        # Check if splash screen is visible/blocking
        blocking_indicators = []
        for element in splash_elements:
            # Check for visibility styles
            style = element.get('style', '')
            if 'display: none' not in style and 'visibility: hidden' not in style:
                blocking_indicators.append(f"Visible splash element: {element.get('class', [])}")
            
            # Check for z-index that might block content
            if 'z-index' in style:
                blocking_indicators.append(f"High z-index splash: {style}")
        
        if blocking_indicators:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Splash screen may be blocking content: {'; '.join(blocking_indicators)}",
                "Remove or modify splash screen to not block Googlebot",
                "0/100"
            )
        
        return self._create_result(
            content,
            TestStatus.WARNING,
            f"Splash screen detected but may not be blocking ({len(splash_elements)} elements)",
            "Monitor splash screen behavior for Googlebot",
            "70/100"
        )
    
    def _check_cookie_dialogs(self, content: PageContent) -> TestResult:
        """Check for cookie consent dialogs that may block content"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Look for cookie dialog indicators
        cookie_indicators = [
            r'cookie',
            r'consent',
            r'privacy',
            r'gdpr',
            r'ccpa'
        ]
        
        cookie_elements = []
        for indicator in cookie_indicators:
            # Check by class name
            elements = soup.find_all(class_=re.compile(indicator, re.I))
            cookie_elements.extend(elements)
            
            # Check by data attributes
            elements = soup.find_all(attrs={'data-testid': re.compile(indicator, re.I)})
            cookie_elements.extend(elements)
            
            # Check by id
            elements = soup.find_all(id=re.compile(indicator, re.I))
            cookie_elements.extend(elements)
        
        if not cookie_elements:
            return self._create_result(
                content,
                TestStatus.PASS,
                "No cookie dialog detected",
                "Page is accessible without cookie dialog blocking",
                "100/100"
            )
        
        # Check for blocking cookie dialogs
        blocking_indicators = []
        for element in cookie_elements:
            # Check for modal/dialog attributes
            if element.get('role') == 'dialog' or 'modal' in element.get('class', []):
                blocking_indicators.append(f"Modal cookie dialog: {element.get('class', [])}")
            
            # Check for high z-index
            style = element.get('style', '')
            if 'z-index' in style and any(z in style for z in ['999', '9999', '1000']):
                blocking_indicators.append(f"High z-index cookie dialog: {style}")
            
            # Check for fixed positioning
            if 'position: fixed' in style or 'position: absolute' in style:
                blocking_indicators.append(f"Fixed position cookie dialog: {style}")
        
        if blocking_indicators:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Cookie dialog may be blocking content: {'; '.join(blocking_indicators)}",
                "Implement cookie consent that doesn't block Googlebot",
                "0/100"
            )
        
        return self._create_result(
            content,
            TestStatus.WARNING,
            f"Cookie dialog detected but may not be blocking ({len(cookie_elements)} elements)",
            "Monitor cookie dialog behavior for Googlebot",
            "70/100"
        )
    
    def _check_modal_dialogs(self, content: PageContent) -> TestResult:
        """Check for modal dialogs that may block content"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Look for modal dialog indicators
        modal_elements = soup.find_all(attrs={'role': 'dialog'})
        modal_elements.extend(soup.find_all(class_=re.compile(r'modal|dialog|popup', re.I)))
        modal_elements.extend(soup.find_all(id=re.compile(r'modal|dialog|popup', re.I)))
        
        if not modal_elements:
            return self._create_result(
                content,
                TestStatus.PASS,
                "No modal dialogs detected",
                "Page is accessible without modal blocking",
                "100/100"
            )
        
        # Check for blocking modals
        blocking_indicators = []
        for element in modal_elements:
            # Check for visibility
            style = element.get('style', '')
            if 'display: none' not in style and 'visibility: hidden' not in style:
                blocking_indicators.append(f"Visible modal: {element.get('class', [])}")
            
            # Check for backdrop/overlay
            if 'backdrop' in element.get('class', []) or 'overlay' in element.get('class', []):
                blocking_indicators.append(f"Modal backdrop detected: {element.get('class', [])}")
        
        if blocking_indicators:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Modal dialogs detected: {'; '.join(blocking_indicators)}",
                "Ensure modals don't block Googlebot from accessing main content",
                "60/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Modal dialogs detected but not blocking ({len(modal_elements)} elements)",
            "Modal dialogs appear to be properly handled",
            "100/100"
        )
    
    def _check_viewport_blocking(self, content: PageContent) -> TestResult:
        """Check for viewport blocking elements"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Look for elements that might block the viewport
        blocking_elements = []
        
        # Check for full-screen overlays
        fullscreen_elements = soup.find_all(attrs={'style': re.compile(r'position:\s*fixed|position:\s*absolute', re.I)})
        for element in fullscreen_elements:
            style = element.get('style', '')
            if any(prop in style for prop in ['top: 0', 'left: 0', 'width: 100%', 'height: 100%']):
                blocking_elements.append(f"Full-screen element: {element.get('class', [])}")
        
        # Check for high z-index elements
        high_z_elements = soup.find_all(attrs={'style': re.compile(r'z-index:\s*[5-9]\d{2,}', re.I)})
        for element in high_z_elements:
            blocking_elements.append(f"High z-index element: {element.get('class', [])}")
        
        if not blocking_elements:
            return self._create_result(
                content,
                TestStatus.PASS,
                "No viewport blocking elements detected",
                "Page viewport is accessible",
                "100/100"
            )
        
        return self._create_result(
            content,
            TestStatus.WARNING,
            f"Potential viewport blocking elements: {'; '.join(blocking_elements)}",
            "Review elements that may block the viewport",
            "70/100"
        )
