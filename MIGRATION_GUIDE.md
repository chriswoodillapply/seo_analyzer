# SEO Test Migration Guide

## Quick Start

This guide shows how to migrate tests from the monolithic `test_executor.py` to individual test classes.

## ✅ What's Already Done

- Base architecture created and tested
- 8 Meta Tags tests migrated as examples
- 100% pass rate achieved

## 📋 Migration Checklist

### Remaining Tests by Category

- **Meta Tags**: 6 remaining (8/14 complete)
- **Header Structure**: 6 tests
- **Images**: 6 tests  
- **Links**: 11 tests
- **Content**: 8 tests
- **Technical SEO**: 13 tests
- **Performance**: 9 tests
- **Core Web Vitals**: 3 tests
- **Accessibility**: 9 tests
- **Mobile Usability**: 5 tests
- **Security**: 4 tests
- **Structured Data**: 2 tests
- **International SEO**: 3 tests

**Total**: 85 tests remaining

## 🔧 Migration Steps

### 1. Pick a Test to Migrate

Look at `src/core/test_executor.py` and find a test method like:

```python
def _test_h1_presence(self, content: PageContent) -> TestResult:
    """Test H1 tag presence"""
    soup = content.rendered_soup or content.static_soup
    h1_tags = soup.find_all('h1')
    
    if len(h1_tags) == 1:
        return TestResult(
            url=content.url,
            test_id='h1_presence',
            test_name='H1 Tag Presence',
            category='Header Structure',
            status=TestStatus.PASS,
            # ... rest of the logic
        )
```

### 2. Create New File

Create `src/tests/headers/h1_presence.py`:

```python
#!/usr/bin/env python3
"""H1 Presence Test"""

from typing import Optional
from src.core.test_interface import (
    SEOTest, TestResult, TestStatus, PageContent,
    TestCategory, TestSeverity
)


class H1PresenceTest(SEOTest):
    """Test if page has exactly one H1 tag"""
    
    @property
    def test_id(self) -> str:
        return "h1_presence"
    
    @property
    def test_name(self) -> str:
        return "H1 Tag Presence"
    
    @property
    def category(self) -> str:
        return TestCategory.HEADER_STRUCTURE
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH  # or MEDIUM, LOW, INFO
    
    def execute(self, content: PageContent) -> Optional[TestResult]:
        """Execute the H1 presence test"""
        soup = content.rendered_soup or content.static_soup
        h1_tags = soup.find_all('h1')
        
        if len(h1_tags) == 1:
            return self._create_result(
                content=content,
                status=TestStatus.PASS,
                issue_description='Page has exactly one H1 tag',
                recommendation='Continue using single H1 for main heading',
                score=f'H1: "{h1_tags[0].text.strip()[:50]}..."'
            )
        elif len(h1_tags) == 0:
            return self._create_result(
                content=content,
                status=TestStatus.FAIL,
                issue_description='Page is missing H1 tag',
                recommendation='Add exactly one H1 tag for the main page heading',
                score='0 H1 tags'
            )
        else:
            return self._create_result(
                content=content,
                status=TestStatus.WARNING,
                issue_description=f'Page has multiple H1 tags ({len(h1_tags)})',
                recommendation='Use only one H1 tag per page',
                score=f'{len(h1_tags)} H1 tags'
            )
```

### 3. Key Changes

When migrating from old to new:

1. **Replace `TestResult(...)`** with **`self._create_result(...)`**
   - The helper method automatically fills in url, test_id, test_name, category, severity

2. **Remove duplicate parameters** from `_create_result()`:
   - ✅ Keep: `status`, `issue_description`, `recommendation`, `score`
   - ❌ Remove: `url`, `test_id`, `test_name`, `category`, `severity`

3. **Return `None`** for tests that don't apply:
   ```python
   if not has_prerequisite:
       return None  # Skip this test
   ```

### 4. Update Category `__init__.py`

Add to `src/tests/headers/__init__.py`:

```python
#!/usr/bin/env python3
"""Header Structure SEO Tests"""

from .h1_presence import H1PresenceTest
from .header_hierarchy import HeaderHierarchyTest
# ... more imports

__all__ = [
    'H1PresenceTest',
    'HeaderHierarchyTest',
    # ... more exports
]
```

### 5. Test It

```python
from src.tests.headers import H1PresenceTest
from src.core.test_registry import TestRegistry
from src.core.test_executor_v2 import SEOTestExecutorV2

registry = TestRegistry()
registry.register(H1PresenceTest())

executor = SEOTestExecutorV2(registry)
results = executor.execute_all_tests(content)

for result in results:
    print(f"{result.status.value}: {result.test_name}")
```

## 📝 Quick Reference

### Category Constants
```python
TestCategory.META_TAGS
TestCategory.HEADER_STRUCTURE
TestCategory.IMAGES
TestCategory.LINKS
TestCategory.CONTENT
TestCategory.TECHNICAL_SEO
TestCategory.PERFORMANCE
TestCategory.CORE_WEB_VITALS
TestCategory.ACCESSIBILITY
TestCategory.MOBILE_USABILITY
TestCategory.SECURITY
TestCategory.STRUCTURED_DATA
TestCategory.INTERNATIONAL_SEO
```

### Severity Constants
```python
TestSeverity.HIGH    # Critical issues
TestSeverity.MEDIUM  # Important issues
TestSeverity.LOW     # Minor issues
TestSeverity.INFO    # Informational
```

### Test Status
```python
TestStatus.PASS     # Test passed
TestStatus.FAIL     # Test failed
TestStatus.WARNING  # Potential issue
TestStatus.INFO     # Informational
TestStatus.ERROR    # Error executing test
```

## 🔄 Batch Migration Script

For faster migration, you can use the template script:

```python
#!/usr/bin/env python3
"""Generate test class from template"""

import sys

TEMPLATE = '''#!/usr/bin/env python3
"""{test_name} Test"""

from typing import Optional
from src.core.test_interface import (
    SEOTest, TestResult, TestStatus, PageContent,
    TestCategory, TestSeverity
)
import re


class {class_name}(SEOTest):
    """{description}"""
    
    @property
    def test_id(self) -> str:
        return "{test_id}"
    
    @property
    def test_name(self) -> str:
        return "{test_name}"
    
    @property
    def category(self) -> str:
        return TestCategory.{category_const}
    
    @property
    def severity(self) -> str:
        return TestSeverity.{severity_const}
    
    def execute(self, content: PageContent) -> Optional[TestResult]:
        """Execute the {test_name} test"""
        # TODO: Implement test logic
        # Copy from _test_{method_name} in test_executor.py
        # Replace TestResult(...) with self._create_result(...)
        pass
'''

# Usage: python generate_test.py H1PresenceTest h1_presence "H1 Tag Presence" HEADER_STRUCTURE HIGH
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: generate_test.py ClassName test_id 'Test Name' CATEGORY SEVERITY")
        sys.exit(1)
    
    class_name = sys.argv[1]
    test_id = sys.argv[2]
    test_name = sys.argv[3]
    category = sys.argv[4]
    severity = sys.argv[5]
    
    code = TEMPLATE.format(
        class_name=class_name,
        test_id=test_id,
        test_name=test_name,
        category_const=category,
        severity_const=severity.upper(),
        description=f"{test_name} SEO Test",
        method_name=test_id
    )
    
    print(code)
```

## 🎯 Priorities

If you want to migrate incrementally, prioritize by:

1. **High Severity Tests First**:
   - Title, Description, H1 tags
   - Canonical URLs
   - Mobile viewport
   - HTTPS/Security

2. **Common Issues**:
   - Meta tags
   - Header structure
   - Images

3. **Advanced Features**:
   - Structured data
   - Performance metrics
   - Accessibility

## ✅ Verification

After migrating tests:

1. **Register with registry**
2. **Execute against test content**
3. **Verify results match old implementation**
4. **Check for None returns** (tests that should skip)
5. **Ensure proper status** (Pass/Fail/Warning/Info)

## 🐛 Common Pitfalls

1. **Forgetting to return None**: Tests that aren't applicable should return None
2. **Wrong category constant**: Use `TestCategory.XXX`, not string
3. **Forgetting imports**: Some tests need `import re` or `import json`
4. **Indentation**: Execute method should be at class level, not nested
5. **Using old TestResult**: Use `self._create_result()` instead

## 📚 Examples

See these for reference:
- `src/tests/meta_tags/title_presence.py` - Simple check
- `src/tests/meta_tags/title_length.py` - With None return
- `src/tests/meta_tags/open_graph.py` - Multiple checks
- `src/tests/meta_tags/robots_meta.py` - Conditional logic

## 🚀 Advanced: Auto-Discovery

Once all tests are migrated, enable auto-discovery:

```python
# In your main code
from src.core.test_registry import TestLoader

# Auto-discover all tests from src.tests package
registry = TestLoader.load_from_directory("src.tests")

print(f"Loaded {registry.get_test_count()} tests")
print(f"Categories: {registry.get_categories()}")
```

## 📊 Progress Tracking

Create a checklist as you go:

```
Meta Tags: [========--] 8/14
Headers:   [----------] 0/6
Images:    [----------] 0/6
...
```

Or track in a file:

```python
MIGRATION_STATUS = {
    "meta_tags": 8,       # 8/14 done
    "headers": 0,         # 0/6 done
    # ... etc
}
```

## 🤝 Need Help?

Refer to:
- `REFACTORING_COMPLETE.md` - Architecture overview
- `test_new_architecture.py` - Working example
- `src/tests/meta_tags/*.py` - Reference implementations

---

**Remember**: The architecture is production-ready NOW. Migration of remaining tests is optional and can be done incrementally!

