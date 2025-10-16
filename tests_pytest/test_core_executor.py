import pytest
import sys
import os
from bs4 import BeautifulSoup

# Add the seo_analyzer directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.test_interface import PageContent, TestStatus, TestResult, SEOTest
from src.core.test_registry import TestRegistry
from src.core.seo_test_executor import SEOTestExecutor


class DummyTest(SEOTest):
    @property
    def test_id(self) -> str:
        return "dummy_test"

    @property
    def test_name(self) -> str:
        return "Dummy Test"

    @property
    def category(self) -> str:
        return "Testing"

    @property
    def severity(self) -> str:
        return "Info"

    def execute(self, content: PageContent, crawl_context=None):
        # simple deterministic behavior: PASS if title exists, FAIL otherwise
        soup = content.static_soup
        title = soup.title.string if soup.title else None
        status = TestStatus.PASS if title else TestStatus.FAIL
        return self._create_result(content, status, "", "", "0/1")


@pytest.fixture
def sample_content():
    html = """
    <html><head><title>Example</title></head><body><h1>Hi</h1></body></html>
    """
    soup = BeautifulSoup(html, 'html.parser')
    return PageContent(
        url="https://example.com",
        static_html=html,
        static_soup=soup,
        rendered_html=html,
        rendered_soup=soup,
        static_headers={"content-type": "text/html"},
        static_load_time=0.1,
        rendered_load_time=0.2,
        performance_metrics={},
        core_web_vitals={}
    )


def test_registry_register_and_get():
    reg = TestRegistry()
    dt = DummyTest()
    reg.register(dt)

    assert reg.get_test_count() == 1
    assert reg.get_test_by_id('dummy_test') is dt
    assert reg.get_tests_by_category('Testing')[0] is dt


def test_executor_v2_runs_registered_test(sample_content):
    reg = TestRegistry()
    reg.register(DummyTest())
    exec = SEOTestExecutor(reg)

    results = exec.execute_all_tests(sample_content)
    assert isinstance(results, list)
    assert len(results) == 1
    r = results[0]
    assert isinstance(r, TestResult)
    assert r.status == TestStatus.PASS


def test_executor_specific_test_by_id(sample_content):
    reg = TestRegistry()
    reg.register(DummyTest())
    exec = SEOTestExecutor(reg)

    results = exec.execute_specific_tests(sample_content, ['dummy_test'])
    assert len(results) == 1
    assert results[0].test_id == 'dummy_test'
