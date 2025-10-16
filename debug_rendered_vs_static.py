#!/usr/bin/env python3
"""Compare static vs rendered content for homepage"""

import sys
import os

# Import from installed src package
from src.core.content_fetcher import ContentFetcher
from bs4 import BeautifulSoup

url = "https://www.applydigital.com"

print('\n' + '='*80)
print('  COMPARING STATIC vs RENDERED CONTENT')
print('='*80)

# Use the actual ContentFetcher that the test uses
fetcher = ContentFetcher()
content = fetcher.fetch_complete(url)

print(f'\nURL: {url}')
print(f'Static HTML size: {len(content.static_html) if content.static_html else 0} bytes')
print(f'Rendered HTML size: {len(content.rendered_html) if content.rendered_html else 0} bytes')

# Analyze STATIC content
print('\n' + '-'*80)
print('STATIC HTML (from requests):')
print('-'*80)
if content.static_soup:
    static_main = content.static_soup.find('main')
    if static_main:
        static_main_text = static_main.get_text()
        static_main_words = len([w for w in static_main_text.split() if len(w) > 2])
        static_main_paragraphs = len(static_main.find_all('p'))
        print(f'  <main> element found: YES')
        print(f'  Main content words: {static_main_words}')
        print(f'  Main paragraphs: {static_main_paragraphs}')
        print(f'  First 200 chars of main: "{static_main_text.strip()[:200]}..."')
    else:
        print(f'  <main> element found: NO')
    
    static_h1 = content.static_soup.find('h1')
    print(f'  H1 found: {static_h1 is not None}')
    if static_h1:
        print(f'  H1 text: "{static_h1.text.strip()}"')

# Analyze RENDERED content
print('\n' + '-'*80)
print('RENDERED HTML (from Playwright after JS):')
print('-'*80)
if content.rendered_soup:
    rendered_main = content.rendered_soup.find('main')
    if rendered_main:
        rendered_main_text = rendered_main.get_text()
        rendered_main_words = len([w for w in rendered_main_text.split() if len(w) > 2])
        rendered_main_paragraphs = len(rendered_main.find_all('p'))
        print(f'  <main> element found: YES')
        print(f'  Main content words: {rendered_main_words}')
        print(f'  Main paragraphs: {rendered_main_paragraphs}')
        print(f'  First 200 chars of main: "{rendered_main_text.strip()[:200]}..."')
    else:
        print(f'  <main> element found: NO')
    
    rendered_h1 = content.rendered_soup.find('h1')
    print(f'  H1 found: {rendered_h1 is not None}')
    if rendered_h1:
        print(f'  H1 text: "{rendered_h1.text.strip()}"')
else:
    print('  NO RENDERED CONTENT AVAILABLE')

# Compare
print('\n' + '='*80)
print('ANALYSIS:')
print('='*80)
if content.static_soup and content.rendered_soup:
    static_words = len([w for w in content.static_soup.get_text().split() if len(w) > 2])
    rendered_words = len([w for w in content.rendered_soup.get_text().split() if len(w) > 2])
    
    print(f'Static total words: {static_words}')
    print(f'Rendered total words: {rendered_words}')
    print(f'Difference: {rendered_words - static_words} words ({((rendered_words/static_words - 1) * 100):.1f}%)')
    
    if rendered_words < static_words * 0.8:
        print('\n[WARNING] Rendered content has LESS content than static!')
        print('This suggests JavaScript may be REMOVING or HIDING content.')
    elif rendered_words > static_words * 1.2:
        print('\n[INFO] Rendered content has MORE content than static.')
        print('This is expected - JavaScript adds dynamic content.')
    else:
        print('\n[OK] Similar content between static and rendered.')
        
print('='*80 + '\n')

fetcher.close()

