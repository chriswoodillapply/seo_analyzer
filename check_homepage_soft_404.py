#!/usr/bin/env python3
"""Check soft 404 result for homepage"""

import pandas as pd

df = pd.read_csv('output/seo_report_20251015_183740.csv')

# Get soft 404 test result
soft_404 = df[df['Test_ID'] == 'soft_404_detection'].iloc[0]

print('\n' + '='*80)
print('  SOFT 404 TEST - HOMEPAGE (Good Page Test)')
print('='*80)
print(f'\nURL: {soft_404["URL"]}')
print(f'Status: {soft_404["Status"]}')
print(f'Score: {soft_404["Score"]}')
print(f'Severity: {soft_404["Severity"]}')
print(f'\nIssue: {soft_404["Issue_Description"]}')
print(f'\nRecommendation: {soft_404["Recommendation"]}')

print('\n' + '='*80)
if soft_404["Status"] == "Pass":
    print('  ✓ SUCCESS: Homepage correctly identified as having real content!')
    print('  ✓ No false positive - detector works correctly!')
else:
    print(f'  ✗ ISSUE: Homepage flagged as {soft_404["Status"]}')
    print('  This may indicate the detector is too sensitive.')
print('='*80 + '\n')

