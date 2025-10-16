#!/usr/bin/env python3
"""
axe-core Accessibility Testing Integration

This module integrates Deque's axe-core accessibility testing engine
to provide comprehensive WCAG compliance checking.
"""

from typing import Dict, List, Any, Optional
from playwright.sync_api import Page
import json


class AxeCoreIntegration:
    """
    Integration with axe-core for accessibility testing.
    
    axe-core is the world's leading digital accessibility toolkit.
    It checks for WCAG 2.0, WCAG 2.1, Section 508, and other accessibility standards.
    """
    
    # axe-core CDN URL (use latest stable version)
    AXE_CORE_SCRIPT_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.2/axe.min.js"
    
    @staticmethod
    def inject_axe_core(page: Page) -> bool:
        """
        Inject axe-core library into the page.
        
        Args:
            page: Playwright Page object
            
        Returns:
            True if injection successful, False otherwise
        """
        try:
            # Load axe-core from CDN
            page.add_script_tag(url=AxeCoreIntegration.AXE_CORE_SCRIPT_URL)
            
            # Wait for axe to be available
            page.wait_for_function("typeof axe !== 'undefined'", timeout=5000)
            
            return True
        except Exception as e:
            print(f"Error injecting axe-core: {e}")
            return False
    
    @staticmethod
    def run_axe_scan(page: Page, options: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Run axe-core accessibility scan on the current page.
        
        Args:
            page: Playwright Page object (must have axe-core injected)
            options: Optional axe configuration (tags, rules, etc.)
            
        Returns:
            Dictionary with axe results including violations, passes, incomplete, and inapplicable
        """
        if options is None:
            options = {}
        
        try:
            # Run axe.run() and return results
            results = page.evaluate("""
                (options) => {
                    return axe.run(document, options);
                }
            """, options)
            
            return results
        except Exception as e:
            print(f"Error running axe scan: {e}")
            return {
                'violations': [],
                'passes': [],
                'incomplete': [],
                'inapplicable': [],
                'error': str(e)
            }
    
    @staticmethod
    def format_axe_results(results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format axe results into a more digestible summary.
        
        Args:
            results: Raw axe-core results
            
        Returns:
            Formatted summary with counts, severity breakdown, and top issues
        """
        violations = results.get('violations', [])
        passes = results.get('passes', [])
        incomplete = results.get('incomplete', [])
        
        # Count violations by severity
        severity_counts = {
            'critical': 0,
            'serious': 0,
            'moderate': 0,
            'minor': 0
        }
        
        for violation in violations:
            impact = violation.get('impact', 'minor')
            severity_counts[impact] = severity_counts.get(impact, 0) + len(violation.get('nodes', []))
        
        # Get top 10 violations
        top_violations = []
        for violation in violations[:10]:
            top_violations.append({
                'id': violation.get('id'),
                'impact': violation.get('impact'),
                'description': violation.get('description'),
                'help': violation.get('help'),
                'helpUrl': violation.get('helpUrl'),
                'nodes_affected': len(violation.get('nodes', []))
            })
        
        return {
            'total_violations': sum(len(v.get('nodes', [])) for v in violations),
            'total_violation_types': len(violations),
            'total_passes': len(passes),
            'total_incomplete': len(incomplete),
            'severity_breakdown': severity_counts,
            'top_violations': top_violations,
            'timestamp': results.get('timestamp'),
            'url': results.get('url')
        }
    
    @staticmethod
    def get_wcag_level_violations(results: Dict[str, Any], level: str = 'AA') -> List[Dict]:
        """
        Filter violations by WCAG level (A, AA, AAA).
        
        Args:
            results: Raw axe-core results
            level: WCAG level to filter ('A', 'AA', or 'AAA')
            
        Returns:
            List of violations matching the WCAG level
        """
        violations = results.get('violations', [])
        filtered = []
        
        wcag_tag = f'wcag{level.lower()}'
        
        for violation in violations:
            tags = violation.get('tags', [])
            if wcag_tag in tags or f'wcag2{level.lower()}' in tags:
                filtered.append(violation)
        
        return filtered


def run_full_accessibility_audit(page: Page) -> Dict[str, Any]:
    """
    Run a comprehensive accessibility audit on a page.
    
    This is a convenience function that:
    1. Injects axe-core
    2. Runs the scan
    3. Formats results
    4. Returns a comprehensive report
    
    Args:
        page: Playwright Page object
        
    Returns:
        Comprehensive accessibility audit report
    """
    integration = AxeCoreIntegration()
    
    # Inject axe-core
    if not integration.inject_axe_core(page):
        return {
            'error': 'Failed to inject axe-core',
            'success': False
        }
    
    # Run scan with WCAG 2.1 AA rules
    options = {
        'runOnly': {
            'type': 'tag',
            'values': ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
        }
    }
    
    results = integration.run_axe_scan(page, options)
    summary = integration.format_axe_results(results)
    
    return {
        'success': True,
        'summary': summary,
        'full_results': results
    }

