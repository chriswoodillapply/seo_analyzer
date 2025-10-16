#!/usr/bin/env python3
"""
Script to refactor all test files to return List[TestResult] instead of Optional[TestResult]
"""

import os
import re
from pathlib import Path

def refactor_test_file(file_path):
    """Refactor a single test file"""
    print(f"Refactoring {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Track changes made
    changes = []
    
    # 1. Add List import if not present
    if 'from typing import' in content and 'List' not in content:
        content = re.sub(
            r'from typing import ([^,\n]+)',
            r'from typing import \1, List',
            content
        )
        changes.append("Added List import")
    
    # 2. Change return type from Optional[TestResult] to List[TestResult]
    old_pattern = r'def execute\(self, content: PageContent, crawl_context: Optional\[\'CrawlContext\'\] = None\) -> Optional\[TestResult\]:'
    new_pattern = r'def execute(self, content: PageContent, crawl_context: Optional[\'CrawlContext\'] = None) -> List[TestResult]:'
    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_pattern, content)
        changes.append("Updated return type to List[TestResult]")
    
    # 3. Wrap single return statements in lists
    # Pattern: return TestResult(...)
    def wrap_single_return(match):
        return f"return [{match.group(0)[7:]}]"  # Remove 'return ' and wrap in []
    
    content = re.sub(r'return TestResult\(', 'return [TestResult(', content)
    changes.append("Wrapped single returns in lists")
    
    # 4. Handle None returns - convert to empty list
    content = re.sub(r'return None', 'return []', content)
    if 'return None' in content:
        changes.append("Converted None returns to empty lists")
    
    # 5. Handle conditional returns that might return None
    # Look for patterns like "if condition: return result else: return None"
    # This is more complex and might need manual review
    
    if changes:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"  Changes: {', '.join(changes)}")
        return True
    else:
        print(f"  No changes needed")
        return False

def main():
    """Refactor all test files"""
    test_dir = Path("seo_analyzer/src/tests")
    
    if not test_dir.exists():
        print(f"Test directory {test_dir} not found")
        return
    
    refactored_count = 0
    total_count = 0
    
    # Find all Python test files
    for py_file in test_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        total_count += 1
        if refactor_test_file(py_file):
            refactored_count += 1
    
    print(f"\nRefactoring complete:")
    print(f"  Total files: {total_count}")
    print(f"  Refactored: {refactored_count}")

if __name__ == "__main__":
    main()
