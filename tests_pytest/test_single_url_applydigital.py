#!/usr/bin/env python3
"""
Single-URL Unit Test for ApplyDigital.com
Runs all tests against only https://www.applydigital.com with caching and minimal reporting.
"""

import pytest
import sys
import os
from datetime import datetime
from pathlib import Path

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.seo_orchestrator import SEOOrchestrator


class TestSingleUrlApplyDigital:
    """Run full test suite against a single URL with caching."""

    @pytest.fixture
    def orchestrator(self):
        return SEOOrchestrator(
            user_agent='SEO-Analyzer-Single-URL/1.0',
            timeout=45,
            headless=True,
            enable_javascript=True,
            output_dir='output/single_url_applydigital',
            verbose=True,
            enable_caching=True,
            cache_max_age_hours=24,
            save_css=True,
            force_refresh=False  # use cache for speed
        )

    def test_all_tests_single_url(self, orchestrator):
        url = 'https://www.applydigital.com'
        with orchestrator:
            results = orchestrator.analyze_single_url(url)

            # Basic assertions
            assert results is not None
            assert len(results) > 0

            # Generate minimal report (JSON only) in output folder
            from src.reporters.report_generator import ReportGenerator
            rg = ReportGenerator('output/single_url_applydigital')
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            base = f'seo_single_url_{ts}'
            json_path = rg.generate_json_report(orchestrator.get_results(), f'{base}.json')

            # Verify file created
            assert Path(json_path).exists()

            # Sanity: should include individual Lighthouse results
            import json
            with open(json_path, 'r') as f:
                data = json.load(f)
            # Support both schemas: list of results OR {summary, results}
            if isinstance(data, list):
                results_list = data
            else:
                # Support different key casings
                results_list = data.get('results', data.get('Results', []))
            assert len(results_list) > 0
            # Some reports use 'Test_ID' while others use 'test_id'
            def _get_test_id(entry):
                return entry.get('test_id') or entry.get('Test_ID') or entry.get('TestId') or ''
            assert any(str(_get_test_id(r)).startswith('lighthouse_') for r in results_list)
