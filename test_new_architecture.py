#!/usr/bin/env python3
"""
Test the new SEO test architecture with Strategy Pattern and Dependency Injection.

This script demonstrates:
1. Creating individual test classes
2. Registering tests with the registry
3. Executing tests with the new executor
4. Getting results and statistics
"""

from bs4 import BeautifulSoup
from src.core.test_interface import PageContent
from src.core.test_registry import TestRegistry
from src.core.test_executor_v2 import SEOTestExecutorV2

# Import the migrated test classes
from src.tests.meta_tags.title_presence import TitlePresenceTest
from src.tests.meta_tags.title_length import TitleLengthTest
from src.tests.meta_tags.description_presence import DescriptionPresenceTest
from src.tests.meta_tags.description_length import DescriptionLengthTest
from src.tests.meta_tags.canonical_url import CanonicalURLTest
from src.tests.meta_tags.robots_meta import RobotsMetaTest
from src.tests.meta_tags.viewport import ViewportTest
from src.tests.meta_tags.open_graph import OpenGraphTest


def create_test_content():
    """Create sample page content for testing"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>SEO Architecture Test - Welcome to Our Site</title>
        <meta name="description" content="This is a comprehensive test of our new SEO architecture using the Strategy Pattern with dependency injection. It demonstrates clean, maintainable code.">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="robots" content="index, follow">
        <link rel="canonical" href="https://example.com/test">
        <meta property="og:title" content="SEO Test Page">
        <meta property="og:description" content="Testing Open Graph">
        <meta property="og:image" content="https://example.com/image.jpg">
    </head>
    <body>
        <h1>Welcome</h1>
        <p>Test content</p>
    </body>
    </html>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    return PageContent(
        url="https://example.com/test",
        static_html=html,
        static_soup=soup,
        rendered_html=html,
        rendered_soup=soup,
        static_headers={},
        static_load_time=0.5,
        rendered_load_time=1.0,
        performance_metrics={},
        core_web_vitals={}
    )


def main():
    print("="*70)
    print("  Testing New SEO Test Architecture")
    print("="*70)
    
    # 1. Create test registry
    print("\n[1] Creating Test Registry...")
    registry = TestRegistry()
    print(f"   Initial test count: {registry.get_test_count()}")
    
    # 2. Register individual test classes
    print("\n[2] Registering Test Classes...")
    test_classes = [
        TitlePresenceTest(),
        TitleLengthTest(),
        DescriptionPresenceTest(),
        DescriptionLengthTest(),
        CanonicalURLTest(),
        RobotsMetaTest(),
        ViewportTest(),
        OpenGraphTest(),
    ]
    
    for test in test_classes:
        registry.register(test)
        print(f"   Registered: {test.test_id} ({test.test_name})")
    
    print(f"\n   Total tests registered: {registry.get_test_count()}")
    print(f"   Categories: {', '.join(registry.get_categories())}")
    
    # 3. Create executor with the registry
    print("\n[3] Creating Test Executor V2...")
    executor = SEOTestExecutorV2(registry)
    print(f"   Executor initialized with {executor.get_test_count()} tests")
    
    # 4. Create test content
    print("\n[4] Creating Test Content...")
    content = create_test_content()
    print(f"   Test URL: {content.url}")
    
    # 5. Execute all tests
    print("\n[5] Executing All Tests...")
    results = executor.execute_all_tests(content)
    print(f"   Tests executed: {len(results)}")
    
    # 6. Display results
    print("\n[6] Test Results:")
    print("-" * 70)
    for result in results:
        status_symbol = {
            "Pass": "[PASS]",
            "Fail": "[FAIL]",
            "Warning": "[WARN]",
            "Info": "[INFO]"
        }.get(result.status.value, "[?]")
        
        print(f"   {status_symbol} {result.test_name}")
        print(f"      Status: {result.status.value} | Score: {result.score}")
        if result.status.value in ["Fail", "Warning"]:
            print(f"      Issue: {result.issue_description}")
    
    # 7. Get statistics
    print("\n[7] Statistics:")
    print("-" * 70)
    stats = executor.get_statistics()
    print(f"   Total Tests: {stats['total_tests']}")
    print(f"   Passed: {stats['passed']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Warnings: {stats['warnings']}")
    print(f"   Info: {stats['info']}")
    print(f"   Pass Rate: {stats['pass_rate']:.1f}%")
    
    # 8. Test category-specific execution
    print("\n[8] Testing Category-Specific Execution...")
    meta_results = executor.execute_tests_by_category(content, "Meta Tags")
    print(f"   Meta Tags tests executed: {len(meta_results)}")
    
    # 9. Test specific test execution
    print("\n[9] Testing Specific Test Execution...")
    specific_results = executor.execute_specific_tests(
        content, 
        ["meta_title_presence", "meta_description_presence"]
    )
    print(f"   Specific tests executed: {len(specific_results)}")
    
    print("\n" + "="*70)
    print("  [SUCCESS] Architecture Test Complete!")
    print("="*70)
    
    print("\nKey Benefits of New Architecture:")
    print("  [+] Each test is a separate, testable class")
    print("  [+] Easy to add new tests without modifying core code")
    print("  [+] Better separation of concerns")
    print("  [+] Dependency injection for flexibility")
    print("  [+] Can execute all, by category, or specific tests")
    print("  [+] Follows SOLID principles")
    

if __name__ == "__main__":
    main()

