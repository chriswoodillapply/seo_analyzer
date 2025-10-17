#!/usr/bin/env python3
"""
End-to-End Unit Test for ApplyDigital.com
Comprehensive test that verifies the entire SEO analysis pipeline works correctly.
"""

import pytest
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator
from src.core.test_interface import TestResult, TestStatus, TestSeverity


class TestEndToEndApplyDigital:
    """End-to-end test for ApplyDigital.com with comprehensive verification"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create SEO orchestrator for end-to-end testing"""
        return SEOOrchestrator(
            user_agent='SEO-Analyzer-E2E/1.0',
            timeout=60,
            headless=True,
            enable_javascript=True,
            output_dir='output/end_to_end_applydigital',
            verbose=True,
            enable_caching=True,
            cache_max_age_hours=24,
            save_css=True,
            force_refresh=True
        )
    
    def test_comprehensive_applydigital_analysis(self, orchestrator):
        """Test comprehensive analysis of ApplyDigital.com with individual results verification"""
        print("\n🚀 END-TO-END TEST - ApplyDigital.com")
        print("="*80)
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🌐 Target: https://www.applydigital.com")
        print("🧪 Tests: All 82 streamlined tests with individual results")
        print("="*80)
        
        with orchestrator:
            # Run comprehensive analysis
            print("🔍 Starting comprehensive analysis...")
            start_time = datetime.now()
            
            summary = orchestrator.analyze_with_crawling(
                start_urls=['https://www.applydigital.com'],
                max_depth=5,  # Deep crawl
                max_urls=50,  # Comprehensive but manageable
                test_ids=None  # Run all tests
            )
            
            analysis_time = datetime.now() - start_time
            print(f"✅ Analysis completed in {analysis_time.total_seconds():.2f}s")
            
            # Verify analysis completed successfully
            assert summary is not None, "Analysis should return summary"
            assert summary['successful'] > 0, "Should have successful results"
            assert summary['total_tests'] > 0, "Should have executed tests"
            
            print(f"📊 Results Summary:")
            print(f"  Successful: {summary['successful']}")
            print(f"  Failed: {summary['failed']}")
            print(f"  Total Tests: {summary['total_tests']}")
            
            # Get detailed results
            all_results = orchestrator.test_executor.get_results()
            assert len(all_results) > 0, "Should have individual results"
            
            print(f"  Individual Results: {len(all_results)}")
            
            # Analyze individual results
            lighthouse_results = [r for r in all_results if r.test_id.startswith('lighthouse_')]
            axe_results = [r for r in all_results if r.test_id.startswith('axe_')]
            
            print(f"\n🔍 Individual Results Breakdown:")
            print(f"  Lighthouse: {len(lighthouse_results)} individual audits")
            print(f"  Axe-core: {len(axe_results)} individual violations")
            print(f"  Other Tests: {len(all_results) - len(lighthouse_results) - len(axe_results)} results")
            
            # Verify individual results are working
            assert len(lighthouse_results) > 0, "Should have individual Lighthouse results"
            assert len(axe_results) > 0, "Should have individual Axe-core results"
            
            # Verify no summary results
            summary_results = [r for r in all_results if 'Lighthouse found' in r.issue_description or 'Axe-core found' in r.issue_description]
            assert len(summary_results) == 0, f"Should not have summary results, found: {len(summary_results)}"
            
            print("✅ SUCCESS: Individual results working correctly!")
            
            # Show sample individual results
            if lighthouse_results:
                print(f"\n📋 Sample Lighthouse Results:")
                for i, result in enumerate(lighthouse_results[:5], 1):
                    print(f"  {i}. {result.test_name}")
                    print(f"     Status: {result.status.value} | Score: {result.score}")
                    print(f"     Issue: {result.issue_description[:60]}...")
            
            if axe_results:
                print(f"\n📋 Sample Axe-core Results:")
                for i, result in enumerate(axe_results[:3], 1):
                    print(f"  {i}. {result.test_name}")
                    print(f"     Status: {result.status.value} | Score: {result.score}")
                    print(f"     Issue: {result.issue_description[:60]}...")
            
            # Generate reports
            print(f"\n📋 Generating Reports...")
            from src.reporters.report_generator import ReportGenerator
            report_generator = ReportGenerator('output/end_to_end_applydigital')
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f'seo_e2e_applydigital_{timestamp}'
            
            csv_path = report_generator.generate_csv_report(all_results, f'{base_filename}.csv')
            excel_path = report_generator.generate_excel_report(all_results, f'{base_filename}.xlsx')
            json_path = report_generator.generate_json_report(all_results, f'{base_filename}.json')
            html_path = report_generator.generate_html_report(all_results, f'{base_filename}.html')
            
            print(f"✅ Reports generated:")
            print(f"  CSV: {csv_path}")
            print(f"  Excel: {excel_path}")
            print(f"  JSON: {json_path}")
            print(f"  HTML: {html_path}")
            
            # Verify output files exist
            output_dir = Path('output/end_to_end_applydigital')
            assert output_dir.exists(), "Output directory should exist"
            
            csv_files = list(output_dir.glob('*.csv'))
            excel_files = list(output_dir.glob('*.xlsx'))
            json_files = list(output_dir.glob('*.json'))
            html_files = list(output_dir.glob('*.html'))
            
            assert len(csv_files) > 0, "Should generate CSV reports"
            assert len(excel_files) > 0, "Should generate Excel reports"
            assert len(json_files) > 0, "Should generate JSON reports"
            assert len(html_files) > 0, "Should generate HTML reports"
            
            # Verify individual results in JSON file
            print(f"\n🔍 Verifying Individual Results in Output Files...")
            import json
            with open(json_files[0], 'r') as f:
                json_data = json.load(f)
            
            individual_lighthouse = [r for r in json_data['results'] if r.get('test_id', '').startswith('lighthouse_')]
            individual_axe = [r for r in json_data['results'] if r.get('test_id', '').startswith('axe_')]
            
            print(f"  JSON Lighthouse Results: {len(individual_lighthouse)}")
            print(f"  JSON Axe-core Results: {len(individual_axe)}")
            
            assert len(individual_lighthouse) > 0, "JSON should contain individual Lighthouse results"
            assert len(individual_axe) > 0, "JSON should contain individual Axe-core results"
            
            # Check for summary results in JSON (should be none)
            json_summary_results = [r for r in json_data['results'] if 'Lighthouse found' in r.get('issue_description', '') or 'Axe-core found' in r.get('issue_description', '')]
            assert len(json_summary_results) == 0, f"JSON should not contain summary results, found: {len(json_summary_results)}"
            
            print("✅ SUCCESS: Individual results verified in output files!")
            
            # Verify test categories
            categories = set()
            for result in all_results:
                categories.add(result.category)
            
            print(f"\n📊 Test Categories: {len(categories)}")
            for category in sorted(categories):
                category_results = [r for r in all_results if r.category == category]
                print(f"  {category}: {len(category_results)} results")
            
            # Verify severity levels
            severities = set()
            for result in all_results:
                severities.add(result.severity)
            
            print(f"\n📊 Severity Levels: {len(severities)}")
            for severity in sorted(severities):
                severity_results = [r for r in all_results if r.severity == severity]
                print(f"  {severity}: {len(severity_results)} results")
            
            total_time = datetime.now() - start_time
            print(f"\n✅ END-TO-END TEST COMPLETE!")
            print(f"📅 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⏱️  Total time: {total_time.total_seconds():.2f}s ({total_time.total_seconds()/60:.1f} minutes)")
            print(f"📁 Output directory: output/end_to_end_applydigital/")
            print("="*80)
    
    def test_individual_results_quality(self, orchestrator):
        """Test that individual results have proper quality and detail"""
        with orchestrator:
            # Run analysis
            summary = orchestrator.analyze_with_crawling(
                start_urls=['https://www.applydigital.com'],
                max_depth=3,
                max_urls=10,
                test_ids=None
            )
            
            all_results = orchestrator.test_executor.get_results()
            lighthouse_results = [r for r in all_results if r.test_id.startswith('lighthouse_')]
            axe_results = [r for r in all_results if r.test_id.startswith('axe_')]
            
            # Verify Lighthouse results have detailed information
            for result in lighthouse_results:
                assert result.test_name.startswith('Lighthouse:'), f"Lighthouse result should have proper name: {result.test_name}"
                assert result.score is not None, f"Lighthouse result should have score: {result.test_id}"
                assert '%' in result.score, f"Lighthouse score should be percentage: {result.score}"
                assert len(result.recommendation) > 20, f"Lighthouse recommendation should be detailed: {result.recommendation}"
                assert result.category in ['Performance', 'Accessibility', 'Meta Tags', 'Security', 'Technical SEO'], f"Lighthouse category should be valid: {result.category}"
            
            # Verify Axe-core results have detailed information
            for result in axe_results:
                assert result.test_name.startswith('Axe-core:'), f"Axe-core result should have proper name: {result.test_name}"
                assert result.score is not None, f"Axe-core result should have score: {result.test_id}"
                assert 'Impact:' in result.score, f"Axe-core score should have impact: {result.score}"
                assert len(result.recommendation) > 20, f"Axe-core recommendation should be detailed: {result.recommendation}"
                assert result.category == 'Accessibility', f"Axe-core category should be Accessibility: {result.category}"
    
    def test_output_file_structure(self, orchestrator):
        """Test that output files have proper structure and content"""
        with orchestrator:
            # Run analysis
            summary = orchestrator.analyze_with_crawling(
                start_urls=['https://www.applydigital.com'],
                max_depth=2,
                max_urls=5,
                test_ids=None
            )
            
            all_results = orchestrator.test_executor.get_results()
            
            # Generate reports
            from src.reporters.report_generator import ReportGenerator
            report_generator = ReportGenerator('output/end_to_end_applydigital')
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f'seo_structure_test_{timestamp}'
            
            csv_path = report_generator.generate_csv_report(all_results, f'{base_filename}.csv')
            json_path = report_generator.generate_json_report(all_results, f'{base_filename}.json')
            
            # Verify CSV structure
            import csv
            with open(csv_path, 'r') as f:
                csv_reader = csv.DictReader(f)
                csv_rows = list(csv_reader)
                
            assert len(csv_rows) > 0, "CSV should have rows"
            assert 'test_id' in csv_rows[0], "CSV should have test_id column"
            assert 'test_name' in csv_rows[0], "CSV should have test_name column"
            assert 'status' in csv_rows[0], "CSV should have status column"
            
            # Verify JSON structure
            import json
            with open(json_path, 'r') as f:
                json_data = json.load(f)
                
            assert 'summary' in json_data, "JSON should have summary"
            assert 'results' in json_data, "JSON should have results"
            assert len(json_data['results']) > 0, "JSON should have results"
            
            # Verify individual results in JSON
            individual_results = [r for r in json_data['results'] if r.get('test_id', '').startswith(('lighthouse_', 'axe_'))]
            assert len(individual_results) > 0, "JSON should contain individual results"
