#!/usr/bin/env python3
"""
Example implementations for additional SEO tests
This file demonstrates how to implement the Phase 1 quick-win tests
"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib.parse import urlparse
import re


@dataclass
class TestResult:
    """Simple test result structure"""
    test_id: str
    test_name: str
    category: str
    status: str  # Pass, Fail, Warning, Info
    severity: str
    issue_description: str
    recommendation: str
    score: str


class AdditionalSEOTests:
    """
    Implementation examples for Phase 1 additional SEO tests
    These are the quick wins that can be implemented easily
    """
    
    # =========================================================================
    # META TAGS - Phase 1
    # =========================================================================
    
    def test_twitter_card_tags(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Check for Twitter Card meta tags"""
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
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status='Pass',
                severity='Low',
                issue_description=f'Found {found_count}/5 Twitter Card tags',
                recommendation='Continue maintaining Twitter Cards for social sharing',
                score=f'{found_count}/5 tags present'
            )
        elif found_count >= 1:
            return TestResult(
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status='Warning',
                severity='Low',
                issue_description=f'Incomplete Twitter Card implementation ({found_count}/5)',
                recommendation='Add twitter:card, twitter:title, twitter:description, twitter:image',
                score=f'{found_count}/5 tags present'
            )
        else:
            return TestResult(
                test_id='twitter_card_tags',
                test_name='Twitter Card Tags',
                category='Meta Tags',
                status='Info',
                severity='Low',
                issue_description='No Twitter Card tags found',
                recommendation='Add Twitter Card tags to improve Twitter sharing appearance',
                score='0/5 tags present'
            )
    
    def test_meta_refresh_redirect(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Detect meta refresh redirects (bad for SEO)"""
        meta_refresh = soup.find('meta', attrs={'http-equiv': 'refresh'})
        
        if meta_refresh:
            content = meta_refresh.get('content', '')
            return TestResult(
                test_id='meta_refresh_redirect',
                test_name='Meta Refresh Detection',
                category='Meta Tags',
                status='Fail',
                severity='High',
                issue_description=f'Meta refresh redirect detected: {content}',
                recommendation='Replace meta refresh with 301/302 HTTP redirect for better SEO',
                score='Meta refresh found'
            )
        else:
            return TestResult(
                test_id='meta_refresh_redirect',
                test_name='Meta Refresh Detection',
                category='Meta Tags',
                status='Pass',
                severity='High',
                issue_description='No meta refresh redirects detected',
                recommendation='Continue using proper HTTP redirects',
                score='No meta refresh'
            )
    
    def test_duplicate_meta_tags(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Check for duplicate title or description tags"""
        titles = soup.find_all('title')
        descriptions = soup.find_all('meta', attrs={'name': 'description'})
        
        issues = []
        if len(titles) > 1:
            issues.append(f'{len(titles)} title tags')
        if len(descriptions) > 1:
            issues.append(f'{len(descriptions)} description tags')
        
        if issues:
            return TestResult(
                test_id='duplicate_meta_tags',
                test_name='Duplicate Meta Tags',
                category='Meta Tags',
                status='Fail',
                severity='High',
                issue_description=f'Duplicate meta tags found: {", ".join(issues)}',
                recommendation='Remove duplicate title/description tags - only one of each allowed',
                score='; '.join(issues)
            )
        else:
            return TestResult(
                test_id='duplicate_meta_tags',
                test_name='Duplicate Meta Tags',
                category='Meta Tags',
                status='Pass',
                severity='High',
                issue_description='No duplicate meta tags detected',
                recommendation='Continue using single title and description tags',
                score='No duplicates'
            )
    
    def test_favicon_presence(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Check for favicon"""
        favicon = (
            soup.find('link', attrs={'rel': 'icon'}) or
            soup.find('link', attrs={'rel': 'shortcut icon'}) or
            soup.find('link', attrs={'rel': 'apple-touch-icon'})
        )
        
        if favicon:
            return TestResult(
                test_id='favicon_presence',
                test_name='Favicon Presence',
                category='Meta Tags',
                status='Pass',
                severity='Low',
                issue_description='Favicon is present',
                recommendation='Continue providing favicon for brand recognition',
                score='Favicon found'
            )
        else:
            return TestResult(
                test_id='favicon_presence',
                test_name='Favicon Presence',
                category='Meta Tags',
                status='Warning',
                severity='Low',
                issue_description='No favicon detected',
                recommendation='Add favicon to improve brand recognition in browser tabs and bookmarks',
                score='No favicon'
            )
    
    # =========================================================================
    # HEADER STRUCTURE - Phase 1
    # =========================================================================
    
    def test_empty_headers(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Detect empty header tags"""
        all_headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        empty_headers = [h for h in all_headers if not h.text.strip()]
        
        if len(empty_headers) == 0:
            return TestResult(
                test_id='empty_headers',
                test_name='Empty Headers Check',
                category='Header Structure',
                status='Pass',
                severity='High',
                issue_description='All header tags contain text',
                recommendation='Continue using meaningful header text',
                score=f'0/{len(all_headers)} empty'
            )
        else:
            header_types = [h.name.upper() for h in empty_headers]
            return TestResult(
                test_id='empty_headers',
                test_name='Empty Headers Check',
                category='Header Structure',
                status='Fail',
                severity='High',
                issue_description=f'{len(empty_headers)} empty header tag(s): {", ".join(header_types)}',
                recommendation='Remove empty headers or add descriptive text',
                score=f'{len(empty_headers)}/{len(all_headers)} empty'
            )
    
    def test_header_level_gaps(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Detect skipped header levels (e.g., H1 -> H3)"""
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headers:
            return None
        
        header_levels = [int(h.name[1]) for h in headers]
        
        gaps = []
        for i in range(len(header_levels) - 1):
            current = header_levels[i]
            next_level = header_levels[i + 1]
            
            # Check if we skipped a level going down
            if next_level > current + 1:
                gaps.append(f'H{current} → H{next_level}')
        
        if not gaps:
            return TestResult(
                test_id='header_level_gaps',
                test_name='Header Level Gaps',
                category='Header Structure',
                status='Pass',
                severity='Medium',
                issue_description='No header level gaps detected',
                recommendation='Continue maintaining proper header hierarchy',
                score='No gaps'
            )
        else:
            return TestResult(
                test_id='header_level_gaps',
                test_name='Header Level Gaps',
                category='Header Structure',
                status='Warning',
                severity='Medium',
                issue_description=f'Header level gaps found: {", ".join(gaps)}',
                recommendation='Use sequential header levels (H1→H2→H3) for proper document structure',
                score=f'{len(gaps)} gap(s)'
            )
    
    # =========================================================================
    # IMAGES - Phase 1
    # =========================================================================
    
    def test_image_dimensions_specified(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Check if images have width/height attributes"""
        images = soup.find_all('img')
        
        if not images:
            return None
        
        images_with_dimensions = [
            img for img in images 
            if img.get('width') and img.get('height')
        ]
        
        percentage = (len(images_with_dimensions) / len(images)) * 100
        
        if percentage >= 80:
            return TestResult(
                test_id='img_dimensions_specified',
                test_name='Image Dimensions',
                category='Images',
                status='Pass',
                severity='Medium',
                issue_description=f'{len(images_with_dimensions)}/{len(images)} images have dimensions',
                recommendation='Continue specifying image dimensions to prevent layout shifts',
                score=f'{percentage:.1f}% with dimensions'
            )
        else:
            return TestResult(
                test_id='img_dimensions_specified',
                test_name='Image Dimensions',
                category='Images',
                status='Warning',
                severity='Medium',
                issue_description=f'Only {len(images_with_dimensions)}/{len(images)} images have dimensions',
                recommendation='Add width/height attributes to images to improve CLS (Core Web Vitals)',
                score=f'{percentage:.1f}% with dimensions'
            )
    
    def test_modern_image_formats(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Check for modern image formats (WebP, AVIF)"""
        images = soup.find_all('img')
        picture_sources = soup.find_all('source', attrs={'type': lambda x: x and 'image' in x})
        
        if not images and not picture_sources:
            return None
        
        modern_formats = 0
        total_sources = 0
        
        # Check img src and srcset
        for img in images:
            src = img.get('src', '')
            srcset = img.get('srcset', '')
            total_sources += 1
            
            if '.webp' in src.lower() or '.avif' in src.lower():
                modern_formats += 1
            elif '.webp' in srcset.lower() or '.avif' in srcset.lower():
                modern_formats += 1
        
        # Check picture sources
        for source in picture_sources:
            type_attr = source.get('type', '').lower()
            if 'webp' in type_attr or 'avif' in type_attr:
                modern_formats += 1
        
        if modern_formats > 0:
            return TestResult(
                test_id='img_modern_formats',
                test_name='Modern Image Formats',
                category='Images',
                status='Pass',
                severity='Low',
                issue_description=f'Using modern image formats (WebP/AVIF)',
                recommendation='Continue using modern formats for better performance',
                score=f'{modern_formats} modern format uses'
            )
        else:
            return TestResult(
                test_id='img_modern_formats',
                test_name='Modern Image Formats',
                category='Images',
                status='Info',
                severity='Low',
                issue_description='No modern image formats detected',
                recommendation='Consider using WebP or AVIF for 25-35% better compression',
                score='Using traditional formats'
            )
    
    def test_responsive_images_srcset(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Check for responsive image implementation"""
        images = soup.find_all('img')
        picture_elements = soup.find_all('picture')
        
        if not images:
            return None
        
        images_with_srcset = [img for img in images if img.get('srcset')]
        responsive_count = len(images_with_srcset) + len(picture_elements)
        
        if responsive_count > 0:
            return TestResult(
                test_id='img_responsive_srcset',
                test_name='Responsive Images',
                category='Images',
                status='Pass',
                severity='Medium',
                issue_description=f'{responsive_count} responsive image implementations found',
                recommendation='Continue using srcset/picture for different screen sizes',
                score=f'{responsive_count} responsive images'
            )
        else:
            return TestResult(
                test_id='img_responsive_srcset',
                test_name='Responsive Images',
                category='Images',
                status='Warning',
                severity='Medium',
                issue_description='No responsive images detected',
                recommendation='Implement srcset or picture elements for better mobile performance',
                score='No srcset/picture'
            )
    
    # =========================================================================
    # LINKS - Phase 1
    # =========================================================================
    
    def test_nofollow_links_analysis(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Analyze nofollow link usage"""
        all_links = soup.find_all('a', href=True)
        
        if not all_links:
            return None
        
        nofollow_links = [
            link for link in all_links 
            if link.get('rel') and 'nofollow' in ' '.join(link.get('rel', []))
        ]
        
        # Check for internal nofollow (potential issue)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        internal_nofollow = [
            link for link in nofollow_links
            if link['href'].startswith('/') or domain in link['href']
        ]
        
        if internal_nofollow:
            return TestResult(
                test_id='nofollow_links_analysis',
                test_name='Nofollow Links Analysis',
                category='Links',
                status='Warning',
                severity='Low',
                issue_description=f'{len(internal_nofollow)} internal links are nofollowed',
                recommendation='Review internal nofollow links - they may block PageRank flow',
                score=f'{len(nofollow_links)} total nofollow ({len(internal_nofollow)} internal)'
            )
        else:
            return TestResult(
                test_id='nofollow_links_analysis',
                test_name='Nofollow Links Analysis',
                category='Links',
                status='Pass',
                severity='Low',
                issue_description=f'{len(nofollow_links)} external nofollow links',
                recommendation='Appropriate nofollow usage for external links',
                score=f'{len(nofollow_links)} nofollow links'
            )
    
    def test_external_link_security(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Check external links for security attributes"""
        parsed_url = urlparse(url)
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
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status='Pass',
                severity='Medium',
                issue_description='No target="_blank" on external links',
                recommendation='Current configuration is secure',
                score='No target="_blank"'
            )
        
        insecure_links = [
            link for link in target_blank_links
            if not (link.get('rel') and 
                   ('noopener' in link.get('rel') or 'noreferrer' in link.get('rel')))
        ]
        
        if not insecure_links:
            return TestResult(
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status='Pass',
                severity='Medium',
                issue_description=f'All {len(target_blank_links)} target="_blank" links are secure',
                recommendation='Continue using rel="noopener noreferrer" for security',
                score=f'{len(target_blank_links)} secure'
            )
        else:
            return TestResult(
                test_id='external_link_security',
                test_name='External Link Security',
                category='Links',
                status='Fail',
                severity='Medium',
                issue_description=f'{len(insecure_links)}/{len(target_blank_links)} target="_blank" links lack security attributes',
                recommendation='Add rel="noopener noreferrer" to external links with target="_blank"',
                score=f'{len(insecure_links)} insecure'
            )
    
    def test_pagination_tags(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Check for pagination rel tags"""
        rel_prev = soup.find('link', attrs={'rel': 'prev'})
        rel_next = soup.find('link', attrs={'rel': 'next'})
        
        # Check if URL suggests pagination
        is_paginated = bool(re.search(r'[\?&]page=|[\?&]p=|/page/\d+', url))
        
        if rel_prev or rel_next:
            tags_found = []
            if rel_prev:
                tags_found.append('prev')
            if rel_next:
                tags_found.append('next')
            
            return TestResult(
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status='Pass',
                severity='Medium',
                issue_description=f'Pagination tags present: {", ".join(tags_found)}',
                recommendation='Continue using rel=prev/next for paginated content',
                score=f'{len(tags_found)} tag(s)'
            )
        elif is_paginated:
            return TestResult(
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status='Warning',
                severity='Medium',
                issue_description='Paginated URL but no rel=prev/next tags',
                recommendation='Add rel=prev/next tags to help search engines understand pagination',
                score='Missing pagination tags'
            )
        else:
            return TestResult(
                test_id='pagination_rel_tags',
                test_name='Pagination Tags',
                category='Links',
                status='Info',
                severity='Medium',
                issue_description='No pagination detected',
                recommendation='N/A - Not a paginated page',
                score='Not applicable'
            )
    
    def test_link_density_ratio(self, soup: BeautifulSoup, url: str) -> TestResult:
        """Calculate link text to total text ratio"""
        # Get all text
        body = soup.find('body')
        if not body:
            return None
        
        total_text = body.get_text()
        total_text_length = len(total_text.strip())
        
        # Get all link text
        links = soup.find_all('a')
        link_text_length = sum(len(link.get_text().strip()) for link in links)
        
        if total_text_length == 0:
            return None
        
        link_density = (link_text_length / total_text_length) * 100
        
        if link_density <= 20:
            return TestResult(
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status='Pass',
                severity='Low',
                issue_description=f'Link density is {link_density:.1f}%',
                recommendation='Good balance of links to content',
                score=f'{link_density:.1f}%'
            )
        elif link_density <= 40:
            return TestResult(
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status='Warning',
                severity='Low',
                issue_description=f'Link density is {link_density:.1f}%',
                recommendation='Consider reducing number of links relative to content',
                score=f'{link_density:.1f}%'
            )
        else:
            return TestResult(
                test_id='link_density_ratio',
                test_name='Link Density',
                category='Links',
                status='Fail',
                severity='Low',
                issue_description=f'High link density: {link_density:.1f}%',
                recommendation='Too many links may dilute link value and harm SEO',
                score=f'{link_density:.1f}%'
            )
    
    # =========================================================================
    # TECHNICAL SEO - Phase 1
    # =========================================================================
    
    def test_url_parameters(self, url: str) -> TestResult:
        """Check for excessive URL parameters"""
        parsed = urlparse(url)
        
        if not parsed.query:
            return TestResult(
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status='Pass',
                severity='Medium',
                issue_description='Clean URL with no parameters',
                recommendation='Continue using clean URLs',
                score='0 parameters'
            )
        
        params = parsed.query.split('&')
        param_count = len(params)
        
        if param_count <= 3:
            return TestResult(
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status='Pass',
                severity='Medium',
                issue_description=f'{param_count} URL parameter(s)',
                recommendation='Parameter count is acceptable',
                score=f'{param_count} parameter(s)'
            )
        else:
            return TestResult(
                test_id='url_parameters',
                test_name='URL Parameters',
                category='Technical SEO',
                status='Warning',
                severity='Medium',
                issue_description=f'Many URL parameters ({param_count})',
                recommendation='Consider reducing parameters or using URL rewriting',
                score=f'{param_count} parameter(s)'
            )
    
    def test_trailing_slash_consistency(self, url: str, soup: BeautifulSoup) -> TestResult:
        """Check trailing slash consistency"""
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        
        if not canonical:
            return None
        
        canonical_url = canonical.get('href', '')
        
        url_has_slash = url.rstrip('/') != url.rstrip('/')[:len(url.rstrip('/'))]
        canonical_has_slash = canonical_url.endswith('/')
        
        # Check if both match
        url_ends_with_slash = url.endswith('/')
        canonical_ends_with_slash = canonical_url.endswith('/')
        
        if url_ends_with_slash == canonical_ends_with_slash:
            return TestResult(
                test_id='trailing_slash_consistency',
                test_name='Trailing Slash Consistency',
                category='Technical SEO',
                status='Pass',
                severity='Low',
                issue_description='URL and canonical have consistent trailing slash usage',
                recommendation='Continue maintaining consistent URL structure',
                score='Consistent'
            )
        else:
            return TestResult(
                test_id='trailing_slash_consistency',
                test_name='Trailing Slash Consistency',
                category='Technical SEO',
                status='Warning',
                severity='Low',
                issue_description='Trailing slash inconsistency between URL and canonical',
                recommendation='Ensure consistent trailing slash usage to avoid duplicate content',
                score='Inconsistent'
            )
    
    def test_mixed_content_detection(self, url: str, soup: BeautifulSoup) -> TestResult:
        """Detect HTTP resources on HTTPS pages"""
        if not url.startswith('https://'):
            return None
        
        # Check for insecure resources
        insecure_resources = []
        
        # Check scripts
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            if script['src'].startswith('http://'):
                insecure_resources.append(f'script: {script["src"][:50]}')
        
        # Check stylesheets
        stylesheets = soup.find_all('link', rel='stylesheet', href=True)
        for style in stylesheets:
            if style['href'].startswith('http://'):
                insecure_resources.append(f'stylesheet: {style["href"][:50]}')
        
        # Check images
        images = soup.find_all('img', src=True)
        for img in images:
            if img['src'].startswith('http://'):
                insecure_resources.append(f'image: {img["src"][:50]}')
        
        # Check iframes
        iframes = soup.find_all('iframe', src=True)
        for iframe in iframes:
            if iframe['src'].startswith('http://'):
                insecure_resources.append(f'iframe: {iframe["src"][:50]}')
        
        if not insecure_resources:
            return TestResult(
                test_id='mixed_content_detection',
                test_name='Mixed Content Detection',
                category='Technical SEO',
                status='Pass',
                severity='High',
                issue_description='No mixed content detected',
                recommendation='All resources loaded securely over HTTPS',
                score='No mixed content'
            )
        else:
            return TestResult(
                test_id='mixed_content_detection',
                test_name='Mixed Content Detection',
                category='Technical SEO',
                status='Fail',
                severity='High',
                issue_description=f'{len(insecure_resources)} HTTP resources on HTTPS page',
                recommendation='Update all resources to use HTTPS to avoid security warnings',
                score=f'{len(insecure_resources)} insecure resources'
            )


# Example usage
if __name__ == '__main__':
    """
    Example of how to use these additional tests
    """
    import requests
    
    # Initialize test class
    tester = AdditionalSEOTests()
    
    # Fetch a page
    url = 'https://example.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Run tests
    results = []
    results.append(tester.test_twitter_card_tags(soup, url))
    results.append(tester.test_meta_refresh_redirect(soup, url))
    results.append(tester.test_duplicate_meta_tags(soup, url))
    results.append(tester.test_favicon_presence(soup, url))
    results.append(tester.test_empty_headers(soup, url))
    results.append(tester.test_header_level_gaps(soup, url))
    results.append(tester.test_image_dimensions_specified(soup, url))
    results.append(tester.test_modern_image_formats(soup, url))
    results.append(tester.test_responsive_images_srcset(soup, url))
    results.append(tester.test_nofollow_links_analysis(soup, url))
    results.append(tester.test_external_link_security(soup, url))
    results.append(tester.test_pagination_tags(soup, url))
    results.append(tester.test_link_density_ratio(soup, url))
    results.append(tester.test_url_parameters(url))
    results.append(tester.test_trailing_slash_consistency(url, soup))
    results.append(tester.test_mixed_content_detection(url, soup))
    
    # Filter out None results
    results = [r for r in results if r is not None]
    
    # Print results
    print(f"\n{'='*70}")
    print(f"SEO Test Results for: {url}")
    print(f"{'='*70}\n")
    
    for result in results:
        status_emoji = {
            'Pass': '✅',
            'Fail': '❌',
            'Warning': '⚠️',
            'Info': 'ℹ️'
        }.get(result.status, '•')
        
        print(f"{status_emoji} {result.test_name}")
        print(f"   Status: {result.status} | Category: {result.category}")
        print(f"   {result.issue_description}")
        print(f"   Score: {result.score}")
        print()
    
    # Summary
    pass_count = sum(1 for r in results if r.status == 'Pass')
    fail_count = sum(1 for r in results if r.status == 'Fail')
    warn_count = sum(1 for r in results if r.status == 'Warning')
    
    print(f"{'='*70}")
    print(f"Summary: {pass_count} passed, {fail_count} failed, {warn_count} warnings")
    print(f"{'='*70}")

