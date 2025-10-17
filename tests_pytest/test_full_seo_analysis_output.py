#!/usr/bin/env python3
"""
Unit Tests for Full SEO Analysis with Proper Output Management
Tests that full SEO analysis runs correctly and outputs go to the output/ folder.
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


class TestFullSEOAnalysisOutput:
    """Test full SEO analysis with proper output management"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create SEO orchestrator for full analysis with proper output directory"""
        return SEOOrchestrator(
            user_agent='SEO-Analyzer-Test/1.0',
            timeout=60,
            headless=True,
            enable_javascript=True,
            output_dir='output/full_seo_analysis_test',
            verbose=True,
            enable_caching=True,
            cache_max_age_hours=1,
            save_css=True,
            force_refresh=True
        )
    
    def test_full_analysis_outputs_to_correct_folder(self, orchestrator):
        """Test that full analysis outputs go to the output/ folder"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            # Run full analysis
            summary = orchestrator.analyze_with_crawling(
                start_urls=[test_url],
                max_depth=3,  # Shallow for testing
                max_urls=10,  # Limited for testing
                test_ids=None  # Run all tests
            )
            
            # Verify analysis completed
            assert summary is not None
            assert summary['successful'] > 0
            assert summary['total_tests'] > 0
            
            # Generate reports explicitly
            from src.reporters.report_generator import ReportGenerator
            report_generator = ReportGenerator('output/full_seo_analysis_test')
            
            # Get all results from the orchestrator
            all_results = orchestrator.test_executor.get_results()
            assert len(all_results) > 0, "Should have test results"
            
            # Generate reports
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_filename = f"seo_analysis_test_{timestamp}"
            
            # Generate all report formats
            csv_path = report_generator.generate_csv_report(all_results, f"{base_filename}.csv")
            excel_path = report_generator.generate_excel_report(all_results, f"{base_filename}.xlsx")
            json_path = report_generator.generate_json_report(all_results, f"{base_filename}.json")
            html_path = report_generator.generate_html_report(all_results, f"{base_filename}.html")
            
            # Check that output directory was created
            output_dir = Path('output/full_seo_analysis_test')
            assert output_dir.exists(), "Output directory should exist"
            
            # Check for expected output files
            csv_files = list(output_dir.glob('*.csv'))
            excel_files = list(output_dir.glob('*.xlsx'))
            json_files = list(output_dir.glob('*.json'))
            html_files = list(output_dir.glob('*.html'))
            
            assert len(csv_files) > 0, f"Should generate CSV reports, found: {csv_files}"
            assert len(excel_files) > 0, f"Should generate Excel reports, found: {excel_files}"
            assert len(json_files) > 0, f"Should generate JSON reports, found: {json_files}"
            assert len(html_files) > 0, f"Should generate HTML reports, found: {html_files}"
    
    def test_individual_results_in_output_files(self, orchestrator):
        """Test that output files contain individual results, not summaries"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            # Run analysis
            summary = orchestrator.analyze_with_crawling(
                start_urls=[test_url],
                max_depth=2,
                max_urls=5,
                test_ids=None
            )
            
            # Check CSV file for individual results
            output_dir = Path('output/full_seo_analysis_test')
            csv_files = list(output_dir.glob('*.csv'))
            assert len(csv_files) > 0, "Should have CSV files"
            
            # Read CSV and check for individual Lighthouse results
            csv_file = csv_files[0]
            with open(csv_file, 'r') as f:
                csv_content = f.read()
                
            # Should have individual Lighthouse results
            assert 'lighthouse_first-contentful-paint' in csv_content, "Should have individual Lighthouse results"
            assert 'lighthouse_largest-contentful-paint' in csv_content, "Should have individual Lighthouse results"
            
            # Should have individual Axe-core results
            assert 'axe_heading-order' in csv_content, "Should have individual Axe-core results"
            assert 'axe_color-contrast' in csv_content, "Should have individual Axe-core results"
            
            # Should NOT have summary results
            assert 'Lighthouse found' not in csv_content, "Should not have summary results"
            assert 'Axe-core found' not in csv_content, "Should not have summary results"
    
    def test_output_files_have_proper_structure(self, orchestrator):
        """Test that output files have proper structure and content"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            # Run analysis
            summary = orchestrator.analyze_with_crawling(
                start_urls=[test_url],
                max_depth=2,
                max_urls=5,
                test_ids=None
            )
            
            # Check Excel file structure
            output_dir = Path('output/full_seo_analysis_test')
            excel_files = list(output_dir.glob('*.xlsx'))
            assert len(excel_files) > 0, "Should have Excel files"
            
            # Check JSON file structure
            json_files = list(output_dir.glob('*.json'))
            assert len(json_files) > 0, "Should have JSON files"
            
            # Read JSON and verify structure
            json_file = json_files[0]
            import json
            with open(json_file, 'r') as f:
                json_data = json.load(f)
            
            # Should have proper structure
            assert 'summary' in json_data, "JSON should have summary"
            assert 'results' in json_data, "JSON should have results"
            assert len(json_data['results']) > 0, "Should have results"
            
            # Check that results are individual
            individual_results = [r for r in json_data['results'] if r.get('test_id', '').startswith('lighthouse_')]
            assert len(individual_results) > 0, "Should have individual Lighthouse results"
    
    def test_caching_works_with_output_folder(self, orchestrator):
        """Test that caching works properly with output folder structure"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            # First run - should create cache
            summary1 = orchestrator.analyze_with_crawling(
                start_urls=[test_url],
                max_depth=2,
                max_urls=5,
                test_ids=None
            )
            
            # Check cache directories exist
            output_dir = Path('output/full_seo_analysis_test')
            content_cache = output_dir / 'content_cache'
            crawl_cache = output_dir / 'crawl_cache'
            
            assert content_cache.exists(), "Content cache should exist"
            assert crawl_cache.exists(), "Crawl cache should exist"
            
            # Second run - should use cache (faster)
            start_time = datetime.now()
            summary2 = orchestrator.analyze_with_crawling(
                start_urls=[test_url],
                max_depth=2,
                max_urls=5,
                test_ids=None
            )
            end_time = datetime.now()
            
            # Should be faster on second run (using cache)
            execution_time = (end_time - start_time).total_seconds()
            assert execution_time < 30, f"Second run should be faster with cache: {execution_time}s"
            
            # Results should be similar
            assert summary1['total_tests'] == summary2['total_tests'], "Should have same number of tests"
    
    def test_output_folder_cleanup(self, orchestrator):
        """Test that output folder can be cleaned up properly"""
        test_url = 'https://www.applydigital.com'
        
        with orchestrator:
            # Run analysis
            summary = orchestrator.analyze_with_crawling(
                start_urls=[test_url],
                max_depth=2,
                max_urls=5,
                test_ids=None
            )
            
            # Check output directory exists
            output_dir = Path('output/full_seo_analysis_test')
            assert output_dir.exists(), "Output directory should exist"
            
            # Clean up
            import shutil
            if output_dir.exists():
                shutil.rmtree(output_dir)
            
            assert not output_dir.exists(), "Output directory should be cleaned up"
