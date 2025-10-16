#!/usr/bin/env python3
"""
Recreate __init__.py files without imports (for auto-discovery)
"""

from pathlib import Path

test_folders = [
    'meta_tags', 'header_structure', 'images', 'links', 'content',
    'technical_seo', 'performance', 'core_web_vitals', 'accessibility',
    'mobile_usability', 'security', 'structured_data', 'international_seo'
]

CATEGORY_NAMES = {
    'meta_tags': 'Meta Tags',
    'header_structure': 'Header Structure',
    'images': 'Images',
    'links': 'Links',
    'content': 'Content',
    'technical_seo': 'Technical SEO',
    'performance': 'Performance',
    'core_web_vitals': 'Core Web Vitals',
    'accessibility': 'Accessibility',
    'mobile_usability': 'Mobile Usability',
    'security': 'Security',
    'structured_data': 'Structured Data',
    'international_seo': 'International SEO'
}

print('='*80)
print('  RECREATING __init__.py FILES')
print('='*80)

for folder in test_folders:
    folder_path = Path(f'src/tests/{folder}')
    if not folder_path.exists():
        continue
    
    init_file = folder_path / '__init__.py'
    category_name = CATEGORY_NAMES.get(folder, folder.replace('_', ' ').title())
    
    # Create a simple __init__.py without imports
    # The TestRegistry will auto-discover tests
    init_content = f'''#!/usr/bin/env python3
"""
{category_name} Tests

This package contains SEO tests for {category_name.lower()}.
Tests are auto-discovered by the TestRegistry - no imports needed.
"""
'''
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print(f'[OK] {init_file}')

print('='*80)
print('  DONE: All __init__.py files recreated')
print('='*80 + '\n')

