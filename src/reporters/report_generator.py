#!/usr/bin/env python3
"""
ReportGenerator - Handles all output formats for SEO analysis results
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import csv
import json
import os


class ReportGenerator:
    """
    Enterprise report generator that outputs SEO analysis results
    in multiple formats (CSV, Excel, JSON, HTML)
    """
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize Report Generator
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_csv_report(
        self,
        results: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """
        Generate CSV report
        
        Args:
            results: List of test result dictionaries
            filename: Optional output filename
            
        Returns:
            Path to generated file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/seo_report_{timestamp}.csv"
        else:
            filename = os.path.join(self.output_dir, filename)
        
        if not results:
            print("Warning: No results to write to CSV")
            return filename
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
            print(f"CSV report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving CSV report: {e}")
            return None
    
    def generate_excel_report(
        self,
        results: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """
        Generate Excel report with multiple sheets
        
        Args:
            results: List of test result dictionaries
            filename: Optional output filename
            
        Returns:
            Path to generated file
        """
        try:
            import pandas as pd
        except ImportError:
            print("Error: pandas required for Excel export. Install with: pip install pandas openpyxl")
            return None
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/seo_report_{timestamp}.xlsx"
        else:
            filename = os.path.join(self.output_dir, filename)
        
        if not results:
            print("Warning: No results to write to Excel")
            return filename
        
        try:
            df = pd.DataFrame(results)
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # All results sheet
                df.to_excel(writer, sheet_name='All Results', index=False)
                
                # Summary by URL
                if 'URL' in df.columns:
                    url_summary = self._create_url_summary(df)
                    url_summary.to_excel(writer, sheet_name='URL Summary', index=False)
                
                # Issues only
                if 'Status' in df.columns:
                    issues = df[df['Status'].isin(['Fail', 'Warning'])].copy()
                    if not issues.empty:
                        issues.to_excel(writer, sheet_name='Issues', index=False)
                    
                    # Passed tests
                    passed = df[df['Status'] == 'Pass'].copy()
                    if not passed.empty:
                        passed.to_excel(writer, sheet_name='Passed', index=False)
                
                # Category breakdown
                if 'Category' in df.columns:
                    category_summary = self._create_category_summary(df)
                    category_summary.to_excel(writer, sheet_name='By Category', index=False)
            
            print(f"Excel report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving Excel report: {e}")
            return None
    
    def generate_json_report(
        self,
        results: List[Dict[str, Any]],
        filename: Optional[str] = None,
        pretty: bool = True
    ) -> str:
        """
        Generate JSON report
        
        Args:
            results: List of test result dictionaries
            filename: Optional output filename
            pretty: Pretty print JSON
            
        Returns:
            Path to generated file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/seo_report_{timestamp}.json"
        else:
            filename = os.path.join(self.output_dir, filename)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(results, f, ensure_ascii=False)
            
            print(f"JSON report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving JSON report: {e}")
            return None
    
    def generate_html_report(
        self,
        results: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """
        Generate HTML report
        
        Args:
            results: List of test result dictionaries
            filename: Optional output filename
            
        Returns:
            Path to generated file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/seo_report_{timestamp}.html"
        else:
            filename = os.path.join(self.output_dir, filename)
        
        try:
            html_content = self._create_html_template(results)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTML report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving HTML report: {e}")
            return None
    
    def generate_all_formats(
        self,
        results: List[Dict[str, Any]],
        base_filename: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate reports in all formats
        
        Args:
            results: List of test result dictionaries
            base_filename: Base filename (without extension)
            
        Returns:
            Dictionary of format -> filename
        """
        if not base_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"seo_report_{timestamp}"
        
        files = {}
        
        files['csv'] = self.generate_csv_report(results, f"{base_filename}.csv")
        files['excel'] = self.generate_excel_report(results, f"{base_filename}.xlsx")
        files['json'] = self.generate_json_report(results, f"{base_filename}.json")
        files['html'] = self.generate_html_report(results, f"{base_filename}.html")
        
        return files
    
    def _create_url_summary(self, df) -> 'pd.DataFrame':
        """Create URL summary dataframe"""
        import pandas as pd
        
        summary_data = []
        
        for url in df['URL'].unique():
            url_data = df[df['URL'] == url]
            
            total = len(url_data)
            passed = len(url_data[url_data['Status'] == 'Pass'])
            failed = len(url_data[url_data['Status'] == 'Fail'])
            warnings = len(url_data[url_data['Status'] == 'Warning'])
            
            pass_rate = (passed / total * 100) if total > 0 else 0
            
            summary_data.append({
                'URL': url,
                'Total_Tests': total,
                'Passed': passed,
                'Failed': failed,
                'Warnings': warnings,
                'Pass_Rate': f'{pass_rate:.1f}%',
                'Status': 'Pass' if failed == 0 else 'Fail'
            })
        
        return pd.DataFrame(summary_data)
    
    def _create_category_summary(self, df) -> 'pd.DataFrame':
        """Create category summary dataframe"""
        import pandas as pd
        
        summary_data = []
        
        for category in df['Category'].unique():
            cat_data = df[df['Category'] == category]
            
            total = len(cat_data)
            passed = len(cat_data[cat_data['Status'] == 'Pass'])
            failed = len(cat_data[cat_data['Status'] == 'Fail'])
            warnings = len(cat_data[cat_data['Status'] == 'Warning'])
            
            pass_rate = (passed / total * 100) if total > 0 else 0
            
            summary_data.append({
                'Category': category,
                'Total_Tests': total,
                'Passed': passed,
                'Failed': failed,
                'Warnings': warnings,
                'Pass_Rate': f'{pass_rate:.1f}%',
                'URLs_Affected': len(cat_data['URL'].unique()) if 'URL' in cat_data.columns else 0
            })
        
        return pd.DataFrame(summary_data)
    
    def _create_html_template(self, results: List[Dict[str, Any]]) -> str:
        """Create HTML report template"""
        
        # Calculate summary statistics
        total_tests = len(results)
        passed = len([r for r in results if r.get('Status') == 'Pass'])
        failed = len([r for r in results if r.get('Status') == 'Fail'])
        warnings = len([r for r in results if r.get('Status') == 'Warning'])
        
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        # Group by URL
        urls = {}
        for result in results:
            url = result.get('URL', 'Unknown')
            if url not in urls:
                urls[url] = []
            urls[url].append(result)
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Analysis Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 32px;
        }}
        .timestamp {{
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .summary-card {{
            padding: 20px;
            border-radius: 6px;
            background: #f8f9fa;
            border-left: 4px solid #3498db;
        }}
        .summary-card.pass {{ border-left-color: #27ae60; }}
        .summary-card.fail {{ border-left-color: #e74c3c; }}
        .summary-card.warning {{ border-left-color: #f39c12; }}
        .summary-card h3 {{
            font-size: 14px;
            color: #7f8c8d;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .summary-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .url-section {{
            margin-bottom: 40px;
        }}
        .url-header {{
            background: #34495e;
            color: white;
            padding: 15px 20px;
            border-radius: 6px 6px 0 0;
            font-size: 18px;
            font-weight: 600;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            background: white;
        }}
        th {{
            background: #ecf0f1;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #2c3e50;
            border-bottom: 2px solid #bdc3c7;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .status {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .status.pass {{
            background: #d4edda;
            color: #155724;
        }}
        .status.fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        .status.warning {{
            background: #fff3cd;
            color: #856404;
        }}
        .status.info {{
            background: #d1ecf1;
            color: #0c5460;
        }}
        .category {{
            display: inline-block;
            padding: 4px 10px;
            background: #e8e8e8;
            border-radius: 4px;
            font-size: 12px;
            color: #555;
        }}
        .severity {{
            font-weight: 600;
        }}
        .severity.critical {{ color: #e74c3c; }}
        .severity.high {{ color: #e67e22; }}
        .severity.medium {{ color: #f39c12; }}
        .severity.low {{ color: #95a5a6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SEO Analysis Report</h1>
        <div class="timestamp">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Tests</h3>
                <div class="value">{total_tests}</div>
            </div>
            <div class="summary-card pass">
                <h3>Passed</h3>
                <div class="value">{passed}</div>
            </div>
            <div class="summary-card fail">
                <h3>Failed</h3>
                <div class="value">{failed}</div>
            </div>
            <div class="summary-card warning">
                <h3>Warnings</h3>
                <div class="value">{warnings}</div>
            </div>
            <div class="summary-card">
                <h3>Pass Rate</h3>
                <div class="value">{pass_rate:.1f}%</div>
            </div>
        </div>
'''
        
        # Add results by URL
        for url, url_results in urls.items():
            html += f'''
        <div class="url-section">
            <div class="url-header">{url}</div>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Category</th>
                        <th>Status</th>
                        <th>Severity</th>
                        <th>Issue Description</th>
                        <th>Recommendation</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
'''
            
            for result in url_results:
                status = result.get('Status', 'Unknown').lower()
                severity = result.get('Severity', 'Unknown').lower()
                
                html += f'''
                    <tr>
                        <td><strong>{result.get('Test_Name', 'N/A')}</strong></td>
                        <td><span class="category">{result.get('Category', 'N/A')}</span></td>
                        <td><span class="status {status}">{result.get('Status', 'N/A')}</span></td>
                        <td><span class="severity {severity}">{result.get('Severity', 'N/A')}</span></td>
                        <td>{result.get('Issue_Description', 'N/A')}</td>
                        <td>{result.get('Recommendation', 'N/A')}</td>
                        <td>{result.get('Score', 'N/A')}</td>
                    </tr>
'''
            
            html += '''
                </tbody>
            </table>
        </div>
'''
        
        html += '''
    </div>
</body>
</html>
'''
        
        return html

