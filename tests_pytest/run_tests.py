#!/usr/bin/env python3
"""
Test Runner for SEO Analyzer
Runs all unit tests with proper output management.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

def run_tests():
    """Run all unit tests with proper configuration"""
    
    print("🧪 SEO Analyzer Unit Test Runner")
    print("=" * 50)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Ensure we're in the right directory
    test_dir = Path(__file__).parent
    os.chdir(test_dir)
    
    # Ensure output directory exists
    output_dir = Path('../output')
    output_dir.mkdir(exist_ok=True)
    
    print("🔧 Test Configuration:")
    print(f"  📁 Test Directory: {test_dir}")
    print(f"  📁 Output Directory: {output_dir.absolute()}")
    print(f"  🐍 Python Path: {sys.executable}")
    print()
    
    # Run different test categories
    test_categories = [
        {
            'name': 'Lighthouse Individual Results',
            'pattern': 'test_lighthouse_individual_results.py',
            'markers': 'lighthouse'
        },
        {
            'name': 'Axe-core Individual Results', 
            'pattern': 'test_axe_core_individual_results.py',
            'markers': 'axe_core'
        },
        {
            'name': 'Full SEO Analysis Output',
            'pattern': 'test_full_seo_analysis_output.py',
            'markers': 'integration'
        },
        {
            'name': 'Core Executor Tests',
            'pattern': 'test_core_executor.py',
            'markers': ''
        },
        {
            'name': 'SEO Orchestrator Tests',
            'pattern': 'test_seo_orchestrator.py',
            'markers': ''
        }
    ]
    
    results = {}
    
    for category in test_categories:
        print(f"🧪 Running {category['name']}...")
        print("-" * 40)
        
        # Build pytest command
        cmd = [sys.executable, '-m', 'pytest', '-v', '--tb=short']
        
        if category['markers']:
            cmd.extend(['-m', category['markers']])
        
        cmd.append(category['pattern'])
        
        # Add output directory configuration
        cmd.extend(['--output-dir', str(output_dir.absolute())])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            results[category['name']] = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            if result.returncode == 0:
                print(f"  ✅ {category['name']} - PASSED")
            else:
                print(f"  ❌ {category['name']} - FAILED")
                print(f"  📝 Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"  ⏰ {category['name']} - TIMEOUT")
            results[category['name']] = {'returncode': -1, 'stdout': '', 'stderr': 'Timeout'}
        except Exception as e:
            print(f"  💥 {category['name']} - ERROR: {e}")
            results[category['name']] = {'returncode': -1, 'stdout': '', 'stderr': str(e)}
        
        print()
    
    # Summary
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for name, result in results.items():
        if result['returncode'] == 0:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}")
            failed += 1
    
    print()
    print(f"📈 Total: {passed + failed} tests")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Output Directory: {output_dir.absolute()}")
    
    if failed > 0:
        print("\n🔍 Failed Test Details:")
        for name, result in results.items():
            if result['returncode'] != 0:
                print(f"\n❌ {name}:")
                print(f"   Error: {result['stderr']}")
    
    print(f"\n📅 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
