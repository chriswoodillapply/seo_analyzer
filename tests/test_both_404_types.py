#!/usr/bin/env python3
"""
Test both HTTP Status and Soft 404 detection
"""

from src.core.seo_orchestrator import SEOOrchestrator
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

with SEOOrchestrator(enable_javascript=False) as orchestrator:
    results1 = orchestrator.analyze_single_url(url1)
rows1 = [result.to_dict() for result in results1] if results1 else []
df1 = pd.DataFrame(rows1)

# Show HTTP Status results
http_status = df1[df1['Test_Name'].str.contains('HTTP|Status Code', case=False, na=False)]
if len(http_status) > 0:
    print(f"\n>> HTTP Status Test:")
    print(f"  Status: {http_status.iloc[0]['Status']}")
    print(f"  Severity: {http_status.iloc[0]['Severity']}")
    print(f"  Details: {http_status.iloc[0].get('Details', 'N/A')}")

# Show Soft 404 results  
soft_404 = df1[df1['Test_Name'].str.contains('Soft 404|404', case=False, na=False)]
if len(soft_404) > 0:
    print(f"\n>> Soft 404 Test:")
    print(f"  Status: {soft_404.iloc[0]['Status']}")
    print(f"  Severity: {soft_404.iloc[0]['Severity']}")
    print(f"  Details: {soft_404.iloc[0].get('Details', 'N/A')}")

# Test 2: Working page (both should pass)
print("\n" + "="*80)
print("TEST 2: Working Page (HTTP 200, normal content)")
print("="*80)
url2 = "https://www.applydigital.com/"
print(f"URL: {url2}")
print("Expected: HTTP Status Test = PASS, Soft 404 Test = PASS")

with SEOOrchestrator(enable_javascript=False) as orchestrator:
    results2 = orchestrator.analyze_single_url(url2)
rows2 = [result.to_dict() for result in results2] if results2 else []
df2 = pd.DataFrame(rows2)

# Show HTTP Status results
http_status2 = df2[df2['Test_Name'].str.contains('HTTP|Status Code', case=False, na=False)]
if len(http_status2) > 0:
    print(f"\n>> HTTP Status Test:")
    print(f"  Status: {http_status2.iloc[0]['Status']}")
    print(f"  Severity: {http_status2.iloc[0]['Severity']}")

# Show Soft 404 results
soft_404_2 = df2[df2['Test_Name'].str.contains('Soft 404|404', case=False, na=False)]
if len(soft_404_2) > 0:
    print(f"\n>> Soft 404 Test:")
    print(f"  Status: {soft_404_2.iloc[0]['Status']}")
    print(f"  Severity: {soft_404_2.iloc[0]['Severity']}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(">> HTTP Status Test: Detects actual 404/500 errors from server")
print(">> Soft 404 Test: Detects pages that return 200 but contain error content")
print(">> Both tests run independently for complete error detection")
print("="*80)

