#!/usr/bin/env python3
"""
Comprehensive script to fix all syntax errors in refactored test files
"""

import os
import re
from pathlib import Path

def fix_file_syntax(file_path):
    """Fix syntax errors in a single file"""
    print(f"Fixing {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix the specific pattern that's causing issues
    # Replace Optional[\'CrawlContext\'] with Optional['CrawlContext']
    content = re.sub(
        r"Optional\\\[\\'CrawlContext\\'\\\]",
        r"Optional['CrawlContext']",
        content
    )
    
    # Fix any other escaped quotes in type hints
    content = re.sub(
        r"\\\[\\'([^']+)\\'\\\]",
        r"['\1']",
        content
    )
    
    # Fix any remaining backslash issues
    content = re.sub(
        r"\\'([^']+)\\'",
        r"'\1'",
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"  Fixed syntax errors")

def main():
    """Fix all test files"""
    test_dir = Path("seo_analyzer/src/tests")
    
    if not test_dir.exists():
        print(f"Test directory {test_dir} not found")
        return
    
    fixed_count = 0
    
    # Find all Python test files
    for py_file in test_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        try:
            fix_file_syntax(py_file)
            fixed_count += 1
        except Exception as e:
            print(f"Error fixing {py_file}: {e}")
    
    print(f"\nComprehensive syntax fix complete:")
    print(f"  Files fixed: {fixed_count}")

if __name__ == "__main__":
    main()
