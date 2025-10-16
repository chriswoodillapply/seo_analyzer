#!/usr/bin/env python3
"""
Fix issues in migrated test files
"""

import os
import re
from pathlib import Path

def fix_test_file(file_path):
    """Fix common issues in a generated test file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Add TYPE_CHECKING import
    if 'if TYPE_CHECKING:' in content and 'from typing import TYPE_CHECKING' not in content:
        content = content.replace(
            'from typing import Optional',
            'from typing import Optional, TYPE_CHECKING'
        )
    
    # Fix 2: Remove duplicate docstrings in execute method
    content = re.sub(
        r'(def execute.*?\n\s+"""Execute.*?""")\s+""".*?"""',
        r'\1',
        content,
        flags=re.DOTALL
    )
    
    # Save fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print('='*80)
    print('  FIXING MIGRATED TEST FILES')
    print('='*80)
    
    test_folders = [
        'meta_tags', 'header_structure', 'images', 'links', 'content',
        'technical_seo', 'performance', 'core_web_vitals', 'accessibility',
        'mobile_usability', 'security', 'structured_data', 'international_seo'
    ]
    
    total_fixed = 0
    for folder in test_folders:
        folder_path = Path(f'src/tests/{folder}')
        if not folder_path.exists():
            continue
        
        test_files = list(folder_path.glob('*.py'))
        test_files = [f for f in test_files if f.name != '__init__.py']
        
        print(f'\nFixing {folder}/ ({len(test_files)} files)...')
        for test_file in test_files:
            try:
                fix_test_file(test_file)
                total_fixed += 1
                print(f'  [OK] {test_file.name}')
            except Exception as e:
                print(f'  [ERROR] {test_file.name}: {e}')
    
    print('\n' + '='*80)
    print(f'  FIXED {total_fixed} TEST FILES')
    print('='*80 + '\n')

if __name__ == '__main__':
    main()

