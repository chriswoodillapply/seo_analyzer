#!/usr/bin/env python3
"""
Comprehensive script to fix missing closing brackets in refactored test files
"""

import os
import re
from pathlib import Path

def fix_brackets_in_file(file_path):
    """Fix missing closing brackets in a test file"""
    print(f"Fixing brackets in {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix the pattern: return [TestResult(...)  -> return [TestResult(...)]
    # This handles cases where the closing bracket is missing from the list
    content = re.sub(
        r'return \[TestResult\([^)]+\)\s*\)\s*$',
        r'return [TestResult(\1)]',
        content,
        flags=re.MULTILINE
    )
    
    # More specific fix for the common pattern
    # Look for lines that end with ) but should end with )]
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Check if this line has a return statement with TestResult that's missing closing bracket
        if 'return [TestResult(' in line and line.strip().endswith(')') and not line.strip().endswith(')]'):
            # Check if the next line is an elif/else/end of function
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if (next_line.startswith('elif ') or 
                    next_line.startswith('else:') or 
                    next_line.startswith('def ') or
                    next_line.startswith('class ') or
                    next_line == '' or
                    next_line.startswith('    #') or
                    next_line.startswith('    @')):
                    # This is likely a missing closing bracket
                    line = line.rstrip() + ']'
                    print(f"  Fixed line {i+1}: {line[:50]}...")
        
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"  Fixed bracket issues")

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
            fix_brackets_in_file(py_file)
            fixed_count += 1
        except Exception as e:
            print(f"Error fixing {py_file}: {e}")
    
    print(f"\nBracket fix complete:")
    print(f"  Files processed: {fixed_count}")

if __name__ == "__main__":
    main()
