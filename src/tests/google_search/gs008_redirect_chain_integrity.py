#!/usr/bin/env python3
"""
GS008: Redirect Chain Integrity Test

Validates redirect chains to ensure they end at canonical with 200 status
and no redirect loops.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import requests
from urllib.parse import urlparse, urljoin


class RedirectChainIntegrityTest(SEOTest):
    """Test to validate redirect chain integrity"""
    
    @property
    def test_id(self) -> str:
        return "GS008"
    
    @property
    def test_name(self) -> str:
        return "Redirect Chain Integrity"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the redirect chain integrity test"""
        results = []
        
        # Check redirect chain
        chain_result = self._check_redirect_chain(content)
        results.append(chain_result)
        
        # Check for redirect loops
        loop_result = self._check_redirect_loops(content)
        results.append(loop_result)
        
        # Check final destination
        destination_result = self._check_final_destination(content)
        results.append(destination_result)
        
        return results
    
    def _check_redirect_chain(self, content: PageContent) -> TestResult:
        """Check redirect chain for proper 301 redirects"""
        url = content.url
        
        try:
            # Follow redirects with limited hops
            response = requests.head(url, allow_redirects=True, timeout=10)
            
            # Check if there were redirects
            if response.url != url:
                redirect_count = len(response.history)
                
                if redirect_count > 3:
                    return self._create_result(
                        content,
                        TestStatus.WARNING,
                        f"Long redirect chain detected ({redirect_count} hops)",
                        "Consider shortening redirect chain to improve performance",
                        "60/100"
                    )
                
                # Check if all redirects are 301
                non_301_redirects = [r for r in response.history if r.status_code != 301]
                if non_301_redirects:
                    return self._create_result(
                        content,
                        TestStatus.WARNING,
                        f"Non-301 redirects found in chain: {[r.status_code for r in non_301_redirects]}",
                        "Use 301 redirects for permanent redirects",
                        "70/100"
                    )
                
                return self._create_result(
                    content,
                    TestStatus.PASS,
                    f"Redirect chain is proper ({redirect_count} hops, all 301)",
                    "Redirect chain follows best practices",
                    "100/100"
                )
            
            return self._create_result(
                content,
                TestStatus.PASS,
                "No redirects detected",
                "URL is direct access",
                "100/100"
            )
            
        except requests.exceptions.TooManyRedirects:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "Too many redirects detected",
                "Fix redirect loop or excessive redirects",
                "0/100"
            )
        except requests.exceptions.RequestException as e:
            return self._create_result(
                content,
                TestStatus.ERROR,
                f"Error checking redirects: {str(e)}",
                "Verify URL accessibility",
                "0/100"
            )
    
    def _check_redirect_loops(self, content: PageContent) -> TestResult:
        """Check for redirect loops"""
        url = content.url
        
        try:
            # Check for redirect loops by following redirects manually
            visited_urls = set()
            current_url = url
            redirect_count = 0
            max_redirects = 10
            
            while redirect_count < max_redirects:
                if current_url in visited_urls:
                    return self._create_result(
                        content,
                        TestStatus.FAIL,
                        f"Redirect loop detected: {current_url}",
                        "Fix redirect loop in server configuration",
                        "0/100"
                    )
                
                visited_urls.add(current_url)
                
                response = requests.head(current_url, allow_redirects=False, timeout=10)
                
                if response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get('Location')
                    if location:
                        current_url = urljoin(current_url, location)
                        redirect_count += 1
                    else:
                        break
                else:
                    break
            
            if redirect_count >= max_redirects:
                return self._create_result(
                    content,
                    TestStatus.WARNING,
                    f"Maximum redirects reached ({max_redirects})",
                    "Check for potential redirect issues",
                    "60/100"
                )
            
            return self._create_result(
                content,
                TestStatus.PASS,
                f"No redirect loops detected ({redirect_count} redirects followed)",
                "Redirect chain is clean",
                "100/100"
            )
            
        except requests.exceptions.RequestException as e:
            return self._create_result(
                content,
                TestStatus.ERROR,
                f"Error checking for redirect loops: {str(e)}",
                "Verify URL accessibility",
                "0/100"
            )
    
    def _check_final_destination(self, content: PageContent) -> TestResult:
        """Check final destination of redirect chain"""
        url = content.url
        
        try:
            response = requests.get(url, allow_redirects=True, timeout=10)
            final_url = response.url
            final_status = response.status_code
            
            if final_status != 200:
                return self._create_result(
                    content,
                    TestStatus.FAIL,
                    f"Redirect chain ends with non-200 status: {final_status}",
                    "Fix redirect chain to end with 200 status",
                    "0/100"
                )
            
            # Check if final URL is different from original
            if final_url != url:
                return self._create_result(
                    content,
                    TestStatus.INFO,
                    f"Redirect chain ends at: {final_url}",
                    "Monitor canonical URL consistency",
                    "90/100"
                )
            
            return self._create_result(
                content,
                TestStatus.PASS,
                f"Redirect chain ends with 200 status at: {final_url}",
                "Redirect chain is properly configured",
                "100/100"
            )
            
        except requests.exceptions.RequestException as e:
            return self._create_result(
                content,
                TestStatus.ERROR,
                f"Error checking final destination: {str(e)}",
                "Verify URL accessibility",
                "0/100"
            )
