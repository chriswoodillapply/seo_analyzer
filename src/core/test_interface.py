#!/usr/bin/env python3
"""
SEO Test Interface and Base Classes

This module defines the abstract base class for all SEO tests, implementing
the Strategy Pattern for pluggable test architecture.

Supports two types of tests:
1. Single-page tests: Analyze one page at a time (most tests)
2. Site-wide tests: Require full crawl context (orphan pages, link distribution, etc.)
"""

from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

if TYPE_CHECKING:
    from .crawl_context import CrawlContext


class TestStatus(Enum):
    """Status of a test result"""
    PASS = "Pass"
    FAIL = "Fail"
    WARNING = "Warning"
    INFO = "Info"
    ERROR = "Error"


@dataclass
class PageContent:
    """Container for fetched page content"""
    url: str
    static_html: str
    static_soup: any  # BeautifulSoup object
    rendered_html: str
    rendered_soup: any  # BeautifulSoup object
    static_headers: dict
    static_load_time: float
    rendered_load_time: float
    performance_metrics: dict
    core_web_vitals: dict


@dataclass
class TestResult:
    """Container for test results"""
    url: str
    test_id: str
    test_name: str
    category: str
    status: TestStatus
    severity: str
    issue_description: str
    recommendation: str
    score: str
    
    def to_dict(self) -> dict:
        """Convert result to dictionary for reporting"""
        return {
            'URL': self.url,
            'Test_ID': self.test_id,
            'Test_Name': self.test_name,
            'Category': self.category,
            'Status': self.status.value,
            'Severity': self.severity,
            'Issue_Description': self.issue_description,
            'Recommendation': self.recommendation,
            'Score': self.score
        }


class SEOTest(ABC):
    """
    Abstract base class for all SEO tests.
    
    All SEO tests must inherit from this class and implement the required
    properties and methods. This enables a plugin-like architecture where
    tests can be added or removed without modifying the core executor.
    
    Two types of tests are supported:
    1. Single-page tests (default): Analyze one page at a time
    2. Site-wide tests: Require CrawlContext with full site data
    """
    
    @property
    @abstractmethod
    def test_id(self) -> str:
        """
        Unique identifier for the test.
        Should be snake_case (e.g., 'title_presence')
        """
        pass
    
    @property
    @abstractmethod
    def test_name(self) -> str:
        """
        Human-readable name for the test.
        Should be Title Case (e.g., 'Title Tag Presence')
        """
        pass
    
    @property
    @abstractmethod
    def category(self) -> str:
        """
        Test category for grouping.
        Examples: 'Meta Tags', 'Performance', 'Accessibility'
        """
        pass
    
    @property
    @abstractmethod
    def severity(self) -> str:
        """
        Severity level of issues found.
        Options: 'Critical', 'High', 'Medium', 'Low', 'Info'
        """
        pass
    
    @property
    def requires_site_context(self) -> bool:
        """
        Whether this test requires site-wide crawl context.
        
        Override this to return True for tests that need:
        - Link graph analysis (orphan pages, link distribution)
        - Content comparison (duplicate/thin content detection)
        - Site structure (page depth, navigation hierarchy)
        
        Returns:
            False by default (single-page test)
        """
        return False
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """
        Execute the test against the provided page content.
        
        This method now ALWAYS returns a List[TestResult] for consistency.
        Tests can return:
        - Empty list [] if test should be skipped
        - Single result [TestResult] for traditional single-result tests
        - Multiple results [TestResult, TestResult, ...] for multi-result tests (Lighthouse, Axe-core)
        
        Args:
            content: PageContent object containing all fetched page data
            crawl_context: Optional CrawlContext for site-wide tests
            
        Returns:
            List of TestResult objects (empty list if test should be skipped)
            
        Note:
            If requires_site_context is True and crawl_context is None, the test
            should return an INFO status indicating site crawl is required.
        """
        # Check if subclass has overridden _execute_single_result for backward compatibility
        single_result = self._execute_single_result(content, crawl_context)
        if single_result is not None:
            return [single_result]
        
        # Default implementation - override in subclasses
        return []
    
    def execute_single(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """
        Execute the test and return a single result (for backward compatibility).
        
        This method provides backward compatibility for tests that return single results.
        It calls execute() and returns the first result, or None if empty.
        
        Args:
            content: PageContent object containing all fetched page data
            crawl_context: Optional CrawlContext for site-wide tests
            
        Returns:
            First TestResult object if any results, None if empty
        """
        results = self.execute(content, crawl_context)
        return results[0] if results else None
    
    def _execute_single_result(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """
        Backward compatibility method for tests that return single results.
        
        Override this method in subclasses that return single results.
        The base execute() method will automatically wrap the result in a list.
        """
        return None
    
    def _create_result(
        self,
        content: PageContent,
        status: TestStatus,
        issue_description: str,
        recommendation: str,
        score: str
    ) -> TestResult:
        """
        Helper method to create a TestResult object.
        
        This ensures consistent result creation across all tests.
        """
        return TestResult(
            url=content.url,
            test_id=self.test_id,
            test_name=self.test_name,
            category=self.category,
            status=status,
            severity=self.severity,
            issue_description=issue_description,
            recommendation=recommendation,
            score=score
        )


class TestCategory:
    """Constants for test categories"""
    META_TAGS = "Meta Tags"
    HEADER_STRUCTURE = "Header Structure"
    IMAGES = "Images"
    LINKS = "Links"
    CONTENT = "Content"
    TECHNICAL_SEO = "Technical SEO"
    PERFORMANCE = "Performance"
    CORE_WEB_VITALS = "Core Web Vitals"
    ACCESSIBILITY = "Accessibility"
    MOBILE_USABILITY = "Mobile Usability"
    SECURITY = "Security"
    STRUCTURED_DATA = "Structured Data"
    INTERNATIONAL_SEO = "International SEO"


class TestSeverity:
    """Constants for test severity levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

