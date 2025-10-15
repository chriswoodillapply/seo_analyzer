#!/usr/bin/env python3
"""
Unit tests for SEOTestExecutor class
"""

import unittest
from bs4 import BeautifulSoup
from src.core.test_executor import SEOTestExecutor, TestResult, TestStatus
from src.core.content_fetcher import PageContent


class TestSEOTestExecutor(unittest.TestCase):
    """Test SEO test execution"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.executor = SEOTestExecutor()
        
        self.good_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Test Page - Good SEO Example With Optimal Length</title>
            <meta name="description" content="This is a well-optimized meta description that provides clear information about the page content.">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="canonical" href="https://example.com/">
        </head>
        <body>
            <h1>Main Heading</h1>
            <h2>Section 1</h2>
            <p>Content paragraph with sufficient text.</p>
            <img src="image.jpg" alt="Descriptive alt text">
            <a href="/page">Link text</a>
        </body>
        </html>
        """
        
        self.bad_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>X</title>
        </head>
        <body>
            <h1>Header 1</h1>
            <h1>Header 2</h1>
            <img src="image.jpg">
        </body>
        </html>
        """
    
    def _create_page_content(self, html, url="https://example.com"):
        """Helper to create PageContent from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        return PageContent(
            url=url,
            status_code=200,
            static_html=html,
            static_soup=soup,
            static_headers={'content-type': 'text/html'},
            static_load_time=1.0
        )
    
    def test_title_presence_pass(self):
        """Test title presence check with good HTML"""
        page_content = self._create_page_content(self.good_html)
        result = self.executor._test_title_presence(page_content)
        
        self.assertIsInstance(result, TestResult)
        self.assertEqual(result.status, TestStatus.PASS)
        self.assertEqual(result.test_id, 'meta_title_presence')
    
    def test_title_presence_fail(self):
        """Test title presence check with missing title"""
        html = "<html><head></head><body></body></html>"
        page_content = self._create_page_content(html)
        result = self.executor._test_title_presence(page_content)
        
        self.assertEqual(result.status, TestStatus.FAIL)
    
    def test_title_length_optimal(self):
        """Test title length with optimal length"""
        page_content = self._create_page_content(self.good_html)
        result = self.executor._test_title_length(page_content)
        
        self.assertEqual(result.status, TestStatus.PASS)
    
    def test_title_length_too_short(self):
        """Test title length with short title"""
        page_content = self._create_page_content(self.bad_html)
        result = self.executor._test_title_length(page_content)
        
        self.assertEqual(result.status, TestStatus.WARNING)
    
    def test_h1_presence_pass(self):
        """Test H1 presence with single H1"""
        page_content = self._create_page_content(self.good_html)
        result = self.executor._test_h1_presence(page_content)
        
        self.assertEqual(result.status, TestStatus.PASS)
    
    def test_h1_presence_multiple(self):
        """Test H1 presence with multiple H1s"""
        page_content = self._create_page_content(self.bad_html)
        result = self.executor._test_h1_presence(page_content)
        
        self.assertEqual(result.status, TestStatus.WARNING)
    
    def test_image_alt_text_pass(self):
        """Test image alt text with all images having alt"""
        page_content = self._create_page_content(self.good_html)
        result = self.executor._test_image_alt_text(page_content)
        
        self.assertEqual(result.status, TestStatus.PASS)
    
    def test_image_alt_text_fail(self):
        """Test image alt text with missing alt"""
        page_content = self._create_page_content(self.bad_html)
        result = self.executor._test_image_alt_text(page_content)
        
        self.assertEqual(result.status, TestStatus.FAIL)
    
    def test_ssl_certificate_https(self):
        """Test SSL certificate check with HTTPS URL"""
        page_content = self._create_page_content(self.good_html, "https://example.com")
        result = self.executor._test_ssl_certificate(page_content)
        
        self.assertEqual(result.status, TestStatus.PASS)
    
    def test_ssl_certificate_http(self):
        """Test SSL certificate check with HTTP URL"""
        page_content = self._create_page_content(self.good_html, "http://example.com")
        result = self.executor._test_ssl_certificate(page_content)
        
        self.assertEqual(result.status, TestStatus.FAIL)
    
    def test_execute_all_tests(self):
        """Test executing all tests"""
        page_content = self._create_page_content(self.good_html)
        results = self.executor.execute_all_tests(page_content)
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 10)  # Should have many tests
        
        # Check all results are TestResult instances
        for result in results:
            self.assertIsInstance(result, TestResult)
    
    def test_execute_specific_tests(self):
        """Test executing specific tests"""
        page_content = self._create_page_content(self.good_html)
        test_ids = ['meta_title_presence', 'h1_presence', 'ssl_certificate']
        results = self.executor.execute_specific_tests(page_content, test_ids)
        
        self.assertEqual(len(results), 3)
        result_ids = [r.test_id for r in results]
        for test_id in test_ids:
            self.assertIn(test_id, result_ids)
    
    def test_result_to_dict(self):
        """Test TestResult to_dict conversion"""
        page_content = self._create_page_content(self.good_html)
        result = self.executor._test_title_presence(page_content)
        result_dict = result.to_dict()
        
        self.assertIsInstance(result_dict, dict)
        self.assertIn('URL', result_dict)
        self.assertIn('Test_Name', result_dict)
        self.assertIn('Status', result_dict)
        self.assertIn('Severity', result_dict)


if __name__ == '__main__':
    unittest.main()

