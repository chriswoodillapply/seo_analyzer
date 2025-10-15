# SEO Test Catalog & Output Format Mapping

## Overview
This document explains how each of the **69 SEO tests** maps to output rows in CSV/Excel reports.

## Output Row Structure

Each test generates **one row per URL** with the following columns:

| Column | Description | Example Values |
|--------|-------------|----------------|
| **URL** | The tested URL | `https://example.com` |
| **Test_Name** | Name of the test | `Page Title Presence` |
| **Category** | Test category | `Meta Tags`, `Performance`, etc. |
| **Status** | Test result | `Pass`, `Fail`, `Warning` |
| **Severity** | Impact level | `Critical`, `High`, `Medium`, `Low`, `Info` |
| **Issue_Description** | What was found | `Missing meta description tag` |
| **Recommendation** | How to fix it | `Add unique meta description (120-160 chars)` |
| **Score** | Category score | `85%` or specific metric |
| **Timestamp** | When tested | `2025-10-15 14:30:00` |
| **Analysis_Type** | Static or Rendered | `Static HTML`, `JavaScript Rendered`, `Both` |
| **Google_Impact** | Affects rankings | `Yes` or `No` |

## Test Categories (15 Total)

### 1. Meta Tags (11 tests)
- **meta_title_presence** - Critical
  - Pass: Title tag exists and not empty
  - Fail: Missing or empty title → "Missing page title tag"
  
- **meta_title_length_chars** - High
  - Pass: 30-60 characters
  - Warning: Under 30 or over 60 → "Title is 75 characters (optimal: 30-60)"
  
- **meta_title_length_pixels** - High
  - Pass: ≤600px
  - Warning: >600px → "Title truncated in SERPs (620px, limit: 600px)"
  
- **meta_description_presence** - High
  - Pass: Description exists
  - Fail: Missing → "Missing meta description"
  
- **meta_description_length_chars** - Medium
  - Pass: 120-160 characters
  - Warning: Outside range → "Description is 95 characters (optimal: 120-160)"
  
- **meta_description_length_pixels** - Medium
  - Pass: ≤920px
  - Warning: >920px → "Description truncated in SERPs"
  
- **canonical_url** - High
  - Pass: Valid canonical URL
  - Fail: Missing/invalid → "Missing canonical URL tag"
  
- **robots_meta_tag** - Medium
  - Pass: Allows indexing
  - Warning: Blocks inappropriately → "Page blocked from indexing"
  
- **viewport_meta_tag** - High
  - Pass: Properly configured
  - Fail: Missing → "Missing viewport meta tag for mobile"
  
- **open_graph_tags** - Low
  - Pass: OG tags present
  - Warning: Missing → "Missing Open Graph tags for social sharing"
  
- **title_h1_match** - Medium
  - Pass: Related but different
  - Warning: Identical or unrelated → "Title and H1 are identical"

### 2. Header Structure (6 tests)
- **h1_presence** - Critical
  - Pass: Exactly one H1
  - Fail: Zero or multiple → "Page has 2 H1 tags (should be exactly 1)"
  
- **h1_uniqueness** - High
  - Pass: Unique across site
  - Fail: Duplicate → "H1 duplicated on 3 other pages"
  
- **header_hierarchy** - Medium
  - Pass: Sequential (H1→H2→H3)
  - Warning: Skips levels → "Headers skip from H2 to H4"
  
- **h2_presence** - Medium
  - Pass: Has H2 tags for content
  - Warning: Missing on long content → "Long content lacks H2 structure"
  
- **duplicate_headers** - Low
  - Pass: All unique
  - Warning: Duplicates found → "3 headers have identical content"
  
- **header_length** - Low
  - Pass: 5-70 characters
  - Warning: Too short/long → "Header too short: 'Go' (min: 5 chars)"

### 3. Images (5 tests)
- **img_alt_text_presence** - High
  - Pass: All images have alt
  - Fail: Missing alt → "12 images missing alt text"
  
- **img_alt_text_quality** - Medium
  - Pass: Descriptive, <100 chars
  - Warning: Poor quality → "8 images have non-descriptive alt text"
  
- **img_title_attributes** - Low
  - Pass: Important images have titles
  - Info: Could improve → "Consider adding title attributes"
  
- **img_file_sizes** - Medium
  - Pass: Images <100KB
  - Warning: Oversized → "5 images over 100KB (largest: 450KB)"
  
- **img_lazy_loading** - Low
  - Pass: Below-fold images lazy load
  - Info: Could improve → "15 images could use lazy loading"

### 4. Links (5 tests)
- **internal_links_count** - Medium
  - Pass: 5-100 internal links
  - Warning: Outside range → "Only 2 internal links (min: 5)"
  
- **external_links_ratio** - Low
  - Pass: Balanced ratio
  - Warning: High external ratio → "External links (45) dominate internal (5)"
  
- **anchor_text_quality** - Medium
  - Pass: Descriptive anchors
  - Warning: Generic text → "12 links use 'click here' or 'read more'"
  
- **missing_anchor_text** - High
  - Pass: All links have text
  - Fail: Missing → "8 links missing anchor text"
  
- **broken_links** - High
  - Pass: All links work
  - Fail: Broken found → "3 broken links (404 errors)"

### 5. Content (4 tests)
- **content_word_count** - Medium
  - Pass: 300+ words
  - Warning: Thin content → "Only 150 words (min: 300)"
  
- **content_readability** - Low
  - Pass: Flesch score >60
  - Warning: Hard to read → "Flesch score: 45 (target: >60)"
  
- **content_uniqueness** - High
  - Pass: Unique content
  - Fail: Duplicates → "Content 85% similar to /other-page"
  
- **content_structure** - Low
  - Pass: Well formatted
  - Warning: Poor structure → "Large text blocks without lists/formatting"

### 6. Technical SEO (5 tests)
- **robots_txt_presence** - Medium
  - Pass: Robots.txt exists
  - Warning: Missing → "No robots.txt file found"
  
- **sitemap_xml_presence** - Medium
  - Pass: Sitemap exists
  - Warning: Missing → "No XML sitemap found"
  
- **ssl_certificate** - Critical
  - Pass: Valid HTTPS
  - Fail: No SSL → "Site uses HTTP instead of HTTPS"
  
- **schema_markup** - Medium
  - Pass: Schema implemented
  - Info: Missing → "No structured data detected"
  
- **canonical_implementation** - High
  - Pass: Proper canonical strategy
  - Fail: Issues → "Canonical points to 404 page"

### 7. Performance (5 tests)
- **page_load_time_http** - Medium
  - Pass: <1 second
  - Warning: Slow → "Server response: 2.3s (target: <1s)"
  
- **page_load_time_full** - High
  - Pass: <3 seconds
  - Warning: Slow → "Page loads in 5.2s (target: <3s)"
  
- **page_size** - Medium
  - Pass: <2MB
  - Warning: Large → "Page size: 3.5MB (target: <2MB)"
  
- **dom_elements_count** - Low
  - Pass: <1500 elements
  - Warning: Excessive → "2,300 DOM elements (target: <1500)"
  
- **render_blocking_resources** - Medium
  - Pass: Minimal blocking
  - Warning: Excessive → "15 render-blocking resources delay rendering"

### 8. Core Web Vitals (5 tests) - **Requires Lighthouse**
- **largest_contentful_paint** - Critical
  - Pass: ≤2.5s
  - Fail: Slow → "LCP: 4.2s (target: ≤2.5s)"
  
- **first_input_delay** - Critical
  - Pass: <100ms
  - Fail: Slow → "FID: 250ms (target: <100ms)"
  
- **cumulative_layout_shift** - Critical
  - Pass: <0.1
  - Fail: Unstable → "CLS: 0.35 (target: <0.1)"
  
- **first_contentful_paint** - High
  - Pass: ≤1.8s
  - Warning: Slow → "FCP: 2.5s (target: ≤1.8s)"
  
- **time_to_interactive** - High
  - Pass: ≤5s
  - Warning: Slow → "TTI: 7.2s (target: ≤5s)"

### 9. Lighthouse Audit (4 tests) - **Requires Lighthouse**
- **lighthouse_performance_score** - High
  - Pass: ≥90
  - Fail: Low → "Performance score: 65 (target: ≥90)"
  
- **lighthouse_accessibility_score** - High
  - Pass: ≥90
  - Fail: Low → "Accessibility score: 72 (target: ≥90)"
  
- **lighthouse_best_practices_score** - Medium
  - Pass: ≥90
  - Warning: Low → "Best practices score: 80 (target: ≥90)"
  
- **lighthouse_seo_score** - High
  - Pass: ≥90
  - Fail: Low → "SEO score: 68 (target: ≥90)"

### 10. Accessibility (5 tests)
- **lang_attribute** - High
  - Pass: Lang attribute set
  - Fail: Missing → "HTML missing lang attribute"
  
- **form_labels** - High
  - Pass: All inputs labeled
  - Fail: Missing → "8 form inputs missing labels"
  
- **semantic_html5** - Medium
  - Pass: Uses semantic elements
  - Warning: Generic markup → "Over-reliance on div/span elements"
  
- **skip_links** - Medium
  - Pass: Skip links present
  - Warning: Missing → "No skip navigation links for keyboard users"
  
- **axe_core_violations** - High
  - Pass: No critical violations
  - Fail: Issues found → "5 critical accessibility violations detected"

### 11. Security Headers (3 tests)
- **content_security_policy** - High
  - Pass: CSP configured
  - Fail: Missing → "Missing Content-Security-Policy header"
  
- **x_frame_options** - Medium
  - Pass: X-Frame-Options set
  - Warning: Missing → "Missing X-Frame-Options header"
  
- **strict_transport_security** - Medium
  - Pass: HSTS enabled
  - Warning: Missing → "Missing HSTS header on HTTPS site"

### 12. Mobile Usability (4 tests)
- **mobile_viewport_config** - Critical
  - Pass: Viewport configured
  - Fail: Missing → "Viewport not configured for mobile"
  
- **mobile_font_sizes** - Medium
  - Pass: Fonts ≥16px
  - Warning: Small → "12 text elements <16px on mobile"
  
- **touch_targets** - Medium
  - Pass: Targets ≥44px
  - Warning: Small → "18 touch targets <44px"
  
- **content_width** - High
  - Pass: No horizontal scroll
  - Fail: Overflow → "Content overflows viewport on mobile"

### 13. Soft 404 Detection (2 tests)
- **soft_404_content_indicators** - High
  - Pass: Real content
  - Fail: Soft 404 detected → "Page returns 200 but contains error content"
  
- **content_length_analysis** - Medium
  - Pass: Sufficient content
  - Warning: Suspicious → "Minimal content suggests soft 404"

### 14. SERP Preview (3 tests)
- **serp_title_display** - High
  - Pass: Title displays fully
  - Warning: Truncated → "Title truncated in Google results"
  
- **serp_description_display** - Medium
  - Pass: Description displays fully
  - Warning: Truncated → "Description truncated in Google results"
  
- **serp_url_display** - Low
  - Pass: Clean URL
  - Warning: Messy → "URL too long with excessive parameters"

### 15. Code Coverage (2 tests) - **Requires Lighthouse**
- **unused_css** - Low
  - Pass: <20% unused
  - Warning: High → "35% of CSS unused (125KB wasted)"
  
- **unused_javascript** - Medium
  - Pass: <20% unused
  - Warning: High → "45% of JavaScript unused (320KB wasted)"

## Example Output for a Single URL

```csv
URL,Test_Name,Category,Status,Severity,Issue_Description,Recommendation,Score,Timestamp,Analysis_Type
https://example.com,Page Title Presence,Meta Tags,Pass,Critical,Page has valid title tag,Continue maintaining proper titles,100%,2025-10-15 14:30:00,Both
https://example.com,Title Length (Pixels),Meta Tags,Warning,High,Title is 620px wide (>600px limit),Reduce title length to prevent truncation,85%,2025-10-15 14:30:00,Both
https://example.com,Meta Description Presence,Meta Tags,Fail,High,Missing meta description tag,Add unique meta description (120-160 chars),0%,2025-10-15 14:30:00,Both
https://example.com,H1 Tag Presence,Header Structure,Pass,Critical,Page has exactly one H1 tag,Maintain single H1 per page,100%,2025-10-15 14:30:00,Both
https://example.com,SSL Certificate,Technical SEO,Pass,Critical,Valid HTTPS with SSL certificate,Continue using HTTPS,100%,2025-10-15 14:30:00,Static HTML
https://example.com,Page Load Time,Performance,Warning,High,Page loads in 4.2s (target: <3s),Optimize resources for faster loading,70%,2025-10-15 14:30:00,Rendered
https://example.com,LCP Score,Core Web Vitals,Fail,Critical,LCP: 4800ms (target: ≤2500ms),Optimize largest element loading,45%,2025-10-15 14:30:00,Lighthouse
...continues for all 69 tests...
```

## Analysis Types

Tests run on different versions of content:

1. **Static HTML Only** (8 tests)
   - Tests that only need the original server response
   - Examples: robots.txt, security headers, SSL

2. **JavaScript Rendered Only** (11 tests)  
   - Tests requiring full page rendering
   - Examples: image sizes, touch targets, skip links

3. **Both Versions** (39 tests)
   - Tested on static AND rendered to detect differences
   - Examples: meta tags, headers, links, content

4. **Lighthouse Required** (11 tests)
   - Need Google Lighthouse/Chrome DevTools
   - Examples: Core Web Vitals, code coverage, performance scores

## Status Determination Logic

```python
if test_passes_all_criteria:
    status = "Pass"
    issue = "All tests passed for {test_name}"
    recommendation = "Continue maintaining current standards"
    
elif test_has_minor_issues:
    status = "Warning"
    issue = "{specific_issue_description}"
    recommendation = "{specific_fix_recommendation}"
    
elif test_fails_critical_criteria:
    status = "Fail"
    issue = "{critical_issue_description}"
    recommendation = "{urgent_fix_recommendation}"
```

## URL Summary

After all individual test rows, each URL gets a summary row:

```csv
URL,Test_Name,Category,Status,Severity,Issue_Description,Recommendation,Score,Timestamp
https://example.com,Overall SEO Health,Summary,Warning,N/A,35 issues found across 12 categories (7 Critical 18 High 10 Medium),Address critical issues first for maximum SEO impact,Overall: 68%,2025-10-15 14:30:00
```

## Report Outputs

The system generates reports in multiple formats:

### 1. CSV Report (`output/seo_report_*.csv`)
- Flat structure with all test results
- One row per test per URL
- Easy to filter/sort in Excel

### 2. Excel Report (`output/seo_report_*.xlsx`)
Multiple sheets:
- **All Results**: Complete test results
- **Summary**: URL-level overview
- **Failed Tests**: Only failures/warnings
- **Passed Tests**: Only successful tests
- **Category Breakdown**: Scores by category
- **Lighthouse Metrics**: Performance details

### 3. JSON Report (`output/seo_report_*.json`)
- Hierarchical structure
- Full technical details
- Machine-readable format

### 4. HTML Report (`output/seo_report_*.html`)
- Visual dashboard
- Color-coded results
- Interactive charts

## Test Execution Flow

For each URL:
1. Fetch static HTML → Run 47 tests (static + both)
2. Render with JavaScript → Run 50 tests (rendered + both)
3. Run Lighthouse audit → Run 11 additional tests
4. Compare static vs rendered → Detect discrepancies
5. Generate rows for all 69+ tests
6. Add summary row with overall status
7. Export to CSV/Excel/JSON/HTML

Total rows per URL: **70-75 rows** (69 tests + summary + any comparison findings)

For 100 URLs: **7,000-7,500 rows** in consolidated report!

