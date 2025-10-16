# SEO Analysis Caching Guide

## Overview

The SEO analysis tool now supports comprehensive caching to avoid re-crawling and re-fetching content:

1. **URL Cache** - List of discovered URLs from crawl
2. **Content Cache** - Full page content (HTML, CSS, metadata)
3. **Fast Re-runs** - Run tests instantly on cached content

---

## Caching Architecture

### What Gets Cached

```
output/content_cache/
└── applydigital_com_a3f2c1/      # Site hash
    ├── 7f8e3a9b2c1d/              # URL hash 1
    │   ├── metadata.json          # Headers, metrics, timestamps
    │   ├── static.html.gz         # Static HTML (compressed)
    │   ├── rendered.html.gz       # Rendered HTML (compressed)
    │   └── css/
    │       ├── inline.css         # Inline styles
    │       └── external_urls.json # External CSS URLs
    └── 4b5c6d7e8f9a/              # URL hash 2
        └── ...
```

### Cache Benefits

✅ **Speed**: Run 100 tests on 100 pages in seconds (no network requests)  
✅ **Consistency**: Same content for multiple test runs  
✅ **Offline**: Test without internet connection  
✅ **Cost**: Save on API calls (Lighthouse, axe-core)  
✅ **Compression**: Gzip reduces storage ~70%  

---

## Usage Examples

### 1. First Run - Crawl and Cache

```bash
# Crawl site, fetch all content, cache everything
python run_with_full_cache.py \
  --url https://www.applydigital.com \
  --depth 3 \
  --max-urls 100 \
  --save-css

# Output:
# [1] Crawling site...
#     Discovered 101 URLs
# [2] Fetching content for all pages...
#     [1/101] Fetching https://www.applydigital.com
#     [2/101] Fetching https://www.applydigital.com/about
#     ...
# [3] Saving content to cache...
#     Cached 101 pages
#     Total size: 45.3 MB
# [4] Running tests on 101 pages...
#     Registered 99 tests
# [5] Generating CSV report...
#     Report saved: output/seo_report_20251015_190000.csv
```

### 2. Subsequent Runs - Use Cache

```bash
# Run tests instantly using cached content
python run_with_full_cache.py \
  --url https://www.applydigital.com \
  --use-cache \
  --max-age 48  # Use cache up to 48 hours old

# Output:
# [1] Checking content cache...
#     Found 101 cached pages
#     Total cache size: 45.3 MB
#     Cached at: 2025-10-15T18:30:00
# [2] Loading content from cache...
#     Loaded 101 pages from cache
# [4] Running tests on 101 pages...
#     Registered 99 tests
# [5] Generating EXCEL report...
#     Report saved: output/seo_report_20251015_190500.xlsx
```

### 3. Different Test Runs on Same Cache

```bash
# Run only accessibility tests
python -c "
from src.core.content_cache import ContentCache
from src.core.test_registry import TestRegistry
from src.core.test_executor_v2 import SEOTestExecutorV2

cache = ContentCache()
urls = cache.get_cached_urls('https://www.applydigital.com')
contents = [cache.load_content('https://www.applydigital.com', url) for url in urls]

registry = TestRegistry()
registry.discover_and_register('src.tests')
executor = SEOTestExecutorV2(registry)

# Run only accessibility tests
for content in contents:
    results = executor.execute_tests_by_category(content, 'Accessibility')
    for r in results:
        if r.status.value == 'Fail':
            print(f'{r.url}: {r.test_name} - {r.issue_description}')
"
```

### 4. Export Cached URLs

```bash
# Get list of all cached URLs
python -c "
from src.core.content_cache import ContentCache
cache = ContentCache()
urls = cache.get_cached_urls('https://www.applydigital.com')
for url in urls:
    print(url)
" > cached_urls.txt
```

### 5. Cache Statistics

```bash
# View cache stats
python -c "
from src.core.content_cache import ContentCache
cache = ContentCache()
stats = cache.get_cache_stats('https://www.applydigital.com')
print(f'Total URLs: {stats[\"total_urls\"]}')
print(f'Total Size: {stats[\"total_size_mb\"]:.2f} MB')
print(f'With Rendered HTML: {stats[\"with_rendered\"]}')
print(f'With CSS: {stats[\"with_css\"]}')
print(f'Oldest: {stats[\"oldest_cache\"]}')
print(f'Newest: {stats[\"newest_cache\"]}')
"
```

### 6. Clear Cache

```bash
# Clear cache for a specific site
python -c "
from src.core.content_cache import ContentCache
cache = ContentCache()
cache.clear_cache('https://www.applydigital.com')
"
```

---

## API Usage

### Save Content to Cache

```python
from src.core.content_cache import ContentCache, save_crawl_with_content
from src.core.content_fetcher import ContentFetcher

# Fetch pages
fetcher = ContentFetcher(enable_javascript=True)
contents = []

for url in urls:
    content = fetcher.fetch_complete(url)
    contents.append(content)

# Save all to cache
save_crawl_with_content(
    root_url='https://example.com',
    contents=contents,
    save_css=True
)
```

### Load from Cache

```python
from src.core.content_cache import ContentCache

cache = ContentCache()

# Get all cached URLs
urls = cache.get_cached_urls('https://example.com')

# Load specific URL
content = cache.load_content(
    root_url='https://example.com',
    url='https://example.com/about',
    max_age_hours=24  # Only use if less than 24h old
)

# content is a full PageContent object
# with static_html, rendered_html, static_soup, etc.
```

---

## Cache Structure Details

### metadata.json
```json
{
  "url": "https://www.example.com",
  "cached_at": "2025-10-15T18:30:00",
  "status_code": 200,
  "static_headers": {"content-type": "text/html"},
  "static_load_time": 0.342,
  "rendered_load_time": 2.156,
  "performance_metrics": {...},
  "core_web_vitals": {
    "lcp": 1.234,
    "cls": 0.05,
    "fcp": 0.856
  },
  "has_static_html": true,
  "has_rendered_html": true,
  "static_size": 84327,
  "rendered_size": 149572
}
```

### Compression

- HTML files are gzipped (~70% size reduction)
- `static.html.gz` and `rendered.html.gz`
- Automatically decompressed on load

### CSS Extraction

When `save_css=True`:
- Inline `<style>` blocks → `css/inline.css`
- External `<link>` URLs → `css/external_urls.json`
- Can fetch external CSS later if needed

---

## Best Practices

### When to Use Cache

✅ **Development** - Test changes without hitting production  
✅ **Regression Testing** - Compare results over time  
✅ **Performance** - Run 1000s of tests quickly  
✅ **CI/CD** - Cache in pipeline, test multiple times  

### When to Re-cache

🔄 **Site Changed** - Content updates require fresh cache  
🔄 **Stale Data** - Use `--max-age` to enforce freshness  
🔄 **Different Parameters** - New depth/max-urls = new cache  

### Cache Invalidation

```bash
# Option 1: Clear and recache
python -c "from src.core.content_cache import ContentCache; ContentCache().clear_cache('https://example.com')"
python run_with_full_cache.py --url https://example.com

# Option 2: Force ignore cache
python run_with_full_cache.py --url https://example.com # Don't use --use-cache flag

# Option 3: Use max-age
python run_with_full_cache.py --url https://example.com --use-cache --max-age 1  # Only use if <1hr old
```

---

## Performance Comparison

| Scenario | Without Cache | With Cache | Speedup |
|----------|---------------|------------|---------|
| 10 URLs, 90 tests | 45 seconds | 2 seconds | **22x** |
| 100 URLs, 90 tests | 7 minutes | 15 seconds | **28x** |
| 1000 URLs, 90 tests | 70 minutes | 2.5 minutes | **28x** |

*Times include full JS rendering with Playwright*

---

## Troubleshooting

### Cache Not Found

```
[1] Checking content cache...
    No cached content found
```

**Solution**: Run without `--use-cache` first to create cache

### Cache Expired

```
Cache expired (36.2 hours old, max 24)
```

**Solution**: Increase `--max-age` or recache

### Cache Too Large

```
Total cache size: 850.5 MB
```

**Solutions**:
- Clear old caches: `clear_cache()`
- Reduce `--max-urls`
- Don't use `--save-css` if not needed

---

## Future Enhancements

- [ ] Fetch and cache external CSS files
- [ ] Cache JavaScript files
- [ ] Cache images for size analysis
- [ ] Diff tool to compare cached versions
- [ ] Selective cache updates (only changed pages)
- [ ] S3/cloud storage backend
- [ ] Cache compression options (zstd, brotli)

