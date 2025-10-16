#!/usr/bin/env python3
"""
Test error handling for HTTP errors (404, 500, etc.)
"""

from src.core.seo_orchestrator import SEOOrchestrator
from src.reporters.report_generator import ReportGenerator
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
    
    # Analyze URL using new orchestrator
    with SEOOrchestrator(enable_javascript=False) as orchestrator:
        test_results = orchestrator.analyze_single_url(url)
    
    # Convert results to DataFrame
    if test_results:
        rows = [result.to_dict() for result in test_results]
        df = pd.DataFrame(rows)
        
        # Show HTTP status test results
        http_status_rows = df[df['Category'] == 'Technical SEO']
        
        if len(http_status_rows) > 0:
            print(f"\n>> HTTP Status Test Results:")
            for _, row in http_status_rows.iterrows():
                if 'http' in row['Test_Name'].lower() or 'status' in row['Test_Name'].lower():
                    print(f"  Status: {row['Severity']}")
                    print(f"  Test: {row['Test_Name']}")
                    print(f"  Result: {row['Status']}")
        else:
            print(f"\n>> Page loaded successfully")
            print(f"  Total tests: {len(df)}")
            print(f"  Categories tested: {df['Category'].nunique()}")
            
            # Count pass/fail/warning
            status_counts = df['Status'].value_counts()
            print(f"  Pass: {status_counts.get('PASS', 0)}")
            print(f"  Fail: {status_counts.get('FAIL', 0)}")
            print(f"  Warning: {status_counts.get('WARNING', 0)}")
    else:
        print(f"\n>> No results (likely error fetching page)")

print("\n" + "="*80)
print("Test complete!")

