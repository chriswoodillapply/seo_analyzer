#!/usr/bin/env python3
"""
SEO Test Executor - Refactored with Strategy Pattern

This module provides the canonical `SEOTestExecutor` implementation (previously
named SEOTestExecutorV2 in `test_executor_v2.py`). It executes tests from a
TestRegistry and returns results for reporting.
"""

from typing import List, Optional, Dict, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, PageContent
from src.core.test_registry import TestRegistry

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class SEOTestExecutor:
    """
    Executes SEO tests using the Strategy Pattern with dependency injection.
    """

    def __init__(self, test_registry: Optional[TestRegistry] = None):
        """
        Initialize the test executor.

        Args:
            test_registry: Optional pre-configured TestRegistry. If None, creates empty registry.
        """
        self.registry = test_registry or TestRegistry()
        self._results: List[TestResult] = []

    def load_tests_from_package(self, package_path: str = "src.tests") -> int:
        """Auto-discover and load tests from a package."""
        return self.registry.discover_and_register(package_path)

    def register_test(self, test: SEOTest) -> None:
        """Register a single test"""
        self.registry.register(test)

    def execute_all_tests(
        self,
        content: PageContent,
        crawl_context: Optional['CrawlContext'] = None
    ) -> List[TestResult]:
        """Execute all registered tests against the provided content."""
        self._results = []

        for test in self.registry.get_all_tests():
            try:
                # All tests now return a list of results
                results = test.execute(content, crawl_context)
                if results:  # Only add if test returns results
                    self._results.extend(results)
            except Exception as e:
                # Log error but continue with other tests
                print(f"Error executing test {test.test_id}: {e}")
                continue

        return self._results

    def execute_tests_by_category(
        self,
        content: PageContent,
        category: str,
        crawl_context: Optional['CrawlContext'] = None
    ) -> List[TestResult]:
        """Execute tests from a specific category."""
        results = []

        for test in self.registry.get_tests_by_category(category):
            try:
                # All tests now return a list of results
                test_results = test.execute(content, crawl_context)
                if test_results:
                    results.extend(test_results)
            except Exception as e:
                print(f"Error executing test {test.test_id}: {e}")
                continue

        return results

    def execute_specific_tests(
        self,
        content: PageContent,
        test_ids: List[str],
        crawl_context: Optional['CrawlContext'] = None
    ) -> List[TestResult]:
        """Execute specific tests by their IDs."""
        results = []

        for test_id in test_ids:
            test = self.registry.get_test_by_id(test_id)
            if test:
                try:
                    # All tests now return a list of results
                    test_results = test.execute(content, crawl_context)
                    if test_results:
                        results.extend(test_results)
                except Exception as e:
                    print(f"Error executing test {test_id}: {e}")
                    continue

        return results

    def get_results(self) -> List[TestResult]:
        """Get the most recent test results"""
        return self._results.copy()

    def get_results_as_dicts(self) -> List[Dict]:
        """Get results as dictionaries for reporting"""
        return [result.to_dict() for result in self._results]

    def get_statistics(self) -> Dict:
        """Get statistics about test results."""
        if not self._results:
            return {}

        from collections import Counter
        from src.core.test_interface import TestStatus

        status_counts = Counter(result.status for result in self._results)
        category_counts = Counter(result.category for result in self._results)

        return {
            'total_tests': len(self._results),
            'passed': status_counts.get(TestStatus.PASS, 0),
            'failed': status_counts.get(TestStatus.FAIL, 0),
            'warnings': status_counts.get(TestStatus.WARNING, 0),
            'info': status_counts.get(TestStatus.INFO, 0),
            'by_category': dict(category_counts),
            'pass_rate': (status_counts.get(TestStatus.PASS, 0) / len(self._results) * 100) if self._results else 0
        }

    def get_test_count(self) -> int:
        """Get the number of registered tests"""
        return self.registry.get_test_count()

    def get_categories(self) -> List[str]:
        """Get all test categories"""
        return self.registry.get_categories()
