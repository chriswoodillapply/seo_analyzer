# SEO Analyzer Testing Guide

## Overview

This guide covers the comprehensive testing framework for the SEO Analyzer, designed to ensure accurate analysis of websites like **www.applydigital.com** and proper handling of various edge cases.

## Test Architecture

### 1. **Unit Test Framework** (`test_seo_analyzer.py`)

The testing framework covers:

- **Positive Test Cases**: Successful analysis scenarios
- **Negative Test Cases**: Error handling (308 redirects, 500 errors)  
- **Performance Tests**: DOM complexity, render-blocking resources
- **Security Tests**: Missing security headers detection
- **Integration Tests**: Real-world URL testing

### 2. **Test Categories**

#### **Positive Testing (`TestSEOAnalyzerPositive`)**
Tests successful SEO analysis with proper HTML:
- ✅ Meta tag analysis (title, description, canonical)
- ✅ Header structure validation (H1-H6)
- ✅ Accessibility compliance
- ✅ Image optimization
- ✅ Performance metrics

#### **Negative Testing (`TestSEOAnalyzerNegative`)**
Tests error scenarios based on applydigital.com findings:
- ❌ **308 Redirects**: `/work` and `/ai` endpoints
- ❌ **500 Server Errors**: `/events/advertising-week-new-york-2025/`
- 🔍 **Soft 404 Detection**: Pages returning 200 but showing error content
- 🔒 **Missing Security Headers**: Content-Security-Policy detection

#### **Performance Testing (`TestSEOAnalyzerPerformance`)**
Advanced performance analysis:
- 📊 DOM complexity (3000+ elements flagged)
- 🚫 Render-blocking resources detection
- ⚡ Load time optimization
- 🖼️ Image lazy loading assessment

#### **Security Testing (`TestSEOAnalyzerSecurityHeaders`)**
Security header analysis (addresses applydigital.com CSP issue):
- 🔐 Content-Security-Policy detection
- 🛡️ X-Frame-Options validation
- 🔒 Strict-Transport-Security checking
- ⚠️ Security score calculation

## Real-World Test Cases

Based on **www.applydigital.com** analysis:

| URL | Expected Behavior | Test Coverage |
|-----|------------------|---------------|
| `https://www.applydigital.com/` | ✅ 200 Response | Full SEO analysis |
| `https://www.applydigital.com/work` | ❌ 308 Redirect | Error handling |
| `https://www.applydigital.com/ai` | ❌ 308 Redirect | Redirect detection |
| `https://www.applydigital.com/events/...` | ❌ 500 Error | Server error handling |
| Security Headers | ❌ Missing CSP | Security analysis |

## Running Tests

### **Full Test Suite**
```bash
python run_tests.py
```

### **Specific Test Categories**
```bash
python run_tests.py positive     # Successful scenarios
python run_tests.py negative     # Error scenarios  
python run_tests.py performance  # Performance analysis
python run_tests.py security     # Security headers
```

### **Integration Tests** (Real URLs)
```bash
python run_tests.py --applydigital
```

### **Demo Script**
```bash
python test_demo.py
```

## Mock Testing Strategy

### **MockResponse Class**
Simulates HTTP responses without hitting real servers:
```python
MockResponse(
    status_code=200,
    content="<html>...</html>",
    headers={'X-Frame-Options': 'DENY'},
    elapsed_seconds=1.2
)
```

### **Test Fixtures**
Pre-defined HTML content for testing:
- ✅ **Good HTML**: Proper SEO structure
- ❌ **Slow HTML**: Performance issues  
- 🔍 **Soft 404 HTML**: Error page content
- 🔒 **Security Headers**: Missing/present combinations

## Security Header Testing

Specifically tests **applydigital.com's missing CSP header**:

```python
def test_missing_security_headers(self):
    """Test detection of missing security headers like CSP"""
    headers = {
        'x-frame-options': 'DENY',
        'x-content-type-options': 'nosniff'
        # Missing: Content-Security-Policy
    }
    
    security_result = analyze_security_headers(headers)
    self.assertFalse(security_result['csp_header'])
    self.assertIn("Missing Content-Security-Policy header", 
                  security_result['issues'])
```

## Advanced Features Tested

### **Soft 404 Detection**
- Content analysis for error keywords
- Title tag error indicators  
- Navigation structure validation
- Confidence scoring (0-100%)

### **Axe-Core Integration**
- Industry-standard accessibility testing
- WCAG compliance validation
- Impact severity classification
- Professional recommendations

### **Performance Analysis**
- DOM complexity scoring
- Render-blocking resource detection
- Image optimization assessment
- Critical resource hints analysis

## Test Coverage

| Feature | Unit Tests | Integration Tests | Mock Tests |
|---------|------------|------------------|------------|
| Meta Analysis | ✅ | ✅ | ✅ |
| Headers | ✅ | ✅ | ✅ |
| Images | ✅ | ✅ | ✅ |
| Links | ✅ | ✅ | ✅ |
| Content | ✅ | ✅ | ✅ |
| Technical SEO | ✅ | ✅ | ✅ |
| Security Headers | ✅ | ✅ | ✅ |
| Performance | ✅ | ✅ | ✅ |
| Accessibility | ✅ | ✅ | ✅ |
| Axe-Core | ✅ | ⚠️ | ✅ |
| Soft 404s | ✅ | ✅ | ✅ |

## Continuous Testing

### **Automated Validation**
The test suite validates:
- All SEO analysis functions work correctly
- Error scenarios are handled gracefully
- Performance metrics are accurate
- Security issues are detected
- Accessibility compliance is measured

### **Real-World Validation**
Integration tests ensure the analyzer works with:
- Modern websites (Apply Digital)
- Various HTTP status codes
- Different security configurations
- Performance optimization levels

## Expected Results

### **Apply Digital Homepage Analysis**
- ✅ Good meta tags and structure
- ⚠️ Missing Content-Security-Policy header
- ✅ Proper accessibility elements
- ✅ Reasonable performance scores

### **Error Page Handling**
- ❌ 308/500 errors handled gracefully
- 🔍 Soft 404s detected with confidence scoring
- ⚡ Fast analysis even with errors

The testing framework ensures the SEO Analyzer provides accurate, professional-grade website analysis comparable to commercial SEO audit tools.

