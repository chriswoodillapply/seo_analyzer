"""
Enterprise SEO Analysis Suite
"""

__version__ = "2.0.0"

from .core.seo_orchestrator import SEOOrchestrator
from .core.content_fetcher import ContentFetcher, PageContent
# Executor and interfaces (renamed)
from .core.seo_test_executor import SEOTestExecutor
from .core.test_interface import TestResult, TestStatus
# Keep the old executor import name for backward compatibility if needed
try:
    from .core.test_executor import SEOTestExecutor as LegacySEOTestExecutor
except Exception:
    LegacySEOTestExecutor = None
from .crawlers.url_crawler import URLCrawler
from .reporters.report_generator import ReportGenerator

__all__ = [
    'SEOOrchestrator',
    'ContentFetcher',
    'PageContent',
    'SEOTestExecutor',
    'TestResult',
    'TestStatus',
    'URLCrawler',
    'ReportGenerator',
]

