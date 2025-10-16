#!/usr/bin/env python3
"""Analyze SEO test results"""

import pandas as pd

# Read the latest report
df = pd.read_csv('output/seo_report_20251015_173245.csv')

print('\n' + '='*80)
print('  DETAILED SEO ANALYSIS - www.applydigital.com')
print('='*80)

# Overall score
total = len(df)
passed = len(df[df['Status'] == 'Pass'])
failed = len(df[df['Status'] == 'Fail'])
warnings = len(df[df['Status'] == 'Warning'])
info = len(df[df['Status'] == 'Info'])

print(f'\nOVERALL RESULTS:')
print(f'  Total Tests:  {total}')
print(f'  Passed:       {passed} ({passed/total*100:.1f}%)')
print(f'  Failed:       {failed} ({failed/total*100:.1f}%)')
print(f'  Warnings:     {warnings} ({warnings/total*100:.1f}%)')
print(f'  Info:         {info} ({info/total*100:.1f}%)')

# Failed tests
print('\n' + '-'*80)
print('CRITICAL ISSUES (Failed Tests):')
print('-'*80)
failed_df = df[df['Status'] == 'Fail']
if len(failed_df) > 0:
    for idx, row in failed_df.iterrows():
        print(f"\n[FAIL] {row['Test_Name']} ({row['Category']})")
        print(f"  Issue: {row['Issue_Description']}")
        print(f"  Fix: {row['Recommendation']}")
else:
    print("None - Great job!")

# Warnings
print('\n' + '-'*80)
print('WARNINGS (Needs Attention):')
print('-'*80)
warning_df = df[df['Status'] == 'Warning']
for idx, row in warning_df.head(10).iterrows():
    print(f"\n[WARN] {row['Test_Name']} ({row['Category']})")
    print(f"  Issue: {row['Issue_Description']}")
    print(f"  Severity: {row['Severity']}")

if len(warning_df) > 10:
    print(f"\n... and {len(warning_df) - 10} more warnings")

# Top performing categories
print('\n' + '-'*80)
print('TOP PERFORMING CATEGORIES:')
print('-'*80)
passed_by_cat = df[df['Status'] == 'Pass'].groupby('Category').size().sort_values(ascending=False)
for cat, count in passed_by_cat.head(5).items():
    total_cat = len(df[df['Category'] == cat])
    print(f"  {cat}: {count}/{total_cat} tests passed")

# Areas needing improvement
print('\n' + '-'*80)
print('AREAS NEEDING IMPROVEMENT:')
print('-'*80)
issues_by_cat = df[df['Status'].isin(['Fail', 'Warning'])].groupby('Category').size().sort_values(ascending=False)
for cat, count in issues_by_cat.head(5).items():
    total_cat = len(df[df['Category'] == cat])
    print(f"  {cat}: {count}/{total_cat} issues found")

# Key wins
print('\n' + '-'*80)
print('KEY WINS:')
print('-'*80)
key_passes = df[df['Status'] == 'Pass'].head(10)
for idx, row in key_passes.iterrows():
    if row['Severity'] in ['High', 'Critical']:
        print(f"  [+] {row['Test_Name']}: {row['Score']}")

print('\n' + '='*80)
print(f"Full reports saved to:")
print(f"  - output/seo_report_20251015_173245.csv")
print(f"  - output/seo_report_20251015_173246.xlsx")
print('='*80 + '\n')

