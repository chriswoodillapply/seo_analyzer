#!/usr/bin/env python3
"""
CrawlContext - Provides site-wide data for multi-page SEO tests
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from urllib.parse import urlparse


@dataclass
class LinkRelationship:
    """Represents a link from one page to another"""
    source_url: str
    target_url: str
    link_text: str
    is_internal: bool
    is_nofollow: bool = False


@dataclass
class PageMetadata:
    """Metadata about a page from the crawl"""
    url: str
    status_code: int
    title: Optional[str] = None
    h1_text: Optional[str] = None  # H1 tag content for uniqueness checking
    word_count: int = 0
    depth_from_home: int = 0
    internal_links_in: int = 0
    internal_links_out: int = 0
    external_links_out: int = 0
    is_indexable: bool = True
    content_hash: Optional[str] = None  # For detecting duplicate content
    

@dataclass
class CrawlContext:
    """
    Site-wide context for multi-page SEO analysis.
    
    This provides the data needed for tests that require:
    - Link graph analysis (orphan pages, link distribution)
    - Content comparison (boilerplate detection, duplicate content)
    - Site structure (page depth, navigation hierarchy)
    - Cross-page patterns
    """
    
    # Basic crawl info
    root_url: str
    total_pages: int = 0
    crawl_depth: int = 0
    
    # All pages discovered in crawl
    all_pages: Dict[str, PageMetadata] = field(default_factory=dict)
    
    # Link graph
    all_links: List[LinkRelationship] = field(default_factory=list)
    internal_links: Dict[str, List[str]] = field(default_factory=dict)  # url -> [urls it links to]
    inbound_links: Dict[str, List[str]] = field(default_factory=dict)   # url -> [urls that link to it]
    
    # Content analysis
    content_hashes: Dict[str, List[str]] = field(default_factory=dict)  # hash -> [urls with that hash]
    common_content_blocks: Dict[str, int] = field(default_factory=dict)  # content_snippet -> count
    
    # Site structure
    page_depths: Dict[str, int] = field(default_factory=dict)  # url -> depth from homepage
    orphan_pages: Set[str] = field(default_factory=set)
    
    def add_page(self, url: str, metadata: PageMetadata):
        """Add a page to the crawl context"""
        self.all_pages[url] = metadata
        self.total_pages = len(self.all_pages)
    
    def add_link(self, source: str, target: str, link_text: str = "", is_internal: bool = True):
        """Add a link relationship"""
        link = LinkRelationship(
            source_url=source,
            target_url=target,
            link_text=link_text,
            is_internal=is_internal
        )
        self.all_links.append(link)
        
        if is_internal:
            # Update internal links
            if source not in self.internal_links:
                self.internal_links[source] = []
            self.internal_links[source].append(target)
            
            # Update inbound links
            if target not in self.inbound_links:
                self.inbound_links[target] = []
            self.inbound_links[target].append(source)
    
    def calculate_page_depth(self):
        """Calculate depth of each page from homepage using BFS"""
        from collections import deque
        
        visited = {self.root_url: 0}
        queue = deque([(self.root_url, 0)])
        
        while queue:
            url, depth = queue.popleft()
            self.page_depths[url] = depth
            
            # Get all pages this URL links to
            for target in self.internal_links.get(url, []):
                if target not in visited:
                    visited[target] = depth + 1
                    queue.append((target, depth + 1))
    
    def find_orphan_pages(self):
        """Find pages with no inbound internal links (except homepage)"""
        self.orphan_pages = set()
        
        for url in self.all_pages.keys():
            if url == self.root_url:
                continue  # Homepage is not an orphan
            
            inbound = self.inbound_links.get(url, [])
            if len(inbound) == 0:
                self.orphan_pages.add(url)
    
    def get_page_depth(self, url: str) -> int:
        """Get depth of a page from homepage (0 = homepage)"""
        return self.page_depths.get(url, -1)
    
    def is_orphan_page(self, url: str) -> bool:
        """Check if a page is an orphan (no inbound links)"""
        return url in self.orphan_pages
    
    def get_inbound_link_count(self, url: str) -> int:
        """Get number of internal pages linking to this URL"""
        return len(self.inbound_links.get(url, []))
    
    def get_outbound_link_count(self, url: str) -> int:
        """Get number of internal pages this URL links to"""
        return len(self.internal_links.get(url, []))
    
    def get_similar_content_pages(self, content_hash: str) -> List[str]:
        """Get all pages with similar content (potential duplicates)"""
        return self.content_hashes.get(content_hash, [])
    
    def finalize(self):
        """
        Finalize the crawl context by calculating derived metrics.
        Call this after all pages have been added.
        """
        self.calculate_page_depth()
        self.find_orphan_pages()
        
        # Update page metadata with calculated values
        for url, metadata in self.all_pages.items():
            metadata.depth_from_home = self.get_page_depth(url)
            metadata.internal_links_in = self.get_inbound_link_count(url)
            metadata.internal_links_out = self.get_outbound_link_count(url)


def build_crawl_context_from_results(crawl_results: List[Dict]) -> CrawlContext:
    """
    Build a CrawlContext from crawl results.
    
    Args:
        crawl_results: List of crawl result dictionaries with url, links, content, etc.
    
    Returns:
        CrawlContext with all site-wide data populated
    """
    if not crawl_results:
        return None
    
    # Get root URL from first result
    root_url = crawl_results[0].get('url', '')
    context = CrawlContext(root_url=root_url)
    
    # First pass: add all pages
    for result in crawl_results:
        url = result.get('url')
        if not url:
            continue
        
        metadata = PageMetadata(
            url=url,
            status_code=result.get('status_code', 200),
            title=result.get('title'),
            word_count=result.get('word_count', 0),
            content_hash=result.get('content_hash')
        )
        context.add_page(url, metadata)
        
        # Track content hashes for duplicate detection
        if metadata.content_hash:
            if metadata.content_hash not in context.content_hashes:
                context.content_hashes[metadata.content_hash] = []
            context.content_hashes[metadata.content_hash].append(url)
    
    # Second pass: add all links
    for result in crawl_results:
        source_url = result.get('url')
        if not source_url:
            continue
        
        internal_links = result.get('internal_links', [])
        for target_url in internal_links:
            context.add_link(source_url, target_url, is_internal=True)
        
        external_links = result.get('external_links', [])
        for target_url in external_links:
            context.add_link(source_url, target_url, is_internal=False)
    
    # Finalize calculations
    context.finalize()
    
    return context

