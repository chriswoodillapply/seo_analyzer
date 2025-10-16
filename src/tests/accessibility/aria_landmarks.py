#!/usr/bin/env python3
"""
ARIA Landmarks Test
"""

from typing import Optional, List, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class AriaLandmarksTest(SEOTest):
    """Test for aria landmarks"""
    
    @property
    def test_id(self) -> str:
        return "aria_landmarks"
    
    @property
    def test_name(self) -> str:
        return "ARIA Landmarks"
    
    @property
    def category(self) -> str:
        return TestCategory.ACCESSIBILITY
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """Execute the aria landmarks test"""
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
            return [TestResult(
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
            return [TestResult(
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
            return [TestResult(
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
    
