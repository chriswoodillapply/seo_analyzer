# Enterprise SEO Analysis Architecture

## Overview

This project uses a clean, enterprise-grade architecture with clear separation of concerns.

## Directory Structure

```
seo/
├── src/                          # Core application code
│   ├── core/                     # Core business logic
│   │   ├── content_fetcher.py    # Fetches static & rendered content
│   │   ├── test_executor.py     # Executes SEO tests dynamically
│   │   └── seo_orchestrator.py  # Main coordinator
│   ├── crawlers/                 # URL discovery
│   │   └── url_crawler.py        # Crawls websites for URLs
│   └── reporters/                # Report generation
│       └── report_generator.py   # Generates CSV, Excel, JSON, HTML reports
├── tests/                        # Unit tests
│   ├── test_content_fetcher.py
│   ├── test_test_executor.py
│   └── test_orchestrator.py
├── examples/                     # Example scripts
├── output/                       # Generated reports
└── seo_analysis.py              # Main entry point
```

## Core Components

### 1. ContentFetcher (`src/core/content_fetcher.py`)
**Responsibility:** Fetch web page content in two modes
- **Static HTML:** Fast, uses requests library
- **Rendered Content:** Executes JavaScript using Playwright
- **Performance Metrics:** Measures Core Web Vitals (LCP, FCP, CLS)

**Key Classes:**
- `ContentFetcher`: Main fetcher with context manager support
- `PageContent`: Data class containing all fetched content

### 2. SEOTestExecutor (`src/core/test_executor.py`)
**Responsibility:** Execute SEO tests on page content
- **Plugin Architecture:** Easy to add new tests
- **40+ Tests:** Meta tags, headers, images, links, content, performance, accessibility, security
- **Test Categories:** Meta Tags, Header Structure, Images, Links, Content, Technical SEO, Performance, Core Web Vitals, Accessibility, Mobile, Security

**Key Classes:**
- `SEOTestExecutor`: Executes tests dynamically
- `TestResult`: Standardized test result format
- `TestStatus`: Pass/Fail/Warning/Info/Error enum

### 3. URLCrawler (`src/crawlers/url_crawler.py`)
**Responsibility:** Discover URLs from websites
- **Dual Discovery:** Static HTML + JavaScript rendering
- **Configurable Depth:** Control crawl depth and max URLs
- **Smart Filtering:** Excludes files, external domains, fragments

**Key Classes:**
- `URLCrawler`: Main crawler with context manager support

### 4. ReportGenerator (`src/reporters/report_generator.py`)
**Responsibility:** Generate reports in multiple formats
- **Formats:** CSV, Excel (multi-sheet), JSON, HTML
- **Smart Summaries:** URL summaries, category breakdowns
- **Beautiful HTML:** Styled, interactive HTML reports

**Key Classes:**
- `ReportGenerator`: Handles all report generation

### 5. SEOOrchestrator (`src/core/seo_orchestrator.py`)
**Responsibility:** Coordinate all components
- **Single URL Analysis:** Analyze one URL
- **Multiple URL Analysis:** Batch processing
- **Crawl + Analysis:** Discover URLs then analyze
- **Comprehensive Reports:** Auto-generate all report formats

**Key Classes:**
- `SEOOrchestrator`: Main coordinator class

## Usage Examples

### Simple Single URL Analysis
```python
from src import SEOOrchestrator

with SEOOrchestrator() as orchestrator:
    # Analyze single URL
    results = orchestrator.analyze_single_url("https://example.com")
    
    # Generate reports
    orchestrator.generate_reports(formats=['csv', 'excel', 'html'])
    
    # Print summary
    orchestrator.print_summary()
```

### Multiple URL Analysis
```python
from src import SEOOrchestrator

urls = [
    "https://example.com",
    "https://example.com/about",
    "https://example.com/contact"
]

with SEOOrchestrator() as orchestrator:
    summary = orchestrator.analyze_multiple_urls(urls)
    orchestrator.generate_reports()
```

### Crawl and Analyze
```python
from src import SEOOrchestrator

with SEOOrchestrator() as orchestrator:
    summary = orchestrator.analyze_with_crawling(
        start_urls=["https://example.com"],
        max_depth=2,
        max_urls=50
    )
    orchestrator.generate_reports()
```

### Command Line
```bash
# Single URL
python seo_analysis.py --url https://example.com

# Multiple URLs
python seo_analysis.py --urls https://example.com https://test.com

# From file
python seo_analysis.py --url-file urls.txt

# With crawling
python seo_analysis.py --url https://example.com --crawl --depth 3 --max-urls 100

# Custom formats
python seo_analysis.py --url https://example.com --formats csv excel json html
```

## Design Principles

1. **Separation of Concerns:** Each class has one clear responsibility
2. **Dependency Injection:** Components can be easily swapped
3. **Context Managers:** Automatic resource cleanup
4. **Testability:** All components have unit tests
5. **Extensibility:** Easy to add new tests, reports, or crawlers
6. **Type Hints:** Full type annotations for IDE support
7. **Error Handling:** Graceful error handling throughout

## Test Coverage

- **ContentFetcher:** 4 tests - fetch operations, error handling
- **SEOTestExecutor:** 13 tests - all test types, result formatting
- **SEOOrchestrator:** 5 tests - single/multiple URL analysis, stats
- **Total:** 22 tests, all passing ✅

## Adding New Tests

To add a new SEO test:

1. Add test method to `SEOTestExecutor` class:
```python
def _test_my_new_feature(self, content: PageContent) -> TestResult:
    # Test logic here
    return TestResult(
        url=content.url,
        test_id='my_new_feature',
        test_name='My New Feature',
        category='Technical SEO',
        status=TestStatus.PASS,  # or FAIL, WARNING
        severity='High',
        issue_description='Feature works correctly',
        recommendation='Keep it up!',
        score='100%'
    )
```

2. Register in `_register_test_methods()`:
```python
'my_new_feature': self._test_my_new_feature,
```

Done! The test will automatically run on all analyzed URLs.

## Performance

- **Static Analysis:** ~1-2 seconds per URL
- **Rendered Analysis:** ~3-5 seconds per URL (includes JavaScript)
- **Memory:** Efficient - processes one URL at a time
- **Scalable:** Can analyze hundreds of URLs in batch

## Requirements

- Python 3.10+
- requests, beautifulsoup4, lxml
- playwright (optional, for JavaScript rendering)
- pandas, openpyxl (for Excel reports)
- rich (for beautiful console output)

See `requirements.txt` for full list.

