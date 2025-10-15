#!/usr/bin/env python3
"""
Test error handling for HTTP errors (404, 500, etc.)
"""

from seo_analyzer import SEOAnalyzer
import pandas as pd

# Test URLs with known errors
test_urls = [
    ("https://www.applydigital.com/events/advertising-week-new-york-2025", "500 Server Error"),
    ("https://www.applydigital.com/this-page-does-not-exist", "404 Not Found"),
    ("https://www.applydigital.com/", "200 OK (working page)")
]

print("Testing HTTP Error Handling\n" + "="*80)

for url, expected in test_urls:
    print(f"\nTesting: {url}")
    print(f"Expected: {expected}")
    print("-" * 80)
    
    # Analyze URL
    analyzer = SEOAnalyzer(url, timeout=15, use_axe=False)
    analyzer.run_analysis()
    
    # Get flattened results
    rows = analyzer._flatten_results_to_rows()
    
    # Convert to DataFrame for easy viewing
    df = pd.DataFrame(rows)
    
    # Show HTTP status test results
    http_status_rows = df[df['Category'] == 'Http Status']
    
    if len(http_status_rows) > 0:
        print(f"\n✓ HTTP Status Test Results:")
        for _, row in http_status_rows.iterrows():
            print(f"  Status: {row['Severity']}")
            print(f"  Issue: {row['Issue_Description']}")
            print(f"  Recommendation: {row['Recommendation']}")
    else:
        print(f"\n✓ Page loaded successfully (HTTP 200)")
        print(f"  Total test rows: {len(df)}")
        print(f"  Categories tested: {df['Category'].nunique()}")
    
    # Show overall status
    overall = df[df['Category'] == 'Overall Status']
    if len(overall) > 0:
        print(f"\n  Overall Status: {overall.iloc[0]['Severity']}")
        print(f"  Description: {overall.iloc[0]['Issue_Description']}")

print("\n" + "="*80)
print("Test complete!")

