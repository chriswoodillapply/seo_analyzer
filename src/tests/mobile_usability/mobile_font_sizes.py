#!/usr/bin/env python3
"""
Mobile Font Sizes Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class MobileFontSizesTest(SEOTest):
    """Test for mobile font sizes"""
    
    @property
    def test_id(self) -> str:
        return "mobile_font_sizes"
    
    @property
    def test_name(self) -> str:
        return "Mobile Font Sizes"
    
    @property
    def category(self) -> str:
        return TestCategory.MOBILE_USABILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the mobile font sizes test"""
        if not content.rendered_soup:
            return [TestResult(
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
        
        # Analyze CSS files for mobile font sizes
        mobile_font_issues = []
        total_css_files = 0
        analyzed_css_files = 0
        
        # Check if CSS files are available
        if not content.css_files:
            return [TestResult(
                url=content.url,
                test_id='mobile_font_sizes',
                test_name='Mobile Font Sizes',
                category='Mobile Usability',
                status=TestStatus.INFO,
                severity='Medium',
                issue_description='No CSS files available for analysis',
                recommendation='CSS files not fetched - enable CSS extraction',
                score='No CSS data'
            )
        
        total_css_files = len(content.css_files)
        
        # Analyze each CSS file
        for css_url, css_content in content.css_files.items():
            analyzed_css_files += 1
            issues = self._analyze_css_for_mobile_fonts(css_content, css_url)
            mobile_font_issues.extend(issues)
        
        # Determine test result based on findings
        if not mobile_font_issues:
            status = TestStatus.PASS
            issue = f'Mobile font sizes are adequate (analyzed {analyzed_css_files}/{total_css_files} CSS files)'
            recommendation = 'Mobile font sizes meet accessibility standards'
            score = 'Good'
        else:
            status = TestStatus.WARNING
            issue = f'Found {len(mobile_font_issues)} mobile font size issues in {analyzed_css_files} CSS files'
            recommendation = 'Increase font sizes to minimum 16px for mobile readability'
            score = f'{len(mobile_font_issues)} issues found'
        
        return [TestResult(
            url=content.url,
            test_id='mobile_font_sizes',
            test_name='Mobile Font Sizes',
            category='Mobile Usability',
            status=status,
            severity='Medium',
            issue_description=issue,
            recommendation=recommendation,
            score=score
        )
    
    def _analyze_css_for_mobile_fonts(self, css_content: str, css_url: str) -> list:
        """Analyze CSS content for mobile font size issues"""
        import re
        
        issues = []
        
        # Find all font-size declarations
        font_size_pattern = r'font-size\s*:\s*([^;]+)'
        font_size_matches = re.findall(font_size_pattern, css_content, re.IGNORECASE)
        
        for match in font_size_matches:
            font_size = match.strip()
            
            # Parse font size value
            size_value = self._parse_font_size(font_size)
            if size_value is None:
                continue
            
            # Check if it's too small for mobile (less than 16px)
            if size_value < 16:
                # Check if it's in a mobile media query
                is_mobile_context = self._is_mobile_context(css_content, font_size)
                
                if is_mobile_context:
                    issues.append({
                        'font_size': font_size,
                        'value_px': size_value,
                        'css_url': css_url,
                        'context': 'mobile'
                    })
        
        return issues
    
    def _parse_font_size(self, font_size: str) -> Optional[float]:
        """Parse font size value to pixels"""
        import re
        
        # Remove any calc() or other functions for now
        font_size = re.sub(r'calc\([^)]+\)', '', font_size)
        
        # Match pixel values
        px_match = re.search(r'(\d+(?:\.\d+)?)\s*px', font_size)
        if px_match:
            return float(px_match.group(1))
        
        # Match em values (assume 16px base)
        em_match = re.search(r'(\d+(?:\.\d+)?)\s*em', font_size)
        if em_match:
            return float(em_match.group(1)) * 16
        
        # Match rem values (assume 16px base)
        rem_match = re.search(r'(\d+(?:\.\d+)?)\s*rem', font_size)
        if rem_match:
            return float(rem_match.group(1)) * 16
        
        return []
    
    def _is_mobile_context(self, css_content: str, font_size: str) -> bool:
        """Check if font size is in a mobile media query context"""
        import re
        
        # Find the context around the font-size declaration
        font_size_index = css_content.find(font_size)
        if font_size_index == -1:
            return False
        
        # Look backwards for media queries
        context_start = max(0, font_size_index - 1000)
        context = css_content[context_start:font_size_index]
        
        # Check for mobile media queries
        mobile_queries = [
            r'@media\s+.*max-width\s*:\s*(\d+)px',
            r'@media\s+.*max-width\s*:\s*(\d+)em',
            r'@media\s+.*max-width\s*:\s*(\d+)rem',
            r'@media\s+.*max-width\s*:\s*(\d+)vw',
            r'@media\s+.*max-width\s*:\s*(\d+)vh'
        ]
        
        for query_pattern in mobile_queries:
            matches = re.findall(query_pattern, context, re.IGNORECASE)
            for match in matches:
                try:
                    value = float(match)
                    # Consider mobile if max-width is less than 768px
                    if value < 768:
                        return True
                except ValueError:
                    continue
        
        return False
    
    # =========================================================================
    # SECURITY TESTS
    # =========================================================================
    
