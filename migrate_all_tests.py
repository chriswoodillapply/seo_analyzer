#!/usr/bin/env python3
"""
Automated Test Migration Script

This script extracts all 94 tests from the monolithic test_executor.py
and generates individual test class files in the appropriate category folders.
"""

import re
import os
from pathlib import Path

# Map test categories to folder names
CATEGORY_MAP = {
    'Meta Tags': 'meta_tags',
    'Header Structure': 'header_structure',
    'Images': 'images',
    'Links': 'links',
    'Content': 'content',
    'Technical SEO': 'technical_seo',
    'Performance': 'performance',
    'Core Web Vitals': 'core_web_vitals',
    'Accessibility': 'accessibility',
    'Mobile Usability': 'mobile_usability',
    'Security': 'security',
    'Structured Data': 'structured_data',
    'International SEO': 'international_seo'
}

# Site-wide tests that require CrawlContext
SITE_WIDE_TESTS = {
    'thin_content_detection',
    'orphan_page_check',
    'link_distribution',
    'page_depth',
}

def parse_test_executor():
    """Parse test_executor.py and extract all test methods"""
    with open('src/core/test_executor.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all test methods
    test_pattern = r'def (_test_\w+)\(self, content: PageContent\) -> TestResult:(.*?)(?=\n    def |\nclass |\Z)'
    tests = re.findall(test_pattern, content, re.DOTALL)
    
    print(f'\nFound {len(tests)} test methods')
    return tests

def extract_test_metadata(method_name, method_body):
    """Extract metadata from a test method"""
    
    # Extract test_id (remove _test_ prefix)
    test_id = method_name.replace('_test_', '')
    
    # Extract test_name from the TestResult
    name_match = re.search(r"test_name=['\"]([^'\"]+)['\"]", method_body)
    test_name = name_match.group(1) if name_match else test_id.replace('_', ' ').title()
    
    # Extract category
    category_match = re.search(r"category=['\"]([^'\"]+)['\"]", method_body)
    category = category_match.group(1) if category_match else 'Technical SEO'
    
    # Extract severity
    severity_match = re.search(r"severity=['\"]([^'\"]+)['\"]", method_body)
    severity = severity_match.group(1) if severity_match else 'Medium'
    
    return {
        'test_id': test_id,
        'test_name': test_name,
        'category': category,
        'severity': severity,
        'method_name': method_name,
        'method_body': method_body
    }

def generate_test_class(metadata):
    """Generate a test class file from metadata"""
    
    test_id = metadata['test_id']
    test_name = metadata['test_name']
    category = metadata['category']
    severity = metadata['severity']
    method_body = metadata['method_body']
    
    # Convert test_id to CamelCase class name
    class_name = ''.join(word.capitalize() for word in test_id.split('_')) + 'Test'
    
    # Check if this is a site-wide test
    requires_site_context = test_id in SITE_WIDE_TESTS
    
    # Generate the class code
    class_code = f'''#!/usr/bin/env python3
"""
{test_name} Test
"""

from typing import Optional
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class {class_name}(SEOTest):
    """Test for {test_name.lower()}"""
    
    @property
    def test_id(self) -> str:
        return "{test_id}"
    
    @property
    def test_name(self) -> str:
        return "{test_name}"
    
    @property
    def category(self) -> str:
        return TestCategory.{category.upper().replace(' ', '_')}
    
    @property
    def severity(self) -> str:
        return TestSeverity.{severity.upper()}
    
'''
    
    if requires_site_context:
        class_code += f'''    @property
    def requires_site_context(self) -> bool:
        return True
    
'''
    
    # Add the execute method with the original logic
    class_code += f'''    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the {test_name.lower()} test"""
{method_body}
'''
    
    return class_code

def get_folder_for_category(category):
    """Get folder name for a category"""
    return CATEGORY_MAP.get(category, 'technical_seo')

def save_test_file(class_code, test_id, category):
    """Save the test class to the appropriate folder"""
    folder = get_folder_for_category(category)
    folder_path = Path(f'src/tests/{folder}')
    folder_path.mkdir(parents=True, exist_ok=True)
    
    file_path = folder_path / f'{test_id}.py'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(class_code)
    
    return file_path

def create_init_files():
    """Create __init__.py files for each test folder"""
    
    for category, folder in CATEGORY_MAP.items():
        folder_path = Path(f'src/tests/{folder}')
        init_file = folder_path / '__init__.py'
        
        # Get all test files in this folder
        test_files = list(folder_path.glob('*.py'))
        test_files = [f for f in test_files if f.name != '__init__.py']
        
        # Generate imports
        imports = []
        for test_file in sorted(test_files):
            module_name = test_file.stem
            # Convert module_name to class name
            class_name = ''.join(word.capitalize() for word in module_name.split('_')) + 'Test'
            imports.append(f'from .{module_name} import {class_name}')
        
        # Generate __all__
        class_names = [''.join(word.capitalize() for word in f.stem.split('_')) + 'Test' for f in sorted(test_files)]
        
        init_content = f'''#!/usr/bin/env python3
"""
{category} Tests
"""

{chr(10).join(imports)}

__all__ = {class_names}
'''
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        print(f'Created {init_file} with {len(test_files)} tests')

def main():
    print('='*80)
    print('  AUTOMATED TEST MIGRATION')
    print('='*80)
    
    # Parse test_executor.py
    print('\n[1] Parsing test_executor.py...')
    tests = parse_test_executor()
    
    # Extract metadata for each test
    print('\n[2] Extracting metadata...')
    test_metadata = []
    for method_name, method_body in tests:
        metadata = extract_test_metadata(method_name, method_body)
        test_metadata.append(metadata)
        print(f'   - {metadata["test_id"]} ({metadata["category"]})')
    
    # Generate test class files
    print(f'\n[3] Generating {len(test_metadata)} test class files...')
    for metadata in test_metadata:
        class_code = generate_test_class(metadata)
        file_path = save_test_file(class_code, metadata['test_id'], metadata['category'])
        print(f'   Created: {file_path}')
    
    # Create __init__.py files
    print('\n[4] Creating __init__.py files...')
    create_init_files()
    
    print('\n' + '='*80)
    print(f'  MIGRATION COMPLETE: {len(test_metadata)} tests migrated!')
    print('='*80)
    print('\nNext steps:')
    print('  1. Review generated test files')
    print('  2. Fix any import/syntax errors')
    print('  3. Update SEOOrchestrator to use TestRegistry')
    print('  4. Run tests to verify')
    print('='*80 + '\n')

if __name__ == '__main__':
    main()

