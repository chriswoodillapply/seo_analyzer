#!/usr/bin/env python3
"""
SEO Test Registry

This module provides a registry system for discovering, registering, and
managing SEO test classes. It implements dependency injection to load tests
dynamically without tight coupling.
"""

from typing import List, Dict, Optional, Type
import importlib
import inspect
import pkgutil
from pathlib import Path

from src.core.test_interface import SEOTest


class TestRegistry:
    """
    Registry for managing SEO test instances.
    
    This class provides dependency injection for test classes, allowing
    tests to be registered manually or discovered automatically from modules.
    """
    
    def __init__(self):
        """Initialize the test registry"""
        self._tests: List[SEOTest] = []
        self._tests_by_id: Dict[str, SEOTest] = {}
        self._tests_by_category: Dict[str, List[SEOTest]] = {}
    
    def register(self, test: SEOTest) -> None:
        """
        Register a single test instance.
        
        Args:
            test: An instance of a class implementing SEOTest
            
        Raises:
            ValueError: If test_id is already registered
        """
        if test.test_id in self._tests_by_id:
            raise ValueError(f"Test with ID '{test.test_id}' is already registered")
        
        self._tests.append(test)
        self._tests_by_id[test.test_id] = test
        
        # Group by category
        if test.category not in self._tests_by_category:
            self._tests_by_category[test.category] = []
        self._tests_by_category[test.category].append(test)
    
    def register_multiple(self, tests: List[SEOTest]) -> None:
        """
        Register multiple test instances.
        
        Args:
            tests: List of test instances
        """
        for test in tests:
            self.register(test)
    
    def get_all_tests(self) -> List[SEOTest]:
        """
        Get all registered tests.
        
        Returns:
            List of all registered test instances
        """
        return self._tests.copy()
    
    def get_test_by_id(self, test_id: str) -> Optional[SEOTest]:
        """
        Get a specific test by its ID.
        
        Args:
            test_id: The unique identifier of the test
            
        Returns:
            The test instance, or None if not found
        """
        return self._tests_by_id.get(test_id)
    
    def get_tests_by_category(self, category: str) -> List[SEOTest]:
        """
        Get all tests in a specific category.
        
        Args:
            category: The category name
            
        Returns:
            List of tests in the category
        """
        return self._tests_by_category.get(category, []).copy()
    
    def get_categories(self) -> List[str]:
        """
        Get all registered test categories.
        
        Returns:
            List of category names
        """
        return list(self._tests_by_category.keys())
    
    def get_test_count(self) -> int:
        """
        Get the total number of registered tests.
        
        Returns:
            Count of registered tests
        """
        return len(self._tests)
    
    def get_test_ids(self) -> List[str]:
        """
        Get all registered test IDs.
        
        Returns:
            List of test IDs
        """
        return list(self._tests_by_id.keys())
    
    def clear(self) -> None:
        """Clear all registered tests"""
        self._tests.clear()
        self._tests_by_id.clear()
        self._tests_by_category.clear()
    
    def discover_and_register(self, package_path: str) -> int:
        """
        Automatically discover and register test classes from a package.
        
        This method scans a package directory for classes that inherit from
        SEOTest and automatically instantiates and registers them.
        
        Args:
            package_path: Python package path (e.g., 'src.tests')
            
        Returns:
            Number of tests discovered and registered
            
        Example:
            registry.discover_and_register('src.tests')
        """
        count = 0
        
        try:
            # Import the package
            package = importlib.import_module(package_path)
            package_dir = Path(package.__file__).parent
            
            # Iterate through all modules in the package
            for importer, module_name, is_pkg in pkgutil.walk_packages(
                path=[str(package_dir)],
                prefix=f"{package_path}."
            ):
                try:
                    # Import the module
                    module = importlib.import_module(module_name)
                    
                    # Find all classes in the module
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        # Check if it's a subclass of SEOTest (but not SEOTest itself)
                        if (issubclass(obj, SEOTest) and 
                            obj is not SEOTest and
                            not inspect.isabstract(obj)):
                            
                            # Instantiate and register the test
                            test_instance = obj()
                            self.register(test_instance)
                            count += 1
                            
                except (ImportError, AttributeError) as e:
                    # Skip modules that can't be imported
                    continue
                    
        except ImportError as e:
            raise ImportError(f"Could not import package '{package_path}': {e}")
        
        return count


class TestLoader:
    """
    Utility class for loading and initializing tests.
    
    This class provides convenience methods for different test loading strategies.
    """
    
    @staticmethod
    def load_from_directory(directory: str) -> TestRegistry:
        """
        Load all tests from a directory.
        
        Args:
            directory: Python package path to load from
            
        Returns:
            TestRegistry with all discovered tests
        """
        registry = TestRegistry()
        registry.discover_and_register(directory)
        return registry
    
    @staticmethod
    def load_from_classes(test_classes: List[Type[SEOTest]]) -> TestRegistry:
        """
        Load tests from a list of test classes.
        
        Args:
            test_classes: List of test class types (not instances)
            
        Returns:
            TestRegistry with instantiated tests
        """
        registry = TestRegistry()
        for test_class in test_classes:
            test_instance = test_class()
            registry.register(test_instance)
        return registry
    
    @staticmethod
    def load_from_instances(test_instances: List[SEOTest]) -> TestRegistry:
        """
        Load tests from a list of test instances.
        
        Args:
            test_instances: List of test instances
            
        Returns:
            TestRegistry with the provided tests
        """
        registry = TestRegistry()
        registry.register_multiple(test_instances)
        return registry

