#!/usr/bin/env python3
"""
Implement the site-wide tests that require CrawlContext
"""

from pathlib import Path

# Test 1: Orphan Page Check
orphan_test = '''#!/usr/bin/env python3
"""
Orphan Page Check Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class OrphanPageCheckTest(SEOTest):
    """Test for orphan pages - pages with no inbound internal links"""
    
    @property
    def test_id(self) -> str:
        return "orphan_page_check"
    
    @property
    def test_name(self) -> str:
        return "Orphan Page Check"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    @property
    def requires_site_context(self) -> bool:
        return True
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the orphan page check test"""
        
        # If no crawl context, return INFO
        if not crawl_context:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='Requires site-wide crawl to detect orphan pages',
                recommendation='Run with --crawl to enable site-wide analysis',
                score='Crawl required'
            )
        
        # Check if this page is an orphan
        is_orphan = crawl_context.is_orphan_page(content.url)
        inbound_count = crawl_context.get_inbound_link_count(content.url)
        
        if is_orphan and content.url != crawl_context.root_url:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.FAIL,
                severity=self.severity,
                issue_description=f'Orphan page detected: No internal links pointing to this page',
                recommendation='Add internal links from other pages to improve discoverability and crawlability',
                score=f'{inbound_count} inbound links'
            )
        else:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.PASS,
                severity=self.severity,
                issue_description=f'Page has {inbound_count} inbound internal link(s)',
                recommendation='Continue maintaining internal link structure',
                score=f'{inbound_count} inbound links'
            )
'''

# Test 2: Page Depth / Navigation Depth
navigation_depth_test = '''#!/usr/bin/env python3
"""
Navigation Depth Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class NavigationDepthTest(SEOTest):
    """Test for page depth from homepage"""
    
    @property
    def test_id(self) -> str:
        return "navigation_depth"
    
    @property
    def test_name(self) -> str:
        return "Page Navigation Depth"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.MEDIUM
    
    @property
    def requires_site_context(self) -> bool:
        return True
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the navigation depth test"""
        
        # If no crawl context, return INFO
        if not crawl_context:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='Requires site crawl to calculate depth from homepage',
                recommendation='Run with --crawl to enable depth analysis',
                score='Crawl required'
            )
        
        # Get page depth
        depth = crawl_context.get_page_depth(content.url)
        
        if depth == -1:
            # Page not reachable from homepage
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.FAIL,
                severity=self.severity,
                issue_description='Page is not reachable from homepage',
                recommendation='Add navigation path from homepage',
                score='Unreachable'
            )
        elif depth <= 3:
            # Good depth (0-3 clicks from homepage)
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.PASS,
                severity=self.severity,
                issue_description=f'Page is {depth} click(s) from homepage',
                recommendation='Good navigation depth for SEO',
                score=f'Depth: {depth}'
            )
        elif depth <= 5:
            # Warning (4-5 clicks)
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.WARNING,
                severity=self.severity,
                issue_description=f'Page is {depth} clicks from homepage (somewhat deep)',
                recommendation='Consider adding shortcuts or improving navigation structure',
                score=f'Depth: {depth}'
            )
        else:
            # Fail (6+ clicks)
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.FAIL,
                severity=self.severity,
                issue_description=f'Page is {depth} clicks from homepage (too deep)',
                recommendation='Improve site architecture to reduce click depth to 3 or fewer',
                score=f'Depth: {depth}'
            )
'''

# Test 3: Deep Link Ratio
deep_link_ratio_test = '''#!/usr/bin/env python3
"""
Deep Link Ratio Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class DeepLinkRatioTest(SEOTest):
    """Test for distribution of internal links to deep pages"""
    
    @property
    def test_id(self) -> str:
        return "deep_link_ratio"
    
    @property
    def test_name(self) -> str:
        return "Deep Link Distribution"
    
    @property
    def category(self) -> str:
        return TestCategory.LINKS
    
    @property
    def severity(self) -> str:
        return TestSeverity.LOW
    
    @property
    def requires_site_context(self) -> bool:
        return True
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the deep link ratio test"""
        
        # If no crawl context, return INFO
        if not crawl_context:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.INFO,
                severity=self.severity,
                issue_description='Requires site-wide analysis for link distribution',
                recommendation='Run with --crawl to analyze link patterns',
                score='Crawl required'
            )
        
        # Get outbound link count
        outbound_count = crawl_context.get_outbound_link_count(content.url)
        
        if outbound_count == 0:
            return TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.WARNING,
                severity=self.severity,
                issue_description='Page has no outbound internal links',
                recommendation='Add relevant internal links to improve site navigation and link equity distribution',
                score='0 outbound links'
            )
        
        # Count deep links (pages at depth 3+)
        deep_links = 0
        for target_url in crawl_context.internal_links.get(content.url, []):
            target_depth = crawl_context.get_page_depth(target_url)
            if target_depth >= 3:
                deep_links += 1
        
        deep_ratio = (deep_links / outbound_count * 100) if outbound_count > 0 else 0
        
        if deep_ratio >= 30:
            status = TestStatus.PASS
            issue = f'Good deep link distribution: {deep_ratio:.1f}% of links go to deeper pages'
            recommendation = 'Continue linking to deep content'
        elif deep_ratio >= 15:
            status = TestStatus.WARNING
            issue = f'Moderate deep link distribution: {deep_ratio:.1f}% of links go to deeper pages'
            recommendation = 'Consider adding more links to deep content pages'
        else:
            status = TestStatus.INFO
            issue = f'Low deep link distribution: {deep_ratio:.1f}% of links go to deeper pages'
            recommendation = 'Add more links to deep pages to improve discoverability'
        
        return TestResult(
            url=content.url,
            test_id=self.test_id,
            test_name=self.test_name,
            category=self.category,
            status=status,
            severity=self.severity,
            issue_description=issue,
            recommendation=recommendation,
            score=f'{deep_links}/{outbound_count} deep links ({deep_ratio:.1f}%)'
        )
'''

# Test 4: Thin Content Detection (site-wide version)
thin_content_test = '''#!/usr/bin/env python3
"""
Thin Content Detection Test
"""

from typing import Optional, TYPE_CHECKING
from src.core.test_interface import SEOTest, TestResult, TestStatus, PageContent, TestCategory, TestSeverity

if TYPE_CHECKING:
    from src.core.crawl_context import CrawlContext


class ThinContentDetectionTest(SEOTest):
    """Test for thin/boilerplate content detection"""
    
    @property
    def test_id(self) -> str:
        return "thin_content_detection"
    
    @property
    def test_name(self) -> str:
        return "Thin Content Detection"
    
    @property
    def category(self) -> str:
        return TestCategory.CONTENT
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    @property
    def requires_site_context(self) -> bool:
        return True
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Execute the thin content detection test"""
        
        # Basic word count check (works without crawl context)
        soup = content.rendered_soup or content.static_soup
        text = soup.get_text()
        words = len([w for w in text.split() if len(w) > 2])
        
        # If no crawl context, do basic check only
        if not crawl_context:
            if words < 300:
                return TestResult(
                    url=content.url,
                    test_id=self.test_id,
                    test_name=self.test_name,
                    category=self.category,
                    status=TestStatus.WARNING,
                    severity=self.severity,
                    issue_description=f'Thin content: {words} words (site-wide analysis requires crawl)',
                    recommendation='Aim for 300+ unique words. Run with --crawl for duplicate detection',
                    score=f'{words} words'
                )
            else:
                return TestResult(
                    url=content.url,
                    test_id=self.test_id,
                    test_name=self.test_name,
                    category=self.category,
                    status=TestStatus.PASS,
                    severity=self.severity,
                    issue_description=f'Sufficient content: {words} words',
                    recommendation='Continue providing valuable content',
                    score=f'{words} words'
                )
        
        # With crawl context, check for duplicate/boilerplate content
        # This is a simplified version - could use content hashing for better detection
        similar_pages = []
        if crawl_context.content_hashes:
            # Find pages with similar word counts (±50 words) as a proxy for duplicates
            for url, metadata in crawl_context.all_pages.items():
                if url != content.url and abs(metadata.word_count - words) < 50:
                    similar_pages.append(url)
        
        duplicate_count = len(similar_pages)
        
        if words < 200:
            status = TestStatus.FAIL
            issue = f'Very thin content: {words} words'
            recommendation = 'Add substantial unique content (aim for 500+ words)'
        elif words < 300:
            status = TestStatus.WARNING
            issue = f'Thin content: {words} words'
            recommendation = 'Expand content to 300+ words with unique value'
        elif duplicate_count > 5:
            status = TestStatus.WARNING
            issue = f'Potential duplicate content: {duplicate_count} similar pages found'
            recommendation = 'Ensure each page has unique, valuable content'
        else:
            status = TestStatus.PASS
            issue = f'Good content length: {words} words'
            recommendation = 'Continue providing substantial unique content'
        
        return TestResult(
            url=content.url,
            test_id=self.test_id,
            test_name=self.test_name,
            category=self.category,
            status=status,
            severity=self.severity,
            issue_description=issue,
            recommendation=recommendation,
            score=f'{words} words, {duplicate_count} similar pages'
        )
'''

# Test 5 & 6: Touch Target Sizes and Color Contrast (require browser rendering with computed styles)
# These remain as stubs since they need browser API access beyond what we have

print('='*80)
print('  IMPLEMENTING SITE-WIDE TESTS')
print('='*80)

tests_to_write = [
    ('src/tests/links/orphan_page_check.py', orphan_test),
    ('src/tests/links/navigation_depth.py', navigation_depth_test),
    ('src/tests/links/deep_link_ratio.py', deep_link_ratio_test),
    ('src/tests/content/thin_content_detection.py', thin_content_test),
]

for file_path, content in tests_to_write:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'[OK] Implemented {Path(file_path).name}')

print('\n' + '='*80)
print('  DONE: 4 site-wide tests implemented')
print('='*80)
print('\nRemaining stubs (require browser computed styles):')
print('  - touch_target_sizes.py (needs element.getBoundingClientRect())')
print('  - color_contrast_check.py (needs getComputedStyle())')
print('='*80 + '\n')

