# Google Search Category Tests (GS001-GS014)

This document describes the comprehensive Google Search category tests implemented to identify and analyze soft 404 issues.

## Overview

The Google Search category contains 14 specialized tests designed to detect the root causes of soft 404 errors by analyzing how Googlebot sees and processes web pages.

## Test Categories

### Core Googlebot Analysis
- **GS001: Googlebot Render Visibility** - Verifies main content visibility to Googlebot
- **GS002: Console Network Errors** - Captures console warnings/errors and network failures
- **GS003: Static vs Rendered Content** - Compares static HTML vs rendered DOM
- **GS004: Overlay Blocking** - Detects blocking cookie dialogs and splash screens

### Google Search Console Integration
- **GS005: Canonical Alignment Inspection** - User-declared vs Google-selected canonical via GSC API
- **GS006: Sitemap Coverage Check** - Sitemap presence vs indexed status
- **GS007: Duplicate Variant Detection** - Detects URL variants causing canonical confusion
- **GS008: Redirect Chain Integrity** - Validates 301 redirect chains

### Content Quality Analysis
- **GS009: SSR No-JS Fallback** - Verifies meaningful content without JavaScript
- **GS010: Thin Content Heuristic** - Detects template-only pages
- **GS011: Hreflang Canonical Consistency** - International SEO consistency
- **GS012: Internal Linking Strength** - Assesses internal linking to target URLs

### Technical Performance
- **GS013: Render Timing Metrics** - Captures render timing metrics
- **GS014: Robots Meta Headers** - Ensures proper robots.txt and meta tags

## Key Features

### GSC Historical Analysis
- **Historical Tracking**: Monitors when pages became soft 404s over time
- **Pattern Detection**: Identifies common causes across failing URLs
- **Cache Management**: 24-hour cache with quota management
- **API Integration**: Direct Google Search Console API integration

### Soft 404 Detection
Based on analysis of Apply Digital's website, the tests identified:
- **Timeline**: Pages became soft 404s on October 1, 2025
- **Root Cause**: Introduction of splash screen and cookie dialog
- **Pattern**: 60% of analyzed URLs affected by overlay blocking
- **Canonical Issues**: Google-selected canonical became "N/A" for affected pages

## Usage

### Running Google Search Tests
```bash
# Run all Google Search category tests
python seo_analysis.py --url https://example.com --category "Google Search"

# Run specific test
python seo_analysis.py --url https://example.com --test-id GS001
```

### Pytest Unit Tests
```bash
# Run Google Search category tests
cd tests_pytest
python -m pytest test_google_search_category.py -v

# Run GSC historical analysis tests
python -m pytest test_gsc_historical_analysis.py -v
```

## Output Structure

```
output/
├── content_cache/          # Cached HTML content
├── crawl_cache/           # Crawl context data  
└── gsc_cache/             # Google Search Console cache
    ├── historical_soft_404s.json    # Historical tracking
    ├── soft_404_patterns.json       # Pattern analysis
    ├── quota_tracking.json          # API quota management
    └── [url_hash].json             # Individual URL inspection data
```

## Configuration

### GSC API Setup
1. Create Google Cloud project
2. Enable Search Console API
3. Create OAuth2 credentials
4. Save as `credentials.json`
5. Run authentication flow to generate `token.pickle`

### Cache Configuration
- **Cache Duration**: 24 hours (configurable)
- **Quota Management**: Automatic daily reset tracking
- **Historical Data**: Maintains timeline of changes
- **Pattern Analysis**: Identifies common soft 404 causes

## Test Results Interpretation

### Critical Issues (GS001-GS004)
- **GS001 Fail**: Main content not visible to Googlebot
- **GS002 Fail**: Console errors blocking rendering
- **GS003 Fail**: Static content too thin, requires JavaScript
- **GS004 Fail**: Overlays blocking content access

### GSC Integration Issues (GS005-GS008)
- **GS005 Fail**: Canonical mismatch between user and Google
- **GS006 Fail**: Sitemap not being indexed
- **GS007 Fail**: Duplicate URL variants causing confusion
- **GS008 Fail**: Redirect chain issues

### Content Quality Issues (GS009-GS012)
- **GS009 Fail**: No meaningful content without JavaScript
- **GS010 Fail**: Content too thin or template-only
- **GS011 Fail**: Hreflang/canonical inconsistencies
- **GS012 Fail**: Insufficient internal linking

### Technical Issues (GS013-GS014)
- **GS013 Fail**: Render timing issues affecting indexing
- **GS014 Fail**: Robots.txt or meta tags blocking indexing

## Historical Analysis

The GSC historical analysis reveals:
- **September 2025**: Pages indexed normally
- **October 1, 2025**: Soft 404 issues begin
- **Correlation**: Introduction of splash screen and cookie dialog
- **Impact**: 60% of analyzed URLs affected

## Recommendations

Based on test results:
1. **Remove/Modify Splash Screen**: Ensure Googlebot can access content
2. **Fix Cookie Dialog**: Implement server-side or bot-friendly consent
3. **Improve SSR**: Ensure meaningful content without JavaScript
4. **Canonical Alignment**: Fix user vs Google canonical mismatches
5. **Content Quality**: Add substantial content to thin pages

## Contributing

When adding new Google Search tests:
1. Follow naming convention: `gs###_descriptive_name.py`
2. Implement `SEOTest` interface
3. Add to `src/tests/google_search/__init__.py`
4. Include pytest unit tests
5. Update this documentation
