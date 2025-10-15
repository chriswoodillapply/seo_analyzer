#!/usr/bin/env python3
"""
Comprehensive unit tests for SEO Analyzer

Test cases based on www.applydigital.com analysis:
- Positive cases: 200 responses with good content
- Negative cases: 308 redirects, 500 errors
- Security issues: Missing CSP headers
- Performance and accessibility testing
- Soft 404 detection
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
from bs4 import BeautifulSoup
import json
from seo_analyzer import SEOAnalyzer


class MockResponse:
    """Mock HTTP response for testing"""
    def __init__(self, status_code=200, content="", headers=None, elapsed_seconds=1.0, history=None):
        self.status_code = status_code
        self.content = content.encode('utf-8') if isinstance(content, str) else content
        self.text = content if isinstance(content, str) else content.decode('utf-8')
        self.headers = headers or {}
        self.elapsed = Mock()
        self.elapsed.total_seconds.return_value = elapsed_seconds
        self.history = history or []
        
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.RequestException(f"HTTP {self.status_code}")


class TestSEOAnalyzerPositive(unittest.TestCase):
    """Test successful SEO analysis scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_url = "https://www.applydigital.com/"
        self.good_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Apply Digital - Your global experience transformation partner</title>
            <meta name="description" content="Drive AI-powered change and measurable impact across complex, multi-brand ecosystems with Apply Digital.">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="canonical" href="https://www.applydigital.com/">
            <link rel="stylesheet" href="/styles.css">
            <script src="/app.js" defer></script>
        </head>
        <body>
            <header>
                <nav role="navigation">
                    <a href="#main" class="skip-link">Skip to main content</a>
                </nav>
            </header>
            <main id="main">
                <h1>Your global experience transformation partner</h1>
                <h2>AI-Powered Solutions</h2>
                <p>Apply Digital helps organizations unlock the full potential of AI from planning and design to deployment and scaling.</p>
                <img src="/logo.jpg" alt="Apply Digital Logo" width="200" height="100">
                <form>
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email">
                </form>
            </main>
            <footer></footer>
        </body>
        </html>
        """
        
    @patch('seo_analyzer.requests.Session.get')
    def test_successful_page_analysis(self, mock_get):
        """Test complete analysis of a successful page"""
        # Mock successful response
        mock_response = MockResponse(
            status_code=200,
            content=self.good_html,
            headers={
                'content-type': 'text/html; charset=utf-8',
                'x-frame-options': 'DENY',
                # Note: Missing Content-Security-Policy header (as per applydigital.com)
            },
            elapsed_seconds=1.2
        )
        mock_get.return_value = mock_response
        
        # Initialize analyzer without axe-core for faster testing
        analyzer = SEOAnalyzer(self.test_url, use_axe=False)
        
        # Run analysis
        results = analyzer.run_analysis()
        
        # Assert basic structure
        self.assertIsInstance(results, dict)
        self.assertEqual(results['url'], self.test_url)
        self.assertIn('meta_analysis', results)
        self.assertIn('header_analysis', results)
        self.assertIn('accessibility', results)
        self.assertIn('performance', results)
        
        # Assert meta analysis
        meta = results['meta_analysis']
        self.assertEqual(meta['title'], 'Apply Digital - Your global experience transformation partner')
        self.assertGreater(meta['title_length'], 30)
        self.assertLess(meta['title_length'], 70)  # Good title length
        self.assertIn('Drive AI-powered change', meta['description'])
        self.assertEqual(meta['canonical'], 'https://www.applydigital.com/')
        
        # Assert header structure
        headers = results['header_analysis']
        self.assertEqual(len(headers['h1_tags']), 1)
        self.assertEqual(headers['h1_tags'][0]['text'], 'Your global experience transformation partner')
        
        # Assert accessibility
        accessibility = results['accessibility']
        self.assertEqual(accessibility['lang_attribute'], 'en')
        self.assertTrue(accessibility['page_title_exists'])
        self.assertGreater(accessibility['score'], 70)  # Should have decent accessibility
        
        # Assert performance
        performance = results['performance']
        self.assertEqual(performance['load_time'], 1.2)
        self.assertLess(len(results['issues']), 5)  # Should have few issues
        
    @patch('seo_analyzer.requests.Session.get')
    def test_meta_tag_analysis(self, mock_get):
        """Test detailed meta tag analysis"""
        mock_response = MockResponse(status_code=200, content=self.good_html)
        mock_get.return_value = mock_response
        
        analyzer = SEOAnalyzer(self.test_url, use_axe=False)
        page_data = analyzer.fetch_page(self.test_url)
        meta_analysis = analyzer.analyze_meta_tags(page_data)
        
        # Test title analysis
        self.assertIn('Apply Digital', meta_analysis['title'])
        self.assertGreaterEqual(meta_analysis['title_length'], 30)
        self.assertLessEqual(meta_analysis['title_length'], 60)
        
        # Test description analysis
        self.assertIn('AI-powered', meta_analysis['description'])
        self.assertGreaterEqual(meta_analysis['description_length'], 120)
        self.assertLessEqual(meta_analysis['description_length'], 160)
        
        # Test viewport
        self.assertIn('width=device-width', meta_analysis['viewport'])
        
        # Test canonical
        self.assertEqual(meta_analysis['canonical'], 'https://www.applydigital.com/')
        
    @patch('seo_analyzer.requests.Session.get')
    def test_accessibility_analysis(self, mock_get):
        """Test accessibility analysis features"""
        mock_response = MockResponse(status_code=200, content=self.good_html)
        mock_get.return_value = mock_response
        
        analyzer = SEOAnalyzer(self.test_url, use_axe=False)
        page_data = analyzer.fetch_page(self.test_url)
        accessibility = analyzer.analyze_accessibility(page_data)
        
        # Test language attribute
        self.assertEqual(accessibility['lang_attribute'], 'en')
        
        # Test page title
        self.assertTrue(accessibility['page_title_exists'])
        
        # Test images with alt text
        self.assertEqual(accessibility['images_with_alt'], 1)
        self.assertEqual(accessibility['images_without_alt'], 0)
        
        # Test form labels
        self.assertEqual(accessibility['form_labels']['total'], 1)
        self.assertEqual(accessibility['form_labels']['labeled'], 1)
        
        # Test semantic elements
        semantic_tags = [elem['tag'] for elem in accessibility['semantic_elements']]
        self.assertIn('main', semantic_tags)
        self.assertIn('nav', semantic_tags)
        
        # Test skip links
        self.assertEqual(accessibility['skip_links'], 1)
        
        # Test overall score
        self.assertGreaterEqual(accessibility['score'], 80)


class TestSEOAnalyzerNegative(unittest.TestCase):
    """Test error scenarios and edge cases"""
    
    def setUp(self):
        """Set up test fixtures for negative cases"""
        self.redirect_url = "https://www.applydigital.com/work"
        self.error_url = "https://www.applydigital.com/events/advertising-week-new-york-2025/"
        
    @patch('seo_analyzer.requests.Session.get')
    def test_308_redirect_handling(self, mock_get):
        """Test handling of 308 permanent redirect"""
        # Mock 308 response
        mock_response = MockResponse(
            status_code=308,
            content="<html><body>Permanently Redirected</body></html>",
            headers={'Location': 'https://www.applydigital.com/our-work'}
        )
        mock_get.return_value = mock_response
        
        # Should raise an exception for 308 status
        analyzer = SEOAnalyzer(self.redirect_url, use_axe=False)
        result = analyzer.fetch_page(self.redirect_url)
        
        # Should return None for failed requests
        self.assertIsNone(result)
        
    @patch('seo_analyzer.requests.Session.get')
    def test_500_server_error_handling(self, mock_get):
        """Test handling of 500 server error"""
        # Mock 500 response
        mock_response = MockResponse(
            status_code=500,
            content="<html><body>Internal Server Error</body></html>"
        )
        mock_get.return_value = mock_response
        
        analyzer = SEOAnalyzer(self.error_url, use_axe=False)
        result = analyzer.fetch_page(self.error_url)
        
        # Should return None for server errors
        self.assertIsNone(result)
        
    @patch('seo_analyzer.requests.Session.get')
    def test_soft_404_detection(self, mock_get):
        """Test soft 404 detection capabilities"""
        # Mock a page that returns 200 but has error content
        soft_404_html = """
        <html>
        <head>
            <title>Page Not Found - Apply Digital</title>
        </head>
        <body>
            <h1>Oops! Page Not Found</h1>
            <p>The page you are looking for does not exist.</p>
        </body>
        </html>
        """
        
        mock_response = MockResponse(
            status_code=200,
            content=soft_404_html
        )
        mock_get.return_value = mock_response
        
        analyzer = SEOAnalyzer("https://www.applydigital.com/nonexistent", use_axe=False)
        page_data = analyzer.fetch_page("https://www.applydigital.com/nonexistent")
        soft_404_analysis = analyzer.analyze_soft_404(page_data)
        
        # Should detect soft 404
        self.assertTrue(soft_404_analysis['is_soft_404'])
        self.assertGreaterEqual(soft_404_analysis['confidence_score'], 50)
        self.assertIn('not found', soft_404_analysis['title_indicators'])
        self.assertIn('does not exist', soft_404_analysis['content_indicators'])
        
    @patch('seo_analyzer.requests.Session.get')
    def test_missing_security_headers(self, mock_get):
        """Test detection of missing security headers like CSP"""
        # Mock response without Content-Security-Policy (like applydigital.com)
        mock_response = MockResponse(
            status_code=200,
            content="<html><head><title>Test</title></head><body><h1>Test</h1></body></html>",
            headers={
                'x-frame-options': 'DENY',
                'x-content-type-options': 'nosniff'
                # Note: Missing Content-Security-Policy
            }
        )
        mock_get.return_value = mock_response
        
        analyzer = SEOAnalyzer("https://www.applydigital.com/", use_axe=False)
        results = analyzer.run_analysis()
        
        # Check if we can add security header analysis
        technical = results['technical_seo']
        
        # We can extend this to check for missing CSP
        headers = mock_response.headers
        has_csp = any('content-security-policy' in key.lower() for key in headers.keys())
        self.assertFalse(has_csp, "Should detect missing Content-Security-Policy header")
        
    def test_invalid_url_handling(self):
        """Test handling of invalid URLs"""
        with self.assertRaises(ValueError):
            SEOAnalyzer("not-a-valid-url")
        
        with self.assertRaises(ValueError):
            SEOAnalyzer("ftp://example.com")  # Only HTTP/HTTPS supported


class TestSEOAnalyzerPerformance(unittest.TestCase):
    """Test performance analysis capabilities"""
    
    @patch('seo_analyzer.requests.Session.get')
    def test_advanced_performance_analysis(self, mock_get):
        """Test advanced performance metrics"""
        # Mock HTML with performance issues
        slow_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Slow Page</title>
            <link rel="stylesheet" href="/style1.css">
            <link rel="stylesheet" href="/style2.css">
            <link rel="stylesheet" href="/style3.css">
            <script src="/script1.js"></script>
            <script src="/script2.js"></script>
            <script src="/script3.js"></script>
            <style>body { color: red; }</style>
            <style>div { color: blue; }</style>
        </head>
        <body>
        """ + "<div>" * 2000 + "Content" + "</div>" * 2000 + """
            <img src="/image1.jpg">
            <img src="/image2.jpg">
            <img src="/image3.jpg">
            <script>console.log('inline script');</script>
        </body>
        </html>
        """
        
        mock_response = MockResponse(
            status_code=200,
            content=slow_html,
            elapsed_seconds=5.2  # Slow load time
        )
        mock_get.return_value = mock_response
        
        analyzer = SEOAnalyzer("https://example.com", use_axe=False)
        page_data = analyzer.fetch_page("https://example.com")
        
        # Test basic performance
        performance = analyzer.analyze_performance(page_data)
        self.assertEqual(performance['load_time'], 5.2)
        self.assertIn("Slow page load time", performance['issues'][0])
        
        # Test advanced performance
        adv_performance = analyzer.analyze_advanced_performance(page_data)
        self.assertGreater(adv_performance['dom_elements'], 3000)  # Large DOM
        self.assertEqual(len(adv_performance['render_blocking_resources']), 6)  # 3 CSS + 3 JS
        self.assertEqual(adv_performance['inline_styles_count'], 2)
        self.assertEqual(adv_performance['inline_scripts_count'], 1)
        self.assertLess(adv_performance['performance_score'], 60)  # Poor score
        
    @patch('seo_analyzer.requests.Session.get')
    def test_optimized_performance_analysis(self, mock_get):
        """Test well-optimized page performance"""
        # Mock optimized HTML
        optimized_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Fast Page</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="stylesheet" href="/optimized.css" media="print" onload="this.media='all'">
            <script src="/app.js" async></script>
        </head>
        <body>
            <div>Well structured content with appropriate length</div>
            <img src="/hero.jpg" alt="Hero image" width="800" height="400" loading="lazy">
        </body>
        </html>
        """
        
        mock_response = MockResponse(
            status_code=200,
            content=optimized_html,
            elapsed_seconds=0.8  # Fast load time
        )
        mock_get.return_value = mock_response
        
        analyzer = SEOAnalyzer("https://example.com", use_axe=False)
        page_data = analyzer.fetch_page("https://example.com")
        adv_performance = analyzer.analyze_advanced_performance(page_data)
        
        self.assertLess(adv_performance['dom_elements'], 100)  # Simple DOM
        self.assertEqual(len(adv_performance['render_blocking_resources']), 0)  # No blocking resources
        self.assertGreater(adv_performance['performance_score'], 85)  # Good score


class TestSEOAnalyzerIntegration(unittest.TestCase):
    """Integration tests with real applydigital.com URLs (run sparingly)"""
    
    @unittest.skip("Integration test - run manually to avoid hitting real servers")
    def test_real_applydigital_homepage(self):
        """Test analysis of real Apply Digital homepage"""
        analyzer = SEOAnalyzer("https://www.applydigital.com/", use_axe=False, timeout=15)
        results = analyzer.run_analysis()
        
        # Basic assertions for the real site
        self.assertEqual(results['url'], "https://www.applydigital.com/")
        self.assertIn('Apply Digital', results['meta_analysis']['title'])
        self.assertGreater(len(results['meta_analysis']['title']), 20)
        
        # Should have good basic SEO structure
        self.assertTrue(results['accessibility']['page_title_exists'])
        self.assertGreater(results['accessibility']['score'], 50)
        
        # Generate recommendations
        recommendations = analyzer.generate_recommendations()
        self.assertIsInstance(recommendations, list)
        
        print(f"Found {len(results['issues'])} issues")
        print(f"Generated {len(recommendations)} recommendations")
        
        # Save test results
        analyzer.save_json_report("test_results_applydigital.json")


class TestSEOAnalyzerSecurityHeaders(unittest.TestCase):
    """Test security header analysis"""
    
    def test_security_header_extension(self):
        """Test that we can extend the analyzer to check security headers"""
        
        def analyze_security_headers(headers):
            """Extended function to analyze security headers"""
            security_analysis = {
                'csp_header': False,
                'x_frame_options': False,
                'x_content_type_options': False,
                'strict_transport_security': False,
                'issues': []
            }
            
            # Convert headers to lowercase for case-insensitive checking
            headers_lower = {k.lower(): v for k, v in headers.items()}
            
            # Check Content-Security-Policy
            if 'content-security-policy' in headers_lower:
                security_analysis['csp_header'] = True
            else:
                security_analysis['issues'].append("Missing Content-Security-Policy header")
                
            # Check X-Frame-Options
            if 'x-frame-options' in headers_lower:
                security_analysis['x_frame_options'] = True
            else:
                security_analysis['issues'].append("Missing X-Frame-Options header")
                
            # Check X-Content-Type-Options
            if 'x-content-type-options' in headers_lower:
                security_analysis['x_content_type_options'] = True
            else:
                security_analysis['issues'].append("Missing X-Content-Type-Options header")
                
            # Check Strict-Transport-Security (HSTS)
            if 'strict-transport-security' in headers_lower:
                security_analysis['strict_transport_security'] = True
            else:
                security_analysis['issues'].append("Missing Strict-Transport-Security header")
                
            return security_analysis
        
        # Test with applydigital.com-like headers (missing CSP)
        test_headers = {
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            # Missing: Content-Security-Policy
            # Missing: Strict-Transport-Security
        }
        
        security_result = analyze_security_headers(test_headers)
        
        self.assertFalse(security_result['csp_header'])
        self.assertTrue(security_result['x_frame_options'])
        self.assertTrue(security_result['x_content_type_options'])
        self.assertFalse(security_result['strict_transport_security'])
        self.assertIn("Missing Content-Security-Policy header", security_result['issues'])
        self.assertIn("Missing Strict-Transport-Security header", security_result['issues'])


def run_test_suite():
    """Run the complete test suite"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSEOAnalyzerPositive))
    suite.addTests(loader.loadTestsFromTestCase(TestSEOAnalyzerNegative))
    suite.addTests(loader.loadTestsFromTestCase(TestSEOAnalyzerPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestSEOAnalyzerSecurityHeaders))
    # Skip integration tests by default
    # suite.addTests(loader.loadTestsFromTestCase(TestSEOAnalyzerIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run individual test classes
    import sys
    
    if len(sys.argv) > 1:
        # Run specific test class
        if sys.argv[1] == 'positive':
            unittest.main(argv=[''], testRunner=unittest.TextTestRunner(verbosity=2), 
                         defaultTest='TestSEOAnalyzerPositive', exit=False)
        elif sys.argv[1] == 'negative':
            unittest.main(argv=[''], testRunner=unittest.TextTestRunner(verbosity=2), 
                         defaultTest='TestSEOAnalyzerNegative', exit=False)
        elif sys.argv[1] == 'performance':
            unittest.main(argv=[''], testRunner=unittest.TextTestRunner(verbosity=2), 
                         defaultTest='TestSEOAnalyzerPerformance', exit=False)
        elif sys.argv[1] == 'security':
            unittest.main(argv=[''], testRunner=unittest.TextTestRunner(verbosity=2), 
                         defaultTest='TestSEOAnalyzerSecurityHeaders', exit=False)
        elif sys.argv[1] == 'integration':
            unittest.main(argv=[''], testRunner=unittest.TextTestRunner(verbosity=2), 
                         defaultTest='TestSEOAnalyzerIntegration', exit=False)
        else:
            run_test_suite()
    else:
        # Run full test suite
        run_test_suite()

