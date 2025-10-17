#!/usr/bin/env python3
"""
Pytest Configuration for SEO Analyzer Tests
Ensures all tests use proper output directory structure and cleanup.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment with proper output directory structure"""
    # Ensure output directory exists
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Create test-specific subdirectories
    test_dirs = [
        'output/test_lighthouse_results',
        'output/test_axe_core_results', 
        'output/full_seo_analysis_test',
        'output/full_applydigital_analysis',
        'output/single_url_applydigital'
    ]
    
    for test_dir in test_dirs:
        Path(test_dir).mkdir(parents=True, exist_ok=True)
    
    yield

    # Optional cleanup after all tests (disabled by default)
    clean_outputs = os.environ.get('CLEAN_TEST_OUTPUTS', '0') in ('1', 'true', 'True')
    if clean_outputs:
        print("\n🧹 Cleaning up test output directories (CLEAN_TEST_OUTPUTS=1)...")
        for test_dir in test_dirs:
            if Path(test_dir).exists():
                shutil.rmtree(test_dir)
                print(f"  ✅ Cleaned {test_dir}")


@pytest.fixture
def test_output_dir():
    """Provide a test-specific output directory"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    test_dir = f'output/test_run_{timestamp}'
    Path(test_dir).mkdir(parents=True, exist_ok=True)
    return test_dir


@pytest.fixture(autouse=True)
def cleanup_after_test(test_output_dir):
    """Clean up test output after each test"""
    yield
    # Cleanup is handled by the session fixture
    pass


def pytest_configure(config):
    """Configure pytest with custom markers and settings"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "lighthouse: marks tests that use Lighthouse"
    )
    config.addinivalue_line(
        "markers", "axe_core: marks tests that use Axe-core"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names"""
    for item in items:
        # Add markers based on test names
        if "lighthouse" in item.name.lower():
            item.add_marker(pytest.mark.lighthouse)
        if "axe_core" in item.name.lower() or "axe" in item.name.lower():
            item.add_marker(pytest.mark.axe_core)
        if "full" in item.name.lower() or "integration" in item.name.lower():
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)
