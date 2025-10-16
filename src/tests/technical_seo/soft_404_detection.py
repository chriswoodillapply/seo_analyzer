#!/usr/bin/env python3
"""
Soft 404 Detection Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class Soft404DetectionTest(SEOTest):
    """Test for soft 404 detection"""
    
    @property
    def test_id(self) -> str:
        return "soft_404_detection"
    
    @property
    def test_name(self) -> str:
        return "Soft 404 Detection"
    
    @property
    def category(self) -> str:
        return TestCategory.TECHNICAL_SEO
    
    @property
    def severity(self) -> str:
        return TestSeverity.CRITICAL
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the soft 404 detection test"""
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
    
