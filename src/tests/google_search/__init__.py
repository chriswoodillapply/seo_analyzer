#!/usr/bin/env python3
"""
Google Search Tests Package

This package contains tests specifically designed to analyze Google Search
performance and identify soft 404 issues using Google Search Console API
and Playwright-based analysis.
"""

from .gs001_googlebot_render_visibility import GooglebotRenderVisibilityTest
from .gs002_console_network_errors import ConsoleNetworkErrorsTest
from .gs003_static_vs_rendered_content import StaticVsRenderedContentTest
from .gs004_overlay_blocking import OverlayBlockingTest
from .gs005_canonical_alignment_inspection import CanonicalAlignmentInspectionTest
from .gs006_sitemap_coverage_check import SitemapCoverageCheckTest
from .gs007_duplicate_variant_detection import DuplicateVariantDetectionTest
from .gs008_redirect_chain_integrity import RedirectChainIntegrityTest
from .gs009_ssr_nojs_fallback import SSRNoscriptFallbackTest
from .gs010_thin_content_heuristic import ThinContentHeuristicTest
from .gs011_hreflang_canonical_consistency import HreflangCanonicalConsistencyTest
from .gs012_internal_linking_strength import InternalLinkingStrengthTest
from .gs013_render_timing_metrics import RenderTimingMetricsTest
from .gs014_robots_meta_headers import RobotsMetaHeadersTest

__all__ = [
    'GooglebotRenderVisibilityTest',
    'ConsoleNetworkErrorsTest', 
    'StaticVsRenderedContentTest',
    'OverlayBlockingTest',
    'CanonicalAlignmentInspectionTest',
    'SitemapCoverageCheckTest',
    'DuplicateVariantDetectionTest',
    'RedirectChainIntegrityTest',
    'SSRNoscriptFallbackTest',
    'ThinContentHeuristicTest',
    'HreflangCanonicalConsistencyTest',
    'InternalLinkingStrengthTest',
    'RenderTimingMetricsTest',
    'RobotsMetaHeadersTest'
]
