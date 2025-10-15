#!/usr/bin/env python3
"""
Site-Wide SEO Analysis Demo

This script demonstrates comprehensive site-wide SEO analysis including:
- Cross-page duplicate detection
- Broken link analysis
- Site architecture analysis
- Orphan page detection
"""

from seo_analyzer import SiteAnalyzer
import sys

def main():
    """Run site-wide SEO analysis demo"""
    
    # Default to Apply Digital for testing
    test_url = "https://www.applydigital.com"
    
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
        
    print(f"\n🔍 Starting comprehensive site analysis for: {test_url}")
    print("=" * 80)
    
    # Initialize site analyzer
    # Use smaller max_pages for demo (10 pages)
    analyzer = SiteAnalyzer(
        base_url=test_url,
        max_pages=10,  # Limit for demo
        use_axe=False,  # Disable axe for faster analysis
        headless=True
    )
    
    try:
        # Run comprehensive site analysis
        results = analyzer.analyze_site()
        
        if results:
            # Display results
            analyzer.display_site_results(results)
            
            # Show detailed duplicate information
            print("\n🔍 DETAILED DUPLICATE ANALYSIS:")
            print("=" * 50)
            
            # Show all duplicate titles
            duplicate_titles = results['duplicate_analysis']['duplicate_titles']
            if duplicate_titles:
                print(f"\n📝 Found {len(duplicate_titles)} sets of duplicate titles:")
                for i, dup in enumerate(duplicate_titles, 1):
                    print(f"\n  {i}. Title: '{dup['title']}'")
                    print(f"     Found on {dup['count']} pages:")
                    for url in dup['urls']:
                        print(f"     • {url}")
                        
            # Show duplicate descriptions
            duplicate_descriptions = results['duplicate_analysis']['duplicate_descriptions']
            if duplicate_descriptions:
                print(f"\n📄 Found {len(duplicate_descriptions)} sets of duplicate descriptions:")
                for i, dup in enumerate(duplicate_descriptions, 1):
                    print(f"\n  {i}. Description: '{dup['description'][:100]}...'")
                    print(f"     Found on {dup['count']} pages:")
                    for url in dup['urls']:
                        print(f"     • {url}")
                        
            # Show duplicate H1s
            duplicate_h1s = results['duplicate_analysis']['duplicate_h1s']
            if duplicate_h1s:
                print(f"\n🏷️ Found {len(duplicate_h1s)} sets of duplicate H1s:")
                for i, dup in enumerate(duplicate_h1s, 1):
                    print(f"\n  {i}. H1: '{dup['h1']}'")
                    print(f"     Found on {dup['count']} pages:")
                    for url in dup['urls']:
                        print(f"     • {url}")
                        
            # Show broken links details
            broken_links = results.get('broken_links', [])
            if broken_links:
                print(f"\n🔗 Found {len(broken_links)} broken links:")
                for i, link in enumerate(broken_links, 1):
                    status = link.get('status_code', 'Network Error')
                    error = link.get('error', '')
                    print(f"\n  {i}. {link['url']}")
                    print(f"     Status: {status}")
                    if error:
                        print(f"     Error: {error}")
                    print(f"     Referenced by {len(link['source_pages'])} page(s):")
                    for source in link['source_pages'][:3]:  # Show first 3
                        print(f"     • {source}")
                    if len(link['source_pages']) > 3:
                        print(f"     ... and {len(link['source_pages']) - 3} more")
                        
            # Show orphan pages
            orphan_pages = results.get('orphan_pages', [])
            if orphan_pages:
                print(f"\n🏝️ Found {len(orphan_pages)} orphan pages (no internal links):")
                for page in orphan_pages:
                    print(f"  • {page}")
                    
            # Save results to JSON
            import json
            filename = f"site_analysis_{test_url.replace('https://', '').replace('http://', '').replace('/', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full results saved to: {filename}")
            
        else:
            print("❌ Analysis failed - no results returned")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

