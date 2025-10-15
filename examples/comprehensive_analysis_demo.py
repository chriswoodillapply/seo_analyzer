#!/usr/bin/env python3
"""
Comprehensive SEO Analysis Demo

Demonstrates all the new features implemented:
1. Cross-page duplicate detection
2. SERP preview analysis
3. Mobile usability testing
4. Broken link detection
5. Site architecture analysis
6. Enhanced header/meta/image/link analysis
"""

from seo_analyzer import SEOAnalyzer, SiteAnalyzer
import sys
import time

def demo_single_page_analysis(url):
    """Demonstrate comprehensive single page analysis"""
    print(f"\n{'='*80}")
    print(f"🔍 SINGLE PAGE COMPREHENSIVE ANALYSIS")
    print(f"{'='*80}")
    print(f"Analyzing: {url}")
    
    # Initialize analyzer with all features enabled
    analyzer = SEOAnalyzer(
        url=url,
        use_axe=False,  # Disable for faster demo
        headless=True
    )
    
    try:
        # Run comprehensive analysis
        results = analyzer.run_analysis()
        
        if results:
            # Display results
            analyzer.display_results()
            
            # Show new feature highlights
            print(f"\n🎯 NEW FEATURE HIGHLIGHTS:")
            print("=" * 50)
            
            # SERP Preview Analysis
            serp_preview = results.get('serp_preview', {})
            if serp_preview:
                print(f"\n📱 SERP Preview Analysis:")
                print(f"   • SERP Score: {serp_preview.get('serp_score', 0)}%")
                print(f"   • Title Pixels: {serp_preview.get('title_pixels', 0)}px")
                print(f"   • Description Pixels: {serp_preview.get('description_pixels', 0)}px")
                print(f"   • Title Truncated: {'Yes' if serp_preview.get('title_truncated') else 'No'}")
                print(f"   • Description Truncated: {'Yes' if serp_preview.get('description_truncated') else 'No'}")
                
            # Mobile Usability Analysis
            mobile_usability = results.get('mobile_usability', {})
            if mobile_usability:
                print(f"\n📱 Mobile Usability Analysis:")
                print(f"   • Mobile Score: {mobile_usability.get('mobile_score', 0)}%")
                print(f"   • Viewport Configured: {'Yes' if mobile_usability.get('viewport_configured') else 'No'}")
                print(f"   • Illegible Font Issues: {len(mobile_usability.get('illegible_font_sizes', []))}")
                print(f"   • Touch Target Issues: {len(mobile_usability.get('target_size_issues', []))}")
                print(f"   • Content Sizing Issues: {len(mobile_usability.get('content_sizing_issues', []))}")
                
            # Enhanced Header Analysis
            header_analysis = results.get('header_analysis', {})
            if header_analysis:
                print(f"\n📋 Enhanced Header Analysis:")
                print(f"   • Non-Sequential Headers: {len(header_analysis.get('non_sequential_headers', []))}")
                print(f"   • Long Headers: {len(header_analysis.get('long_headers', []))}")
                print(f"   • Missing Headers: {header_analysis.get('missing_headers', [])}")
                
                # Show duplicate detection
                duplicates = header_analysis.get('duplicate_headers', {})
                if duplicates:
                    print(f"   • Duplicate Headers Found:")
                    for level, dups in duplicates.items():
                        print(f"     - {level.upper()}: {len(dups)} duplicates")
                        
            # Enhanced Meta Analysis
            meta_analysis = results.get('meta_analysis', {})
            if meta_analysis:
                print(f"\n🏷️ Enhanced Meta Analysis:")
                print(f"   • Title Same as H1: {'Yes' if meta_analysis.get('title_same_as_h1') else 'No'}")
                print(f"   • Title Pixels: {meta_analysis.get('title_pixels', 0)}px")
                print(f"   • Description Pixels: {meta_analysis.get('description_pixels', 0)}px")
                
            # Enhanced Link Analysis
            link_analysis = results.get('link_analysis', {})
            if link_analysis:
                print(f"\n🔗 Enhanced Link Analysis:")
                print(f"   • Non-Descriptive Anchors: {link_analysis.get('non_descriptive_anchors', 0)}")
                print(f"   • Missing Anchor Text: {link_analysis.get('missing_anchor_text', 0)}")
                print(f"   • High External Outlinks: {'Yes' if link_analysis.get('high_external_outlinks') else 'No'}")
                
            # Enhanced Image Analysis
            image_analysis = results.get('image_analysis', {})
            if image_analysis:
                print(f"\n🖼️ Enhanced Image Analysis:")
                print(f"   • Images Over 100KB: {image_analysis.get('images_over_100kb', 0)}")
                print(f"   • Long Alt Text: {image_analysis.get('long_alt_text', 0)}")
                
            print(f"\n💾 Analysis completed successfully!")
            return True
            
        else:
            print("❌ Single page analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during single page analysis: {e}")
        return False

def demo_site_wide_analysis(base_url, max_pages=5):
    """Demonstrate site-wide analysis with duplicate detection"""
    print(f"\n{'='*80}")
    print(f"🌐 SITE-WIDE COMPREHENSIVE ANALYSIS")
    print(f"{'='*80}")
    print(f"Analyzing: {base_url} (max {max_pages} pages)")
    
    # Initialize site analyzer
    site_analyzer = SiteAnalyzer(
        base_url=base_url,
        max_pages=max_pages,
        use_axe=False,  # Disable for faster demo
        headless=True
    )
    
    try:
        # Run site-wide analysis
        results = site_analyzer.analyze_site()
        
        if results:
            # Display results
            site_analyzer.display_site_results(results)
            
            # Show site-wide feature highlights
            print(f"\n🎯 SITE-WIDE FEATURE HIGHLIGHTS:")
            print("=" * 50)
            
            # Duplicate Analysis
            duplicate_analysis = results.get('duplicate_analysis', {})
            print(f"\n🔍 Cross-Page Duplicate Detection:")
            print(f"   • Duplicate Title Sets: {len(duplicate_analysis.get('duplicate_titles', []))}")
            print(f"   • Duplicate Description Sets: {len(duplicate_analysis.get('duplicate_descriptions', []))}")
            print(f"   • Duplicate H1 Sets: {len(duplicate_analysis.get('duplicate_h1s', []))}")
            print(f"   • Duplicate H2 Sets: {len(duplicate_analysis.get('duplicate_h2s', []))}")
            
            # Show some duplicate examples
            if duplicate_analysis.get('duplicate_titles'):
                print(f"\n   📝 Sample Duplicate Titles:")
                for i, dup in enumerate(duplicate_analysis['duplicate_titles'][:2], 1):
                    print(f"      {i}. '{dup['title'][:60]}...' (appears on {dup['count']} pages)")
                    
            # Broken Links
            broken_links = results.get('broken_links', [])
            print(f"\n🔗 Broken Link Detection:")
            print(f"   • Total Broken Links: {len(broken_links)}")
            if broken_links:
                print(f"   • Sample Broken Links:")
                for i, link in enumerate(broken_links[:3], 1):
                    status = link.get('status_code', 'Network Error')
                    print(f"      {i}. {link['url']} (Status: {status})")
                    
            # Site Architecture
            orphan_pages = results.get('orphan_pages', [])
            print(f"\n🏗️ Site Architecture Analysis:")
            print(f"   • Total Pages Analyzed: {results.get('pages_analyzed', 0)}")
            print(f"   • Orphan Pages Found: {len(orphan_pages)}")
            if orphan_pages:
                print(f"   • Sample Orphan Pages:")
                for page in orphan_pages[:3]:
                    print(f"      • {page}")
                    
            print(f"\n💾 Site-wide analysis completed successfully!")
            return True
            
        else:
            print("❌ Site-wide analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during site-wide analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive analysis demo"""
    
    # Test URLs
    test_urls = [
        "https://www.applydigital.com",
        "https://example.com"
    ]
    
    if len(sys.argv) > 1:
        test_urls = [sys.argv[1]]
        
    print("🚀 COMPREHENSIVE SEO ANALYSIS DEMO")
    print("=" * 80)
    print("This demo showcases all new features implemented:")
    print("• Cross-page duplicate detection")
    print("• SERP preview analysis with pixel-accurate truncation")
    print("• Mobile usability testing")
    print("• Enhanced header/meta/image/link analysis")
    print("• Broken link detection")
    print("• Site architecture analysis")
    print("• Orphan page detection")
    
    success_count = 0
    
    for url in test_urls:
        print(f"\n🎯 Testing with: {url}")
        
        # Single page analysis
        if demo_single_page_analysis(url):
            success_count += 1
            
        # Small delay between analyses
        time.sleep(2)
        
        # Site-wide analysis (limited to 5 pages for demo)
        if demo_site_wide_analysis(url, max_pages=5):
            success_count += 1
            
        # Separator
        print(f"\n{'='*80}")
        
    # Summary
    total_tests = len(test_urls) * 2  # 2 tests per URL
    print(f"\n📊 DEMO SUMMARY:")
    print(f"   • Tests Completed: {success_count}/{total_tests}")
    print(f"   • Success Rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print(f"\n✅ All demos completed successfully!")
        print(f"🎉 SEO Analyzer now has comprehensive Screaming Frog-level features!")
    else:
        print(f"\n⚠️ Some demos had issues - check output above")
        
    print(f"\n🚀 Ready for production SEO analysis!")

if __name__ == "__main__":
    main()

