# Enterprise SEO Analysis Tool

A professional, enterprise-grade SEO analysis tool built with Python that performs comprehensive SEO audits on websites with URL crawling, JavaScript rendering, and detailed reporting.

## Features

- **URL Crawling**: Automatically discover and analyze all pages on a website with configurable depth and limits
- **JavaScript Rendering**: Analyze both static HTML and fully rendered content using Playwright
- **Comprehensive SEO Tests**: 93 comprehensive SEO tests across 13 categories:
  - Meta Tags (title, description, keywords, Open Graph, Twitter Cards, favicon, etc.)
  - Header Structure (H1-H6 hierarchy, gaps, empty headers)
  - Images (alt text, dimensions, modern formats, responsive images)
  - Links (internal/external, broken links, nofollow, pagination, link density)
  - Content Quality (word count, readability, freshness, multimedia diversity)
  - Technical SEO (robots.txt, sitemap, canonical, URL structure, redirects, mixed content)
  - Performance (load times, compression, caching, CDN, render-blocking resources)
  - Core Web Vitals (LCP, CLS, FCP)
  - Accessibility (ARIA landmarks, form handling, focus indicators, video captions)
  - Mobile Usability (viewport, responsive images, touch targets)
  - Security (HTTPS, headers, SRI, iframe security, cookies, CORS)
  - Structured Data (Schema.org markup for Organization, Breadcrumb, Video)
  - International SEO (hreflang, content language, geo-targeting)
- **Multiple Report Formats**: CSV, Excel, HTML, and JSON
- **Verbose Logging**: Detailed progress tracking during analysis
- **Enterprise Architecture**: Clean, modular, testable code structure

## Architecture

The tool follows enterprise software design principles with clear separation of concerns:

```
seo_analyzer/
├── src/
│   ├── core/
│   │   ├── content_fetcher.py    # Fetches static & rendered content
│   │   ├── test_executor.py      # Executes SEO tests
│   │   └── seo_orchestrator.py   # Main coordinator
│   ├── crawlers/
│   │   └── url_crawler.py         # URL discovery engine
│   ├── analyzers/
│   │   └── test_catalog.py        # SEO test definitions
│   └── reporters/
│       └── report_generator.py    # Multi-format reporting
├── tests/                          # Comprehensive unit tests
├── seo_analysis.py                 # CLI entry point
└── requirements.txt                # Dependencies
```

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/chriswoodillapply/seo_analyzer.git
cd seo_analyzer
```

2. **Create a virtual environment**:
```bash
python -m venv seo_env
```

3. **Activate the virtual environment**:
- Windows: `seo_env\Scripts\activate`
- Mac/Linux: `source seo_env/bin/activate`

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Install Playwright browsers** (for JavaScript rendering):
```bash
playwright install chromium
```

## Usage

### Analyze a Single URL

```bash
python seo_analysis.py --url https://example.com
```

### Analyze Multiple URLs

```bash
python seo_analysis.py --urls https://example.com https://test.com
```

### Crawl and Analyze a Website

```bash
python seo_analysis.py --url https://example.com --crawl --depth 3 --max-urls 100
```

### Generate Specific Report Formats

```bash
python seo_analysis.py --url https://example.com --formats csv excel html
```

### Verbose Output

```bash
python seo_analysis.py --url https://example.com --crawl --verbose
```

### Advanced Options

```bash
python seo_analysis.py \
  --url https://example.com \
  --crawl \
  --depth 10 \
  --max-urls 200 \
  --formats csv excel html json \
  --timeout 30 \
  --no-javascript \
  --output-dir reports \
  --verbose
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | Single URL to analyze | - |
| `--urls` | Multiple URLs to analyze | - |
| `--url-file` | File containing URLs (one per line) | - |
| `--crawl` | Enable URL crawling | False |
| `--depth` | Maximum crawl depth | 3 |
| `--max-urls` | Maximum URLs to discover | 50 |
| `--formats` | Report formats (csv, excel, html, json) | csv |
| `--timeout` | Request timeout in seconds | 30 |
| `--no-javascript` | Disable JavaScript rendering | False |
| `--output-dir` | Output directory for reports | output |
| `--filename` | Base filename for reports | seo_report_TIMESTAMP |
| `--verbose` | Enable detailed logging | False |
| `--user-agent` | Custom User-Agent string | Default |
| `--headless` | Run browser in headless mode | True |

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_content_fetcher.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Example Output

```
======================================================================
 Enterprise SEO Analysis
======================================================================
URLs to analyze: 1
Crawling: Enabled
JavaScript: Enabled
Report formats: csv, excel, html
======================================================================

=== Starting URL Discovery ===
Discovered 102 URLs

=== Analyzing 102 URLs ===

[1/102] Analyzing: https://www.example.com
  > Fetching static content...
  > Static HTML: 84327 bytes
  > Rendered HTML: 149572 bytes
  > Load time: 0.25s
  > Running SEO tests...
  > Results: 26 passed, 0 failed, 4 warnings
  Completed 36 tests

============================================================
SEO ANALYSIS SUMMARY
============================================================
URLs Analyzed:     102
Total Tests:       3,662
Passed:            2,450
Failed:            40
Warnings:          559
Pass Rate:         66.9%
============================================================
```

## Dependencies

- **requests**: HTTP requests
- **beautifulsoup4**: HTML parsing
- **lxml**: XML/HTML processing
- **playwright**: JavaScript rendering
- **pandas**: Data manipulation
- **openpyxl**: Excel file generation
- **nest_asyncio**: Async compatibility

## Development

### Project Structure

- **ContentFetcher**: Fetches and measures page content (static and JavaScript-rendered)
- **URLCrawler**: Discovers URLs through crawling with depth control
- **SEOTestExecutor**: Executes all SEO tests with pluggable test catalog
- **ReportGenerator**: Creates reports in multiple formats
- **SEOOrchestrator**: Coordinates all components and manages workflow

### Adding New Tests

1. Add test definition to `src/analyzers/test_catalog.py`
2. Implement test method in the catalog class
3. Tests are automatically discovered and executed

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Chris Wood - Apply Digital

## Support

For issues or questions, please open an issue on GitHub.
