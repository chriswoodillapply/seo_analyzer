#!/usr/bin/env python3
"""
Demo script to showcase SEO Analyzer capabilities with new architecture

This script demonstrates:
1. Positive analysis (good website)
2. Error handling
3. Multiple URL analysis
4. Report generation
"""

from src.core.seo_orchestrator import SEOOrchestrator
from src.reporters.report_generator import ReportGenerator
from rich.console import Console
from rich.panel import Panel

def demo_single_url_analysis():
    """Demo single URL analysis"""
    console = Console()
    
    console.print(Panel.fit("[bold cyan]Demo: Single URL Analysis[/bold cyan]"))
    
    test_url = "https://www.applydigital.com/"
    console.print(f"\nAnalyzing: {test_url}")
    
    with SEOOrchestrator(enable_javascript=False) as orchestrator:
        results = orchestrator.analyze_single_url(test_url)
        
        if results:
            console.print(f"\n[green]>> Analysis Complete[/green]")
            console.print(f"  Total tests run: {len(results)}")
            
            # Count by status
            pass_count = sum(1 for r in results if r.status.value == 'PASS')
            fail_count = sum(1 for r in results if r.status.value == 'FAIL')
            warning_count = sum(1 for r in results if r.status.value == 'WARNING')
            
            console.print(f"  Pass: {pass_count}")
            console.print(f"  Fail: {fail_count}")
            console.print(f"  Warning: {warning_count}")
            
            # Show a few test results
            console.print(f"\n[bold]Sample Test Results:[/bold]")
            for result in results[:5]:
                status_color = {
                    'PASS': 'green',
                    'FAIL': 'red',
                    'WARNING': 'yellow'
                }.get(result.status.value, 'white')
                
                console.print(f"  [{status_color}]{result.status.value}[/{status_color}] - {result.test_id}")
        else:
            console.print("[red]>> Analysis failed[/red]")

def demo_multiple_urls():
    """Demo multiple URL analysis"""
    console = Console()
    
    console.print(Panel.fit("[bold cyan]Demo: Multiple URL Analysis[/bold cyan]"))
    
    test_urls = [
        "https://www.applydigital.com/",
        "https://www.applydigital.com/work"
    ]
    
    console.print(f"\nAnalyzing {len(test_urls)} URLs...")
    
    with SEOOrchestrator(enable_javascript=False) as orchestrator:
        summary = orchestrator.analyze_multiple_urls(test_urls)
        
        console.print(f"\n[bold]Analysis Summary:[/bold]")
        console.print(f"  Total URLs: {summary.get('total_urls', 0)}")
        console.print(f"  Successful: {summary.get('successful', 0)}")
        console.print(f"  Failed: {summary.get('failed', 0)}")

def demo_error_handling():
    """Demo error handling for 404 pages"""
    console = Console()
    
    console.print(Panel.fit("[bold cyan]Demo: Error Handling (404 Detection)[/bold cyan]"))
    
    error_url = "https://www.applydigital.com/this-does-not-exist"
    console.print(f"\nTesting 404 URL: {error_url}")
    
    with SEOOrchestrator(enable_javascript=False) as orchestrator:
        results = orchestrator.analyze_single_url(error_url)
        
        if results:
            # Look for HTTP status tests
            http_tests = [r for r in results if 'http' in r.test_id.lower() or 'status' in r.test_id.lower()]
            
            if http_tests:
                console.print(f"\n[bold]HTTP Status Tests:[/bold]")
                for test in http_tests:
                    status_color = 'red' if test.status.value == 'FAIL' else 'yellow'
                    console.print(f"  [{status_color}]{test.status.value}[/{status_color}] - {test.test_id}")
                    if test.details:
                        console.print(f"    Details: {test.details}")
            else:
                console.print("[yellow]>> No HTTP status tests found in results[/yellow]")
        else:
            console.print("[red]>> Analysis failed (expected for 404)[/red]")

def main():
    """Main demo function"""
    console = Console()
    
    console.print("[bold cyan]SEO Analyzer - New Architecture Demo[/bold cyan]\n")
    
    # Run demos
    try:
        demo_single_url_analysis()
        print("\n" + "="*60 + "\n")
        
        demo_multiple_urls()
        print("\n" + "="*60 + "\n")
        
        demo_error_handling()
        print("\n" + "="*60 + "\n")
        
        console.print("[bold green]>> Demo completed successfully![/bold green]")
        console.print("\n[green]The new SEO Analyzer architecture includes:[/green]")
        console.print("  >> SEOOrchestrator: High-level analysis coordination")
        console.print("  >> ContentFetcher: HTML and JavaScript rendering")
        console.print("  >> SEOTestExecutor: Modular test execution")
        console.print("  >> ReportGenerator: Multi-format report generation")
        
    except Exception as e:
        console.print(f"[red]>> Demo encountered an error: {e}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
