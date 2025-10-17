#!/usr/bin/env python3
"""
Soft 404 Analyzer - Integrated with SEO Analyzer Framework

This test integrates with the existing SEO analyzer to provide comprehensive
soft 404 analysis using the same infrastructure.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.seo_orchestrator import SEOOrchestrator
from src.core.content_fetcher import ContentFetcher
from src.core.content_cache import ContentCache
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import json
from datetime import datetime
import re

@dataclass
class Soft404Result:
    """Results from soft 404 analysis"""
    url: str
    status: str  # 'failing' or 'passing'
    title: str
    meta_description: str
    h1_count: int
    h2_count: int
    content_length: int
    word_count: int
    internal_links: int
    external_links: int
    images: int
    videos: int
    forms: int
    canonical_url: str
    has_splash_screen: bool
    has_cookie_dialog: bool
    has_navigation: bool
    has_footer: bool
    content_blocks: int
    error_messages: List[str]
    response_time: float
    file_size: int
    status_code: int
    rendered_content_available: bool
    static_content_available: bool

class Soft404Analyzer:
    """Integrated soft 404 analyzer using existing SEO framework"""
    
    def __init__(self):
        self.orchestrator = SEOOrchestrator()
        self.content_fetcher = ContentFetcher()
        self.content_cache = ContentCache()
        
        # Test URLs
        self.failing_urls = [
            'https://www.applydigital.com/',
            'https://www.applydigital.com/insights/learn/optimizing-for-ai-search/',
            'https://www.applydigital.com/insights/learn/composable-commerce-driving-modern-business/',
            'https://www.applydigital.com/reign/',
            'https://www.applydigital.com/leadership/'
        ]
        
        self.passing_urls = [
            'https://www.applydigital.com/leadership/dom-selvon/',
            'https://www.applydigital.com/ai-solutions-playbook/',
            'https://www.applydigital.com/insights/learn/advantages-of-using-markup-in-jamstack/',
            'https://www.applydigital.com/insights/learn/personalization-at-the-heart-of-experience-driven-commerce-actionable-insights-from-bigsummit/',
            'https://www.applydigital.com/insights/learn/boost-your-content-with-contentful/'
        ]

    def analyze_content_structure(self, soup) -> Dict:
        """Analyze content structure using BeautifulSoup"""
        from bs4 import BeautifulSoup
        
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, 'html.parser')
        
        analysis = {
            'h1_count': len(soup.find_all('h1')),
            'h2_count': len(soup.find_all('h2')),
            'content_blocks': len(soup.find_all(['section', 'article', 'div'], class_=re.compile(r'content|main|body'))),
            'has_splash_screen': bool(soup.find('div', class_=re.compile(r'splash', re.I))),
            'has_cookie_dialog': bool(soup.find('dialog', {'data-testid': 'cookie-consent'}) or 
                                    soup.find('div', class_=re.compile(r'cookie', re.I))),
            'has_navigation': bool(soup.find('nav') or soup.find('header')),
            'has_footer': bool(soup.find('footer')),
            'images': len(soup.find_all('img')),
            'videos': len(soup.find_all(['video', 'iframe'])),
            'forms': len(soup.find_all('form'))
        }
        return analysis

    def extract_seo_elements(self, soup) -> Dict:
        """Extract SEO-specific elements"""
        from bs4 import BeautifulSoup
        
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, 'html.parser')
        
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ''
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc_text = meta_desc.get('content', '') if meta_desc else ''
        
        canonical = soup.find('link', rel='canonical')
        canonical_url = canonical.get('href', '') if canonical else ''
        
        return {
            'title': title_text,
            'meta_description': meta_desc_text,
            'canonical_url': canonical_url
        }

    def detect_error_messages(self, soup) -> List[str]:
        """Detect common error messages in content"""
        from bs4 import BeautifulSoup
        
        if isinstance(soup, str):
            soup = BeautifulSoup(soup, 'html.parser')
        
        error_patterns = [
            r'not found', r'error', r'404', r'page not found',
            r'component unknown', r'failed to load', r'timeout',
            r'service unavailable', r'503', r'500'
        ]
        
        text_content = soup.get_text().lower()
        found_errors = []
        
        for pattern in error_patterns:
            if re.search(pattern, text_content):
                found_errors.append(pattern)
                
        return found_errors

    def analyze_page(self, url: str, status: str) -> Optional[Soft404Result]:
        """Analyze a single page using the SEO framework"""
        print(f"Analyzing {status} page: {url}")
        
        try:
            # Use the existing content fetcher
            page_content = self.content_fetcher.fetch_complete(url)
            
            if not page_content:
                print(f"Failed to fetch content for {url}")
                return None
            
            # Use rendered content if available, otherwise static
            content_to_analyze = page_content.rendered_soup or page_content.static_soup
            
            if not content_to_analyze:
                print(f"No content available for {url}")
                return None
            
            # Analyze content structure
            structure = self.analyze_content_structure(content_to_analyze)
            
            # Extract SEO elements
            seo_elements = self.extract_seo_elements(content_to_analyze)
            
            # Get text content for word count
            text_content = content_to_analyze.get_text() if hasattr(content_to_analyze, 'get_text') else str(content_to_analyze)
            word_count = len(text_content.split())
            
            # Extract links using existing method
            internal_links, external_links = self.orchestrator._extract_links_from_content(page_content)
            
            # Detect error messages
            error_messages = self.detect_error_messages(content_to_analyze)
            
            # Get content length
            content_length = len(str(content_to_analyze))
            
            return Soft404Result(
                url=url,
                status=status,
                title=seo_elements['title'],
                meta_description=seo_elements['meta_description'],
                h1_count=structure['h1_count'],
                h2_count=structure['h2_count'],
                content_length=content_length,
                word_count=word_count,
                internal_links=len(internal_links),
                external_links=len(external_links),
                images=structure['images'],
                videos=structure['videos'],
                forms=structure['forms'],
                canonical_url=seo_elements['canonical_url'],
                has_splash_screen=structure['has_splash_screen'],
                has_cookie_dialog=structure['has_cookie_dialog'],
                has_navigation=structure['has_navigation'],
                has_footer=structure['has_footer'],
                content_blocks=structure['content_blocks'],
                error_messages=error_messages,
                response_time=0.0,  # Would need to measure this
                file_size=content_length,
                status_code=200,  # Would need to get from response
                rendered_content_available=bool(page_content.rendered_soup),
                static_content_available=bool(page_content.static_soup)
            )
            
        except Exception as e:
            print(f"Error analyzing {url}: {e}")
            return None

    def run_analysis(self) -> List[Soft404Result]:
        """Run analysis on all URLs"""
        results = []
        
        # Analyze failing pages
        for url in self.failing_urls:
            result = self.analyze_page(url, 'failing')
            if result:
                results.append(result)
        
        # Analyze passing pages
        for url in self.passing_urls:
            result = self.analyze_page(url, 'passing')
            if result:
                results.append(result)
                
        return results

    def generate_comparison_report(self, results: List[Soft404Result]) -> str:
        """Generate detailed comparison report"""
        failing_pages = [r for r in results if r.status == 'failing']
        passing_pages = [r for r in results if r.status == 'passing']
        
        report = f"""
# Soft 404 Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
Analyzed {len(failing_pages)} failing pages vs {len(passing_pages)} passing pages.

## Key Metrics Comparison

### Content Depth
"""
        
        # Calculate averages
        metrics = [
            ('Content Length (bytes)', 'content_length'),
            ('Word Count', 'word_count'),
            ('H1 Tags', 'h1_count'),
            ('H2 Tags', 'h2_count'),
            ('Content Blocks', 'content_blocks'),
            ('Internal Links', 'internal_links'),
            ('External Links', 'external_links'),
            ('Images', 'images'),
            ('Videos', 'videos'),
            ('Forms', 'forms')
        ]
        
        for metric_name, metric_attr in metrics:
            failing_avg = sum(getattr(p, metric_attr) for p in failing_pages) / len(failing_pages)
            passing_avg = sum(getattr(p, metric_attr) for p in passing_pages) / len(passing_pages)
            difference = ((passing_avg - failing_avg) / failing_avg * 100) if failing_avg > 0 else 0
            
            report += f"""
**{metric_name}:**
- Failing pages: {failing_avg:.1f}
- Passing pages: {passing_avg:.1f}
- Difference: {difference:+.1f}%
"""
        
        # Technical issues
        report += "\n### Technical Issues\n"
        
        # Splash screen
        failing_splash = sum(1 for p in failing_pages if p.has_splash_screen)
        passing_splash = sum(1 for p in passing_pages if p.has_splash_screen)
        
        report += f"""
**Splash Screen:**
- Failing pages: {failing_splash}/{len(failing_pages)} ({failing_splash/len(failing_pages)*100:.1f}%)
- Passing pages: {passing_splash}/{len(passing_pages)} ({passing_splash/len(passing_pages)*100:.1f}%)
"""
        
        # Cookie dialog
        failing_cookie = sum(1 for p in failing_pages if p.has_cookie_dialog)
        passing_cookie = sum(1 for p in passing_pages if p.has_cookie_dialog)
        
        report += f"""
**Cookie Dialog:**
- Failing pages: {failing_cookie}/{len(failing_pages)} ({failing_cookie/len(failing_pages)*100:.1f}%)
- Passing pages: {passing_cookie}/{len(passing_pages)} ({passing_cookie/len(passing_pages)*100:.1f}%)
"""
        
        # Content availability
        failing_rendered = sum(1 for p in failing_pages if p.rendered_content_available)
        passing_rendered = sum(1 for p in passing_pages if p.rendered_content_available)
        
        report += f"""
**Rendered Content Available:**
- Failing pages: {failing_rendered}/{len(failing_pages)} ({failing_rendered/len(failing_pages)*100:.1f}%)
- Passing pages: {passing_rendered}/{len(passing_pages)} ({passing_rendered/len(passing_pages)*100:.1f}%)
"""
        
        # Error messages
        failing_errors = sum(len(p.error_messages) for p in failing_pages)
        passing_errors = sum(len(p.error_messages) for p in passing_pages)
        
        report += f"""
**Error Messages:**
- Failing pages total: {failing_errors}
- Passing pages total: {passing_errors}
"""
        
        # Detailed analysis
        report += "\n## Detailed Page Analysis\n"
        
        for page in results:
            report += f"""
### {page.status.upper()}: {page.url}
- Title: {page.title[:100]}{'...' if len(page.title) > 100 else ''}
- Content Length: {page.content_length:,} bytes
- Word Count: {page.word_count:,} words
- H1/H2 Tags: {page.h1_count}/{page.h2_count}
- Links: {page.internal_links} internal, {page.external_links} external
- Media: {page.images} images, {page.videos} videos, {page.forms} forms
- Structure: {page.content_blocks} content blocks
- Technical: Splash={page.has_splash_screen}, Cookie={page.has_cookie_dialog}
- Content: Rendered={page.rendered_content_available}, Static={page.static_content_available}
- Errors: {', '.join(page.error_messages) if page.error_messages else 'None'}
"""
        
        # Recommendations
        report += """
## Key Findings & Recommendations

### Critical Differences:
1. **Content Depth**: Passing pages have more substantial content
2. **Technical Issues**: Address splash screens and cookie dialogs
3. **Content Availability**: Ensure rendered content is accessible
4. **Error Handling**: Fix any error messages or broken elements

### Action Items:
1. Fix technical issues blocking crawlers
2. Improve content depth on failing pages
3. Ensure proper content rendering
4. Test with Google Search Console
"""
        
        return report

    def save_results(self, results: List[Soft404Result], report: str):
        """Save results to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save raw data
        with open(f'soft_404_analysis_{timestamp}.json', 'w') as f:
            json.dump([r.__dict__ for r in results], f, indent=2)
        
        # Save report
        with open(f'soft_404_report_{timestamp}.md', 'w') as f:
            f.write(report)
        
        print(f"Results saved to soft_404_analysis_{timestamp}.json")
        print(f"Report saved to soft_404_report_{timestamp}.md")

def main():
    """Main execution function"""
    print("Starting Integrated Soft 404 Analysis...")
    print("=" * 50)
    
    analyzer = Soft404Analyzer()
    results = analyzer.run_analysis()
    
    if results:
        report = analyzer.generate_comparison_report(results)
        analyzer.save_results(results, report)
        
        print("\nAnalysis Complete!")
        print("=" * 50)
        print(report)
    else:
        print("No results to analyze.")

if __name__ == "__main__":
    main()
