#!/usr/bin/env python3
"""Add missing imports to test files"""

from pathlib import Path
import re as regex_module

# Tests that need 're' import based on error output
tests_needing_re = [
    'src/tests/content/content_freshness_date.py',
    'src/tests/content/table_of_contents.py',
    'src/tests/international_seo/content_language_meta.py',
    'src/tests/international_seo/geo_targeting_meta.py',
    'src/tests/links/pagination_tags.py',
    'src/tests/meta_tags/meta_refresh_redirect.py',
    'src/tests/mobile_usability/intrusive_interstitial.py',
]

print('='*80)
print('  ADDING MISSING IMPORTS')
print('='*80)

for test_file in tests_needing_re:
    file_path = Path(test_file)
    if not file_path.exists():
        print(f'[SKIP] {test_file} - not found')
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if 're' is already imported
    if regex_module.search(r'^import re\b', content, regex_module.MULTILINE):
        print(f'[SKIP] {test_file} - already has re import')
        continue
    
    # Find the imports section and add 're'
    if 'from typing import' in content:
        # Add after typing import
        content = content.replace(
            'from typing import Optional, TYPE_CHECKING',
            'from typing import Optional, TYPE_CHECKING\nimport re'
        )
    elif 'from src.core.test_interface import' in content:
        # Add before src imports
        content = content.replace(
            'from src.core.test_interface import',
            'import re\nfrom src.core.test_interface import'
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'[OK] {test_file} - added re import')

print('\n' + '='*80)
print('  DONE: Added missing imports')
print('='*80 + '\n')

