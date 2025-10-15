#!/usr/bin/env python3
"""
Unit tests for SEOOrchestrator class
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from src.core.seo_orchestrator import SEOOrchestrator
from src.core.content_fetcher import PageContent
from src.core.test_executor import TestResult, TestStatus


class TestSEOOrchestrator(unittest.TestCase):
    """Test SEO orchestrator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_url = "https://example.com"
    
    @patch('src.core.content_fetcher.ContentFetcher.fetch_complete')
    def test_analyze_single_url(self, mock_fetch):
        """Test single URL analysis"""
        # Mock page content
        from bs4 import BeautifulSoup
        html = "<html><head><title>Test</title></head><body><h1>Test</h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        mock_page_content = PageContent(
            url=self.test_url,
            status_code=200,
            static_html=html,
            static_soup=soup,
            static_headers={},
            static_load_time=1.0
        )
        mock_fetch.return_value = mock_page_content
        
        orchestrator = SEOOrchestrator(enable_javascript=False)
        results = orchestrator.analyze_single_url(self.test_url)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIn(self.test_url, orchestrator.analyzed_urls)
    
    @patch('src.core.content_fetcher.ContentFetcher.fetch_complete')
    def test_analyze_multiple_urls(self, mock_fetch):
        """Test multiple URL analysis"""
        from bs4 import BeautifulSoup
        html = "<html><head><title>Test</title></head><body><h1>Test</h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        mock_page_content = PageContent(
            url=self.test_url,
            status_code=200,
            static_html=html,
            static_soup=soup,
            static_headers={},
            static_load_time=1.0
        )
        mock_fetch.return_value = mock_page_content
        
        urls = ["https://example.com", "https://test.com"]
        orchestrator = SEOOrchestrator(enable_javascript=False)
        summary = orchestrator.analyze_multiple_urls(urls)
        
        self.assertIsInstance(summary, dict)
        self.assertEqual(summary['total_urls'], 2)
        self.assertIn('successful', summary)
        self.assertIn('failed', summary)
    
    def test_get_summary_stats_empty(self):
        """Test summary stats with no results"""
        orchestrator = SEOOrchestrator(enable_javascript=False)
        stats = orchestrator.get_summary_stats()
        
        self.assertEqual(stats, {})
    
    @patch('src.core.content_fetcher.ContentFetcher.fetch_complete')
    def test_get_summary_stats_with_results(self, mock_fetch):
        """Test summary stats with results"""
        from bs4 import BeautifulSoup
        html = "<html><head><title>Test</title></head><body><h1>Test</h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        mock_page_content = PageContent(
            url=self.test_url,
            status_code=200,
            static_html=html,
            static_soup=soup,
            static_headers={},
            static_load_time=1.0
        )
        mock_fetch.return_value = mock_page_content
        
        orchestrator = SEOOrchestrator(enable_javascript=False)
        orchestrator.analyze_single_url(self.test_url)
        
        stats = orchestrator.get_summary_stats()
        
        self.assertIn('total_tests', stats)
        self.assertIn('passed', stats)
        self.assertIn('failed', stats)
        self.assertIn('warnings', stats)
        self.assertIn('pass_rate', stats)
        self.assertIn('categories', stats)
    
    def test_context_manager(self):
        """Test orchestrator as context manager"""
        with SEOOrchestrator(enable_javascript=False) as orchestrator:
            self.assertIsNotNone(orchestrator)
        
        # Should cleanup successfully


if __name__ == '__main__':
    unittest.main()

