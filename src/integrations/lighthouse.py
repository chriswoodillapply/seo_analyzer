#!/usr/bin/env python3
"""
Google Lighthouse Integration

This module integrates Google Lighthouse for comprehensive
performance, accessibility, SEO, and best practices auditing.
"""

from typing import Dict, List, Any, Optional
import subprocess
import json
import tempfile
from pathlib import Path


class LighthouseIntegration:
    """
    Integration with Google Lighthouse.
    
    Lighthouse is an open-source tool from Google for improving the quality of web pages.
    It provides audits for performance, accessibility, progressive web apps, SEO, and more.
    """
    
    @staticmethod
    def check_lighthouse_installed() -> bool:
        """
        Check if Lighthouse CLI is installed.
        
        Returns:
            True if lighthouse is available, False otherwise
        """
        try:
            result = subprocess.run(
                ['lighthouse', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    @staticmethod
    def run_lighthouse(
        url: str,
        output_format: str = 'json',
        categories: Optional[List[str]] = None,
        chrome_flags: Optional[List[str]] = None,
        extra_args: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Run Lighthouse audit on a URL.
        
        Args:
            url: URL to audit
            output_format: Output format ('json', 'html', 'csv')
            categories: List of categories to test (default: all)
            chrome_flags: Additional Chrome flags
            extra_args: Additional Lighthouse CLI arguments
            
        Returns:
            Lighthouse results as dictionary (if json format), or path to output file
        """
        if not LighthouseIntegration.check_lighthouse_installed():
            print("Error: Lighthouse is not installed")
            print("Install with: npm install -g lighthouse")
            return None
        
        # Default categories: performance, accessibility, best-practices, seo
        if categories is None:
            categories = ['performance', 'accessibility', 'best-practices', 'seo']
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{output_format}', delete=False) as f:
            output_path = f.name
        
        # Build command
        cmd = [
            'lighthouse',
            url,
            f'--output={output_format}',
            f'--output-path={output_path}',
            '--quiet',
            '--chrome-flags=--headless'
        ]
        
        # Add categories (comma-separated)
        if categories:
            categories_str = ','.join(categories)
            cmd.append(f'--only-categories={categories_str}')
        
        # Add Chrome flags
        if chrome_flags:
            chrome_flags_str = ' '.join(chrome_flags)
            cmd.append(f'--chrome-flags="{chrome_flags_str}"')
        
        # Add extra arguments
        if extra_args:
            cmd.extend(extra_args)
        
        try:
            # Run Lighthouse
            print(f"Running Lighthouse on {url}...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode != 0:
                print(f"Lighthouse error: {result.stderr}")
                return None
            
            # Read results
            if output_format == 'json':
                with open(output_path, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                
                # Clean up temp file
                Path(output_path).unlink(missing_ok=True)
                
                return results
            else:
                # Return path to output file for HTML/CSV
                return {'output_file': output_path}
                
        except subprocess.TimeoutExpired:
            print(f"Lighthouse timeout after 120 seconds")
            return None
        except Exception as e:
            print(f"Error running Lighthouse: {e}")
            return None
    
    @staticmethod
    def format_lighthouse_results(results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format Lighthouse results into a summary.
        
        Args:
            results: Raw Lighthouse JSON results
            
        Returns:
            Formatted summary with scores and key metrics
        """
        if not results:
            return {}
        
        categories = results.get('categories', {})
        audits = results.get('audits', {})
        
        # Extract category scores (0-100)
        scores = {}
        for cat_name, cat_data in categories.items():
            scores[cat_name] = {
                'score': cat_data.get('score', 0) * 100,  # Convert to percentage
                'title': cat_data.get('title')
            }
        
        # Extract key performance metrics
        performance_metrics = {}
        if 'performance' in categories:
            key_metrics = [
                'first-contentful-paint',
                'largest-contentful-paint',
                'total-blocking-time',
                'cumulative-layout-shift',
                'speed-index'
            ]
            
            for metric in key_metrics:
                if metric in audits:
                    audit = audits[metric]
                    performance_metrics[metric] = {
                        'displayValue': audit.get('displayValue'),
                        'score': audit.get('score', 0) * 100
                    }
        
        # Extract failing audits
        failing_audits = []
        for audit_name, audit_data in audits.items():
            score = audit_data.get('score')
            if score is not None and score < 0.9:  # Less than 90%
                failing_audits.append({
                    'id': audit_name,
                    'title': audit_data.get('title'),
                    'description': audit_data.get('description'),
                    'score': score * 100,
                    'displayValue': audit_data.get('displayValue')
                })
        
        # Sort by score (worst first)
        failing_audits.sort(key=lambda x: x['score'])
        
        return {
            'url': results.get('finalDisplayedUrl', results.get('requestedUrl')),
            'fetch_time': results.get('fetchTime'),
            'user_agent': results.get('userAgent'),
            'scores': scores,
            'performance_metrics': performance_metrics,
            'failing_audits': failing_audits[:20],  # Top 20
            'lighthouse_version': results.get('lighthouseVersion')
        }
    
    @staticmethod
    def get_seo_recommendations(results: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Extract SEO-specific recommendations from Lighthouse results.
        
        Args:
            results: Raw Lighthouse JSON results
            
        Returns:
            List of SEO recommendations
        """
        if not results:
            return []
        
        audits = results.get('audits', {})
        recommendations = []
        
        # SEO-related audits
        seo_audits = [
            'document-title',
            'meta-description',
            'robots-txt',
            'canonical',
            'hreflang',
            'structured-data',
            'crawlable-anchors',
            'link-text'
        ]
        
        for audit_id in seo_audits:
            if audit_id in audits:
                audit = audits[audit_id]
                score = audit.get('score')
                
                if score is not None and score < 1.0:
                    recommendations.append({
                        'audit': audit.get('title'),
                        'description': audit.get('description'),
                        'recommendation': audit.get('displayValue', 'See details'),
                        'severity': 'high' if score < 0.5 else 'medium'
                    })
        
        return recommendations


def run_quick_lighthouse_audit(url: str) -> Optional[Dict[str, Any]]:
    """
    Run a quick Lighthouse audit with default settings.
    
    Args:
        url: URL to audit
        
    Returns:
        Formatted audit summary
    """
    integration = LighthouseIntegration()
    
    # Run Lighthouse
    results = integration.run_lighthouse(url)
    
    if not results:
        return None
    
    # Format results
    summary = integration.format_lighthouse_results(results)
    seo_recs = integration.get_seo_recommendations(results)
    
    return {
        'success': True,
        'summary': summary,
        'seo_recommendations': seo_recs
    }

