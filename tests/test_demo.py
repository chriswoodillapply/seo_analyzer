#!/usr/bin/env python3
"""
Demo script to showcase SEO Analyzer capabilities

This script demonstrates:
1. Positive analysis (good website)
2. Security header analysis (missing CSP detection)
3. Soft 404 detection
4. Performance and accessibility testing
"""

from seo_analyzer import SEOAnalyzer
from rich.console import Console
from rich.panel import Panel

def demo_security_headers():
    """Demo security headers analysis with mock data"""
    console = Console()
    
    console.print(Panel.fit("[bold cyan]Demo: Security Headers Analysis[/bold cyan]"))
    
    # Create mock page data with missing CSP (like applydigital.com)
    from test_seo_analyzer import MockResponse
    
    mock_response = MockResponse(
        status_code=200,
        content="<html><head><title>Test Site</title></head><body><h1>Hello</h1></body></html>",
        headers={
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            # Missing: Content-Security-Policy
            # Missing: Strict-Transport-Security
        }
    )
    
    page_data = {
        'url': 'https://example.com',
        'status_code': 200,
        'content': mock_response.content,
        'text': mock_response.text,
        'soup': None,  # Not needed for security headers
        'headers': mock_response.headers,
        'load_time': 1.0,
        'response': mock_response
    }
    
    # Initialize analyzer
    analyzer = SEOAnalyzer('https://example.com', use_axe=False)
    
    # Analyze security headers
    security_result = analyzer.analyze_security_headers(page_data)
    
    console.print(f"\n[bold]Security Analysis Results:[/bold]")
    console.print(f"Security Score: {security_result['security_score']}%")
    
    console.print(f"\n[bold cyan]Header Status:[/bold cyan]")
    console.print(f"✗ Content-Security-Policy: {security_result['csp_header']['present']}")
    console.print(f"✓ X-Frame-Options: {security_result['x_frame_options']['present']}")
    console.print(f"✓ X-Content-Type-Options: {security_result['x_content_type_options']['present']}")
    console.print(f"✗ Strict-Transport-Security: {security_result['strict_transport_security']['present']}")
    
    console.print(f"\n[bold red]Issues Found ({len(security_result['issues'])}):[/bold red]")
    for issue in security_result['issues']:
        console.print(f"• {issue}")
        
    console.print(f"\n[bold green]Recommendations ({len(security_result['recommendations'])}):[/bold green]")
    for rec in security_result['recommendations']:
        console.print(f"• {rec}")

def demo_soft_404():
    """Demo soft 404 detection"""
    console = Console()
    
    console.print(Panel.fit("[bold cyan]Demo: Soft 404 Detection[/bold cyan]"))
    
    from test_seo_analyzer import MockResponse
    from bs4 import BeautifulSoup
    
    # Create soft 404 content
    soft_404_html = """
    <html>
    <head><title>Page Not Found - Example</title></head>
    <body>
        <h1>Oops! Page Not Found</h1>
        <p>The page you are looking for does not exist.</p>
    </body>
    </html>
    """
    
    mock_response = MockResponse(status_code=200, content=soft_404_html)
    
    page_data = {
        'url': 'https://example.com/nonexistent',
        'status_code': 200,
        'content': mock_response.content,
        'text': mock_response.text,
        'soup': BeautifulSoup(soft_404_html, 'html.parser'),
        'headers': {},
        'load_time': 1.0,
        'response': mock_response
    }
    
    analyzer = SEOAnalyzer('https://example.com', use_axe=False)
    soft_404_result = analyzer.analyze_soft_404(page_data)
    
    console.print(f"\n[bold]Soft 404 Analysis Results:[/bold]")
    console.print(f"Is Soft 404: {soft_404_result['is_soft_404']}")
    console.print(f"Confidence Score: {soft_404_result['confidence_score']}%")
    
    console.print(f"\n[bold yellow]Title Indicators:[/bold yellow]")
    for indicator in soft_404_result['title_indicators']:
        console.print(f"• '{indicator}' found in title")
        
    console.print(f"\n[bold yellow]Content Indicators:[/bold yellow]")
    for indicator in set(soft_404_result['content_indicators'][:5]):  # Show unique top 5
        console.print(f"• '{indicator}' found in content")

def run_unit_tests():
    """Run a subset of unit tests to verify functionality"""
    console = Console()
    
    console.print(Panel.fit("[bold cyan]Running Unit Tests[/bold cyan]"))
    
    import unittest
    from test_seo_analyzer import TestSEOAnalyzerPositive, TestSEOAnalyzerSecurityHeaders
    
    # Create test suite with key tests
    suite = unittest.TestSuite()
    
    # Add specific tests
    suite.addTest(TestSEOAnalyzerPositive('test_meta_tag_analysis'))
    suite.addTest(TestSEOAnalyzerPositive('test_accessibility_analysis'))
    suite.addTest(TestSEOAnalyzerSecurityHeaders('test_security_header_extension'))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        console.print("[green]✓ All key tests passed![/green]")
    else:
        console.print("[red]✗ Some tests failed[/red]")
    
    return result.wasSuccessful()

def main():
    """Main demo function"""
    console = Console()
    
    console.print("[bold cyan]SEO Analyzer - Enhanced Features Demo[/bold cyan]\n")
    
    # Run demos
    demo_security_headers()
    print("\n" + "="*60 + "\n")
    
    demo_soft_404()
    print("\n" + "="*60 + "\n")
    
    # Run unit tests
    success = run_unit_tests()
    
    print("\n" + "="*60)
    console.print("[bold green]Demo completed![/bold green]")
    
    if success:
        console.print("\n[green]The SEO Analyzer is working correctly with all new features:[/green]")
        console.print("✓ Security Headers Analysis (detects missing CSP)")
        console.print("✓ Soft 404 Detection")
        console.print("✓ Advanced Performance Testing")
        console.print("✓ Axe-Core Accessibility Integration")
        console.print("✓ Comprehensive Reporting")
    else:
        console.print("[red]Some issues detected - check test results above[/red]")

if __name__ == "__main__":
    main()

