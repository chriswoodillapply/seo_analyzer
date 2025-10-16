#!/usr/bin/env python3
"""
Lighthouse Comprehensive Audit Test

This test runs Google Lighthouse and returns multiple results for each audit.
Lighthouse provides comprehensive performance, accessibility, SEO, and best practices audits.
"""

from typing import List, Optional, Dict, Any
from src.core.test_interface import SEOTest, TestResult, TestStatus, TestCategory, TestSeverity
from src.core.test_interface import PageContent
from src.integrations.lighthouse import LighthouseIntegration
import subprocess
import json
import tempfile
from pathlib import Path


class LighthouseAuditTest(SEOTest):
    """
    Comprehensive Lighthouse audit test that returns multiple results.
    
    This test runs Google Lighthouse and creates individual TestResult objects
    for each failing audit, providing detailed recommendations.
    """
    
    @property
    def test_id(self) -> str:
        return "lighthouse_audit"
    
    @property
    def test_name(self) -> str:
        return "Lighthouse Comprehensive Audit"
    
    @property
    def category(self) -> str:
        return TestCategory.PERFORMANCE
    
    @property
    def severity(self) -> str:
        return TestSeverity.HIGH
    
    def execute(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> Optional[TestResult]:
        """Single result fallback - returns overall Lighthouse score"""
        results = self.execute_multiple(content, crawl_context)
        if not results:
            return None
        
        # Return a summary result
        total_issues = len(results)
        failed_audits = [r for r in results if r.status == TestStatus.FAIL]
        warning_audits = [r for r in results if r.status == TestStatus.WARNING]
        
        if failed_audits:
            status = TestStatus.FAIL
            issue = f"Lighthouse found {len(failed_audits)} critical issues and {len(warning_audits)} warnings"
            recommendation = f"Address {len(failed_audits)} critical Lighthouse issues for better performance and SEO"
        elif warning_audits:
            status = TestStatus.WARNING
            issue = f"Lighthouse found {len(warning_audits)} warnings"
            recommendation = f"Address {len(warning_audits)} Lighthouse warnings for optimal performance"
        else:
            status = TestStatus.PASS
            issue = "Lighthouse audit passed with no issues"
            recommendation = "Excellent! All Lighthouse audits passed"
        
        return TestResult(
            url=content.url,
            test_id=self.test_id,
            test_name=self.test_name,
            category=self.category,
            status=status,
            severity=self.severity,
            issue_description=issue,
            recommendation=recommendation,
            score=f"{total_issues} total audits"
        )
    
    def execute_multiple(self, content: PageContent, crawl_context: Optional['CrawlContext'] = None) -> List[TestResult]:
        """
        Execute Lighthouse audit and return multiple results for each failing audit.
        
        Returns:
            List of TestResult objects, one for each failing Lighthouse audit
        """
        results = []
        
        try:
            # Check if Lighthouse is available
            if not LighthouseIntegration.check_lighthouse_installed():
                return [TestResult(
                    url=content.url,
                    test_id=self.test_id,
                    test_name=self.test_name,
                    category=self.category,
                    status=TestStatus.INFO,
                    severity=TestSeverity.MEDIUM,
                    issue_description="Lighthouse CLI not installed",
                    recommendation="Install Lighthouse: npm install -g lighthouse",
                    score="Not available"
                )]
            
            # Run Lighthouse audit
            lighthouse_results = LighthouseIntegration.run_lighthouse(
                content.url,
                categories=['performance', 'accessibility', 'best-practices', 'seo']
            )
            
            if not lighthouse_results:
                return [TestResult(
                    url=content.url,
                    test_id=self.test_id,
                    test_name=self.test_name,
                    category=self.category,
                    status=TestStatus.ERROR,
                    severity=TestSeverity.HIGH,
                    issue_description="Lighthouse audit failed to run",
                    recommendation="Check Lighthouse installation and network connectivity",
                    score="Error"
                )]
            
            # Extract and process audits
            audits = lighthouse_results.get('audits', {})
            categories = lighthouse_results.get('categories', {})
            
            # Get category scores for context
            category_scores = {}
            for cat_name, cat_data in categories.items():
                score = cat_data.get('score', 0)
                category_scores[cat_name] = score * 100 if score is not None else 0
            
            # Process each audit
            for audit_id, audit_data in audits.items():
                score = audit_data.get('score')
                if score is None:
                    continue  # Skip audits without scores
                
                # Only create results for failing or warning audits
                if score >= 0.9:  # 90% or higher is considered passing
                    continue
                
                # Determine status based on score
                if score < 0.5:  # Less than 50%
                    status = TestStatus.FAIL
                    severity = TestSeverity.CRITICAL
                elif score < 0.8:  # Less than 80%
                    status = TestStatus.FAIL
                    severity = TestSeverity.HIGH
                else:  # 80-89%
                    status = TestStatus.WARNING
                    severity = TestSeverity.MEDIUM
                
                # Get audit details
                title = audit_data.get('title', audit_id)
                description = audit_data.get('description', '')
                display_value = audit_data.get('displayValue', '')
                
                # Create detailed recommendation
                recommendation = self._create_lighthouse_recommendation(
                    audit_id, audit_data, category_scores
                )
                
                # Create test result
                result = TestResult(
                    url=content.url,
                    test_id=f"lighthouse_{audit_id}",
                    test_name=f"Lighthouse: {title}",
                    category=self._get_audit_category(audit_id),
                    status=status,
                    severity=severity,
                    issue_description=f"{title}: {description}",
                    recommendation=recommendation,
                    score=f"{int(score * 100)}%"
                )
                
                results.append(result)
            
            # If no failing audits, create a success result
            if not results:
                results.append(TestResult(
                    url=content.url,
                    test_id=f"lighthouse_{self.test_id}",
                    test_name=f"Lighthouse: All Audits Passed",
                    category=self.category,
                    status=TestStatus.PASS,
                    severity=TestSeverity.LOW,
                    issue_description="All Lighthouse audits passed",
                    recommendation="Excellent performance and SEO compliance",
                    score="100%"
                ))
            
        except Exception as e:
            results.append(TestResult(
                url=content.url,
                test_id=self.test_id,
                test_name=self.test_name,
                category=self.category,
                status=TestStatus.ERROR,
                severity=TestSeverity.HIGH,
                issue_description=f"Lighthouse audit error: {str(e)}",
                recommendation="Check Lighthouse installation and configuration",
                score="Error"
            ))
        
        return results
    
    def _get_audit_category(self, audit_id: str) -> str:
        """Map Lighthouse audit ID to test category"""
        if any(keyword in audit_id for keyword in ['performance', 'speed', 'blocking', 'render']):
            return TestCategory.PERFORMANCE
        elif any(keyword in audit_id for keyword in ['accessibility', 'aria', 'color', 'contrast']):
            return TestCategory.ACCESSIBILITY
        elif any(keyword in audit_id for keyword in ['seo', 'meta', 'title', 'description', 'canonical']):
            return TestCategory.META_TAGS
        elif any(keyword in audit_id for keyword in ['security', 'https', 'csp', 'xss']):
            return TestCategory.SECURITY
        else:
            return TestCategory.TECHNICAL_SEO
    
    def _create_lighthouse_recommendation(
        self, 
        audit_id: str, 
        audit_data: Dict[str, Any], 
        category_scores: Dict[str, float]
    ) -> str:
        """Create detailed recommendation based on audit data"""
        title = audit_data.get('title', audit_id)
        display_value = audit_data.get('displayValue', '')
        score = audit_data.get('score', 0)
        
        # Get category context
        category = self._get_audit_category(audit_id)
        if category == TestCategory.PERFORMANCE:
            category_score = category_scores.get('performance', 0)
            context = f"Performance score: {category_score:.0f}%"
        elif category == TestCategory.ACCESSIBILITY:
            category_score = category_scores.get('accessibility', 0)
            context = f"Accessibility score: {category_score:.0f}%"
        elif category == TestCategory.META_TAGS:
            category_score = category_scores.get('seo', 0)
            context = f"SEO score: {category_score:.0f}%"
        else:
            category_score = category_scores.get('best-practices', 0)
            context = f"Best practices score: {category_score:.0f}%"
        
        # Create recommendation
        if display_value:
            recommendation = f"Improve {title}: {display_value}. {context}"
        else:
            recommendation = f"Address {title} issue. {context}"
        
        # Add specific recommendations for common audits
        if audit_id == 'first-contentful-paint':
            recommendation += " Consider optimizing critical rendering path and reducing render-blocking resources."
        elif audit_id == 'largest-contentful-paint':
            recommendation += " Optimize images and reduce server response time for better LCP."
        elif audit_id == 'cumulative-layout-shift':
            recommendation += " Reserve space for images and avoid inserting content above existing content."
        elif audit_id == 'document-title':
            recommendation += " Add a unique, descriptive title tag to each page."
        elif audit_id == 'meta-description':
            recommendation += " Add meta descriptions to improve click-through rates from search results."
        
        return recommendation
