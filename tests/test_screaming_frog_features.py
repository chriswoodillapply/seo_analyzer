#!/usr/bin/env python3
"""
Test Enhanced SEO Analyzer Features Based on Screaming Frog Analysis

This test suite validates the new features added based on Screaming Frog's test coverage:
- Enhanced H1-H6 analysis
- Google pixel-based title/description lengths
- Anchor text quality analysis
- Image file size detection
- URL length analysis
- Security header analysis
"""

import unittest
from unittest.mock import Mock
from bs4 import BeautifulSoup
from seo_analyzer import SEOAnalyzer
from test_seo_analyzer import MockResponse


class TestScreamingFrogEnhancements(unittest.TestCase):
    """Test new features inspired by Screaming Frog analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = SEOAnalyzer("https://example.com", use_axe=False)
        
    def test_pixel_based_title_analysis(self):
        """Test Google pixel-based title length calculation"""
        # Test pixel calculation
        short_title = "Test"  # Should be ~28 pixels
        long_title = "This is a very long title that should exceed Google's pixel limit for display in search results"
        
        short_pixels = self.analyzer.calculate_google_pixels(short_title)
        long_pixels = self.analyzer.calculate_google_pixels(long_title)
        
        self.assertLess(short_pixels, 200)  # Should be below threshold
        self.assertGreater(long_pixels, 561)  # Should exceed threshold
        
    def test_enhanced_meta_analysis(self):
        """Test enhanced meta tag analysis with pixel-based limits"""
        html = """
        <html>
        <head>
            <title>Short</title>
            <meta name="description" content="Very short description">
        </head>
        <body><h1>Different Header</h1></body>
        </html>
        """
        
        page_data = {
            'soup': BeautifulSoup(html, 'html.parser'),
            'url': 'https://example.com',
            'text': html
        }
        
        meta_analysis = self.analyzer.analyze_meta_tags(page_data)
        
        # Should detect short title and description
        self.assertIn("Below", str(meta_analysis['issues']))
        self.assertGreater(len(meta_analysis['recommendations']), 0)
        self.assertFalse(meta_analysis['title_same_as_h1'])  # Different from H1
        
    def test_title_same_as_h1_detection(self):
        """Test detection when title matches H1 exactly"""
        html = """
        <html>
        <head><title>Same Title</title></head>
        <body><h1>Same Title</h1></body>
        </html>
        """
        
        page_data = {
            'soup': BeautifulSoup(html, 'html.parser'),
            'url': 'https://example.com',
            'text': html
        }
        
        meta_analysis = self.analyzer.analyze_meta_tags(page_data)
        
        self.assertTrue(meta_analysis['title_same_as_h1'])
        self.assertIn("Same as H1", str(meta_analysis['issues']))
        
    def test_enhanced_header_analysis(self):
        """Test comprehensive H1-H6 analysis"""
        html = """
        <html>
        <body>
            <h1>Main Title</h1>
            <h3>Skipped H2</h3>
            <h2>Section 1</h2>
            <h2>Section 1</h2>
            <h1>Another H1</h1>
            <h2>This is a very long header that exceeds the recommended 70 character limit for conciseness</h2>
        </body>
        </html>
        """
        
        page_data = {
            'soup': BeautifulSoup(html, 'html.parser'),
            'url': 'https://example.com'
        }
        
        header_analysis = self.analyzer.analyze_headers(page_data)
        
        # Should detect multiple H1s
        self.assertIn("Multiple H1", str(header_analysis['issues']))
        
        # Should detect non-sequential headers (H3 before H2)
        self.assertGreater(len(header_analysis['non_sequential_headers']), 0)
        
        # Should detect duplicate H2s
        self.assertIn('h2', header_analysis['duplicate_headers'])
        
        # Should detect long headers
        self.assertGreater(len(header_analysis['long_headers']), 0)
        
        # Should have recommendations
        self.assertGreater(len(header_analysis['recommendations']), 0)
        
    def test_missing_h2_detection(self):
        """Test detection of missing H2 tags"""
        html = """
        <html>
        <body>
            <h1>Main Title</h1>
            <h3>No H2 Before This</h3>
        </body>
        </html>
        """
        
        page_data = {
            'soup': BeautifulSoup(html, 'html.parser'),
            'url': 'https://example.com'
        }
        
        header_analysis = self.analyzer.analyze_headers(page_data)
        
        self.assertIn('h2', header_analysis['missing_headers'])
        self.assertIn("Missing H2", str(header_analysis['issues']))
        
    def test_enhanced_image_analysis(self):
        """Test enhanced image analysis with Screaming Frog features"""
        html = """
        <html>
        <body>
            <img src="/small-image.jpg" alt="Good alt text">
            <img src="/large-hero-image.jpg" alt="">
            <img src="/another-image.jpg" alt="This is a very long alt text that exceeds the recommended 100 character limit for image descriptions">
            <img src="/no-alt-image.jpg">
        </body>
        </html>
        """
        
        page_data = {
            'soup': BeautifulSoup(html, 'html.parser'),
            'url': 'https://example.com'
        }
        
        image_analysis = self.analyzer.analyze_images(page_data)
        
        # Should detect missing alt text
        self.assertGreater(image_analysis['images_without_alt'], 0)
        
        # Should detect empty alt text
        self.assertGreater(image_analysis['images_with_empty_alt'], 0)
        
        # Should detect long alt text
        self.assertGreater(image_analysis['long_alt_text'], 0)
        
        # Should have Screaming Frog style issue messages
        self.assertIn("Alt Text Missing", str(image_analysis['issues']))
        self.assertIn("Alt Text Over 100 Characters", str(image_analysis['issues']))
        
        # Should have recommendations
        self.assertGreater(len(image_analysis['recommendations']), 0)
        
    def test_anchor_text_analysis(self):
        """Test non-descriptive anchor text detection"""
        html = """
        <html>
        <body>
            <a href="/page1">Click here</a>
            <a href="/page2">Learn more</a>
            <a href="/page3">Descriptive link text about the destination</a>
            <a href="/page4"></a>
            <a href="/page5"><img src="/icon.jpg" alt=""></a>
            <a href="/page6"><img src="/icon2.jpg" alt="Good alt text"></a>
        </body>
        </html>
        """
        
        page_data = {
            'soup': BeautifulSoup(html, 'html.parser'),
            'url': 'https://example.com'
        }
        
        link_analysis = self.analyzer.analyze_links(page_data)
        
        # Should detect non-descriptive anchor text
        self.assertGreater(link_analysis['non_descriptive_anchors'], 0)
        
        # Should detect missing anchor text
        self.assertGreater(link_analysis['missing_anchor_text'], 0)
        
        # Should have Screaming Frog style issue messages
        self.assertIn("Non-Descriptive Anchor Text", str(link_analysis['issues']))
        self.assertIn("No Anchor Text", str(link_analysis['issues']))
        
        # Should have recommendations
        self.assertGreater(len(link_analysis['recommendations']), 0)
        
    def test_high_external_outlinks_detection(self):
        """Test detection of high external outlinks"""
        html = "<html><body>"
        
        # Add 15 external links (threshold is 10)
        for i in range(15):
            html += f'<a href="https://external{i}.com">External Link {i}</a>'
            
        html += "</body></html>"
        
        page_data = {
            'soup': BeautifulSoup(html, 'html.parser'),
            'url': 'https://example.com'
        }
        
        link_analysis = self.analyzer.analyze_links(page_data)
        
        self.assertTrue(link_analysis['high_external_outlinks'])
        self.assertIn("High External Outlinks", str(link_analysis['issues']))
        
    def test_url_length_analysis(self):
        """Test URL length analysis"""
        # Long URL (over 115 characters)
        long_url = "https://example.com/very/long/path/that/exceeds/the/recommended/115/character/limit/for/urls/according/to/screaming/frog/analysis"
        
        page_data = {
            'url': long_url
        }
        
        url_analysis = self.analyzer.analyze_url_seo(page_data)
        
        self.assertTrue(url_analysis['is_long_url'])
        self.assertIn("Over 115 Characters", str(url_analysis['issues']))
        self.assertGreater(len(url_analysis['recommendations']), 0)
        
    def test_security_headers_analysis(self):
        """Test comprehensive security headers analysis"""
        page_data = {
            'headers': {
                'X-Frame-Options': 'DENY',
                'X-Content-Type-Options': 'nosniff',
                # Missing: Content-Security-Policy
                # Missing: Strict-Transport-Security
            },
            'url': 'https://example.com'
        }
        
        security_analysis = self.analyzer.analyze_security_headers(page_data)
        
        # Should detect missing CSP
        self.assertFalse(security_analysis['csp_header']['present'])
        
        # Should detect missing HSTS
        self.assertFalse(security_analysis['strict_transport_security']['present'])
        
        # Should have present headers
        self.assertTrue(security_analysis['x_frame_options']['present'])
        self.assertTrue(security_analysis['x_content_type_options']['present'])
        
        # Should calculate security score
        self.assertLess(security_analysis['security_score'], 100)
        self.assertGreater(security_analysis['security_score'], 0)
        
        # Should have issues and recommendations
        self.assertIn("Content-Security-Policy", str(security_analysis['issues']))
        self.assertGreater(len(security_analysis['recommendations']), 0)
        
    def test_comprehensive_analysis_with_enhancements(self):
        """Test full analysis with all enhancements"""
        # Create comprehensive test HTML
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page That Has A Very Long Title Exceeding Recommended Length</title>
            <meta name="description" content="Short desc">
        </head>
        <body>
            <h1>Test Page That Has A Very Long Title Exceeding Recommended Length</h1>
            <h3>Skipped H2</h3>
            <h2>Section</h2>
            <img src="/large-hero.jpg" alt="" width="1920" height="1080">
            <img src="/small.jpg" alt="This is a very long alt text description that exceeds one hundred characters limit set by accessibility guidelines">
            <a href="/page1">Click here</a>
            <a href="https://external1.com">External 1</a>
            <a href="https://external2.com">External 2</a>
            <p>This is content that might be too short for proper SEO.</p>
        </body>
        </html>
        """
        
        mock_response = MockResponse(
            status_code=200,
            content=html,
            headers={
                'X-Frame-Options': 'DENY',
                # Missing CSP
            }
        )
        
        page_data = {
            'url': 'https://example.com/very-long-url-path-that-exceeds-recommended-length-limits-set-by-screaming-frog-analysis-tools',
            'status_code': 200,
            'content': mock_response.content,
            'text': mock_response.text,
            'soup': BeautifulSoup(html, 'html.parser'),
            'headers': mock_response.headers,
            'load_time': 1.2,
            'response': mock_response
        }
        
        # Run all analyses
        meta_results = self.analyzer.analyze_meta_tags(page_data)
        header_results = self.analyzer.analyze_headers(page_data)
        image_results = self.analyzer.analyze_images(page_data)
        link_results = self.analyzer.analyze_links(page_data)
        url_results = self.analyzer.analyze_url_seo(page_data)
        security_results = self.analyzer.analyze_security_headers(page_data)
        
        # Verify comprehensive detection
        total_issues = 0
        total_recommendations = 0
        
        for results in [meta_results, header_results, image_results, link_results, url_results, security_results]:
            total_issues += len(results.get('issues', []))
            total_recommendations += len(results.get('recommendations', []))
            
        # Should find multiple issues across all categories
        self.assertGreater(total_issues, 10)  # Expect significant issues
        self.assertGreater(total_recommendations, 8)  # Expect actionable recommendations
        
        # Verify specific Screaming Frog style detections
        self.assertIn("Same as H1", str(meta_results['issues']))  # Title = H1
        self.assertIn("Non-Sequential", str(header_results['issues']))  # H3 before H2
        self.assertIn("Alt Text Over 100", str(image_results['issues']))  # Long alt text
        self.assertIn("Non-Descriptive", str(link_results['issues']))  # "Click here"
        self.assertIn("Over 115 Characters", str(url_results['issues']))  # Long URL
        self.assertIn("Content-Security-Policy", str(security_results['issues']))  # Missing CSP


def run_screaming_frog_tests():
    """Run the Screaming Frog enhancement tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestScreamingFrogEnhancements)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n{'='*60}")
    print(f"Screaming Frog Enhancement Tests Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.wasSuccessful():
        print("✅ All Screaming Frog enhancements working correctly!")
    else:
        print("❌ Some enhancements need attention")
        
    return result.wasSuccessful()


if __name__ == '__main__':
    run_screaming_frog_tests()

