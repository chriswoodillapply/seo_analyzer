#!/usr/bin/env python3
"""
GS010: Thin Content Heuristic Test

Detects thin content using word count, headings ratio, and template-only
detection to identify pages that may be flagged as soft 404s.
"""

from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent
from typing import Optional, List
import re


class ThinContentHeuristicTest(SEOTest):
    """Test to detect thin content using heuristics"""
    
    @property
    def test_id(self) -> str:
        return "GS010"
    
    @property
    def test_name(self) -> str:
        return "Thin Content Heuristic"
    
    @property
    def category(self) -> str:
        return "Google Search"
    
    @property
    def severity(self) -> str:
        return "High"
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the thin content heuristic test"""
        results = []
        
        # Check word count
        word_count_result = self._check_word_count(content)
        results.append(word_count_result)
        
        # Check headings ratio
        headings_result = self._check_headings_ratio(content)
        results.append(headings_result)
        
        # Check for template-only content
        template_result = self._check_template_only_content(content)
        results.append(template_result)
        
        # Check content density
        density_result = self._check_content_density(content)
        results.append(density_result)
        
        return results
    
    def _check_word_count(self, content: PageContent) -> TestResult:
        """Check word count for thin content"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Extract main content
        main_content = self._extract_main_content(soup)
        word_count = len(main_content.split())
        
        # Remove common template words
        template_words = ['home', 'about', 'contact', 'services', 'products', 'login', 'register', 'search', 'menu', 'navigation']
        content_words = [word.lower() for word in main_content.split()]
        unique_words = len(set(content_words))
        
        if word_count < 100:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Content is very thin ({word_count} words)",
                "Add substantial content to avoid soft 404 classification",
                "0/100"
            )
        
        if word_count < 300:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Content may be thin ({word_count} words)",
                "Consider adding more substantial content",
                "60/100"
            )
        
        if unique_words < 50:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Low vocabulary diversity ({unique_words} unique words)",
                "Add more varied content to improve quality",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Content has adequate word count ({word_count} words, {unique_words} unique)",
            "Content length is sufficient",
            "100/100"
        )
    
    def _check_headings_ratio(self, content: PageContent) -> TestResult:
        """Check headings to content ratio"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Count headings
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        h4_tags = soup.find_all('h4')
        h5_tags = soup.find_all('h5')
        h6_tags = soup.find_all('h6')
        
        total_headings = len(h1_tags) + len(h2_tags) + len(h3_tags) + len(h4_tags) + len(h5_tags) + len(h6_tags)
        
        # Count paragraphs
        p_tags = soup.find_all('p')
        paragraph_count = len(p_tags)
        
        if total_headings == 0:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "No headings found",
                "Add heading structure to organize content",
                "0/100"
            )
        
        if paragraph_count == 0:
            return self._create_result(
                content,
                TestStatus.FAIL,
                "No paragraphs found",
                "Add paragraph content to provide substance",
                "0/100"
            )
        
        # Calculate ratio
        if paragraph_count > 0:
            heading_ratio = total_headings / paragraph_count
        else:
            heading_ratio = float('inf')
        
        if heading_ratio > 0.5:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"High heading to paragraph ratio ({heading_ratio:.2f})",
                "Add more paragraph content to balance headings",
                "60/100"
            )
        
        if total_headings > 20:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Too many headings ({total_headings})",
                "Consolidate headings to improve content structure",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Good heading structure ({total_headings} headings, {paragraph_count} paragraphs)",
            "Content has proper heading hierarchy",
            "100/100"
        )
    
    def _check_template_only_content(self, content: PageContent) -> TestResult:
        """Check for template-only content"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Extract all text content
        all_text = soup.get_text().strip()
        words = all_text.split()
        
        # Check for common template patterns
        template_patterns = [
            r'lorem ipsum',
            r'placeholder',
            r'sample text',
            r'coming soon',
            r'under construction',
            r'page not found',
            r'error 404',
            r'no content',
            r'empty page'
        ]
        
        template_matches = []
        for pattern in template_patterns:
            if re.search(pattern, all_text, re.IGNORECASE):
                template_matches.append(pattern)
        
        if template_matches:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Template content detected: {', '.join(template_matches)}",
                "Replace template content with actual content",
                "0/100"
            )
        
        # Check for navigation-only content
        nav_elements = soup.find_all(['nav', 'header', 'footer'])
        nav_text = ""
        for nav in nav_elements:
            nav_text += nav.get_text().strip() + " "
        
        nav_word_count = len(nav_text.split())
        total_word_count = len(words)
        
        if nav_word_count > total_word_count * 0.8:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Content appears to be mostly navigation ({nav_word_count}/{total_word_count} words)",
                "Add substantial main content beyond navigation",
                "40/100"
            )
        
        # Check for very short content
        if total_word_count < 50:
            return self._create_result(
                content,
                TestStatus.FAIL,
                f"Content is too short ({total_word_count} words)",
                "Add substantial content to avoid thin content classification",
                "0/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"No template content detected ({total_word_count} words)",
            "Content appears to be substantial and original",
            "100/100"
        )
    
    def _check_content_density(self, content: PageContent) -> TestResult:
        """Check content density and quality"""
        soup = content.rendered_soup or content.static_soup
        if not soup:
            return self._create_result(
                content,
                TestStatus.ERROR,
                "No content available for analysis",
                "Ensure page content is properly fetched",
                "0/100"
            )
        
        # Extract main content
        main_content = self._extract_main_content(soup)
        word_count = len(main_content.split())
        
        # Count different content types
        images = len(soup.find_all('img'))
        links = len(soup.find_all('a'))
        lists = len(soup.find_all(['ul', 'ol']))
        tables = len(soup.find_all('table'))
        
        # Calculate content diversity score
        diversity_score = 0
        if images > 0:
            diversity_score += 1
        if links > 5:
            diversity_score += 1
        if lists > 0:
            diversity_score += 1
        if tables > 0:
            diversity_score += 1
        
        if diversity_score < 2 and word_count < 500:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Low content diversity (score: {diversity_score})",
                "Add images, links, lists, or tables to improve content richness",
                "60/100"
            )
        
        if word_count < 200:
            return self._create_result(
                content,
                TestStatus.WARNING,
                f"Content may be insufficient ({word_count} words)",
                "Add more substantial content",
                "70/100"
            )
        
        return self._create_result(
            content,
            TestStatus.PASS,
            f"Good content density ({word_count} words, diversity score: {diversity_score})",
            "Content has adequate substance and diversity",
            "100/100"
        )
    
    def _extract_main_content(self, soup) -> str:
        """Extract main content from soup"""
        # Try to find main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'main|content'))
        
        if main_content:
            return main_content.get_text().strip()
        
        # Fallback to body content
        body = soup.find('body')
        if body:
            return body.get_text().strip()
        
        return soup.get_text().strip()
