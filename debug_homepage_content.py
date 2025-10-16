#!/usr/bin/env python3
"""Debug homepage content detection"""

import requests
from bs4 import BeautifulSoup

url = "https://www.applydigital.com"

# Fetch and parse
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')

print('\n' + '='*80)
print('  DEBUGGING HOMEPAGE CONTENT STRUCTURE')
print('='*80)

# Total content
total_text = soup.get_text()
total_words = len([w for w in total_text.split() if len(w) > 2])
print(f'\nTotal page words: {total_words}')

# Check for main element
main = soup.find('main')
print(f'\n<main> element found: {main is not None}')
if main:
    main_text = main.get_text()
    main_words = len([w for w in main_text.split() if len(w) > 2])
    print(f'  Main element words: {main_words}')
    print(f'  Main element paragraphs: {len(main.find_all("p"))}')

# Check for article
article = soup.find('article')
print(f'\n<article> element found: {article is not None}')
if article:
    article_words = len([w for w in article.get_text().split() if len(w) > 2])
    print(f'  Article words: {article_words}')

# Check for common content divs
content_divs = soup.find_all('div', class_=lambda x: x and any(c in str(x).lower() for c in ['content', 'body', 'main']))
print(f'\nContent divs found: {len(content_divs)}')
if content_divs:
    for i, div in enumerate(content_divs[:3]):
        div_classes = ' '.join(div.get('class', []))
        div_words = len([w for w in div.get_text().split() if len(w) > 2])
        print(f'  Div {i+1} class="{div_classes[:50]}..." words: {div_words}')

# Check sections
sections = soup.find_all('section')
print(f'\n<section> elements found: {len(sections)}')
if sections:
    section_words = sum(len([w for w in s.get_text().split() if len(w) > 2]) for s in sections)
    print(f'  Total section words: {section_words}')

# Check H1
h1 = soup.find('h1')
print(f'\nH1 found: {h1 is not None}')
if h1:
    print(f'  H1 text: "{h1.text.strip()}"')

# Check paragraphs
all_p = soup.find_all('p')
print(f'\nTotal <p> tags: {len(all_p)}')
if all_p:
    p_words = sum(len([w for w in p.get_text().split() if len(w) > 2]) for p in all_p)
    print(f'  Total words in paragraphs: {p_words}')

print('\n' + '='*80)
print('CONCLUSION:')
print('='*80)
print('The page structure likely uses:')
print('  - <section> elements instead of <main>')
print('  - Or div-based layout without semantic HTML')
print('  - Content is there, but detector is looking in wrong place')
print('='*80 + '\n')

