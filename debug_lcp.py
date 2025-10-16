#!/usr/bin/env python3
"""Debug LCP measurement"""

from playwright.sync_api import sync_playwright
import time

url = "https://www.applydigital.com"

print('\n' + '='*80)
print('  DEBUGGING LCP MEASUREMENT')
print('='*80)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print(f'\n1. Navigating to {url}...')
    page.goto(url, wait_until='networkidle')
    
    print('2. Waiting 5 seconds for LCP to stabilize...')
    page.wait_for_timeout(5000)
    
    print('3. Checking what Performance API entries are available...')
    
    result = page.evaluate('''() => {
        const debug = {};
        
        // Check supported entry types
        debug.supportedTypes = PerformanceObserver.supportedEntryTypes || [];
        
        // Try to get all entry types
        const allTypes = ['largest-contentful-paint', 'paint', 'layout-shift', 'navigation', 'resource'];
        debug.availableEntries = {};
        
        for (const type of allTypes) {
            try {
                const entries = performance.getEntriesByType(type);
                debug.availableEntries[type] = entries.length;
                if (type === 'largest-contentful-paint' && entries.length > 0) {
                    const lcp = entries[entries.length - 1];
                    debug.lcpDetails = {
                        startTime: lcp.startTime,
                        size: lcp.size,
                        renderTime: lcp.renderTime,
                        loadTime: lcp.loadTime,
                        url: lcp.url || 'N/A',
                        element: lcp.element ? lcp.element.tagName : 'N/A'
                    };
                }
            } catch (e) {
                debug.availableEntries[type] = 'ERROR: ' + e.message;
            }
        }
        
        return debug;
    }''')
    
    print('\n4. RESULTS:')
    print('-' * 80)
    print(f'Supported Entry Types: {result.get("supportedTypes", [])}')
    print(f'\nAvailable Entries:')
    for entry_type, count in result.get('availableEntries', {}).items():
        print(f'  {entry_type}: {count}')
    
    if 'lcpDetails' in result:
        print(f'\nLCP Details:')
        for key, value in result['lcpDetails'].items():
            print(f'  {key}: {value}')
    else:
        print('\n[WARNING] No LCP entries found!')
        print('This could mean:')
        print('  - Browser doesn\'t support LCP')
        print('  - Page loaded too quickly')
        print('  - No contentful elements rendered')
    
    browser.close()

print('='*80 + '\n')

