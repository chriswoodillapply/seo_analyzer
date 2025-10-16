#!/usr/bin/env python3
"""Check for missing tests"""

from pathlib import Path
import sys
sys.path.insert(0, 'src')

from src.core.test_registry import TestRegistry

print('='*80)
print('  CHECKING FOR MISSING TESTS')
print('='*80)

# Step 1: Count test files on disk
print('\n[1] Counting test files on disk...')
test_files = list(Path('src/tests').rglob('*.py'))
test_files = [f for f in test_files if f.name != '__init__.py']
print(f'   Total test files on disk: {len(test_files)}')

# Show by category
categories = {}
for f in test_files:
    category = f.parent.name
    if category not in categories:
        categories[category] = []
    categories[category].append(f.stem)

print('\n   Breakdown by category:')
for cat in sorted(categories.keys()):
    print(f'      {cat:25} | {len(categories[cat]):3} files')

# Step 2: Check how many tests are discovered and registered
print('\n[2] Discovering and registering tests...')
registry = TestRegistry()
try:
    count = registry.discover_and_register('src.tests')
    print(f'   Tests discovered and registered: {count}')
except Exception as e:
    print(f'   ERROR: {e}')
    import traceback
    traceback.print_exc()

# Step 3: Compare
print('\n[3] Analysis:')
print('-'*80)
print(f'   Test files on disk:          {len(test_files)}')
print(f'   Tests registered:            {count}')
print(f'   Difference:                  {len(test_files) - count}')

if len(test_files) != count:
    print(f'\n   [WARNING] {len(test_files) - count} test(s) not registered!')
    print('   Possible reasons:')
    print('      - Syntax errors in test files')
    print('      - Import errors')
    print('      - Abstract classes not instantiable')
    print('      - Missing __init__ method')
    
    # Try to find which files failed
    print('\n[4] Checking which tests failed to load...')
    registered_ids = set(registry.get_test_ids())
    
    # List all test files
    all_test_file_names = set(f.stem for f in test_files)
    
    print(f'\n   Registered test IDs: {len(registered_ids)}')
    print(f'   Test file names: {len(all_test_file_names)}')
    
    # Check for files that might have failed
    print('\n   Potential issues:')
    for cat, tests in sorted(categories.items()):
        for test_name in tests:
            if test_name not in registered_ids:
                test_file = Path(f'src/tests/{cat}/{test_name}.py')
                print(f'      [{cat}] {test_name} - file exists but not registered')
                
                # Try to import it manually to see the error
                try:
                    import importlib
                    module_name = f'src.tests.{cat}.{test_name}'
                    module = importlib.import_module(module_name)
                    print(f'           Module imports OK')
                    
                    # Try to find the test class
                    import inspect
                    from src.core.test_interface import SEOTest
                    found_class = False
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, SEOTest) and obj is not SEOTest:
                            print(f'           Found class: {name}')
                            try:
                                instance = obj()
                                print(f'           Can instantiate: YES')
                                print(f'           Test ID: {instance.test_id}')
                                found_class = True
                            except Exception as e:
                                print(f'           Can instantiate: NO - {e}')
                    
                    if not found_class:
                        print(f'           [ERROR] No valid SEOTest subclass found')
                        
                except Exception as e:
                    print(f'           [ERROR] Import failed: {e}')

print('\n' + '='*80)
print('  DONE')
print('='*80 + '\n')

