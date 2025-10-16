#!/usr/bin/env python3
"""
SEOTestExecutor - Executes SEO tests dynamically based on test catalog
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re

from .content_fetcher import PageContent


class TestStatus(Enum):
    """Test execution status"""
    PASS = "Pass"
    FAIL = "Fail"
    WARNING = "Warning"
    INFO = "Info"
    ERROR = "Error"


@dataclass
class TestResult:
    """Result of a single test execution"""
    url: str
    test_id: str
    test_name: str
    category: str
    status: TestStatus
    severity: str
    issue_description: str
    recommendation: str
    score: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for reporting"""
        return {
            'URL': self.url,
            'Test_ID': self.test_id,
            'Test_Name': self.test_name,
            'Category': self.category,
            'Status': self.status.value,
            'Severity': self.severity,
            'Issue_Description': self.issue_description,
            'Recommendation': self.recommendation,
            'Score': self.score,
            'Timestamp': self.timestamp
        }


class SEOTestExecutor:
    """
    Executes SEO tests on fetched page content
    Implements a plugin-based architecture for easy test addition
    """
    
    def __init__(self):
        """Initialize the test executor"""
        self.test_methods = self._register_test_methods()
    
    def _register_test_methods(self) -> Dict[str, callable]:
        """Register all test methods"""
        return {
            # Meta Tags Tests
            'meta_title_presence': self._test_title_presence,
            'meta_title_length': self._test_title_length,
            'meta_description_presence': self._test_description_presence,
            'meta_description_length': self._test_description_length,
            'canonical_url': self._test_canonical_url,
            'robots_meta_tag': self._test_robots_meta,
            'viewport_meta_tag': self._test_viewport,
            'open_graph_tags': self._test_open_graph,
            
            # Header Structure Tests
            'h1_presence': self._test_h1_presence,
            'h1_uniqueness': self._test_h1_uniqueness,
            'header_hierarchy': self._test_header_hierarchy,
            'h2_presence': self._test_h2_presence,
            
            # Image Tests
            'img_alt_text': self._test_image_alt_text,
            'img_lazy_loading': self._test_image_lazy_loading,
            
            # Link Tests
            'internal_links': self._test_internal_links,
            'external_links': self._test_external_links,
            'anchor_text_quality': self._test_anchor_text_quality,
            
            # Content Tests
            'content_word_count': self._test_content_word_count,
            'soft_404_detection': self._test_soft_404_detection,
            'content_readability': self._test_content_readability,
            'content_structure': self._test_content_structure,
            
            # Technical SEO Tests
            'ssl_certificate': self._test_ssl_certificate,
            'robots_txt': self._test_robots_txt,
            'sitemap_xml': self._test_sitemap_xml,
            'schema_markup': self._test_schema_markup,
            
            # Performance Tests
            'page_load_time': self._test_page_load_time,
            'page_size': self._test_page_size,
            'dom_complexity': self._test_dom_complexity,
            
            # Core Web Vitals Tests
            'largest_contentful_paint': self._test_lcp,
            'cumulative_layout_shift': self._test_cls,
            'first_contentful_paint': self._test_fcp,
            
            # Accessibility Tests
            'lang_attribute': self._test_lang_attribute,
            'form_labels': self._test_form_labels,
            'semantic_html': self._test_semantic_html,
            
            # Mobile Tests
            'mobile_viewport': self._test_mobile_viewport,
            'mobile_font_sizes': self._test_mobile_font_sizes,
            
            # Security Tests
            'security_headers': self._test_security_headers,
            
            # ========== NEW TESTS - PHASE 1 ==========
            # Additional Meta Tags Tests
            'twitter_card_tags': self._test_twitter_card_tags,
            'meta_refresh_redirect': self._test_meta_refresh_redirect,
            'duplicate_meta_tags': self._test_duplicate_meta_tags,
            'favicon_presence': self._test_favicon_presence,
            
            # Additional Header Tests
            'empty_headers': self._test_empty_headers,
            'header_level_gaps': self._test_header_level_gaps,
            
            # Additional Image Tests
            'img_dimensions_specified': self._test_image_dimensions,
            'img_modern_formats': self._test_modern_image_formats,
            'img_responsive_srcset': self._test_responsive_images_srcset,
            
            # Additional Link Tests
            'nofollow_links_analysis': self._test_nofollow_links_analysis,
            'external_link_security': self._test_external_link_security,
            'pagination_rel_tags': self._test_pagination_tags,
            'link_density_ratio': self._test_link_density_ratio,
            
            # Additional Technical SEO Tests
            'url_parameters': self._test_url_parameters,
            'trailing_slash_consistency': self._test_trailing_slash_consistency,
            'mixed_content_detection': self._test_mixed_content_detection,
            
            # Additional Performance Tests
            'gzip_compression': self._test_gzip_compression,
            'cache_headers': self._test_cache_headers,
            
            # ========== NEW TESTS - PHASE 2 ==========
            # Structured Data Tests
            'schema_organization': self._test_schema_organization,
            'schema_breadcrumb': self._test_schema_breadcrumb,
            'video_schema_markup': self._test_video_schema_markup,
            
            # International SEO Tests
            'hreflang_tags': self._test_hreflang_tags,
            'meta_keywords_presence': self._test_meta_keywords,
            
            # Content Analysis Tests
            'header_keyword_optimization': self._test_header_keyword_optimization,
            'content_freshness_date': self._test_content_freshness_date,
            'multimedia_diversity': self._test_multimedia_diversity,
            
            # Advanced Image Tests
            'img_oversized_files': self._test_oversized_images,
            
            # Advanced Link Tests
            'broken_internal_links': self._test_broken_internal_links,
            'table_of_contents': self._test_table_of_contents,
            
            # Advanced Technical SEO Tests
            'sitemap_index_presence': self._test_sitemap_index,
            'robots_txt_quality': self._test_robots_txt_quality,
            'url_structure_analysis': self._test_url_structure_analysis,
            'redirect_chain_detection': self._test_redirect_chain_detection,
            'www_consistency': self._test_www_consistency,
            
            # Advanced Performance Tests
            'render_blocking_resources': self._test_render_blocking_resources,
            'third_party_scripts': self._test_third_party_scripts,
            
            # Additional Accessibility Tests
            'aria_landmarks': self._test_aria_landmarks,
            
            # ========== NEW TESTS - PHASE 3 ==========
            # Performance Optimization
            'cdn_usage': self._test_cdn_usage,
            'web_font_optimization': self._test_web_font_optimization,
            
            # Mobile Optimization
            'mobile_content_width': self._test_mobile_content_width,
            'responsive_image_strategy': self._test_responsive_image_strategy,
            
            # Accessibility Enhancements
            'heading_accessibility_gaps': self._test_heading_accessibility_gaps,
            'form_error_handling': self._test_form_error_handling,
            
            # Security Enhancements
            'subresource_integrity': self._test_subresource_integrity,
            'iframe_security': self._test_iframe_security,
            'cors_headers': self._test_cors_headers,
            'cookie_security_flags': self._test_cookie_security_flags,
            
            # International Enhancements
            'content_language_meta': self._test_content_language_meta,
            
            # ========== NEW TESTS - PHASE 4 ==========
            # Multi-Page Analysis (Placeholders)
            'thin_content_detection': self._test_thin_content_detection,
            'orphan_page_check': self._test_orphan_page_check,
            'deep_link_ratio': self._test_deep_link_ratio,
            'navigation_depth': self._test_navigation_depth,
            'touch_target_sizes': self._test_touch_target_sizes,
            'intrusive_interstitial': self._test_intrusive_interstitial,
            'color_contrast_check': self._test_color_contrast_check,
            'focus_visible_styles': self._test_focus_visible_styles,
            'video_captions': self._test_video_captions,
            'hreflang_validation': self._test_hreflang_validation,
            'geo_targeting_meta': self._test_geo_targeting_meta,
            'amp_version_presence': self._test_amp_version_presence,
        }
    
    def execute_all_tests(self, page_content: PageContent) -> List[TestResult]:
        """
        Execute all applicable tests on the page content
        
        Args:
            page_content: Fetched page content
            
        Returns:
            List of test results
        """
        results = []
        
        # Execute each registered test
        for test_id, test_method in self.test_methods.items():
            try:
                result = test_method(page_content)
                if result:
                    results.append(result)
            except Exception as e:
                # Log error but continue with other tests
                results.append(TestResult(
                    url=page_content.url,
                    test_id=test_id,
                    test_name=f"Test: {test_id}",
                    category="Test Error",
                    status=TestStatus.ERROR,
                    severity="Error",
                    issue_description=f"Test execution failed: {str(e)}",
                    recommendation="Check test implementation",
                    score="N/A"
                ))
        
        return results
    
    def execute_specific_tests(
        self,
        page_content: PageContent,
        test_ids: List[str]
    ) -> List[TestResult]:
        """
        Execute specific tests by ID
        
        Args:
            page_content: Fetched page content
            test_ids: List of test IDs to execute
            
        Returns:
            List of test results
        """
        results = []
        
        for test_id in test_ids:
            if test_id in self.test_methods:
                try:
                    result = self.test_methods[test_id](page_content)
                    if result:
                        results.append(result)
                except Exception as e:
                    results.append(TestResult(
                        url=page_content.url,
                        test_id=test_id,
                        test_name=f"Test: {test_id}",
                        category="Test Error",
                        status=TestStatus.ERROR,
                        severity="Error",
                        issue_description=f"Test execution failed: {str(e)}",
                        recommendation="Check test implementation",
                        score="N/A"
                    ))
        
        return results
    
    # =========================================================================
    # META TAGS TESTS
    # =========================================================================
    
    def _test_title_presence(self, content: PageContent) -> TestResult:
        """Test if page has a title tag"""
        soup = content.rendered_soup or content.static_soup
        title = soup.find('title')
        
        if title and title.text.strip():
            return TestResult(
                url=content.url,
                test_id='meta_title_presence',
                test_name='Page Title Presence',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Critical',
                issue_description='Page has a valid title tag',
                recommendation='Continue maintaining proper title tags',
                score=f'Title: "{title.text.strip()[:50]}..."'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='meta_title_presence',
                test_name='Page Title Presence',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='Critical',
                issue_description='Missing or empty title tag',
                recommendation='Add a descriptive, unique title tag to the page',
                score='No title found'
            )
    
    def _test_title_length(self, content: PageContent) -> TestResult:
        """Test title length"""
        soup = content.rendered_soup or content.static_soup
        title = soup.find('title')
        
        if not title:
            return None
        
        title_text = title.text.strip()
        length = len(title_text)
        
        # Estimate pixel width (rough calculation)
        pixel_width = length * 10  # Approximate
        
        if 30 <= length <= 60:
            status = TestStatus.PASS
            issue = f'Title length is optimal ({length} characters, ~{pixel_width}px)'
            recommendation = 'Title length is well optimized'
        elif length < 30:
            status = TestStatus.WARNING
            issue = f'Title is too short ({length} characters)'
            recommendation = 'Expand title to 30-60 characters for better SEO'
        else:
            status = TestStatus.WARNING
            issue = f'Title is too long ({length} characters, ~{pixel_width}px)'
            recommendation = 'Shorten title to prevent truncation in search results'
        
        return TestResult(
            url=content.url,
            test_id='meta_title_length',
            test_name='Title Length',
            category='Meta Tags',
            status=status,
            severity='High',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{length} chars / ~{pixel_width}px'
        )
    
    def _test_description_presence(self, content: PageContent) -> TestResult:
        """Test if page has meta description"""
        soup = content.rendered_soup or content.static_soup
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        if meta_desc and meta_desc.get('content', '').strip():
            desc_text = meta_desc['content'].strip()
            return TestResult(
                url=content.url,
                test_id='meta_description_presence',
                test_name='Meta Description Presence',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Page has a meta description',
                recommendation='Continue maintaining unique meta descriptions',
                score=f'{len(desc_text)} characters'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='meta_description_presence',
                test_name='Meta Description Presence',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Missing or empty meta description',
                recommendation='Add unique, compelling meta description (120-160 chars)',
                score='No description found'
            )
    
    def _test_description_length(self, content: PageContent) -> TestResult:
        """Test meta description length"""
        soup = content.rendered_soup or content.static_soup
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc or not meta_desc.get('content'):
            return None
        
        desc_text = meta_desc['content'].strip()
        length = len(desc_text)
        
        if 120 <= length <= 160:
            status = TestStatus.PASS
            issue = f'Description length is optimal ({length} characters)'
            recommendation = 'Description length is well optimized'
        elif length < 120:
            status = TestStatus.WARNING
            issue = f'Description is too short ({length} characters)'
            recommendation = 'Expand description to 120-160 characters'
        else:
            status = TestStatus.WARNING
            issue = f'Description is too long ({length} characters)'
            recommendation = 'Shorten description to prevent truncation in SERPs'
        
        return TestResult(
            url=content.url,
            test_id='meta_description_length',
            test_name='Meta Description Length',
            category='Meta Tags',
            status=status,
            severity='Medium',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{length} characters'
        )
    
    def _test_canonical_url(self, content: PageContent) -> TestResult:
        """Test canonical URL"""
        soup = content.rendered_soup or content.static_soup
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        
        if canonical and canonical.get('href'):
            return TestResult(
                url=content.url,
                test_id='canonical_url',
                test_name='Canonical URL',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Canonical URL is properly set',
                recommendation='Ensure canonical URL points to the preferred version',
                score=f'Points to: {canonical["href"][:50]}...'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='canonical_url',
                test_name='Canonical URL',
                category='Meta Tags',
                status=TestStatus.WARNING,
                severity='High',
                issue_description='Missing canonical URL',
                recommendation='Add canonical URL to prevent duplicate content issues',
                score='No canonical tag found'
            )
    
    def _test_robots_meta(self, content: PageContent) -> TestResult:
        """Test robots meta tag"""
        soup = content.rendered_soup or content.static_soup
        robots = soup.find('meta', attrs={'name': 'robots'})
        
        if robots:
            robots_content = robots.get('content', '').lower()
            if 'noindex' in robots_content or 'nofollow' in robots_content:
                return TestResult(
                    url=content.url,
                    test_id='robots_meta_tag',
                    test_name='Robots Meta Tag',
                    category='Meta Tags',
                    status=TestStatus.WARNING,
                    severity='Medium',
                    issue_description=f'Robots tag restricts indexing: {robots_content}',
                    recommendation='Review if this page should be restricted from search engines',
                    score=robots_content
                )
        
        return TestResult(
            url=content.url,
            test_id='robots_meta_tag',
            test_name='Robots Meta Tag',
            category='Meta Tags',
            status=TestStatus.PASS,
            severity='Medium',
            issue_description='Page allows indexing and following',
            recommendation='Continue allowing search engine access',
            score='No restrictions'
        )
    
    def _test_viewport(self, content: PageContent) -> TestResult:
        """Test viewport meta tag"""
        soup = content.rendered_soup or content.static_soup
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        
        if viewport and viewport.get('content'):
            return TestResult(
                url=content.url,
                test_id='viewport_meta_tag',
                test_name='Viewport Meta Tag',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Viewport is properly configured for mobile',
                recommendation='Continue maintaining proper viewport configuration',
                score=viewport['content']
            )
        else:
            return TestResult(
                url=content.url,
                test_id='viewport_meta_tag',
                test_name='Viewport Meta Tag',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Missing viewport meta tag',
                recommendation='Add viewport meta tag for mobile responsiveness',
                score='No viewport tag'
            )
    
    def _test_open_graph(self, content: PageContent) -> TestResult:
        """Test Open Graph tags"""
        soup = content.rendered_soup or content.static_soup
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        
        og_count = sum([bool(og_title), bool(og_desc), bool(og_image)])
        
        if og_count >= 2:
            return TestResult(
                url=content.url,
                test_id='open_graph_tags',
                test_name='Open Graph Tags',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Found {og_count}/3 recommended Open Graph tags',
                recommendation='Continue maintaining Open Graph tags for social sharing',
                score=f'{og_count}/3 tags present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='open_graph_tags',
                test_name='Open Graph Tags',
                category='Meta Tags',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Missing Open Graph tags ({og_count}/3 found)',
                recommendation='Add og:title, og:description, and og:image for better social sharing',
                score=f'{og_count}/3 tags present'
            )
    
    # =========================================================================
    # HEADER STRUCTURE TESTS
    # =========================================================================
    
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
                severity='Critical',
                issue_description='Page has exactly one H1 tag',
                recommendation='Continue using single H1 for main heading',
                score=f'H1: "{h1_tags[0].text.strip()[:50]}..."'
            )
        elif len(h1_tags) == 0:
            return TestResult(
                url=content.url,
                test_id='h1_presence',
                test_name='H1 Tag Presence',
                category='Header Structure',
                status=TestStatus.FAIL,
                severity='Critical',
                issue_description='Page is missing H1 tag',
                recommendation='Add exactly one H1 tag for the main page heading',
                score='0 H1 tags'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='h1_presence',
                test_name='H1 Tag Presence',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Critical',
                issue_description=f'Page has {len(h1_tags)} H1 tags (should have 1)',
                recommendation='Use exactly one H1 tag per page',
                score=f'{len(h1_tags)} H1 tags'
            )
    
    def _test_h1_uniqueness(self, content: PageContent) -> TestResult:
        """Test H1 uniqueness (placeholder - requires multi-page context)"""
        soup = content.rendered_soup or content.static_soup
        h1_tags = soup.find_all('h1')
        
        if h1_tags:
            return TestResult(
                url=content.url,
                test_id='h1_uniqueness',
                test_name='H1 Tag Uniqueness',
                category='Header Structure',
                status=TestStatus.INFO,
                severity='High',
                issue_description='H1 uniqueness check requires multi-page analysis',
                recommendation='Ensure H1 is unique across all pages',
                score='Multi-page check required'
            )
        return None
    
    def _test_header_hierarchy(self, content: PageContent) -> TestResult:
        """Test header hierarchy"""
        soup = content.rendered_soup or content.static_soup
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headers:
            return TestResult(
                url=content.url,
                test_id='header_hierarchy',
                test_name='Header Hierarchy',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No header tags found',
                recommendation='Add proper header structure for content organization',
                score='No headers'
            )
        
        # Check for proper hierarchy
        header_levels = [int(h.name[1]) for h in headers]
        has_h1 = 1 in header_levels
        
        if has_h1:
            return TestResult(
                url=content.url,
                test_id='header_hierarchy',
                test_name='Header Hierarchy',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Found proper header structure with {len(headers)} headers',
                recommendation='Maintain logical header hierarchy',
                score=f'{len(headers)} total headers'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='header_hierarchy',
                test_name='Header Hierarchy',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Header hierarchy missing H1',
                recommendation='Add H1 tag for proper content structure',
                score=f'{len(headers)} headers without H1'
            )
    
    def _test_h2_presence(self, content: PageContent) -> TestResult:
        """Test H2 tag presence"""
        soup = content.rendered_soup or content.static_soup
        h2_tags = soup.find_all('h2')
        
        if len(h2_tags) >= 2:
            return TestResult(
                url=content.url,
                test_id='h2_presence',
                test_name='H2 Tag Presence',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Page has {len(h2_tags)} H2 tags for content structure',
                recommendation='Continue using H2 tags to organize content sections',
                score=f'{len(h2_tags)} H2 tags'
            )
        elif len(h2_tags) == 0:
            return TestResult(
                url=content.url,
                test_id='h2_presence',
                test_name='H2 Tag Presence',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No H2 tags found',
                recommendation='Add H2 tags to structure content sections',
                score='0 H2 tags'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='h2_presence',
                test_name='H2 Tag Presence',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Page has H2 tags',
                recommendation='Consider adding more H2 tags for longer content',
                score=f'{len(h2_tags)} H2 tag'
            )
    
    # =========================================================================
    # IMAGE TESTS
    # =========================================================================
    
    def _test_image_alt_text(self, content: PageContent) -> TestResult:
        """Test image alt text"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return TestResult(
                url=content.url,
                test_id='img_alt_text',
                test_name='Image Alt Text',
                category='Images',
                status=TestStatus.INFO,
                severity='High',
                issue_description='No images found on page',
                recommendation='N/A - No images present',
                score='0 images'
            )
        
        missing_alt = [img for img in images if not img.get('alt')]
        
        if len(missing_alt) == 0:
            return TestResult(
                url=content.url,
                test_id='img_alt_text',
                test_name='Image Alt Text',
                category='Images',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'All {len(images)} images have alt text',
                recommendation='Continue providing descriptive alt text',
                score=f'{len(images)}/{len(images)} images with alt'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_alt_text',
                test_name='Image Alt Text',
                category='Images',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{len(missing_alt)} of {len(images)} images missing alt text',
                recommendation='Add descriptive alt text to all images for accessibility',
                score=f'{len(images)-len(missing_alt)}/{len(images)} images with alt'
            )
    
    def _test_image_lazy_loading(self, content: PageContent) -> TestResult:
        """Test image lazy loading"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return None
        
        lazy_images = [img for img in images if img.get('loading') == 'lazy']
        
        if len(lazy_images) > 0:
            return TestResult(
                url=content.url,
                test_id='img_lazy_loading',
                test_name='Image Lazy Loading',
                category='Images',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'{len(lazy_images)} of {len(images)} images use lazy loading',
                recommendation='Consider lazy loading for below-fold images',
                score=f'{len(lazy_images)}/{len(images)} lazy loaded'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_lazy_loading',
                test_name='Image Lazy Loading',
                category='Images',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No images use lazy loading',
                recommendation='Implement lazy loading for below-fold images to improve performance',
                score='0 lazy loaded images'
            )
    
    # =========================================================================
    # LINK TESTS
    # =========================================================================
    
    def _test_internal_links(self, content: PageContent) -> TestResult:
        """Test internal links"""
        soup = content.rendered_soup or content.static_soup
        links = soup.find_all('a', href=True)
        
        from urllib.parse import urlparse
        page_domain = urlparse(content.url).netloc
        
        internal_links = [
            link for link in links
            if link['href'].startswith('/') or page_domain in link['href']
        ]
        
        if 5 <= len(internal_links) <= 100:
            return TestResult(
                url=content.url,
                test_id='internal_links',
                test_name='Internal Links Count',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Page has {len(internal_links)} internal links',
                recommendation='Maintain balanced internal linking structure',
                score=f'{len(internal_links)} internal links'
            )
        elif len(internal_links) < 5:
            return TestResult(
                url=content.url,
                test_id='internal_links',
                test_name='Internal Links Count',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Only {len(internal_links)} internal links found',
                recommendation='Add more internal links to improve site navigation',
                score=f'{len(internal_links)} internal links'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='internal_links',
                test_name='Internal Links Count',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Too many internal links ({len(internal_links)})',
                recommendation='Reduce number of internal links for better user experience',
                score=f'{len(internal_links)} internal links'
            )
    
    def _test_external_links(self, content: PageContent) -> TestResult:
        """Test external links"""
        soup = content.rendered_soup or content.static_soup
        links = soup.find_all('a', href=True)
        
        from urllib.parse import urlparse
        page_domain = urlparse(content.url).netloc
        
        external_links = [
            link for link in links
            if link['href'].startswith('http') and page_domain not in link['href']
        ]
        
        return TestResult(
            url=content.url,
            test_id='external_links',
            test_name='External Links',
            category='Links',
            status=TestStatus.INFO,
            severity='Low',
            issue_description=f'Page has {len(external_links)} external links',
            recommendation='Ensure external links are relevant and trustworthy',
            score=f'{len(external_links)} external links'
        )
    
    def _test_anchor_text_quality(self, content: PageContent) -> TestResult:
        """Test anchor text quality"""
        soup = content.rendered_soup or content.static_soup
        links = soup.find_all('a', href=True)
        
        generic_anchors = ['click here', 'read more', 'here', 'link', 'more']
        poor_quality = [
            link for link in links
            if link.text.strip().lower() in generic_anchors
        ]
        
        if len(poor_quality) == 0:
            return TestResult(
                url=content.url,
                test_id='anchor_text_quality',
                test_name='Anchor Text Quality',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='All anchor text is descriptive',
                recommendation='Continue using descriptive anchor text',
                score=f'{len(links)} links with good anchor text'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='anchor_text_quality',
                test_name='Anchor Text Quality',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'{len(poor_quality)} links have generic anchor text',
                recommendation='Replace generic anchor text with descriptive, keyword-rich text',
                score=f'{len(poor_quality)}/{len(links)} poor quality'
            )
    
    # =========================================================================
    # CONTENT TESTS
    # =========================================================================
    
    def _test_content_word_count(self, content: PageContent) -> TestResult:
        """Test content word count"""
        soup = content.rendered_soup or content.static_soup
        text = soup.get_text()
        words = len(text.split())
        
        if words >= 300:
            return TestResult(
                url=content.url,
                test_id='content_word_count',
                test_name='Content Word Count',
                category='Content',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Page has sufficient content ({words} words)',
                recommendation='Continue providing comprehensive content',
                score=f'{words} words'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='content_word_count',
                test_name='Content Word Count',
                category='Content',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Thin content detected ({words} words)',
                recommendation='Add more valuable content (target 300+ words)',
                score=f'{words} words'
            )
    
    def _test_soft_404_detection(self, content: PageContent) -> TestResult:
        """
        Detect soft 404s - pages that return 200 but are actually error/empty pages.
        
        Based on Google's guidance:
        - Pages with "not found / no results / 0 items" messages returning 200
        - Pages with very thin or no main content
        - Pages that are mostly template/boilerplate
        - Empty search results or listing pages
        """
        # Use RENDERED content (what Google sees after JS execution)
        soup = content.rendered_soup if content.rendered_soup else content.static_soup
        
        # Also check static to see if there's a disconnect
        static_soup = content.static_soup
        
        # Collect indicators
        soft_404_indicators = []
        soft_404_score = 0
        
        # 1. Check for classic "not found" / error phrases (HIGHEST PRIORITY)
        error_phrases = [
            'not found', 'page not found', '404', 'page doesn\'t exist',
            'no results', 'no items', '0 results', '0 items', '0 products',
            'nothing found', 'nothing to display', 'no entries',
            'no articles', 'no posts', 'no content available',
            'page missing', 'page unavailable', 'content unavailable',
            'coming soon', 'under construction', 'page removed'
        ]
        
        # Check in multiple places
        body_text = soup.get_text().lower()
        
        # Check title
        title = soup.find('title')
        if title:
            title_text = title.text.strip().lower()
            for phrase in error_phrases:
                if phrase in title_text:
                    soft_404_indicators.append(f'Error phrase in title: "{phrase}"')
                    soft_404_score += 40  # Very strong signal
                    break
        
        # Check H1
        h1_tags = soup.find_all('h1')
        if h1_tags:
            h1_text = ' '.join([h1.text.strip().lower() for h1 in h1_tags])
            for phrase in error_phrases:
                if phrase in h1_text:
                    soft_404_indicators.append(f'Error phrase in H1: "{phrase}"')
                    soft_404_score += 35
                    break
        
        # Check main content area for error messages
        main_content = soup.find(['main', 'article', 'div'], class_=lambda x: x and any(c in str(x).lower() for c in ['main', 'content', 'body']))
        if main_content:
            main_text = main_content.get_text().strip().lower()
            for phrase in ['no results', 'no items', '0 results', '0 items', '0 products', 'not found']:
                if phrase in main_text[:500]:  # Check first 500 chars of main content
                    soft_404_indicators.append(f'Empty state message in main content: "{phrase}"')
                    soft_404_score += 30
                    break
        
        # 2. Check word count (CRITICAL for Google)
        # Google expects meaningful content, not just template
        text = soup.get_text()
        words = len([w for w in text.split() if len(w) > 2])  # Real words only
        
        if words < 50:
            soft_404_indicators.append(f'Extremely thin content ({words} words)')
            soft_404_score += 45  # Almost certainly a soft 404
        elif words < 150:
            soft_404_indicators.append(f'Very thin content ({words} words)')
            soft_404_score += 30
        elif words < 300:
            soft_404_indicators.append(f'Thin content ({words} words)')
            soft_404_score += 15
        
        # 3. Check for missing H1 (common in empty pages)
        if len(h1_tags) == 0:
            soft_404_indicators.append('Missing H1 tag')
            soft_404_score += 25
        
        # 4. Check main content depth
        if main_content:
            main_words = len([w for w in main_content.get_text().split() if len(w) > 2])
            if main_words < 30:
                soft_404_indicators.append(f'Minimal main content ({main_words} words)')
                soft_404_score += 30
            
            # Check if main content is mostly empty
            paragraphs = main_content.find_all('p')
            if len(paragraphs) == 0:
                soft_404_indicators.append('No paragraphs in main content')
                soft_404_score += 20
        else:
            # No main content area at all
            soft_404_indicators.append('No main content element found')
            soft_404_score += 25
        
        # 5. Check for disconnect between static and rendered (JS issue)
        if content.rendered_soup and content.static_soup:
            static_words = len(content.static_soup.get_text().split())
            rendered_words = len(content.rendered_soup.get_text().split())
            
            # If rendered has way less content than static, something's wrong
            if rendered_words < static_words * 0.5 and rendered_words < 200:
                soft_404_indicators.append(f'Content decreased after JS render ({static_words}→{rendered_words} words)')
                soft_404_score += 20
        
        # 6. Check content-to-template ratio
        # If page is mostly navigation/boilerplate, it's thin
        nav_elements = len(soup.find_all(['nav', 'header', 'footer', 'aside']))
        content_elements = len(soup.find_all(['article', 'main', 'section', 'p']))
        
        if content_elements < 3 and nav_elements > 0:
            soft_404_indicators.append('Mostly template/boilerplate (low content-to-chrome ratio)')
            soft_404_score += 20
        
        # 7. Check for "0 items" or "empty" indicators in HTML/classes
        empty_classes = ['empty', 'no-results', 'no-items', 'not-found', 'error-page']
        for element in soup.find_all(class_=True):
            classes = ' '.join(element.get('class', [])).lower()
            for empty_class in empty_classes:
                if empty_class in classes:
                    soft_404_indicators.append(f'Empty state CSS class detected: "{empty_class}"')
                    soft_404_score += 15
                    break
        
        # 8. Check for search results with 0 results
        # Look for result count indicators
        result_indicators = soup.find_all(text=lambda t: t and any(x in t.lower() for x in ['0 results', 'no results', '0 items', 'no items found']))
        if result_indicators:
            soft_404_indicators.append('Zero results message found')
            soft_404_score += 25
        
        # 9. Check for proper article/product structure
        # Absence of expected content structure can indicate empty page
        has_article = soup.find(['article', 'div'], class_=lambda x: x and 'article' in str(x).lower())
        has_product = soup.find(['div', 'section'], class_=lambda x: x and 'product' in str(x).lower())
        has_content_structure = bool(has_article or has_product or soup.find('main'))
        
        if not has_content_structure and words < 300:
            soft_404_indicators.append('No recognizable content structure')
            soft_404_score += 15
        
        # Determine status based on score
        if soft_404_score >= 70:
            status = TestStatus.FAIL
            issue = 'SOFT 404 DETECTED: Page returns 200 but is clearly error/empty page'
            recommendation = 'CRITICAL: Return proper 404/410 status OR add substantial content. Google will treat this as a soft 404.'
        elif soft_404_score >= 45:
            status = TestStatus.FAIL
            issue = 'Likely soft 404: Page shows multiple signs of being empty/error page'
            recommendation = 'HIGH PRIORITY: Review this page. Consider returning 404/410 or adding real content to avoid soft 404 classification.'
        elif soft_404_score >= 25:
            status = TestStatus.WARNING
            issue = 'Possible soft 404: Page shows some indicators of thin/empty content'
            recommendation = 'Review page content. May be flagged as soft 404 by Google. Consider adding more content or proper redirect.'
        else:
            return TestResult(
                url=content.url,
                test_id='soft_404_detection',
                test_name='Soft 404 Detection',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Critical',
                issue_description='Page has substantive content, no soft 404 indicators',
                recommendation='Page appears to have meaningful content',
                score='No soft 404'
            )
        
        # Build detailed issue description
        indicators_text = '; '.join(soft_404_indicators[:5])  # Top 5 indicators
        if len(soft_404_indicators) > 5:
            indicators_text += f' (+{len(soft_404_indicators)-5} more)'
        
        return TestResult(
            url=content.url,
            test_id='soft_404_detection',
            test_name='Soft 404 Detection',
            category='Technical SEO',
            status=status,
            severity='Critical',
            issue_description=f'{issue}. Indicators: {indicators_text}',
            recommendation=recommendation,
            score=f'Risk score: {soft_404_score}/100 ({len(soft_404_indicators)} indicators)'
        )
    
    def _test_content_readability(self, content: PageContent) -> TestResult:
        """Test content readability (simplified)"""
        soup = content.rendered_soup or content.static_soup
        text = soup.get_text()
        
        sentences = len([s for s in text.split('.') if s.strip()])
        words = len(text.split())
        
        if sentences > 0:
            avg_sentence_length = words / sentences
            
            if avg_sentence_length <= 20:
                status = TestStatus.PASS
                issue = 'Content has good readability'
                recommendation = 'Continue writing clear, concise content'
            else:
                status = TestStatus.WARNING
                issue = 'Content may be difficult to read'
                recommendation = 'Use shorter sentences for better readability'
            
            return TestResult(
                url=content.url,
                test_id='content_readability',
                test_name='Content Readability',
                category='Content',
                status=status,
                severity='Low',
                issue_description=issue,
                recommendation=recommendation,
                score=f'Avg {avg_sentence_length:.1f} words/sentence'
            )
        
        return None
    
    def _test_content_structure(self, content: PageContent) -> TestResult:
        """Test content structure"""
        soup = content.rendered_soup or content.static_soup
        
        paragraphs = len(soup.find_all('p'))
        lists = len(soup.find_all(['ul', 'ol']))
        headers = len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
        
        structure_score = paragraphs + lists + headers
        
        if structure_score >= 10:
            return TestResult(
                url=content.url,
                test_id='content_structure',
                test_name='Content Structure',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='Content is well-structured',
                recommendation='Continue using proper HTML formatting',
                score=f'P:{paragraphs} Lists:{lists} Headers:{headers}'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='content_structure',
                test_name='Content Structure',
                category='Content',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='Limited content structure',
                recommendation='Add more paragraphs, lists, and headers for better structure',
                score=f'P:{paragraphs} Lists:{lists} Headers:{headers}'
            )
    
    # =========================================================================
    # TECHNICAL SEO TESTS
    # =========================================================================
    
    def _test_ssl_certificate(self, content: PageContent) -> TestResult:
        """Test SSL certificate"""
        is_https = content.url.startswith('https://')
        
        if is_https:
            return TestResult(
                url=content.url,
                test_id='ssl_certificate',
                test_name='SSL Certificate',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Critical',
                issue_description='Site uses HTTPS',
                recommendation='Continue maintaining valid SSL certificate',
                score='HTTPS enabled'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='ssl_certificate',
                test_name='SSL Certificate',
                category='Technical SEO',
                status=TestStatus.FAIL,
                severity='Critical',
                issue_description='Site uses HTTP (not secure)',
                recommendation='Implement HTTPS with valid SSL certificate immediately',
                score='HTTP only'
            )
    
    def _test_robots_txt(self, content: PageContent) -> TestResult:
        """Test robots.txt presence"""
        from urllib.parse import urlparse
        parsed = urlparse(content.url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            import requests
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                return TestResult(
                    url=content.url,
                    test_id='robots_txt',
                    test_name='Robots.txt Presence',
                    category='Technical SEO',
                    status=TestStatus.PASS,
                    severity='Medium',
                    issue_description='Robots.txt file found',
                    recommendation='Ensure robots.txt is properly configured',
                    score='File exists'
                )
        except:
            pass
        
        return TestResult(
            url=content.url,
            test_id='robots_txt',
            test_name='Robots.txt Presence',
            category='Technical SEO',
            status=TestStatus.WARNING,
            severity='Medium',
            issue_description='Robots.txt file not found',
            recommendation='Create robots.txt file to guide search engines',
            score='File not found'
        )
    
    def _test_sitemap_xml(self, content: PageContent) -> TestResult:
        """Test sitemap.xml presence"""
        from urllib.parse import urlparse
        parsed = urlparse(content.url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
        
        try:
            import requests
            response = requests.get(sitemap_url, timeout=5)
            if response.status_code == 200:
                return TestResult(
                    url=content.url,
                    test_id='sitemap_xml',
                    test_name='XML Sitemap Presence',
                    category='Technical SEO',
                    status=TestStatus.PASS,
                    severity='Medium',
                    issue_description='XML sitemap found',
                    recommendation='Ensure sitemap is up to date and submitted to search engines',
                    score='File exists'
                )
        except:
            pass
        
        return TestResult(
            url=content.url,
            test_id='sitemap_xml',
            test_name='XML Sitemap Presence',
            category='Technical SEO',
            status=TestStatus.WARNING,
            severity='Medium',
            issue_description='XML sitemap not found',
            recommendation='Create and submit XML sitemap to search engines',
            score='File not found'
        )
    
    def _test_schema_markup(self, content: PageContent) -> TestResult:
        """Test schema markup presence"""
        soup = content.rendered_soup or content.static_soup
        
        # Check for JSON-LD
        json_ld = soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        # Check for microdata
        microdata = soup.find_all(attrs={'itemscope': True})
        
        schema_count = len(json_ld) + len(microdata)
        
        if schema_count > 0:
            return TestResult(
                url=content.url,
                test_id='schema_markup',
                test_name='Schema Markup',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Found {schema_count} schema markup instances',
                recommendation='Continue implementing relevant structured data',
                score=f'{schema_count} schema blocks'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='schema_markup',
                test_name='Schema Markup',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No schema markup found',
                recommendation='Implement structured data for rich snippets',
                score='No schema found'
            )
    
    # =========================================================================
    # PERFORMANCE TESTS
    # =========================================================================
    
    def _test_page_load_time(self, content: PageContent) -> TestResult:
        """Test page load time"""
        load_time = content.rendered_load_time or content.static_load_time
        
        if load_time < 3:
            status = TestStatus.PASS
            issue = f'Page loads in {load_time:.2f} seconds'
            recommendation = 'Page load time is good'
        elif load_time < 5:
            status = TestStatus.WARNING
            issue = f'Page loads in {load_time:.2f} seconds'
            recommendation = 'Consider optimizing for faster load times'
        else:
            status = TestStatus.FAIL
            issue = f'Page loads slowly ({load_time:.2f} seconds)'
            recommendation = 'Optimize images, scripts, and server response for faster loading'
        
        return TestResult(
            url=content.url,
            test_id='page_load_time',
            test_name='Page Load Time',
            category='Performance',
            status=status,
            severity='High',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{load_time:.2f}s'
        )
    
    def _test_page_size(self, content: PageContent) -> TestResult:
        """Test page size"""
        html = content.rendered_html or content.static_html
        size_bytes = len(html.encode('utf-8'))
        size_kb = size_bytes / 1024
        size_mb = size_kb / 1024
        
        if size_kb < 500:
            status = TestStatus.PASS
            issue = f'Page size is good ({size_kb:.1f} KB)'
            recommendation = 'Page size is well optimized'
        elif size_kb < 2000:
            status = TestStatus.WARNING
            issue = f'Page size is moderate ({size_kb:.1f} KB)'
            recommendation = 'Consider compressing resources for faster loading'
        else:
            status = TestStatus.FAIL
            issue = f'Page size is large ({size_mb:.2f} MB)'
            recommendation = 'Optimize and compress page resources significantly'
        
        return TestResult(
            url=content.url,
            test_id='page_size',
            test_name='Page Size',
            category='Performance',
            status=status,
            severity='Medium',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{size_kb:.1f} KB'
        )
    
    def _test_dom_complexity(self, content: PageContent) -> TestResult:
        """Test DOM complexity"""
        soup = content.rendered_soup or content.static_soup
        dom_elements = len(soup.find_all())
        
        if dom_elements < 1500:
            status = TestStatus.PASS
            issue = f'DOM has {dom_elements} elements (good)'
            recommendation = 'DOM complexity is well managed'
        elif dom_elements < 3000:
            status = TestStatus.WARNING
            issue = f'DOM has {dom_elements} elements (moderate)'
            recommendation = 'Consider simplifying page structure'
        else:
            status = TestStatus.FAIL
            issue = f'DOM has {dom_elements} elements (excessive)'
            recommendation = 'Reduce DOM complexity for better performance'
        
        return TestResult(
            url=content.url,
            test_id='dom_complexity',
            test_name='DOM Complexity',
            category='Performance',
            status=status,
            severity='Low',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{dom_elements} elements'
        )
    
    # =========================================================================
    # CORE WEB VITALS TESTS
    # =========================================================================
    
    def _test_lcp(self, content: PageContent) -> TestResult:
        """Test Largest Contentful Paint"""
        if not content.core_web_vitals or 'lcp' not in content.core_web_vitals:
            return TestResult(
                url=content.url,
                test_id='largest_contentful_paint',
                test_name='Largest Contentful Paint (LCP)',
                category='Core Web Vitals',
                status=TestStatus.INFO,
                severity='Critical',
                issue_description='LCP measurement not available',
                recommendation='Enable JavaScript rendering for Core Web Vitals',
                score='Not measured'
            )
        
        lcp = content.core_web_vitals['lcp']
        
        if lcp <= 2500:
            status = TestStatus.PASS
            issue = f'LCP is good ({lcp:.0f}ms)'
            recommendation = 'LCP is within recommended threshold'
        elif lcp <= 4000:
            status = TestStatus.WARNING
            issue = f'LCP needs improvement ({lcp:.0f}ms)'
            recommendation = 'Optimize largest content element loading'
        else:
            status = TestStatus.FAIL
            issue = f'LCP is poor ({lcp:.0f}ms)'
            recommendation = 'Significantly optimize largest element loading'
        
        return TestResult(
            url=content.url,
            test_id='largest_contentful_paint',
            test_name='Largest Contentful Paint (LCP)',
            category='Core Web Vitals',
            status=status,
            severity='Critical',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{lcp:.0f}ms'
        )
    
    def _test_cls(self, content: PageContent) -> TestResult:
        """Test Cumulative Layout Shift"""
        if not content.core_web_vitals or 'cls' not in content.core_web_vitals:
            return TestResult(
                url=content.url,
                test_id='cumulative_layout_shift',
                test_name='Cumulative Layout Shift (CLS)',
                category='Core Web Vitals',
                status=TestStatus.INFO,
                severity='Critical',
                issue_description='CLS measurement not available',
                recommendation='Enable JavaScript rendering for Core Web Vitals',
                score='Not measured'
            )
        
        cls = content.core_web_vitals['cls']
        
        if cls <= 0.1:
            status = TestStatus.PASS
            issue = f'CLS is good ({cls:.3f})'
            recommendation = 'Visual stability is excellent'
        elif cls <= 0.25:
            status = TestStatus.WARNING
            issue = f'CLS needs improvement ({cls:.3f})'
            recommendation = 'Reduce layout shifts by reserving space for dynamic content'
        else:
            status = TestStatus.FAIL
            issue = f'CLS is poor ({cls:.3f})'
            recommendation = 'Significantly reduce layout shifts for better user experience'
        
        return TestResult(
            url=content.url,
            test_id='cumulative_layout_shift',
            test_name='Cumulative Layout Shift (CLS)',
            category='Core Web Vitals',
            status=status,
            severity='Critical',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{cls:.3f}'
        )
    
    def _test_fcp(self, content: PageContent) -> TestResult:
        """Test First Contentful Paint"""
        if not content.core_web_vitals or 'fcp' not in content.core_web_vitals:
            return TestResult(
                url=content.url,
                test_id='first_contentful_paint',
                test_name='First Contentful Paint (FCP)',
                category='Core Web Vitals',
                status=TestStatus.INFO,
                severity='High',
                issue_description='FCP measurement not available',
                recommendation='Enable JavaScript rendering for Core Web Vitals',
                score='Not measured'
            )
        
        fcp = content.core_web_vitals['fcp']
        
        if fcp <= 1800:
            status = TestStatus.PASS
            issue = f'FCP is good ({fcp:.0f}ms)'
            recommendation = 'First paint is within recommended threshold'
        elif fcp <= 3000:
            status = TestStatus.WARNING
            issue = f'FCP needs improvement ({fcp:.0f}ms)'
            recommendation = 'Optimize critical rendering path'
        else:
            status = TestStatus.FAIL
            issue = f'FCP is poor ({fcp:.0f}ms)'
            recommendation = 'Significantly optimize initial page rendering'
        
        return TestResult(
            url=content.url,
            test_id='first_contentful_paint',
            test_name='First Contentful Paint (FCP)',
            category='Core Web Vitals',
            status=status,
            severity='High',
            issue_description=issue,
            recommendation=recommendation,
            score=f'{fcp:.0f}ms'
        )
    
    # =========================================================================
    # ACCESSIBILITY TESTS
    # =========================================================================
    
    def _test_lang_attribute(self, content: PageContent) -> TestResult:
        """Test HTML lang attribute"""
        soup = content.rendered_soup or content.static_soup
        html_tag = soup.find('html')
        
        if html_tag and html_tag.get('lang'):
            return TestResult(
                url=content.url,
                test_id='lang_attribute',
                test_name='Language Attribute',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='High',
                issue_description='HTML lang attribute is set',
                recommendation='Continue maintaining proper lang attribute',
                score=f'Lang: {html_tag["lang"]}'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='lang_attribute',
                test_name='Language Attribute',
                category='Accessibility',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Missing HTML lang attribute',
                recommendation='Add lang attribute to HTML element for accessibility',
                score='No lang attribute'
            )
    
    def _test_form_labels(self, content: PageContent) -> TestResult:
        """Test form labels"""
        soup = content.rendered_soup or content.static_soup
        inputs = soup.find_all('input')
        labels = soup.find_all('label')
        
        if not inputs:
            return None
        
        if len(labels) >= len(inputs):
            return TestResult(
                url=content.url,
                test_id='form_labels',
                test_name='Form Labels',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'Form inputs have proper labels',
                recommendation='Continue providing labels for all form inputs',
                score=f'{len(labels)} labels for {len(inputs)} inputs'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='form_labels',
                test_name='Form Labels',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'Some inputs may be missing labels',
                recommendation='Associate labels with all form inputs',
                score=f'{len(labels)} labels for {len(inputs)} inputs'
            )
    
    def _test_semantic_html(self, content: PageContent) -> TestResult:
        """Test semantic HTML usage"""
        soup = content.rendered_soup or content.static_soup
        
        semantic_tags = soup.find_all(['nav', 'main', 'article', 'section', 'aside', 'header', 'footer'])
        
        if len(semantic_tags) >= 3:
            return TestResult(
                url=content.url,
                test_id='semantic_html',
                test_name='Semantic HTML5 Elements',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Page uses {len(semantic_tags)} semantic HTML5 elements',
                recommendation='Continue using semantic elements for better accessibility',
                score=f'{len(semantic_tags)} semantic tags'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='semantic_html',
                test_name='Semantic HTML5 Elements',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Limited use of semantic HTML5 elements',
                recommendation='Use semantic elements (nav, main, article, etc.) instead of divs',
                score=f'{len(semantic_tags)} semantic tags'
            )
    
    # =========================================================================
    # MOBILE TESTS
    # =========================================================================
    
    def _test_mobile_viewport(self, content: PageContent) -> TestResult:
        """Test mobile viewport (same as viewport test)"""
        return self._test_viewport(content)
    
    def _test_mobile_font_sizes(self, content: PageContent) -> TestResult:
        """Test mobile font sizes (requires rendering)"""
        if not content.rendered_soup:
            return TestResult(
                url=content.url,
                test_id='mobile_font_sizes',
                test_name='Mobile Font Sizes',
                category='Mobile Usability',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='Font size check requires JavaScript rendering',
                recommendation='Enable JavaScript rendering for mobile checks',
                score='Not measured'
            )
        
        return TestResult(
            url=content.url,
            test_id='mobile_font_sizes',
            test_name='Mobile Font Sizes',
            category='Mobile Usability',
            status=TestStatus.INFO,
            severity='Medium',
            issue_description='Mobile font size check requires CSS analysis',
            recommendation='Ensure minimum 16px font size for mobile readability',
            score='Manual check required'
        )
    
    # =========================================================================
    # SECURITY TESTS
    # =========================================================================
    
    def _test_security_headers(self, content: PageContent) -> TestResult:
        """Test security headers"""
        headers = content.static_headers
        
        security_headers = {
            'X-Frame-Options': False,
            'X-Content-Type-Options': False,
            'Strict-Transport-Security': False,
            'Content-Security-Policy': False
        }
        
        for header in security_headers.keys():
            if header in headers or header.lower() in headers:
                security_headers[header] = True
        
        found_count = sum(security_headers.values())
        
        if found_count >= 3:
            return TestResult(
                url=content.url,
                test_id='security_headers',
                test_name='Security Headers',
                category='Security',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'Found {found_count}/4 recommended security headers',
                recommendation='Continue maintaining security headers',
                score=f'{found_count}/4 headers present'
            )
        elif found_count >= 1:
            return TestResult(
                url=content.url,
                test_id='security_headers',
                test_name='Security Headers',
                category='Security',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'Only {found_count}/4 security headers found',
                recommendation='Add missing security headers for better protection',
                score=f'{found_count}/4 headers present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='security_headers',
                test_name='Security Headers',
                category='Security',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='No security headers found',
                recommendation='Implement security headers (X-Frame-Options, CSP, HSTS, etc.)',
                score='0/4 headers present'
            )
    
    # =========================================================================
    # ADDITIONAL META TAGS TESTS - PHASE 1
    # =========================================================================
    
    def _test_twitter_card_tags(self, content: PageContent) -> TestResult:
        """Check for Twitter Card meta tags"""
        soup = content.rendered_soup or content.static_soup
        twitter_tags = {
            'twitter:card': soup.find('meta', attrs={'name': 'twitter:card'}),
            'twitter:site': soup.find('meta', attrs={'name': 'twitter:site'}),
            'twitter:title': soup.find('meta', attrs={'name': 'twitter:title'}),
            'twitter:description': soup.find('meta', attrs={'name': 'twitter:description'}),
            'twitter:image': soup.find('meta', attrs={'name': 'twitter:image'}),
        }
        
        found_tags = {k: v for k, v in twitter_tags.items() if v is not None}
        found_count = len(found_tags)
        
        if found_count >= 3:
            return TestResult(
                url=content.url,
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Found {found_count}/5 Twitter Card tags',
                recommendation='Continue maintaining Twitter Cards for social sharing',
                score=f'{found_count}/5 tags present'
            )
        elif found_count >= 1:
            return TestResult(
                url=content.url,
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Incomplete Twitter Card implementation ({found_count}/5)',
                recommendation='Add twitter:card, twitter:title, twitter:description, twitter:image',
                score=f'{found_count}/5 tags present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No Twitter Card tags found',
                recommendation='Add Twitter Card tags to improve Twitter sharing appearance',
                score='0/5 tags present'
            )
    
    def _test_meta_refresh_redirect(self, content: PageContent) -> TestResult:
        """Detect meta refresh redirects (bad for SEO)"""
        soup = content.rendered_soup or content.static_soup
        meta_refresh = soup.find('meta', attrs={'http-equiv': re.compile(r'refresh', re.I)})
        
        if meta_refresh:
            refresh_content = meta_refresh.get('content', '')
            return TestResult(
                url=content.url,
                test_id='meta_refresh_redirect',
                test_name='Meta Refresh Detection',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'Meta refresh redirect detected: {refresh_content}',
                recommendation='Replace meta refresh with 301/302 HTTP redirect for better SEO',
                score='Meta refresh found'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='meta_refresh_redirect',
                test_name='Meta Refresh Detection',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No meta refresh redirects detected',
                recommendation='Continue using proper HTTP redirects',
                score='No meta refresh'
            )
    
    def _test_duplicate_meta_tags(self, content: PageContent) -> TestResult:
        """Check for duplicate title or description tags"""
        soup = content.rendered_soup or content.static_soup
        titles = soup.find_all('title')
        descriptions = soup.find_all('meta', attrs={'name': 'description'})
        
        issues = []
        if len(titles) > 1:
            issues.append(f'{len(titles)} title tags')
        if len(descriptions) > 1:
            issues.append(f'{len(descriptions)} description tags')
        
        if issues:
            return TestResult(
                url=content.url,
                test_id='duplicate_meta_tags',
                test_name='Duplicate Meta Tags',
                category='Meta Tags',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'Duplicate meta tags found: {", ".join(issues)}',
                recommendation='Remove duplicate title/description tags - only one of each allowed',
                score='; '.join(issues)
            )
        else:
            return TestResult(
                url=content.url,
                test_id='duplicate_meta_tags',
                test_name='Duplicate Meta Tags',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No duplicate meta tags detected',
                recommendation='Continue using single title and description tags',
                score='No duplicates'
            )
    
    def _test_favicon_presence(self, content: PageContent) -> TestResult:
        """Check for favicon"""
        soup = content.rendered_soup or content.static_soup
        favicon = (
            soup.find('link', attrs={'rel': 'icon'}) or
            soup.find('link', attrs={'rel': 'shortcut icon'}) or
            soup.find('link', attrs={'rel': 'apple-touch-icon'})
        )
        
        if favicon:
            return TestResult(
                url=content.url,
                test_id='favicon_presence',
                test_name='Favicon Presence',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='Favicon is present',
                recommendation='Continue providing favicon for brand recognition',
                score='Favicon found'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='favicon_presence',
                test_name='Favicon Presence',
                category='Meta Tags',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='No favicon detected',
                recommendation='Add favicon to improve brand recognition in browser tabs and bookmarks',
                score='No favicon'
            )


    
    # =========================================================================
    # ADDITIONAL HEADER TESTS - PHASE 1
    # =========================================================================
    
    def _test_empty_headers(self, content: PageContent) -> TestResult:
        """Detect empty header tags"""
        soup = content.rendered_soup or content.static_soup
        all_headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        empty_headers = [h for h in all_headers if not h.text.strip()]
        
        if len(empty_headers) == 0:
            return TestResult(
                url=content.url,
                test_id='empty_headers',
                test_name='Empty Headers Check',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='High',
                issue_description='All header tags contain text',
                recommendation='Continue using meaningful header text',
                score=f'0/{len(all_headers)} empty'
            )
        else:
            header_types = [h.name.upper() for h in empty_headers]
            return TestResult(
                url=content.url,
                test_id='empty_headers',
                test_name='Empty Headers Check',
                category='Header Structure',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{len(empty_headers)} empty header tag(s): {", ".join(header_types)}',
                recommendation='Remove empty headers or add descriptive text',
                score=f'{len(empty_headers)}/{len(all_headers)} empty'
            )
    
    def _test_header_level_gaps(self, content: PageContent) -> TestResult:
        """Detect skipped header levels (e.g., H1 -> H3)"""
        soup = content.rendered_soup or content.static_soup
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headers:
            return None
        
        header_levels = [int(h.name[1]) for h in headers]
        
        gaps = []
        for i in range(len(header_levels) - 1):
            current = header_levels[i]
            next_level = header_levels[i + 1]
            
            if next_level > current + 1:
                gaps.append(f'H{current} → H{next_level}')
        
        if not gaps:
            return TestResult(
                url=content.url,
                test_id='header_level_gaps',
                test_name='Header Level Gaps',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No header level gaps detected',
                recommendation='Continue maintaining proper header hierarchy',
                score='No gaps'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='header_level_gaps',
                test_name='Header Level Gaps',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Header level gaps found: {", ".join(gaps)}',
                recommendation='Use sequential header levels (H1→H2→H3) for proper document structure',
                score=f'{len(gaps)} gap(s)'
            )
    
    # =========================================================================
    # ADDITIONAL IMAGE TESTS - PHASE 1
    # =========================================================================
    
    def _test_image_dimensions(self, content: PageContent) -> TestResult:
        """Check if images have width/height attributes"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return None
        
        images_with_dimensions = [
            img for img in images 
            if img.get('width') and img.get('height')
        ]
        
        percentage = (len(images_with_dimensions) / len(images)) * 100 if images else 0
        
        if percentage >= 80:
            return TestResult(
                url=content.url,
                test_id='img_dimensions_specified',
                test_name='Image Dimensions',
                category='Images',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{len(images_with_dimensions)}/{len(images)} images have dimensions',
                recommendation='Continue specifying image dimensions to prevent layout shifts',
                score=f'{percentage:.1f}% with dimensions'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_dimensions_specified',
                test_name='Image Dimensions',
                category='Images',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Only {len(images_with_dimensions)}/{len(images)} images have dimensions',
                recommendation='Add width/height attributes to images to improve CLS (Core Web Vitals)',
                score=f'{percentage:.1f}% with dimensions'
            )
    
    def _test_modern_image_formats(self, content: PageContent) -> TestResult:
        """Check for modern image formats (WebP, AVIF)"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        picture_sources = soup.find_all('source', attrs={'type': lambda x: x and 'image' in x})
        
        if not images and not picture_sources:
            return None
        
        modern_formats = 0
        
        for img in images:
            src = img.get('src', '')
            srcset = img.get('srcset', '')
            
            if '.webp' in src.lower() or '.avif' in src.lower():
                modern_formats += 1
            elif '.webp' in srcset.lower() or '.avif' in srcset.lower():
                modern_formats += 1
        
        for source in picture_sources:
            type_attr = source.get('type', '').lower()
            if 'webp' in type_attr or 'avif' in type_attr:
                modern_formats += 1
        
        if modern_formats > 0:
            return TestResult(
                url=content.url,
                test_id='img_modern_formats',
                test_name='Modern Image Formats',
                category='Images',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Using modern image formats (WebP/AVIF)',
                recommendation='Continue using modern formats for better performance',
                score=f'{modern_formats} modern format uses'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_modern_formats',
                test_name='Modern Image Formats',
                category='Images',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No modern image formats detected',
                recommendation='Consider using WebP or AVIF for 25-35% better compression',
                score='Using traditional formats'
            )
    
    def _test_responsive_images_srcset(self, content: PageContent) -> TestResult:
        """Check for responsive image implementation"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        picture_elements = soup.find_all('picture')
        
        if not images:
            return None
        
        images_with_srcset = [img for img in images if img.get('srcset')]
        responsive_count = len(images_with_srcset) + len(picture_elements)
        
        if responsive_count > 0:
            return TestResult(
                url=content.url,
                test_id='img_responsive_srcset',
                test_name='Responsive Images',
                category='Images',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{responsive_count} responsive image implementations found',
                recommendation='Continue using srcset/picture for different screen sizes',
                score=f'{responsive_count} responsive images'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_responsive_srcset',
                test_name='Responsive Images',
                category='Images',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No responsive images detected',
                recommendation='Implement srcset or picture elements for better mobile performance',
                score='No srcset/picture'
            )
    
    # =========================================================================
    # ADDITIONAL LINK TESTS - PHASE 1
    # =========================================================================
    
    def _test_nofollow_links_analysis(self, content: PageContent) -> TestResult:
        """Analyze nofollow link usage"""
        from urllib.parse import urlparse
        soup = content.rendered_soup or content.static_soup
        all_links = soup.find_all('a', href=True)
        
        if not all_links:
            return None
        
        nofollow_links = [
            link for link in all_links 
            if link.get('rel') and 'nofollow' in ' '.join(link.get('rel', []))
        ]
        
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        internal_nofollow = [
            link for link in nofollow_links
            if link['href'].startswith('/') or domain in link['href']
        ]
        
        if internal_nofollow:
            return TestResult(
                url=content.url,
                test_id='nofollow_links_analysis',
                test_name='Nofollow Links Analysis',
                category='Links',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'{len(internal_nofollow)} internal links are nofollowed',
                recommendation='Review internal nofollow links - they may block PageRank flow',
                score=f'{len(nofollow_links)} total nofollow ({len(internal_nofollow)} internal)'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='nofollow_links_analysis',
                test_name='Nofollow Links Analysis',
                category='Links',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'{len(nofollow_links)} external nofollow links',
                recommendation='Appropriate nofollow usage for external links',
                score=f'{len(nofollow_links)} nofollow links'
            )
    
    def _test_external_link_security(self, content: PageContent) -> TestResult:
        """Check external links for security attributes"""
        from urllib.parse import urlparse
        soup = content.rendered_soup or content.static_soup
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        external_links = [
            link for link in soup.find_all('a', href=True)
            if link['href'].startswith('http') and domain not in link['href']
        ]
        
        if not external_links:
            return None
        
        target_blank_links = [
            link for link in external_links
            if link.get('target') == '_blank'
        ]
        
        if not target_blank_links:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No target="_blank" on external links',
                recommendation='Current configuration is secure',
                score='No target="_blank"'
            )
        
        insecure_links = [
            link for link in target_blank_links
            if not (link.get('rel') and 
                   ('noopener' in str(link.get('rel')) or 'noreferrer' in str(link.get('rel'))))
        ]
        
        if not insecure_links:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'All {len(target_blank_links)} target="_blank" links are secure',
                recommendation='Continue using rel="noopener noreferrer" for security',
                score=f'{len(target_blank_links)} secure'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.FAIL,
                severity='Medium',
                issue_description=f'{len(insecure_links)}/{len(target_blank_links)} target="_blank" links lack security attributes',
                recommendation='Add rel="noopener noreferrer" to external links with target="_blank"',
                score=f'{len(insecure_links)} insecure'
            )
    
    def _test_pagination_tags(self, content: PageContent) -> TestResult:
        """Check for pagination rel tags"""
        soup = content.rendered_soup or content.static_soup
        rel_prev = soup.find('link', attrs={'rel': 'prev'})
        rel_next = soup.find('link', attrs={'rel': 'next'})
        
        is_paginated = bool(re.search(r'[\?&]page=|[\?&]p=|/page/\d+', content.url))
        
        if rel_prev or rel_next:
            tags_found = []
            if rel_prev:
                tags_found.append('prev')
            if rel_next:
                tags_found.append('next')
            
            return TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Pagination tags present: {", ".join(tags_found)}',
                recommendation='Continue using rel=prev/next for paginated content',
                score=f'{len(tags_found)} tag(s)'
            )
        elif is_paginated:
            return TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Paginated URL but no rel=prev/next tags',
                recommendation='Add rel=prev/next tags to help search engines understand pagination',
                score='Missing pagination tags'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='No pagination detected',
                recommendation='N/A - Not a paginated page',
                score='Not applicable'
            )
    
    def _test_link_density_ratio(self, content: PageContent) -> TestResult:
        """Calculate link text to total text ratio"""
        soup = content.rendered_soup or content.static_soup
        body = soup.find('body')
        if not body:
            return None
        
        total_text = body.get_text()
        total_text_length = len(total_text.strip())
        
        links = soup.find_all('a')
        link_text_length = sum(len(link.get_text().strip()) for link in links)
        
        if total_text_length == 0:
            return None
        
        link_density = (link_text_length / total_text_length) * 100
        
        if link_density <= 20:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Link density is {link_density:.1f}%',
                recommendation='Good balance of links to content',
                score=f'{link_density:.1f}%'
            )
        elif link_density <= 40:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Link density is {link_density:.1f}%',
                recommendation='Consider reducing number of links relative to content',
                score=f'{link_density:.1f}%'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.FAIL,
                severity='Low',
                issue_description=f'High link density: {link_density:.1f}%',
                recommendation='Too many links may dilute link value and harm SEO',
                score=f'{link_density:.1f}%'
            )
    
    # =========================================================================
    # ADDITIONAL TECHNICAL SEO TESTS - PHASE 1
    # =========================================================================
    
    def _test_url_parameters(self, content: PageContent) -> TestResult:
        """Check for excessive URL parameters"""
        from urllib.parse import urlparse
        parsed = urlparse(content.url)
        
        if not parsed.query:
            return TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Clean URL with no parameters',
                recommendation='Continue using clean URLs',
                score='0 parameters'
            )
        
        params = parsed.query.split('&')
        param_count = len(params)
        
        if param_count <= 3:
            return TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{param_count} URL parameter(s)',
                recommendation='Parameter count is acceptable',
                score=f'{param_count} parameter(s)'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Many URL parameters ({param_count})',
                recommendation='Consider reducing parameters or using URL rewriting',
                score=f'{param_count} parameter(s)'
            )
    
    def _test_trailing_slash_consistency(self, content: PageContent) -> TestResult:
        """Check trailing slash consistency"""
        soup = content.rendered_soup or content.static_soup
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        
        if not canonical:
            return None
        
        canonical_url = canonical.get('href', '')
        
        url_ends_with_slash = content.url.endswith('/')
        canonical_ends_with_slash = canonical_url.endswith('/')
        
        if url_ends_with_slash == canonical_ends_with_slash:
            return TestResult(
                url=content.url,
                test_id='trailing_slash_consistency',
                test_name='Trailing Slash Consistency',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='URL and canonical have consistent trailing slash usage',
                recommendation='Continue maintaining consistent URL structure',
                score='Consistent'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='trailing_slash_consistency',
                test_name='Trailing Slash Consistency',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='Trailing slash inconsistency between URL and canonical',
                recommendation='Ensure consistent trailing slash usage to avoid duplicate content',
                score='Inconsistent'
            )
    
    def _test_mixed_content_detection(self, content: PageContent) -> TestResult:
        """Detect HTTP resources on HTTPS pages"""
        if not content.url.startswith('https://'):
            return None
        
        soup = content.rendered_soup or content.static_soup
        insecure_resources = []
        
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            if script['src'].startswith('http://'):
                insecure_resources.append(f'script: {script["src"][:50]}')
        
        stylesheets = soup.find_all('link', rel='stylesheet', href=True)
        for style in stylesheets:
            if style['href'].startswith('http://'):
                insecure_resources.append(f'stylesheet: {style["href"][:50]}')
        
        images = soup.find_all('img', src=True)
        for img in images:
            if img['src'].startswith('http://'):
                insecure_resources.append(f'image: {img["src"][:50]}')
        
        iframes = soup.find_all('iframe', src=True)
        for iframe in iframes:
            if iframe['src'].startswith('http://'):
                insecure_resources.append(f'iframe: {iframe["src"][:50]}')
        
        if not insecure_resources:
            return TestResult(
                url=content.url,
                test_id='mixed_content_detection',
                test_name='Mixed Content Detection',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No mixed content detected',
                recommendation='All resources loaded securely over HTTPS',
                score='No mixed content'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='mixed_content_detection',
                test_name='Mixed Content Detection',
                category='Technical SEO',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{len(insecure_resources)} HTTP resources on HTTPS page',
                recommendation='Update all resources to use HTTPS to avoid security warnings',
                score=f'{len(insecure_resources)} insecure resources'
            )
    
    # =========================================================================
    # ADDITIONAL PERFORMANCE TESTS - PHASE 1
    # =========================================================================
    
    def _test_gzip_compression(self, content: PageContent) -> TestResult:
        """Check if response is compressed (gzip/brotli)"""
        headers = content.static_headers
        
        encoding = headers.get('Content-Encoding', '').lower()
        
        if 'gzip' in encoding or 'br' in encoding:
            return TestResult(
                url=content.url,
                test_id='gzip_compression',
                test_name='Compression',
                category='Performance',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'Response is compressed ({encoding})',
                recommendation='Continue using compression for optimal performance',
                score=f'{encoding} enabled'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='gzip_compression',
                test_name='Compression',
                category='Performance',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='No compression detected',
                recommendation='Enable gzip or brotli compression to reduce file size by 60-80%',
                score='No compression'
            )
    
    def _test_cache_headers(self, content: PageContent) -> TestResult:
        """Check for proper cache-control headers"""
        headers = content.static_headers
        
        cache_control = headers.get('Cache-Control', '')
        expires = headers.get('Expires', '')
        etag = headers.get('ETag', '')
        
        has_caching = bool(cache_control or expires or etag)
        
        if has_caching:
            return TestResult(
                url=content.url,
                test_id='cache_headers',
                test_name='Browser Caching',
                category='Performance',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Caching headers are present',
                recommendation='Continue maintaining proper cache headers',
                score=f'Cache-Control: {cache_control[:50]}'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='cache_headers',
                test_name='Browser Caching',
                category='Performance',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No caching headers found',
                recommendation='Add Cache-Control headers to improve repeat visit performance',
                score='No cache headers'
            )

    
    # =========================================================================
    # ADDITIONAL HEADER TESTS - PHASE 1
    # =========================================================================
    
    def _test_empty_headers(self, content: PageContent) -> TestResult:
        """Detect empty header tags"""
        soup = content.rendered_soup or content.static_soup
        all_headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        empty_headers = [h for h in all_headers if not h.text.strip()]
        
        if len(empty_headers) == 0:
            return TestResult(
                url=content.url,
                test_id='empty_headers',
                test_name='Empty Headers Check',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='High',
                issue_description='All header tags contain text',
                recommendation='Continue using meaningful header text',
                score=f'0/{len(all_headers)} empty'
            )
        else:
            header_types = [h.name.upper() for h in empty_headers]
            return TestResult(
                url=content.url,
                test_id='empty_headers',
                test_name='Empty Headers Check',
                category='Header Structure',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{len(empty_headers)} empty header tag(s): {", ".join(header_types)}',
                recommendation='Remove empty headers or add descriptive text',
                score=f'{len(empty_headers)}/{len(all_headers)} empty'
            )
    
    def _test_header_level_gaps(self, content: PageContent) -> TestResult:
        """Detect skipped header levels (e.g., H1 -> H3)"""
        soup = content.rendered_soup or content.static_soup
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headers:
            return None
        
        header_levels = [int(h.name[1]) for h in headers]
        
        gaps = []
        for i in range(len(header_levels) - 1):
            current = header_levels[i]
            next_level = header_levels[i + 1]
            
            if next_level > current + 1:
                gaps.append(f'H{current} → H{next_level}')
        
        if not gaps:
            return TestResult(
                url=content.url,
                test_id='header_level_gaps',
                test_name='Header Level Gaps',
                category='Header Structure',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No header level gaps detected',
                recommendation='Continue maintaining proper header hierarchy',
                score='No gaps'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='header_level_gaps',
                test_name='Header Level Gaps',
                category='Header Structure',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Header level gaps found: {", ".join(gaps)}',
                recommendation='Use sequential header levels (H1→H2→H3) for proper document structure',
                score=f'{len(gaps)} gap(s)'
            )
    
    # =========================================================================
    # ADDITIONAL IMAGE TESTS - PHASE 1
    # =========================================================================
    
    def _test_image_dimensions(self, content: PageContent) -> TestResult:
        """Check if images have width/height attributes"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return None
        
        images_with_dimensions = [
            img for img in images 
            if img.get('width') and img.get('height')
        ]
        
        percentage = (len(images_with_dimensions) / len(images)) * 100 if images else 0
        
        if percentage >= 80:
            return TestResult(
                url=content.url,
                test_id='img_dimensions_specified',
                test_name='Image Dimensions',
                category='Images',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{len(images_with_dimensions)}/{len(images)} images have dimensions',
                recommendation='Continue specifying image dimensions to prevent layout shifts',
                score=f'{percentage:.1f}% with dimensions'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_dimensions_specified',
                test_name='Image Dimensions',
                category='Images',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Only {len(images_with_dimensions)}/{len(images)} images have dimensions',
                recommendation='Add width/height attributes to images to improve CLS (Core Web Vitals)',
                score=f'{percentage:.1f}% with dimensions'
            )
    
    def _test_modern_image_formats(self, content: PageContent) -> TestResult:
        """Check for modern image formats (WebP, AVIF)"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        picture_sources = soup.find_all('source', attrs={'type': lambda x: x and 'image' in x})
        
        if not images and not picture_sources:
            return None
        
        modern_formats = 0
        
        for img in images:
            src = img.get('src', '')
            srcset = img.get('srcset', '')
            
            if '.webp' in src.lower() or '.avif' in src.lower():
                modern_formats += 1
            elif '.webp' in srcset.lower() or '.avif' in srcset.lower():
                modern_formats += 1
        
        for source in picture_sources:
            type_attr = source.get('type', '').lower()
            if 'webp' in type_attr or 'avif' in type_attr:
                modern_formats += 1
        
        if modern_formats > 0:
            return TestResult(
                url=content.url,
                test_id='img_modern_formats',
                test_name='Modern Image Formats',
                category='Images',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Using modern image formats (WebP/AVIF)',
                recommendation='Continue using modern formats for better performance',
                score=f'{modern_formats} modern format uses'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_modern_formats',
                test_name='Modern Image Formats',
                category='Images',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No modern image formats detected',
                recommendation='Consider using WebP or AVIF for 25-35% better compression',
                score='Using traditional formats'
            )
    
    def _test_responsive_images_srcset(self, content: PageContent) -> TestResult:
        """Check for responsive image implementation"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        picture_elements = soup.find_all('picture')
        
        if not images:
            return None
        
        images_with_srcset = [img for img in images if img.get('srcset')]
        responsive_count = len(images_with_srcset) + len(picture_elements)
        
        if responsive_count > 0:
            return TestResult(
                url=content.url,
                test_id='img_responsive_srcset',
                test_name='Responsive Images',
                category='Images',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{responsive_count} responsive image implementations found',
                recommendation='Continue using srcset/picture for different screen sizes',
                score=f'{responsive_count} responsive images'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_responsive_srcset',
                test_name='Responsive Images',
                category='Images',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No responsive images detected',
                recommendation='Implement srcset or picture elements for better mobile performance',
                score='No srcset/picture'
            )
    
    # =========================================================================
    # ADDITIONAL LINK TESTS - PHASE 1
    # =========================================================================
    
    def _test_nofollow_links_analysis(self, content: PageContent) -> TestResult:
        """Analyze nofollow link usage"""
        from urllib.parse import urlparse
        soup = content.rendered_soup or content.static_soup
        all_links = soup.find_all('a', href=True)
        
        if not all_links:
            return None
        
        nofollow_links = [
            link for link in all_links 
            if link.get('rel') and 'nofollow' in ' '.join(link.get('rel', []))
        ]
        
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        internal_nofollow = [
            link for link in nofollow_links
            if link['href'].startswith('/') or domain in link['href']
        ]
        
        if internal_nofollow:
            return TestResult(
                url=content.url,
                test_id='nofollow_links_analysis',
                test_name='Nofollow Links Analysis',
                category='Links',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'{len(internal_nofollow)} internal links are nofollowed',
                recommendation='Review internal nofollow links - they may block PageRank flow',
                score=f'{len(nofollow_links)} total nofollow ({len(internal_nofollow)} internal)'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='nofollow_links_analysis',
                test_name='Nofollow Links Analysis',
                category='Links',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'{len(nofollow_links)} external nofollow links',
                recommendation='Appropriate nofollow usage for external links',
                score=f'{len(nofollow_links)} nofollow links'
            )
    
    def _test_external_link_security(self, content: PageContent) -> TestResult:
        """Check external links for security attributes"""
        from urllib.parse import urlparse
        soup = content.rendered_soup or content.static_soup
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        external_links = [
            link for link in soup.find_all('a', href=True)
            if link['href'].startswith('http') and domain not in link['href']
        ]
        
        if not external_links:
            return None
        
        target_blank_links = [
            link for link in external_links
            if link.get('target') == '_blank'
        ]
        
        if not target_blank_links:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No target="_blank" on external links',
                recommendation='Current configuration is secure',
                score='No target="_blank"'
            )
        
        insecure_links = [
            link for link in target_blank_links
            if not (link.get('rel') and 
                   ('noopener' in str(link.get('rel')) or 'noreferrer' in str(link.get('rel'))))
        ]
        
        if not insecure_links:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'All {len(target_blank_links)} target="_blank" links are secure',
                recommendation='Continue using rel="noopener noreferrer" for security',
                score=f'{len(target_blank_links)} secure'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status=TestStatus.FAIL,
                severity='Medium',
                issue_description=f'{len(insecure_links)}/{len(target_blank_links)} target="_blank" links lack security attributes',
                recommendation='Add rel="noopener noreferrer" to external links with target="_blank"',
                score=f'{len(insecure_links)} insecure'
            )
    
    def _test_pagination_tags(self, content: PageContent) -> TestResult:
        """Check for pagination rel tags"""
        soup = content.rendered_soup or content.static_soup
        rel_prev = soup.find('link', attrs={'rel': 'prev'})
        rel_next = soup.find('link', attrs={'rel': 'next'})
        
        is_paginated = bool(re.search(r'[?&]page=|[?&]p=|/page/\d+', content.url))
        
        if rel_prev or rel_next:
            tags_found = []
            if rel_prev:
                tags_found.append('prev')
            if rel_next:
                tags_found.append('next')
            
            return TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Pagination tags present: {", ".join(tags_found)}',
                recommendation='Continue using rel=prev/next for paginated content',
                score=f'{len(tags_found)} tag(s)'
            )
        elif is_paginated:
            return TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Paginated URL but no rel=prev/next tags',
                recommendation='Add rel=prev/next tags to help search engines understand pagination',
                score='Missing pagination tags'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='No pagination detected',
                recommendation='N/A - Not a paginated page',
                score='Not applicable'
            )
    
    def _test_link_density_ratio(self, content: PageContent) -> TestResult:
        """Calculate link text to total text ratio"""
        soup = content.rendered_soup or content.static_soup
        body = soup.find('body')
        if not body:
            return None
        
        total_text = body.get_text()
        total_text_length = len(total_text.strip())
        
        links = soup.find_all('a')
        link_text_length = sum(len(link.get_text().strip()) for link in links)
        
        if total_text_length == 0:
            return None
        
        link_density = (link_text_length / total_text_length) * 100
        
        if link_density <= 20:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Link density is {link_density:.1f}%',
                recommendation='Good balance of links to content',
                score=f'{link_density:.1f}%'
            )
        elif link_density <= 40:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Link density is {link_density:.1f}%',
                recommendation='Consider reducing number of links relative to content',
                score=f'{link_density:.1f}%'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status=TestStatus.FAIL,
                severity='Low',
                issue_description=f'High link density: {link_density:.1f}%',
                recommendation='Too many links may dilute link value and harm SEO',
                score=f'{link_density:.1f}%'
            )
    
    # =========================================================================
    # ADDITIONAL TECHNICAL SEO TESTS - PHASE 1
    # =========================================================================
    
    def _test_url_parameters(self, content: PageContent) -> TestResult:
        """Check for excessive URL parameters"""
        from urllib.parse import urlparse
        parsed = urlparse(content.url)
        
        if not parsed.query:
            return TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Clean URL with no parameters',
                recommendation='Continue using clean URLs',
                score='0 parameters'
            )
        
        params = parsed.query.split('&')
        param_count = len(params)
        
        if param_count <= 3:
            return TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{param_count} URL parameter(s)',
                recommendation='Parameter count is acceptable',
                score=f'{param_count} parameter(s)'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Many URL parameters ({param_count})',
                recommendation='Consider reducing parameters or using URL rewriting',
                score=f'{param_count} parameter(s)'
            )
    
    def _test_trailing_slash_consistency(self, content: PageContent) -> TestResult:
        """Check trailing slash consistency"""
        soup = content.rendered_soup or content.static_soup
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        
        if not canonical:
            return None
        
        canonical_url = canonical.get('href', '')
        
        url_ends_with_slash = content.url.endswith('/')
        canonical_ends_with_slash = canonical_url.endswith('/')
        
        if url_ends_with_slash == canonical_ends_with_slash:
            return TestResult(
                url=content.url,
                test_id='trailing_slash_consistency',
                test_name='Trailing Slash Consistency',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='URL and canonical have consistent trailing slash usage',
                recommendation='Continue maintaining consistent URL structure',
                score='Consistent'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='trailing_slash_consistency',
                test_name='Trailing Slash Consistency',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='Trailing slash inconsistency between URL and canonical',
                recommendation='Ensure consistent trailing slash usage to avoid duplicate content',
                score='Inconsistent'
            )
    
    def _test_mixed_content_detection(self, content: PageContent) -> TestResult:
        """Detect HTTP resources on HTTPS pages"""
        if not content.url.startswith('https://'):
            return None
        
        soup = content.rendered_soup or content.static_soup
        insecure_resources = []
        
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            if script['src'].startswith('http://'):
                insecure_resources.append(f'script: {script["src"][:50]}')
        
        stylesheets = soup.find_all('link', rel='stylesheet', href=True)
        for style in stylesheets:
            if style['href'].startswith('http://'):
                insecure_resources.append(f'stylesheet: {style["href"][:50]}')
        
        images = soup.find_all('img', src=True)
        for img in images:
            if img['src'].startswith('http://'):
                insecure_resources.append(f'image: {img["src"][:50]}')
        
        iframes = soup.find_all('iframe', src=True)
        for iframe in iframes:
            if iframe['src'].startswith('http://'):
                insecure_resources.append(f'iframe: {iframe["src"][:50]}')
        
        if not insecure_resources:
            return TestResult(
                url=content.url,
                test_id='mixed_content_detection',
                test_name='Mixed Content Detection',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No mixed content detected',
                recommendation='All resources loaded securely over HTTPS',
                score='No mixed content'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='mixed_content_detection',
                test_name='Mixed Content Detection',
                category='Technical SEO',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{len(insecure_resources)} HTTP resources on HTTPS page',
                recommendation='Update all resources to use HTTPS to avoid security warnings',
                score=f'{len(insecure_resources)} insecure resources'
            )
    
    # =========================================================================
    # ADDITIONAL PERFORMANCE TESTS - PHASE 1
    # =========================================================================
    
    def _test_gzip_compression(self, content: PageContent) -> TestResult:
        """Check if response is compressed (gzip/brotli)"""
        headers = content.static_headers
        
        encoding = headers.get('Content-Encoding', '').lower()
        
        if 'gzip' in encoding or 'br' in encoding:
            return TestResult(
                url=content.url,
                test_id='gzip_compression',
                test_name='Compression',
                category='Performance',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'Response is compressed ({encoding})',
                recommendation='Continue using compression for optimal performance',
                score=f'{encoding} enabled'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='gzip_compression',
                test_name='Compression',
                category='Performance',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='No compression detected',
                recommendation='Enable gzip or brotli compression to reduce file size by 60-80%',
                score='No compression'
            )
    
    def _test_cache_headers(self, content: PageContent) -> TestResult:
        """Check for proper cache-control headers"""
        headers = content.static_headers
        
        cache_control = headers.get('Cache-Control', '')
        expires = headers.get('Expires', '')
        etag = headers.get('ETag', '')
        
        has_caching = bool(cache_control or expires or etag)
        
        if has_caching:
            return TestResult(
                url=content.url,
                test_id='cache_headers',
                test_name='Browser Caching',
                category='Performance',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Caching headers are present',
                recommendation='Continue maintaining proper cache headers',
                score=f'Cache-Control: {cache_control[:50]}'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='cache_headers',
                test_name='Browser Caching',
                category='Performance',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No caching headers found',
                recommendation='Add Cache-Control headers to improve repeat visit performance',
                score='No cache headers'
            )

    
    # =========================================================================
    # =========================================================================
    # PHASE 2 TESTS - FULL IMPLEMENTATIONS
    # =========================================================================
    
    def _test_schema_organization(self, content: PageContent) -> TestResult:
        """Check for Organization schema markup"""
        import json
        soup = content.rendered_soup or content.static_soup
        
        # Find all JSON-LD scripts
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        has_organization = False
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                # Handle both single objects and arrays
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if item.get('@type') == 'Organization':
                        has_organization = True
                        break
            except:
                continue
        
        if has_organization:
            return TestResult(
                url=content.url,
                test_id='schema_organization',
                test_name='Organization Schema',
                category='Structured Data',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Organization schema markup found',
                recommendation='Continue maintaining Organization structured data',
                score='Organization schema present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='schema_organization',
                test_name='Organization Schema',
                category='Structured Data',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No Organization schema markup found',
                recommendation='Add Organization schema to help search engines understand your business',
                score='No Organization schema'
            )
    
    def _test_schema_breadcrumb(self, content: PageContent) -> TestResult:
        """Check for Breadcrumb schema"""
        import json
        soup = content.rendered_soup or content.static_soup
        
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        has_breadcrumb = False
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if item.get('@type') == 'BreadcrumbList':
                        has_breadcrumb = True
                        break
            except:
                continue
        
        if has_breadcrumb:
            return TestResult(
                url=content.url,
                test_id='schema_breadcrumb',
                test_name='Breadcrumb Schema',
                category='Structured Data',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='BreadcrumbList schema found',
                recommendation='Continue using breadcrumb markup for better SERP display',
                score='Breadcrumb schema present'
            )
        else:
            return None  # Not all pages need breadcrumbs
    
    def _test_video_schema_markup(self, content: PageContent) -> TestResult:
        """Check for VideoObject schema on pages with videos"""
        import json
        soup = content.rendered_soup or content.static_soup
        
        # Check if page has video elements
        videos = soup.find_all(['video', 'iframe'])
        video_iframes = [v for v in videos if v.name == 'iframe' and ('youtube' in str(v.get('src', '')) or 'vimeo' in str(v.get('src', '')))]
        has_video_elements = len(soup.find_all('video')) > 0 or len(video_iframes) > 0
        
        if not has_video_elements:
            return None  # No video, no need to check
        
        # Check for VideoObject schema
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        has_video_schema = False
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if item.get('@type') == 'VideoObject':
                        has_video_schema = True
                        break
            except:
                continue
        
        if has_video_schema:
            return TestResult(
                url=content.url,
                test_id='video_schema_markup',
                test_name='Video Schema Markup',
                category='Structured Data',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='VideoObject schema found for video content',
                recommendation='Continue using video schema for rich snippets',
                score='Video schema present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='video_schema_markup',
                test_name='Video Schema Markup',
                category='Structured Data',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='Video content found but no VideoObject schema',
                recommendation='Add VideoObject schema to enable video rich snippets',
                score='Missing video schema'
            )
    
    def _test_hreflang_tags(self, content: PageContent) -> TestResult:
        """Check for hreflang tags for international targeting"""
        soup = content.rendered_soup or content.static_soup
        hreflang_tags = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
        
        if len(hreflang_tags) > 0:
            languages = [tag.get('hreflang') for tag in hreflang_tags]
            return TestResult(
                url=content.url,
                test_id='hreflang_tags',
                test_name='Hreflang Tags',
                category='International SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Found {len(hreflang_tags)} hreflang tags',
                recommendation='Ensure hreflang tags are properly implemented with reciprocal links',
                score=f'{len(hreflang_tags)} language(s): {", ".join(languages[:5])}'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='hreflang_tags',
                test_name='Hreflang Tags',
                category='International SEO',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='No hreflang tags found',
                recommendation='If serving international audiences, implement hreflang tags',
                score='No hreflang'
            )
    
    def _test_meta_keywords(self, content: PageContent) -> TestResult:
        """Check for obsolete meta keywords tag"""
        soup = content.rendered_soup or content.static_soup
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
            return TestResult(
                url=content.url,
                test_id='meta_keywords_presence',
                test_name='Meta Keywords (Obsolete)',
                category='Meta Tags',
                status=TestStatus.INFO,
                severity='Info',
                issue_description='Meta keywords tag found (not used by major search engines)',
                recommendation='Meta keywords are obsolete and can be removed',
                score=f'Present: {len(keywords)} chars'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='meta_keywords_presence',
                test_name='Meta Keywords (Obsolete)',
                category='Meta Tags',
                status=TestStatus.PASS,
                severity='Info',
                issue_description='No obsolete meta keywords tag',
                recommendation='Good - meta keywords are not needed',
                score='Not present'
            )
    
    def _test_header_keyword_optimization(self, content: PageContent) -> TestResult:
        """Check if title keywords appear in H1"""
        soup = content.rendered_soup or content.static_soup
        title = soup.find('title')
        h1 = soup.find('h1')
        
        if not title or not h1:
            return None
        
        title_text = title.text.strip().lower()
        h1_text = h1.text.strip().lower()
        
        # Extract words from title (simple approach)
        title_words = set([w for w in title_text.split() if len(w) > 3])
        h1_words = set([w for w in h1_text.split() if len(w) > 3])
        
        if not title_words:
            return None
        
        common_words = title_words.intersection(h1_words)
        overlap_percentage = (len(common_words) / len(title_words)) * 100 if title_words else 0
        
        if overlap_percentage >= 30:
            return TestResult(
                url=content.url,
                test_id='header_keyword_optimization',
                test_name='Title/H1 Keyword Alignment',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Good keyword alignment between title and H1 ({overlap_percentage:.0f}%)',
                recommendation='Continue aligning title and H1 keywords for relevance',
                score=f'{overlap_percentage:.0f}% overlap'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='header_keyword_optimization',
                test_name='Title/H1 Keyword Alignment',
                category='Content',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description=f'Low keyword alignment between title and H1 ({overlap_percentage:.0f}%)',
                recommendation='Use similar keywords in title and H1 for better topical relevance',
                score=f'{overlap_percentage:.0f}% overlap'
            )
    
    def _test_content_freshness_date(self, content: PageContent) -> TestResult:
        """Check for content freshness indicators"""
        import json
        soup = content.rendered_soup or content.static_soup
        
        # Check for schema datePublished/dateModified
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        has_date_schema = False
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    if 'datePublished' in item or 'dateModified' in item:
                        has_date_schema = True
                        break
            except:
                continue
        
        # Check for common date meta tags
        date_meta = soup.find('meta', attrs={'property': re.compile(r'(article:published_time|article:modified_time)', re.I)})
        
        if has_date_schema or date_meta:
            return TestResult(
                url=content.url,
                test_id='content_freshness_date',
                test_name='Content Freshness Indicators',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='Content date metadata found',
                recommendation='Continue maintaining date metadata for content freshness signals',
                score='Date metadata present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='content_freshness_date',
                test_name='Content Freshness Indicators',
                category='Content',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No date metadata found',
                recommendation='Consider adding publication/modified dates for content freshness',
                score='No date metadata'
            )
    
    def _test_multimedia_diversity(self, content: PageContent) -> TestResult:
        """Check for diverse media types"""
        soup = content.rendered_soup or content.static_soup
        
        media_types = {
            'images': len(soup.find_all('img')),
            'videos': len(soup.find_all('video')),
            'audio': len(soup.find_all('audio')),
            'iframes': len([i for i in soup.find_all('iframe') if 'youtube' in str(i.get('src', '')) or 'vimeo' in str(i.get('src', ''))])
        }
        
        total_media = sum(media_types.values())
        media_type_count = sum(1 for v in media_types.values() if v > 0)
        
        if media_type_count >= 2:
            return TestResult(
                url=content.url,
                test_id='multimedia_diversity',
                test_name='Multimedia Diversity',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Diverse media types found ({media_type_count} types, {total_media} total)',
                recommendation='Continue using diverse media to engage users',
                score=f'{media_type_count} media types'
            )
        elif media_type_count == 1:
            return TestResult(
                url=content.url,
                test_id='multimedia_diversity',
                test_name='Multimedia Diversity',
                category='Content',
                status=TestStatus.INFO,
                severity='Low',
                issue_description=f'Limited media diversity ({total_media} items of 1 type)',
                recommendation='Consider adding varied media types (images, videos, audio)',
                score='1 media type'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='multimedia_diversity',
                test_name='Multimedia Diversity',
                category='Content',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='No multimedia content found',
                recommendation='Add images, videos, or other media to enhance engagement',
                score='No media'
            )
    
    def _test_oversized_images(self, content: PageContent) -> TestResult:
        """Check for potentially oversized images"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img', src=True)
        
        if not images:
            return None
        
        # Look for images without optimization indicators
        potentially_large = []
        for img in images:
            src = img.get('src', '')
            # Check for lack of optimization indicators
            if not any(indicator in src.lower() for indicator in ['thumb', 'small', 'compressed', 'optimized', 'webp', 'avif']):
                # Check if it's a full-size image indicator
                if any(size in src.lower() for size in ['full', 'original', 'large', 'hires', 'hi-res']):
                    potentially_large.append(src[:50])
        
        if len(potentially_large) > 0:
            return TestResult(
                url=content.url,
                test_id='img_oversized_files',
                test_name='Potentially Oversized Images',
                category='Images',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'{len(potentially_large)} potentially oversized images detected',
                recommendation='Optimize and compress images to improve page load speed',
                score=f'{len(potentially_large)} potentially large'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='img_oversized_files',
                test_name='Potentially Oversized Images',
                category='Images',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No obvious oversized images detected',
                recommendation='Continue optimizing images for web delivery',
                score='Images appear optimized'
            )
    
    def _test_broken_internal_links(self, content: PageContent) -> TestResult:
        """Check for broken internal links - Basic check"""
        from urllib.parse import urlparse, urljoin
        soup = content.rendered_soup or content.static_soup
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        internal_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') or domain in href:
                internal_links.append(href)
        
        if len(internal_links) == 0:
            return None
        
        # Basic checks for obviously broken links
        suspicious_links = []
        for link in internal_links:
            # Check for common broken link patterns
            if '#' in link and link.count('#') > 1:
                suspicious_links.append(link[:50])
            elif link.endswith('//'):
                suspicious_links.append(link[:50])
        
        if suspicious_links:
            return TestResult(
                url=content.url,
                test_id='broken_internal_links',
                test_name='Internal Link Quality',
                category='Links',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'{len(suspicious_links)} suspicious internal links found',
                recommendation='Review and fix malformed internal links',
                score=f'{len(suspicious_links)} suspicious'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='broken_internal_links',
                test_name='Internal Link Quality',
                category='Links',
                status=TestStatus.PASS,
                severity='High',
                issue_description=f'{len(internal_links)} internal links appear well-formed',
                recommendation='Continue maintaining quality internal links',
                score=f'{len(internal_links)} links OK'
            )
    
    def _test_table_of_contents(self, content: PageContent) -> TestResult:
        """Detect table of contents presence"""
        soup = content.rendered_soup or content.static_soup
        
        # Look for common TOC patterns
        toc_indicators = soup.find_all(attrs={'class': re.compile(r'(toc|table[-_]of[-_]contents)', re.I)})
        toc_nav = soup.find('nav', attrs={'aria-label': re.compile(r'table of contents', re.I)})
        
        # Also check for lists with many anchor links to headers
        header_ids = [h.get('id') for h in soup.find_all(['h2', 'h3', 'h4']) if h.get('id')]
        toc_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('#') and href[1:] in header_ids:
                toc_links.append(href)
        
        has_toc = len(toc_indicators) > 0 or toc_nav is not None or len(toc_links) >= 3
        
        if has_toc:
            return TestResult(
                url=content.url,
                test_id='table_of_contents',
                test_name='Table of Contents',
                category='Content',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='Table of contents detected',
                recommendation='TOC improves UX and may trigger jump-to links in SERPs',
                score='TOC present'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='table_of_contents',
                test_name='Table of Contents',
                category='Content',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No table of contents detected',
                recommendation='For long content, add TOC for better navigation',
                score='No TOC'
            )
    
    def _test_sitemap_index(self, content: PageContent) -> TestResult:
        """Check for sitemap index file"""
        from urllib.parse import urlparse
        import requests
        
        parsed = urlparse(content.url)
        sitemap_index_url = f"{parsed.scheme}://{parsed.netloc}/sitemap_index.xml"
        
        try:
            response = requests.head(sitemap_index_url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                return TestResult(
                    url=content.url,
                    test_id='sitemap_index_presence',
                    test_name='Sitemap Index',
                    category='Technical SEO',
                    status=TestStatus.PASS,
                    severity='Low',
                    issue_description='Sitemap index file found',
                    recommendation='Sitemap index is useful for large sites with multiple sitemaps',
                    score='Index file exists'
                )
        except:
            pass
        
        return TestResult(
            url=content.url,
            test_id='sitemap_index_presence',
            test_name='Sitemap Index',
            category='Technical SEO',
            status=TestStatus.INFO,
            severity='Low',
            issue_description='No sitemap index file found',
            recommendation='For sites with 50,000+ URLs, consider using sitemap index',
            score='No index file'
        )
    
    def _test_robots_txt_quality(self, content: PageContent) -> TestResult:
        """Check robots.txt quality"""
        from urllib.parse import urlparse
        import requests
        
        parsed = urlparse(content.url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                robots_content = response.text
                
                # Check for common issues
                issues = []
                if 'Disallow: /' in robots_content and 'Allow:' not in robots_content:
                    issues.append('Blocking entire site')
                if robots_content.count('Disallow:') > 50:
                    issues.append('Too many disallow rules')
                if 'Sitemap:' not in robots_content:
                    issues.append('No sitemap reference')
                
                if not issues:
                    return TestResult(
                        url=content.url,
                        test_id='robots_txt_quality',
                        test_name='Robots.txt Quality',
                        category='Technical SEO',
                        status=TestStatus.PASS,
                        severity='Medium',
                        issue_description='Robots.txt appears well-configured',
                        recommendation='Continue maintaining robots.txt best practices',
                        score='Well configured'
                    )
                else:
                    return TestResult(
                        url=content.url,
                        test_id='robots_txt_quality',
                        test_name='Robots.txt Quality',
                        category='Technical SEO',
                        status=TestStatus.WARNING,
                        severity='Medium',
                        issue_description=f'Robots.txt issues: {", ".join(issues)}',
                        recommendation='Review and optimize robots.txt configuration',
                        score=f'{len(issues)} issue(s)'
                    )
        except:
            pass
        
        return None
    
    def _test_url_structure_analysis(self, content: PageContent) -> TestResult:
        """Analyze URL structure quality"""
        from urllib.parse import urlparse
        
        parsed = urlparse(content.url)
        path = parsed.path
        
        # Analyze URL characteristics
        issues = []
        url_length = len(content.url)
        
        if url_length > 100:
            issues.append(f'Long URL ({url_length} chars)')
        
        if '_' in path:
            issues.append('Underscores in URL (hyphens preferred)')
        
        if path.count('/') > 5:
            issues.append('Deep URL structure')
        
        if any(char in path for char in ['%', '&', '=', '?']) and parsed.query:
            issues.append('Special characters in path')
        
        # Check for descriptive words
        path_parts = [p for p in path.split('/') if p and not p.isdigit()]
        if len(path_parts) == 0:
            issues.append('No descriptive words in URL')
        
        if not issues:
            return TestResult(
                url=content.url,
                test_id='url_structure_analysis',
                test_name='URL Structure Quality',
                category='Technical SEO',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='URL structure is SEO-friendly',
                recommendation='Continue using clean, descriptive URLs',
                score='Well structured'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='url_structure_analysis',
                test_name='URL Structure Quality',
                category='Technical SEO',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'URL structure issues: {", ".join(issues[:3])}',
                recommendation='Use short, descriptive URLs with hyphens',
                score=f'{len(issues)} issue(s)'
            )
    
    def _test_redirect_chain_detection(self, content: PageContent) -> TestResult:
        """Detect redirect chains - Basic check"""
        # This requires tracking the request history
        # For now, return info status as full implementation needs request tracking
        return TestResult(
            url=content.url,
            test_id='redirect_chain_detection',
            test_name='Redirect Chain Detection',
            category='Technical SEO',
            status=TestStatus.INFO,
            severity='High',
            issue_description='Redirect chain check requires request history tracking',
            recommendation='Manually verify no redirect chains exist (max 1 redirect)',
            score='Manual check needed'
        )
    
    def _test_www_consistency(self, content: PageContent) -> TestResult:
        """Check www vs non-www consistency"""
        from urllib.parse import urlparse
        import requests
        
        parsed = urlparse(content.url)
        domain = parsed.netloc
        
        # Determine current version
        has_www = domain.startswith('www.')
        
        # Test the alternate version
        if has_www:
            alt_domain = domain[4:]  # Remove www.
        else:
            alt_domain = f'www.{domain}'
        
        alt_url = f'{parsed.scheme}://{alt_domain}{parsed.path}'
        
        try:
            response = requests.head(alt_url, timeout=5, allow_redirects=False)
            if response.status_code in [301, 302, 307, 308]:
                return TestResult(
                    url=content.url,
                    test_id='www_consistency',
                    test_name='WWW Consistency',
                    category='Technical SEO',
                    status=TestStatus.PASS,
                    severity='High',
                    issue_description='Proper redirect from alternate version',
                    recommendation='Continue maintaining single canonical version',
                    score='Redirect configured'
                )
            else:
                return TestResult(
                    url=content.url,
                    test_id='www_consistency',
                    test_name='WWW Consistency',
                    category='Technical SEO',
                    status=TestStatus.WARNING,
                    severity='High',
                    issue_description='Both www and non-www versions may be accessible',
                    recommendation='Configure 301 redirect to single canonical version',
                    score='Both versions accessible'
                )
        except:
            return TestResult(
                url=content.url,
                test_id='www_consistency',
                test_name='WWW Consistency',
                category='Technical SEO',
                status=TestStatus.INFO,
                severity='High',
                issue_description='Could not verify www consistency',
                recommendation='Manually verify www/non-www redirects properly',
                score='Verification failed'
            )
    
    def _test_render_blocking_resources(self, content: PageContent) -> TestResult:
        """Check for render-blocking resources"""
        soup = content.rendered_soup or content.static_soup
        
        # Count render-blocking scripts and stylesheets
        blocking_scripts = [s for s in soup.find_all('script', src=True) 
                           if s.parent.name == 'head' and not s.get('async') and not s.get('defer')]
        
        blocking_styles = soup.find_all('link', rel='stylesheet')
        non_blocking_styles = [s for s in blocking_styles 
                               if s.get('media') and s.get('media') != 'all' and s.get('media') != 'screen']
        
        actual_blocking_styles = len(blocking_styles) - len(non_blocking_styles)
        total_blocking = len(blocking_scripts) + actual_blocking_styles
        
        if total_blocking == 0:
            return TestResult(
                url=content.url,
                test_id='render_blocking_resources',
                test_name='Render-Blocking Resources',
                category='Performance',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No render-blocking resources detected',
                recommendation='Excellent - all resources are async or deferred',
                score='0 blocking resources'
            )
        elif total_blocking <= 3:
            return TestResult(
                url=content.url,
                test_id='render_blocking_resources',
                test_name='Render-Blocking Resources',
                category='Performance',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'{total_blocking} render-blocking resources found',
                recommendation='Consider async/defer for scripts, critical CSS inline',
                score=f'{total_blocking} blocking'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='render_blocking_resources',
                test_name='Render-Blocking Resources',
                category='Performance',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'{total_blocking} render-blocking resources (scripts: {len(blocking_scripts)}, styles: {actual_blocking_styles})',
                recommendation='Significantly reduce render-blocking resources for better FCP/LCP',
                score=f'{total_blocking} blocking'
            )
    
    def _test_third_party_scripts(self, content: PageContent) -> TestResult:
        """Check third-party script usage"""
        from urllib.parse import urlparse
        soup = content.rendered_soup or content.static_soup
        parsed_url = urlparse(content.url)
        domain = parsed_url.netloc
        
        all_scripts = soup.find_all('script', src=True)
        third_party = [s for s in all_scripts 
                      if s['src'].startswith('http') and domain not in s['src']]
        
        if len(third_party) == 0:
            return TestResult(
                url=content.url,
                test_id='third_party_scripts',
                test_name='Third-Party Scripts',
                category='Performance',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No third-party scripts detected',
                recommendation='Great - minimal external dependencies',
                score='0 third-party scripts'
            )
        elif len(third_party) <= 5:
            return TestResult(
                url=content.url,
                test_id='third_party_scripts',
                test_name='Third-Party Scripts',
                category='Performance',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description=f'{len(third_party)} third-party scripts found',
                recommendation='Monitor third-party script impact on performance',
                score=f'{len(third_party)} scripts'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='third_party_scripts',
                test_name='Third-Party Scripts',
                category='Performance',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Many third-party scripts ({len(third_party)})',
                recommendation='Reduce third-party scripts or load them asynchronously',
                score=f'{len(third_party)} scripts'
            )
    
    def _test_aria_landmarks(self, content: PageContent) -> TestResult:
        """Check for ARIA landmark roles"""
        soup = content.rendered_soup or content.static_soup
        
        landmark_roles = ['banner', 'navigation', 'main', 'complementary', 'contentinfo', 'search', 'form']
        found_landmarks = {}
        
        for role in landmark_roles:
            elements = soup.find_all(attrs={'role': role})
            if elements:
                found_landmarks[role] = len(elements)
        
        # Also check for semantic HTML5 elements that have implicit roles
        semantic_elements = {
            'header': 'banner',
            'nav': 'navigation',
            'main': 'main',
            'aside': 'complementary',
            'footer': 'contentinfo'
        }
        
        for tag, role in semantic_elements.items():
            if soup.find(tag) and role not in found_landmarks:
                found_landmarks[role] = 1
        
        landmark_count = len(found_landmarks)
        
        if landmark_count >= 3:
            return TestResult(
                url=content.url,
                test_id='aria_landmarks',
                test_name='ARIA Landmarks',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Good landmark structure ({landmark_count} landmarks)',
                recommendation='Continue using ARIA landmarks for screen reader navigation',
                score=f'{landmark_count} landmarks'
            )
        elif landmark_count >= 1:
            return TestResult(
                url=content.url,
                test_id='aria_landmarks',
                test_name='ARIA Landmarks',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Limited landmarks ({landmark_count})',
                recommendation='Add more ARIA landmarks (banner, navigation, main, contentinfo)',
                score=f'{landmark_count} landmark(s)'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='aria_landmarks',
                test_name='ARIA Landmarks',
                category='Accessibility',
                status=TestStatus.FAIL,
                severity='Medium',
                issue_description='No ARIA landmarks found',
                recommendation='Implement ARIA landmarks for better accessibility',
                score='0 landmarks'
            )
    
    # =========================================================================
    # PHASE 3 TESTS - FULL IMPLEMENTATIONS
    # =========================================================================
    
    def _test_cdn_usage(self, content: PageContent) -> TestResult:
        """Check if site uses a CDN"""
        headers = content.static_headers
        
        # Common CDN indicators in headers
        cdn_headers = [
            'cf-ray',  # Cloudflare
            'x-amz-cf-id',  # Amazon CloudFront
            'x-cache',  # Various CDNs
            'x-cdn',
            'x-fastly-request-id',  # Fastly
            'x-akamai-transformed',  # Akamai
        ]
        
        cdn_detected = any(header.lower() in [h.lower() for h in headers.keys()] 
                          for header in cdn_headers)
        
        # Also check server header for CDN indicators
        server = headers.get('Server', '').lower()
        cdn_in_server = any(cdn in server for cdn in ['cloudflare', 'cloudfront', 'fastly', 'akamai'])
        
        if cdn_detected or cdn_in_server:
            return TestResult(
                url=content.url,
                test_id='cdn_usage',
                test_name='CDN Usage',
                category='Performance',
                status=TestStatus.PASS,
                severity='Low',
                issue_description='CDN detected',
                recommendation='Continue using CDN for optimal global performance',
                score='CDN in use'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='cdn_usage',
                test_name='CDN Usage',
                category='Performance',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No CDN detected',
                recommendation='Consider using a CDN to improve global load times',
                score='No CDN detected'
            )
    
    def _test_web_font_optimization(self, content: PageContent) -> TestResult:
        """Check for web font optimization"""
        soup = content.rendered_soup or content.static_soup
        
        # Check for preconnect to font providers
        preconnects = soup.find_all('link', rel='preconnect')
        font_preconnect = any('fonts.' in str(link.get('href', '')) for link in preconnects)
        
        # Check for preload of fonts
        preloads = soup.find_all('link', rel='preload', as_='font')
        
        # Check stylesheets for font-display property (would need CSS parsing)
        # For now, just check if fonts are being loaded
        font_links = [link for link in soup.find_all('link', href=True) 
                     if 'fonts.' in link.get('href', '') or '.woff' in link.get('href', '')]
        
        optimizations_found = []
        if font_preconnect:
            optimizations_found.append('preconnect')
        if preloads:
            optimizations_found.append('preload')
        
        if not font_links:
            return None  # No fonts, no need to check
        
        if len(optimizations_found) >= 1:
            return TestResult(
                url=content.url,
                test_id='web_font_optimization',
                test_name='Web Font Optimization',
                category='Performance',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Font optimization detected: {", ".join(optimizations_found)}',
                recommendation='Continue optimizing font loading with preload/preconnect',
                score=f'{len(optimizations_found)} optimization(s)'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='web_font_optimization',
                test_name='Web Font Optimization',
                category='Performance',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='Web fonts found but no optimization detected',
                recommendation='Add font-display: swap and preconnect to font providers',
                score='Not optimized'
            )
    
    def _test_mobile_content_width(self, content: PageContent) -> TestResult:
        """Check mobile content width configuration"""
        soup = content.rendered_soup or content.static_soup
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        
        if not viewport:
            return TestResult(
                url=content.url,
                test_id='mobile_content_width',
                test_name='Mobile Content Width',
                category='Mobile Usability',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='No viewport meta tag',
                recommendation='Add viewport meta tag for mobile responsiveness',
                score='No viewport'
            )
        
        viewport_content = viewport.get('content', '').lower()
        
        # Check for proper configuration
        has_width = 'width=device-width' in viewport_content
        has_no_max_scale = 'maximum-scale' not in viewport_content or 'maximum-scale=1' not in viewport_content
        
        if has_width and has_no_max_scale:
            return TestResult(
                url=content.url,
                test_id='mobile_content_width',
                test_name='Mobile Content Width',
                category='Mobile Usability',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Proper mobile viewport configuration',
                recommendation='Continue maintaining responsive design',
                score='Well configured'
            )
        elif has_width:
            return TestResult(
                url=content.url,
                test_id='mobile_content_width',
                test_name='Mobile Content Width',
                category='Mobile Usability',
                status=TestStatus.WARNING,
                severity='High',
                issue_description='Viewport configured but may restrict zooming',
                recommendation='Avoid maximum-scale=1 to allow user zooming',
                score='Viewport with restrictions'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='mobile_content_width',
                test_name='Mobile Content Width',
                category='Mobile Usability',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Viewport not properly configured',
                recommendation='Set viewport width=device-width for responsive design',
                score='Misconfigured'
            )
    
    def _test_responsive_image_strategy(self, content: PageContent) -> TestResult:
        """Evaluate responsive image implementation strategy"""
        soup = content.rendered_soup or content.static_soup
        images = soup.find_all('img')
        
        if not images:
            return None
        
        with_srcset = len([img for img in images if img.get('srcset')])
        with_sizes = len([img for img in images if img.get('sizes')])
        picture_elements = len(soup.find_all('picture'))
        
        responsive_count = with_srcset + picture_elements
        responsive_percentage = (responsive_count / len(images)) * 100 if images else 0
        
        if responsive_percentage >= 50:
            return TestResult(
                url=content.url,
                test_id='responsive_image_strategy',
                test_name='Responsive Image Strategy',
                category='Mobile Usability',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Good responsive image implementation ({responsive_percentage:.0f}%)',
                recommendation='Continue using srcset/picture for responsive images',
                score=f'{responsive_percentage:.0f}% responsive'
            )
        elif responsive_count > 0:
            return TestResult(
                url=content.url,
                test_id='responsive_image_strategy',
                test_name='Responsive Image Strategy',
                category='Mobile Usability',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Partial responsive images ({responsive_percentage:.0f}%)',
                recommendation='Implement srcset for more images to serve appropriate sizes',
                score=f'{responsive_percentage:.0f}% responsive'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='responsive_image_strategy',
                test_name='Responsive Image Strategy',
                category='Mobile Usability',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No responsive images detected',
                recommendation='Implement responsive images with srcset/picture elements',
                score='Not responsive'
            )
    
    def _test_heading_accessibility_gaps(self, content: PageContent) -> TestResult:
        """Check heading structure for accessibility (similar to header_level_gaps but accessibility-focused)"""
        soup = content.rendered_soup or content.static_soup
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headers:
            return TestResult(
                url=content.url,
                test_id='heading_accessibility_gaps',
                test_name='Heading Accessibility',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='No heading structure found',
                recommendation='Add proper heading hierarchy for screen reader navigation',
                score='No headings'
            )
        
        header_levels = [int(h.name[1]) for h in headers]
        
        # Check if starts with H1
        if header_levels[0] != 1:
            return TestResult(
                url=content.url,
                test_id='heading_accessibility_gaps',
                test_name='Heading Accessibility',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Heading structure does not start with H1 (starts with H{header_levels[0]})',
                recommendation='Begin heading hierarchy with H1 for accessibility',
                score='Missing H1 first'
            )
        
        # Check for gaps
        gaps = []
        for i in range(len(header_levels) - 1):
            if header_levels[i + 1] > header_levels[i] + 1:
                gaps.append(f'H{header_levels[i]}→H{header_levels[i+1]}')
        
        if not gaps:
            return TestResult(
                url=content.url,
                test_id='heading_accessibility_gaps',
                test_name='Heading Accessibility',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='Proper heading hierarchy for screen readers',
                recommendation='Continue maintaining sequential heading levels',
                score='Proper hierarchy'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='heading_accessibility_gaps',
                test_name='Heading Accessibility',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Heading gaps affect screen reader navigation: {", ".join(gaps)}',
                recommendation='Use sequential heading levels (H1→H2→H3) for accessibility',
                score=f'{len(gaps)} gap(s)'
            )
    
    def _test_form_error_handling(self, content: PageContent) -> TestResult:
        """Check form error handling for accessibility"""
        soup = content.rendered_soup or content.static_soup
        forms = soup.find_all('form')
        
        if not forms:
            return None
        
        inputs_with_aria = 0
        total_inputs = 0
        
        for form in forms:
            inputs = form.find_all(['input', 'select', 'textarea'])
            total_inputs += len(inputs)
            
            for input_elem in inputs:
                if input_elem.get('aria-describedby') or input_elem.get('aria-invalid') or input_elem.get('aria-errormessage'):
                    inputs_with_aria += 1
        
        if total_inputs == 0:
            return None
        
        percentage = (inputs_with_aria / total_inputs) * 100 if total_inputs else 0
        
        if percentage >= 50:
            return TestResult(
                url=content.url,
                test_id='form_error_handling',
                test_name='Form Error Handling',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Forms have accessibility attributes ({percentage:.0f}%)',
                recommendation='Continue providing accessible form error handling',
                score=f'{percentage:.0f}% accessible'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='form_error_handling',
                test_name='Form Error Handling',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Limited form accessibility ({percentage:.0f}%)',
                recommendation='Add aria-describedby and aria-invalid for form error handling',
                score=f'{percentage:.0f}% accessible'
            )
    
    def _test_subresource_integrity(self, content: PageContent) -> TestResult:
        """Check for Subresource Integrity on external resources"""
        soup = content.rendered_soup or content.static_soup
        
        # Find external scripts and stylesheets
        external_scripts = [s for s in soup.find_all('script', src=True) 
                           if s['src'].startswith('http') and 'cdn' in s['src'].lower()]
        external_styles = [s for s in soup.find_all('link', rel='stylesheet', href=True) 
                          if s['href'].startswith('http') and 'cdn' in s['href'].lower()]
        
        total_external = len(external_scripts) + len(external_styles)
        
        if total_external == 0:
            return None
        
        with_sri = 0
        for resource in external_scripts + external_styles:
            if resource.get('integrity'):
                with_sri += 1
        
        percentage = (with_sri / total_external) * 100 if total_external else 0
        
        if percentage >= 80:
            return TestResult(
                url=content.url,
                test_id='subresource_integrity',
                test_name='Subresource Integrity (SRI)',
                category='Security',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'SRI implemented on {percentage:.0f}% of CDN resources',
                recommendation='Continue using SRI for external resources',
                score=f'{percentage:.0f}% protected'
            )
        elif percentage > 0:
            return TestResult(
                url=content.url,
                test_id='subresource_integrity',
                test_name='Subresource Integrity (SRI)',
                category='Security',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Partial SRI implementation ({percentage:.0f}%)',
                recommendation='Add integrity attributes to all CDN resources',
                score=f'{percentage:.0f}% protected'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='subresource_integrity',
                test_name='Subresource Integrity (SRI)',
                category='Security',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'{total_external} external resources without SRI',
                recommendation='Implement SRI to protect against compromised CDNs',
                score='No SRI protection'
            )
    
    def _test_iframe_security(self, content: PageContent) -> TestResult:
        """Check iframe security attributes"""
        soup = content.rendered_soup or content.static_soup
        iframes = soup.find_all('iframe')
        
        if not iframes:
            return None
        
        secure_iframes = 0
        for iframe in iframes:
            if iframe.get('sandbox'):
                secure_iframes += 1
        
        percentage = (secure_iframes / len(iframes)) * 100 if iframes else 0
        
        if percentage >= 80:
            return TestResult(
                url=content.url,
                test_id='iframe_security',
                test_name='Iframe Security',
                category='Security',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'{percentage:.0f}% of iframes have sandbox attribute',
                recommendation='Continue sandboxing iframes for security',
                score=f'{percentage:.0f}% sandboxed'
            )
        elif len(iframes) <= 2 and all('youtube.com' in str(iframe.get('src', '')) or 'vimeo.com' in str(iframe.get('src', '')) for iframe in iframes):
            return TestResult(
                url=content.url,
                test_id='iframe_security',
                test_name='Iframe Security',
                category='Security',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description=f'{len(iframes)} trusted iframe(s) (YouTube/Vimeo)',
                recommendation='Consider adding sandbox attributes even for trusted sources',
                score='Trusted sources'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='iframe_security',
                test_name='Iframe Security',
                category='Security',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'{len(iframes) - secure_iframes} iframes without sandbox attribute',
                recommendation='Add sandbox attribute to iframes to limit capabilities',
                score=f'{percentage:.0f}% sandboxed'
            )
    
    def _test_cors_headers(self, content: PageContent) -> TestResult:
        """Check CORS headers configuration"""
        headers = content.static_headers
        
        cors_header = headers.get('Access-Control-Allow-Origin', '')
        
        if cors_header:
            if cors_header == '*':
                return TestResult(
                    url=content.url,
                    test_id='cors_headers',
                    test_name='CORS Headers',
                    category='Security',
                    status=TestStatus.WARNING,
                    severity='Low',
                    issue_description='CORS allows all origins (*)',
                    recommendation='Restrict CORS to specific trusted origins',
                    score='Permissive'
                )
            else:
                return TestResult(
                    url=content.url,
                    test_id='cors_headers',
                    test_name='CORS Headers',
                    category='Security',
                    status=TestStatus.PASS,
                    severity='Low',
                    issue_description='CORS configured with specific origins',
                    recommendation='Continue maintaining restrictive CORS policy',
                    score='Restricted'
                )
        else:
            return TestResult(
                url=content.url,
                test_id='cors_headers',
                test_name='CORS Headers',
                category='Security',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No CORS headers present',
                recommendation='CORS not needed if not serving APIs',
                score='No CORS'
            )
    
    def _test_cookie_security_flags(self, content: PageContent) -> TestResult:
        """Check cookie security flags"""
        headers = content.static_headers
        
        # Get Set-Cookie headers (might be multiple)
        set_cookie = headers.get('Set-Cookie', '')
        
        if not set_cookie:
            return TestResult(
                url=content.url,
                test_id='cookie_security_flags',
                test_name='Cookie Security Flags',
                category='Security',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='No cookies set',
                recommendation='N/A - No cookies detected',
                score='No cookies'
            )
        
        # Check for security flags
        has_secure = 'Secure' in set_cookie
        has_httponly = 'HttpOnly' in set_cookie
        has_samesite = 'SameSite' in set_cookie
        
        flags_count = sum([has_secure, has_httponly, has_samesite])
        
        if flags_count >= 2:
            return TestResult(
                url=content.url,
                test_id='cookie_security_flags',
                test_name='Cookie Security Flags',
                category='Security',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description=f'Cookies have {flags_count}/3 security flags',
                recommendation='Continue using Secure, HttpOnly, and SameSite flags',
                score=f'{flags_count}/3 flags'
            )
        else:
            missing = []
            if not has_secure:
                missing.append('Secure')
            if not has_httponly:
                missing.append('HttpOnly')
            if not has_samesite:
                missing.append('SameSite')
            
            return TestResult(
                url=content.url,
                test_id='cookie_security_flags',
                test_name='Cookie Security Flags',
                category='Security',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description=f'Cookies missing flags: {", ".join(missing)}',
                recommendation='Add Secure, HttpOnly, and SameSite flags to cookies',
                score=f'{flags_count}/3 flags'
            )
    
    def _test_content_language_meta(self, content: PageContent) -> TestResult:
        """Check for content language metadata"""
        headers = content.static_headers
        soup = content.rendered_soup or content.static_soup
        
        # Check HTTP header
        http_lang = headers.get('Content-Language', '')
        
        # Check HTML lang attribute
        html_tag = soup.find('html')
        html_lang = html_tag.get('lang') if html_tag else ''
        
        # Check meta tag
        meta_lang = soup.find('meta', attrs={'http-equiv': re.compile(r'content-language', re.I)})
        
        if http_lang or html_lang:
            return TestResult(
                url=content.url,
                test_id='content_language_meta',
                test_name='Content Language',
                category='International SEO',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Language specified: {html_lang or http_lang}',
                recommendation='Continue specifying content language',
                score=html_lang or http_lang
            )
        else:
            return TestResult(
                url=content.url,
                test_id='content_language_meta',
                test_name='Content Language',
                category='International SEO',
                status=TestStatus.WARNING,
                severity='Low',
                issue_description='No language specification found',
                recommendation='Add lang attribute to HTML tag',
                score='No language specified'
            )
    
    # =========================================================================
    # PHASE 4 TESTS - INFO/PLACEHOLDER IMPLEMENTATIONS
    # =========================================================================
    
    def _test_thin_content_detection(self, content: PageContent) -> TestResult:
        """Detect thin/boilerplate content - Requires multi-page analysis"""
        return TestResult(
            url=content.url,
            test_id='thin_content_detection',
            test_name='Thin Content Detection',
            category='Content',
            status=TestStatus.INFO,
            severity='High',
            issue_description='Requires multi-page analysis to detect boilerplate content',
            recommendation='Ensure each page has unique, valuable content',
            score='Multi-page check'
        )
    
    def _test_orphan_page_check(self, content: PageContent) -> TestResult:
        """Check for orphan pages - Requires site crawl"""
        return TestResult(
            url=content.url,
            test_id='orphan_page_check',
            test_name='Orphan Page Check',
            category='Links',
            status=TestStatus.INFO,
            severity='High',
            issue_description='Requires site-wide crawl to detect orphan pages',
            recommendation='Ensure all pages are linked from other pages',
            score='Site-wide check'
        )
    
    def _test_deep_link_ratio(self, content: PageContent) -> TestResult:
        """Analyze deep link distribution - Requires site analysis"""
        return TestResult(
            url=content.url,
            test_id='deep_link_ratio',
            test_name='Deep Link Ratio',
            category='Links',
            status=TestStatus.INFO,
            severity='Low',
            issue_description='Requires site-wide analysis for link distribution',
            recommendation='Ensure good distribution of links to deep pages',
            score='Site-wide check'
        )
    
    def _test_navigation_depth(self, content: PageContent) -> TestResult:
        """Calculate navigation depth from homepage"""
        return TestResult(
            url=content.url,
            test_id='navigation_depth',
            test_name='Navigation Depth',
            category='Links',
            status=TestStatus.INFO,
            severity='Medium',
            issue_description='Requires site crawl to calculate depth from homepage',
            recommendation='Keep important pages within 3 clicks of homepage',
            score='Crawl required'
        )
    
    def _test_touch_target_sizes(self, content: PageContent) -> TestResult:
        """Check touch target sizes for mobile"""
        return TestResult(
            url=content.url,
            test_id='touch_target_sizes',
            test_name='Touch Target Sizes',
            category='Mobile Usability',
            status=TestStatus.INFO,
            severity='Medium',
            issue_description='Requires rendering with computed styles to measure touch targets',
            recommendation='Ensure interactive elements are minimum 48x48px',
            score='Manual/tool check'
        )
    
    def _test_intrusive_interstitial(self, content: PageContent) -> TestResult:
        """Detect intrusive interstitials"""
        soup = content.rendered_soup or content.static_soup
        
        # Basic check for modal/overlay indicators
        modals = soup.find_all(attrs={'class': re.compile(r'(modal|popup|overlay|interstitial)', re.I)})
        
        if len(modals) > 0:
            return TestResult(
                url=content.url,
                test_id='intrusive_interstitial',
                test_name='Intrusive Interstitials',
                category='Mobile Usability',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'{len(modals)} potential modal/popup elements found',
                recommendation='Ensure popups are not intrusive on mobile (Google penalty risk)',
                score=f'{len(modals)} potential popups'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='intrusive_interstitial',
                test_name='Intrusive Interstitials',
                category='Mobile Usability',
                status=TestStatus.PASS,
                severity='High',
                issue_description='No obvious intrusive popups detected',
                recommendation='Continue avoiding intrusive interstitials',
                score='No popups detected'
            )
    
    def _test_color_contrast_check(self, content: PageContent) -> TestResult:
        """Check color contrast for accessibility"""
        return TestResult(
            url=content.url,
            test_id='color_contrast_check',
            test_name='Color Contrast',
            category='Accessibility',
            status=TestStatus.INFO,
            severity='High',
            issue_description='Requires CSS analysis and rendering to check WCAG contrast ratios',
            recommendation='Ensure 4.5:1 contrast ratio for normal text (WCAG AA)',
            score='Manual/tool check'
        )
    
    def _test_focus_visible_styles(self, content: PageContent) -> TestResult:
        """Check for visible focus indicators"""
        soup = content.rendered_soup or content.static_soup
        
        # Look for CSS that might disable focus
        styles = soup.find_all('style')
        outline_none_found = False
        
        for style in styles:
            if style.string and ('outline:none' in style.string.replace(' ', '') or 'outline: none' in style.string):
                outline_none_found = True
                break
        
        if outline_none_found:
            return TestResult(
                url=content.url,
                test_id='focus_visible_styles',
                test_name='Focus Indicators',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='Medium',
                issue_description='CSS may be removing focus outlines',
                recommendation='If removing outlines, provide alternative focus indicators',
                score='Outline removal detected'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='focus_visible_styles',
                test_name='Focus Indicators',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='Medium',
                issue_description='No obvious focus indicator removal',
                recommendation='Ensure all interactive elements have visible focus state',
                score='Focus styles intact'
            )
    
    def _test_video_captions(self, content: PageContent) -> TestResult:
        """Check for video captions/subtitles"""
        soup = content.rendered_soup or content.static_soup
        videos = soup.find_all('video')
        
        if not videos:
            return None
        
        videos_with_tracks = 0
        for video in videos:
            tracks = video.find_all('track')
            if tracks:
                videos_with_tracks += 1
        
        if videos_with_tracks == len(videos):
            return TestResult(
                url=content.url,
                test_id='video_captions',
                test_name='Video Captions',
                category='Accessibility',
                status=TestStatus.PASS,
                severity='High',
                issue_description='All videos have caption tracks',
                recommendation='Continue providing captions for accessibility',
                score=f'{videos_with_tracks}/{len(videos)} captioned'
            )
        elif videos_with_tracks > 0:
            return TestResult(
                url=content.url,
                test_id='video_captions',
                test_name='Video Captions',
                category='Accessibility',
                status=TestStatus.WARNING,
                severity='High',
                issue_description=f'Only {videos_with_tracks}/{len(videos)} videos have captions',
                recommendation='Add <track> elements with captions for all videos',
                score=f'{videos_with_tracks}/{len(videos)} captioned'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='video_captions',
                test_name='Video Captions',
                category='Accessibility',
                status=TestStatus.FAIL,
                severity='High',
                issue_description='Videos found but no captions',
                recommendation='Add caption tracks for WCAG compliance',
                score='0 captioned'
            )
    
    def _test_hreflang_validation(self, content: PageContent) -> TestResult:
        """Validate hreflang implementation"""
        soup = content.rendered_soup or content.static_soup
        hreflang_tags = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
        
        if not hreflang_tags:
            return None
        
        # Check for x-default
        has_x_default = any(tag.get('hreflang') == 'x-default' for tag in hreflang_tags)
        
        # Check for valid language codes (basic validation)
        invalid_codes = []
        for tag in hreflang_tags:
            hreflang = tag.get('hreflang', '')
            if hreflang != 'x-default' and not re.match(r'^[a-z]{2}(-[A-Z]{2})?$', hreflang):
                invalid_codes.append(hreflang)
        
        if has_x_default and not invalid_codes:
            return TestResult(
                url=content.url,
                test_id='hreflang_validation',
                test_name='Hreflang Validation',
                category='International SEO',
                status=TestStatus.PASS,
                severity='High',
                issue_description='Hreflang tags properly implemented with x-default',
                recommendation='Ensure reciprocal hreflang links exist',
                score='Well configured'
            )
        elif invalid_codes:
            return TestResult(
                url=content.url,
                test_id='hreflang_validation',
                test_name='Hreflang Validation',
                category='International SEO',
                status=TestStatus.FAIL,
                severity='High',
                issue_description=f'Invalid hreflang codes: {", ".join(invalid_codes[:3])}',
                recommendation='Use valid ISO language-country codes (e.g., en-US)',
                score=f'{len(invalid_codes)} invalid'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='hreflang_validation',
                test_name='Hreflang Validation',
                category='International SEO',
                status=TestStatus.WARNING,
                severity='High',
                issue_description='Hreflang tags present but missing x-default',
                recommendation='Add x-default hreflang for unmatched languages',
                score='Missing x-default'
            )
    
    def _test_geo_targeting_meta(self, content: PageContent) -> TestResult:
        """Check for geographic targeting meta tags"""
        soup = content.rendered_soup or content.static_soup
        
        geo_tags = soup.find_all('meta', attrs={'name': re.compile(r'^geo\.', re.I)})
        
        if geo_tags:
            tag_names = [tag.get('name') for tag in geo_tags]
            return TestResult(
                url=content.url,
                test_id='geo_targeting_meta',
                test_name='Geographic Targeting',
                category='International SEO',
                status=TestStatus.PASS,
                severity='Low',
                issue_description=f'Geographic meta tags found: {", ".join(tag_names)}',
                recommendation='Continue using geo tags for local targeting',
                score=f'{len(geo_tags)} geo tags'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='geo_targeting_meta',
                test_name='Geographic Targeting',
                category='International SEO',
                status=TestStatus.INFO,
                severity='Low',
                issue_description='No geographic targeting meta tags',
                recommendation='If targeting local areas, add geo.region/geo.placename tags',
                score='No geo tags'
            )
    
    def _test_amp_version_presence(self, content: PageContent) -> TestResult:
        """Check for AMP version"""
        soup = content.rendered_soup or content.static_soup
        amp_link = soup.find('link', attrs={'rel': 'amphtml'})
        
        if amp_link:
            return TestResult(
                url=content.url,
                test_id='amp_version_presence',
                test_name='AMP Version',
                category='Technical SEO',
                status=TestStatus.INFO,
                severity='Info',
                issue_description='AMP version available',
                recommendation='Ensure AMP version is properly maintained',
                score='AMP available'
            )
        else:
            return TestResult(
                url=content.url,
                test_id='amp_version_presence',
                test_name='AMP Version',
                category='Technical SEO',
                status=TestStatus.INFO,
                severity='Info',
                issue_description='No AMP version',
                recommendation='AMP is optional; focus on Core Web Vitals instead',
                score='No AMP'
            )
