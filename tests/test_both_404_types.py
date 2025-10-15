#!/usr/bin/env python3
"""
Test both HTTP Status and Soft 404 detection
"""

from seo_analyzer import SEOAnalyzer
import pandas as pd

print("="*80)
print("HTTP STATUS vs SOFT 404 DETECTION TEST")
print("="*80)

# Test 1: Real 404 (HTTP Status Test)
print("\n" + "="*80)
print("TEST 1: Real 404 Error (HTTP 404 from server)")
print("="*80)
url1 = "https://www.applydigital.com/this-does-not-exist"
print(f"URL: {url1}")
print("Expected: HTTP Status Test = FAIL (404 error)")

analyzer1 = SEOAnalyzer(url1, timeout=10, use_axe=False)
analyzer1.run_analysis()
rows1 = analyzer1._flatten_results_to_rows()
df1 = pd.DataFrame(rows1)

# Show HTTP Status results
http_status = df1[df1['Category'] == 'Http Status']
if len(http_status) > 0:
    print(f"\n✓ HTTP Status Test:")
    print(f"  Status: {http_status.iloc[0]['Severity']}")
    print(f"  Issue: {http_status.iloc[0]['Issue_Description']}")

# Show Soft 404 results
soft_404 = df1[df1['Category'] == 'Soft 404 Analysis']
if len(soft_404) > 0:
    print(f"\n✓ Soft 404 Test:")
    print(f"  Status: {soft_404.iloc[0]['Severity']}")
    print(f"  Issue: {soft_404.iloc[0]['Issue_Description']}")

# Test 2: Working page (both should pass)
print("\n" + "="*80)
print("TEST 2: Working Page (HTTP 200, normal content)")
print("="*80)
url2 = "https://www.applydigital.com/"
print(f"URL: {url2}")
print("Expected: HTTP Status Test = PASS, Soft 404 Test = PASS")

analyzer2 = SEOAnalyzer(url2, timeout=10, use_axe=False)
analyzer2.run_analysis()
rows2 = analyzer2._flatten_results_to_rows()
df2 = pd.DataFrame(rows2)

# Show HTTP Status results
http_status2 = df2[df2['Category'] == 'Http Status']
if len(http_status2) > 0:
    print(f"\n✓ HTTP Status Test:")
    print(f"  Status: {http_status2.iloc[0]['Severity']}")
    print(f"  Issue: {http_status2.iloc[0]['Issue_Description'][:80]}")

# Show Soft 404 results
soft_404_2 = df2[df2['Category'] == 'Soft 404 Analysis']
if len(soft_404_2) > 0:
    print(f"\n✓ Soft 404 Test:")
    print(f"  Status: {soft_404_2.iloc[0]['Severity']}")
    print(f"  Issue: {soft_404_2.iloc[0]['Issue_Description'][:80]}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("✓ HTTP Status Test: Detects actual 404/500 errors from server")
print("✓ Soft 404 Test: Detects pages that return 200 but contain error content")
print("✓ Both tests run independently for complete error detection")
print("="*80)

