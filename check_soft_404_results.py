#!/usr/bin/env python3
"""Check soft 404 detection results"""

import pandas as pd

df = pd.read_csv('output/seo_report_20251015_183553.csv')

# Get soft 404 test results
soft_404 = df[df['Test_ID'] == 'soft_404_detection']

print('\n' + '='*80)
print('  SOFT 404 DETECTION RESULTS')
print('='*80)

if len(soft_404) == 0:
    print('\n[ERROR] No soft_404_detection test found!')
    print('Available Test IDs:', df['Test_ID'].unique()[:20])
else:
    for idx, row in soft_404.iterrows():
        print(f'\n{row["URL"]}')
        print(f'  Status: {row["Status"]}')
        print(f'  Score: {row["Score"]}')
        print(f'  Severity: {row["Severity"]}')
        print(f'  Issue: {row["Issue_Description"][:200]}')
        if len(row["Issue_Description"]) > 200:
            print(f'         ...{row["Issue_Description"][-50:]}')
        print(f'  Recommendation: {row["Recommendation"][:150]}')

print('\n' + '='*80)
print('SUMMARY:')
print('='*80)
print(f'Total URLs tested: {len(soft_404)}')
print(f'Failed: {len(soft_404[soft_404["Status"] == "Fail"])}')
print(f'Warning: {len(soft_404[soft_404["Status"] == "Warning"])}')
print(f'Passed: {len(soft_404[soft_404["Status"] == "Pass"])}')
print('='*80 + '\n')

