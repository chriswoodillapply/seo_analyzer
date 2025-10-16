#!/usr/bin/env python3
"""Check Core Web Vitals results"""

import pandas as pd

df = pd.read_csv('output/seo_report_20251015_184010.csv')

# Get CWV test results
cwv_tests = df[df['Category'] == 'Core Web Vitals']

print('\n' + '='*80)
print('  CORE WEB VITALS RESULTS')
print('='*80)

for idx, row in cwv_tests.iterrows():
    print(f'\n{row["Test_Name"]}')
    print(f'  Status: {row["Status"]}')
    print(f'  Score: {row["Score"]}')
    print(f'  Issue: {row["Issue_Description"]}')

print('\n' + '='*80)
print('SUMMARY:')
print('='*80)
print(f'Total CWV tests: {len(cwv_tests)}')
print(f'Passed: {len(cwv_tests[cwv_tests["Status"] == "Pass"])}')
print(f'Failed: {len(cwv_tests[cwv_tests["Status"] == "Fail"])}')
print(f'Warning: {len(cwv_tests[cwv_tests["Status"] == "Warning"])}')
print(f'Info: {len(cwv_tests[cwv_tests["Status"] == "Info"])}')
print('='*80 + '\n')

