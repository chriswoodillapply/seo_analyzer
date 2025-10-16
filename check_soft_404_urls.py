#!/usr/bin/env python3
"""Check current results for potential soft 404 URLs"""

import pandas as pd

df = pd.read_csv('output/seo_report_20251015_175559.csv')

test_urls = [
    'https://www.applydigital.com/work',
    'https://www.applydigital.com/events',
    'https://www.applydigital.com/insights/learn',
    'https://www.applydigital.com/insights/news'
]

print("\n" + "="*80)
print("CHECKING POTENTIAL SOFT 404 URLs")
print("="*80)

for url in test_urls:
    page = df[df['URL'] == url]
    
    if len(page) == 0:
        print(f"\n{url}")
        print("  NOT FOUND in results")
        continue
    
    print(f"\n{url}")
    print(f"  Total Tests: {len(page)}")
    print(f"  Pass: {len(page[page['Status']=='Pass'])}")
    print(f"  Fail: {len(page[page['Status']=='Fail'])}")
    print(f"  Warnings: {len(page[page['Status']=='Warning'])}")
    
    # Check word count
    word_count = page[page['Test_ID'] == 'content_word_count']
    if not word_count.empty:
        print(f"  Word Count: {word_count.iloc[0]['Score']}")
    
    # Check title
    title = page[page['Test_ID'] == 'meta_title_presence']
    if not title.empty:
        print(f"  Title: {title.iloc[0]['Score']}")
    
    # Check H1
    h1 = page[page['Test_ID'] == 'h1_presence']
    if not h1.empty:
        print(f"  H1: {h1.iloc[0]['Score']}")

print("\n" + "="*80)
print("CONCLUSION:")
print("="*80)
print("These pages likely have:")
print("  - Low word counts")
print("  - Generic titles/H1s")
print("  - Minimal actual content")
print("\nThey should be flagged as SOFT 404s!")
print("="*80 + "\n")

