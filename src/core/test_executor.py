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

