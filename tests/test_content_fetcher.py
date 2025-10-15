#!/usr/bin/env python3
"""
Unit tests for ContentFetcher class
"""

import unittest
from unittest.mock import Mock, patch
from src.core.content_fetcher import ContentFetcher, PageContent


class MockResponse:
    """Mock HTTP response for testing"""
    def __init__(self, status_code=200, text="", headers=None):
        self.status_code = status_code
        self.text = text
        self.content = text.encode('utf-8') if isinstance(text, str) else text
        self.headers = headers or {}
        self.url = "https://example.com"
        
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


class TestContentFetcher(unittest.TestCase):
    """Test ContentFetcher functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_url = "https://example.com"
        self.good_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Test Page</title>
            <meta name="description" content="Test description">
        </head>
        <body>
            <h1>Test Header</h1>
            <p>Test content</p>
        </body>
        </html>
        """
    
    @patch('src.core.content_fetcher.requests.Session.get')
    def test_fetch_static_content_success(self, mock_get):
        """Test successful static content fetch"""
        mock_response = MockResponse(
            status_code=200,
            text=self.good_html,
            headers={'content-type': 'text/html'}
        )
        mock_get.return_value = mock_response
        
        fetcher = ContentFetcher(enable_javascript=False)
        result = fetcher.fetch_static_content(self.test_url)
        
        self.assertEqual(result['status_code'], 200)
        self.assertIn('Test Page', result['html'])
        self.assertIsNotNone(result['soup'])
        self.assertIsNone(result['error'])
    
    @patch('src.core.content_fetcher.requests.Session.get')
    def test_fetch_static_content_error(self, mock_get):
        """Test error handling in static content fetch"""
        mock_get.side_effect = Exception("Connection timeout")
        
        fetcher = ContentFetcher(enable_javascript=False)
        result = fetcher.fetch_static_content(self.test_url)
        
        self.assertEqual(result['status_code'], 0)
        self.assertIsNotNone(result['error'])
        self.assertIn('Connection timeout', result['error'])
    
    @patch('src.core.content_fetcher.requests.Session.get')
    def test_fetch_complete_without_javascript(self, mock_get):
        """Test complete fetch without JavaScript rendering"""
        mock_response = MockResponse(
            status_code=200,
            text=self.good_html,
            headers={'content-type': 'text/html'}
        )
        mock_get.return_value = mock_response
        
        fetcher = ContentFetcher(enable_javascript=False)
        page_content = fetcher.fetch_complete(self.test_url)
        
        self.assertIsInstance(page_content, PageContent)
        self.assertEqual(page_content.url, self.test_url)
        self.assertEqual(page_content.status_code, 200)
        self.assertIsNotNone(page_content.static_soup)
        self.assertIsNone(page_content.rendered_html)
        self.assertIsNone(page_content.error)
    
    def test_context_manager(self):
        """Test ContentFetcher as context manager"""
        with ContentFetcher(enable_javascript=False) as fetcher:
            self.assertIsNotNone(fetcher)
        
        # Should cleanup successfully


if __name__ == '__main__':
    unittest.main()

