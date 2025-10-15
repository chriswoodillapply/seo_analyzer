# URL Discovery & Analysis Workflow

## 🎯 Two-Step Process

### Step 1: Discover URLs (Review First)
### Step 2: Analyze URLs (Run Full SEO Tests)

---

## Step 1: URL Discovery

### Quick Start
```bash
# Discover URLs from a website (depth 3, max 100 URLs)
python discover_urls.py https://www.applydigital.com --depth 3 --max-urls 100
```

### Options
```bash
# Deep crawl (5 levels, up to 1000 URLs)
python discover_urls.py https://example.com --depth 5 --max-urls 1000

# Fast discovery (no JavaScript rendering)
python discover_urls.py https://example.com --no-javascript

# Multiple starting points
python discover_urls.py https://example.com https://example.com/blog

# Custom output location
python discover_urls.py https://example.com --output my_urls.txt
```

### Output Files Created

1. **Detailed List** (`discovered_urls_DOMAIN_TIMESTAMP.txt`)
   - Includes comments showing depth levels
   - Shows discovery method (static/javascript)
   - Grouped by crawl depth
   - Total URL count and metadata

2. **Simple List** (`discovered_urls_DOMAIN_TIMESTAMP_simple.txt`)
   - One URL per line
   - No comments
   - Ready to use with `multi_url_analyzer.py`

### Example Output
```
Starting URL Discovery
Base URL(s): https://www.applydigital.com
Max Depth: 3
Max URLs: 100
JavaScript Rendering: Enabled

✓ URL Discovery Complete
Time elapsed: 47.0 seconds

Discovery Summary
├─ Total URLs Discovered: 85
├─ URLs Visited: 73
├─ Failed URLs: 0
├─ Depth 0: 1 URLs
├─ Depth 1: 14 URLs
├─ Depth 2: 27 URLs
├─ Depth 3: 31 URLs
└─ Depth 4: 12 URLs

✓ URLs saved to: output/discovered_urls_www_applydigital_com_20251015_122051.txt
✓ Simple list saved to: output/discovered_urls_www_applydigital_com_20251015_122051_simple.txt
```

---

## Step 2: Review & Filter URLs

### Review the Discovered URLs
```bash
# Open the detailed list to review
notepad output/discovered_urls_www_applydigital_com_20251015_122051.txt

# Or use the simple list
notepad output/discovered_urls_www_applydigital_com_20251015_122051_simple.txt
```

### Filter URLs (Optional)
You can manually edit the `_simple.txt` file to:
- Remove URLs you don't want to test
- Add additional URLs
- Prioritize certain pages

Example filtering:
```bash
# Keep only main pages (remove blog posts, news, etc.)
# Edit the file and remove lines you don't want

# Or use grep to filter
grep -v "/insights/" discovered_urls_simple.txt > filtered_urls.txt
grep -v "/events/" filtered_urls.txt > final_urls.txt
```

---

## Step 3: Run Full SEO Analysis

### Analyze All Discovered URLs
```bash
# Using the simple list file
python multi_url_analyzer.py --url-file output/discovered_urls_www_applydigital_com_20251015_122051_simple.txt --output excel

# This will:
# 1. Load all 85 URLs from the file
# 2. Run all 69 SEO tests on each URL
# 3. Generate consolidated report with ~5,950 rows (85 URLs × 70 rows each)
# 4. Save to output/multi_url_analysis_TIMESTAMP.xlsx
```

### Analysis Options
```bash
# CSV output only (faster, smaller file)
python multi_url_analyzer.py --url-file discovered_urls.txt --output csv

# Both CSV and Excel
python multi_url_analyzer.py --url-file discovered_urls.txt --output all

# Disable JavaScript rendering (faster but less accurate)
python multi_url_analyzer.py --url-file discovered_urls.txt --disable-javascript

# Custom output filename
python multi_url_analyzer.py --url-file discovered_urls.txt --output excel --save-dir output/reports
```

---

## Complete Workflow Example

### Scenario: Analyze Apply Digital Website

```bash
# Step 1: Discover URLs (depth 5, max 500)
python discover_urls.py https://www.applydigital.com --depth 5 --max-urls 500

# Output shows:
# ✓ Found 437 URLs
# ✓ Saved to: output/discovered_urls_www_applydigital_com_20251015_122051_simple.txt

# Step 2: Review the URLs
notepad output/discovered_urls_www_applydigital_com_20251015_122051_simple.txt

# (Optional) Edit file to remove unwanted URLs
# Maybe keep only 100 most important pages

# Step 3: Run full SEO analysis on reviewed URLs
python multi_url_analyzer.py --url-file output/discovered_urls_www_applydigital_com_20251015_122051_simple.txt --output excel

# Output shows:
# Analyzing 100 URLs with 69 tests each...
# ✓ Report saved: output/multi_url_analysis_20251015_123000.xlsx
# Total rows: 7,000 (100 URLs × 70 rows each)
```

---

## Understanding the Output

### URL Discovery Report
```
output/discovered_urls_www_applydigital_com_20251015_122051.txt
```
**Contains:**
- Header with metadata (base URL, max depth, total count)
- URLs grouped by discovery depth
- Discovery method for each URL (static HTML or JavaScript)

**Example:**
```
# URL Discovery Results
# Base URL: https://www.applydigital.com
# Max Depth: 3
# Total URLs: 85

# --- Depth 0 (1 URLs) ---
https://www.applydigital.com

# --- Depth 1 (14 URLs) ---
https://www.applydigital.com/about-us
https://www.applydigital.com/work
https://www.applydigital.com/services
...

# --- Depth 2 (27 URLs) ---
https://www.applydigital.com/work/retail-and-cpg
https://www.applydigital.com/services/bigcommerce
...
```

### SEO Analysis Report
```
output/multi_url_analysis_20251015_123000.xlsx
```
**Contains Multiple Sheets:**
1. **All Results** - Every test for every URL (~7,000 rows)
2. **URL Summary** - Overview per URL (100 rows)
3. **Issues Found** - Only failures/warnings
4. **Passed Tests** - Only successful tests
5. **Category Summary** - Scores by category

**Each row includes:**
- URL, Test Name, Category, Status (Pass/Warning/Fail)
- Severity, Issue Description, Recommendation
- Score, Timestamp, Analysis Type

---

## Performance Estimates

### URL Discovery Time
| URLs | Depth | JavaScript | Time |
|------|-------|-----------|------|
| 100  | 3     | Yes       | ~45-60s |
| 500  | 5     | Yes       | 3-5 min |
| 1000 | 5     | Yes       | 5-10 min |
| 100  | 3     | No        | ~20-30s |

### SEO Analysis Time
| URLs | Tests/URL | Total Tests | Time |
|------|-----------|-------------|------|
| 10   | 69        | 690         | ~5 min |
| 50   | 69        | 3,450       | ~25 min |
| 100  | 69        | 6,900       | ~45 min |
| 500  | 69        | 34,500      | ~4 hours |
| 1000 | 69        | 69,000      | ~8 hours |

*Times are estimates and vary based on website speed and system performance*

---

## Tips & Best Practices

### 1. Start Small
```bash
# First, discover a small set to review
python discover_urls.py https://example.com --depth 2 --max-urls 50

# Review and validate
# Then scale up if needed
python discover_urls.py https://example.com --depth 5 --max-urls 500
```

### 2. Use Depth Wisely
- **Depth 1-2**: Main navigation pages only
- **Depth 3**: Include category/section pages
- **Depth 4-5**: Include individual content pages
- **Depth 6+**: May include paginated lists, archives (often not needed)

### 3. Filter by Content Type
```bash
# Discover all URLs first
python discover_urls.py https://example.com --depth 5 --max-urls 1000

# Then filter the simple list
# Keep only important pages, remove:
# - Paginated results (?page=2, ?page=3, etc.)
# - Tag archives
# - Date-based archives
# - Search result pages
# - Login/logout pages
```

### 4. Parallel Analysis
For very large sites (1000+ URLs), consider splitting:
```bash
# Split URL list into batches
split -l 100 discovered_urls_simple.txt batch_

# Analyze batches separately (can run in parallel)
python multi_url_analyzer.py --url-file batch_aa --output excel
python multi_url_analyzer.py --url-file batch_ab --output excel
python multi_url_analyzer.py --url-file batch_ac --output excel

# Combine reports afterwards
```

### 5. Schedule Regular Scans
```bash
# Create a script to run weekly
# 1. Discover URLs
# 2. Compare with previous week (check for new/removed pages)
# 3. Run analysis on changed pages only
# 4. Generate trend report
```

---

## Troubleshooting

### Issue: JavaScript rendering slow/failing
**Solution:**
```bash
# Try without JavaScript first
python discover_urls.py https://example.com --no-javascript

# If you need JavaScript for SPA sites, ensure Playwright is installed
pip install playwright
playwright install chromium
```

### Issue: Too many URLs discovered
**Solution:**
```bash
# Reduce depth
python discover_urls.py https://example.com --depth 2 --max-urls 100

# Or manually filter the output file
```

### Issue: Missing important URLs
**Solution:**
```bash
# Use multiple seed URLs
python discover_urls.py https://example.com https://example.com/products https://example.com/blog

# Or manually add them to the simple list file
```

### Issue: Discovery taking too long
**Solution:**
```bash
# Reduce timeout
python discover_urls.py https://example.com --timeout 10

# Disable JavaScript
python discover_urls.py https://example.com --no-javascript

# Limit max URLs
python discover_urls.py https://example.com --max-urls 100
```

---

## Next Steps

After running the analysis:

1. **Review the consolidated report**
   - Focus on failed and warning tests first
   - Identify patterns across multiple URLs

2. **Prioritize fixes**
   - Critical issues first (SSL, H1, titles)
   - High impact issues next (performance, mobile)
   - Quick wins (alt text, meta descriptions)

3. **Track progress**
   - Re-run analysis after fixes
   - Compare reports to measure improvement
   - Monitor new URLs as site grows

4. **Automate**
   - Schedule weekly/monthly scans
   - Set up alerts for critical issues
   - Track trends over time

---

## Files Reference

- **`discover_urls.py`** - URL discovery tool
- **`multi_url_analyzer.py`** - Multi-URL SEO analysis
- **`seo_analyzer.py`** - Core analysis engine (69 tests)
- **`seo_test_catalog.py`** - Complete test definitions
- **`TEST_OUTPUT_MAPPING.md`** - Test documentation
- **`SEO_TESTING_SYSTEM_OVERVIEW.md`** - System overview

