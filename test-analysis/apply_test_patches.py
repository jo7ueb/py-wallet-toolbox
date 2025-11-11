#!/usr/bin/env python3
"""
Apply patches to Python test files based on AI comparison report.

This script parses the comparison report, identifies missing verifications,
and applies patches to Python test files to improve semantic similarity scores.
"""

import re
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def parse_report(file_path: Path) -> List[Dict]:
    """Parse the markdown comparison report into structured data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all test sections
    # Split by test headers, then process each
    test_headers = list(re.finditer(r'^## Test (\d+): (.+?) \*\*(PASS|FAIL)\*\*', content, re.MULTILINE))
    
    matches = []
    for i, header in enumerate(test_headers):
        test_num = int(header.group(1))
        test_name = header.group(2)
        status = header.group(3)
        start_pos = header.end()
        # Find end of section (next test header or end of file)
        if i + 1 < len(test_headers):
            end_pos = test_headers[i + 1].start()
        else:
            end_pos = len(content)
        section = content[start_pos:end_pos]
        matches.append((test_num, test_name, status, section))
    
    tests = []
    for test_num, test_name, status, section in matches:
        # Only process FAIL tests
        if status != 'FAIL':
            continue
        
        test_info = extract_test_info(test_num, test_name, status, section)
        if test_info:
            tests.append(test_info)
    
    return tests


def extract_test_info(test_num: int, test_name: str, status: str, section: str) -> Optional[Dict]:
    """Extract test information from a markdown section."""
    
    # Extract TypeScript code block
    ts_match = re.search(r'```typescript\n(.*?)```', section, re.DOTALL)
    ts_code = ts_match.group(1) if ts_match else ''
    
    # Extract Python code block
    py_match = re.search(r'```python\n(.*?)```', section, re.DOTALL)
    py_code = py_match.group(1) if py_match else ''
    
    # Extract Python file path
    py_file_match = re.search(r'### Python Test: (.+)', section)
    py_file = py_file_match.group(1).strip() if py_file_match else ''
    
    # Extract similarity scores
    similarity_match = re.search(r'\*\*Similarity Score\*\*: ([\d.]+)%', section)
    semantic_match = re.search(r'- Semantic: ([\d.]+)%', section)
    
    similarity = float(similarity_match.group(1)) if similarity_match else 0.0
    semantic = float(semantic_match.group(1)) if semantic_match else 0.0
    
    # Extract critical issues
    issues = []
    issues_section = re.search(r'\*\*Critical Issues:\*\*(.*?)(?:\*\*[A-Z]|$)', section, re.DOTALL)
    if issues_section:
        issue_text = issues_section.group(1)
        # Look for missing verifications line
        verif_match = re.search(r'missing verifications:\s*([^\n]+)', issue_text, re.IGNORECASE)
        if verif_match:
            verif_str = verif_match.group(1).strip()
            # Split by comma and clean
            verifications = [v.strip() for v in verif_str.split(',')]
            issues.extend([{'type': 'missing_verification', 'name': v} for v in verifications])
    
    return {
        'test_num': test_num,
        'test_name': test_name,
        'status': status,
        'ts_code': ts_code,
        'py_code': py_code,
        'py_file': py_file,
        'similarity': similarity,
        'semantic': semantic,
        'issues': issues
    }


def filter_verification_issues(issues: List[Dict]) -> List[Dict]:
    """Filter to only include missing_verifications type."""
    return [issue for issue in issues if issue.get('type') == 'missing_verification']


def find_ts_assertion(verification_name: str, ts_code: str) -> Optional[str]:
    """Find the TypeScript assertion code for a verification."""
    # Normalize verification name (e.g., "snapshot.length" -> look for "snapshot.length")
    # Try different patterns
    patterns = [
        rf'expect\({re.escape(verification_name)}\)\.(.+)',
        rf'expect\((\w+)\.{re.escape(verification_name.split(".")[-1])}\)\.(.+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ts_code)
        if match:
            # Get the full line
            lines = ts_code.split('\n')
            for i, line in enumerate(lines):
                if verification_name in line and 'expect' in line:
                    # Get the full assertion (may span multiple lines)
                    assertion = line.strip()
                    # Check if next line continues the assertion
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith('.'):
                        assertion += ' ' + lines[i + 1].strip()
                    return assertion
    
    # Try to find by property name only
    prop_name = verification_name.split('.')[-1]
    for line in ts_code.split('\n'):
        if prop_name in line and 'expect' in line and ('toBe' in line or 'toHaveBeenCalled' in line):
            return line.strip()
    
    return None


def convert_to_python_assertion(ts_assertion: str) -> Optional[str]:
    """Convert TypeScript assertion to Python equivalent."""
    if not ts_assertion:
        return None
    
    # Pattern: expect(obj.length).toBeGreaterThan(N)
    match = re.search(r'expect\((\w+)\.length\)\.toBeGreaterThan\((\d+)\)', ts_assertion)
    if match:
        obj = match.group(1)
        n = match.group(2)
        # Extract comment if present
        comment_match = re.search(r'//\s*(.+)', ts_assertion)
        comment = f"  # {comment_match.group(1)}" if comment_match else ""
        return f"assert len({obj}) > {n}{comment}"
    
    # Pattern: expect(obj.length).toBe(N)
    match = re.search(r'expect\((\w+)\.length\)\.toBe\((\d+)\)', ts_assertion)
    if match:
        obj = match.group(1)
        n = match.group(2)
        return f"assert len({obj}) == {n}"
    
    # Pattern: expect(Array.isArray(obj)).toBe(true)
    match = re.search(r'expect\(Array\.isArray\((\w+)\)\)\.toBe\(true\)', ts_assertion)
    if match:
        obj = match.group(1)
        return f"assert isinstance({obj}, (list, bytes))  # Check snapshot is array-like"
    
    # Pattern: expect(obj.property).toBe(value)
    match = re.search(r'expect\((\w+)\.(\w+)\)\.toBe\((.+)\)', ts_assertion)
    if match:
        obj = match.group(1)
        prop = match.group(2)
        value = match.group(3)
        if value == 'true':
            return f"assert {obj}.{prop} is True"
        elif value == 'false':
            return f"assert {obj}.{prop} is False"
        else:
            return f"assert {obj}.{prop} == {value}"
    
    # Pattern: expect(mock.method).toHaveBeenCalledTimes(N)
    match = re.search(r'expect\((\w+)\.(\w+)\)\.toHaveBeenCalledTimes\((\d+)\)', ts_assertion)
    if match:
        obj = match.group(1)
        method = match.group(2)
        n = match.group(3)
        # Extract comment if present
        comment_match = re.search(r'//\s*(.+)', ts_assertion)
        comment = f"  # {comment_match.group(1)}" if comment_match else ""
        return f"assert {obj}.{method}.call_count == {n}{comment}"
    
    return None


def read_python_file(file_path: str) -> List[str]:
    """Read the actual Python test file."""
    full_path = Path(file_path)
    if not full_path.exists():
        # Try relative to current directory
        full_path = Path.cwd() / file_path
    if not full_path.exists():
        raise FileNotFoundError(f"Python file not found: {file_path}")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.readlines()


def find_insertion_point(verification_name: str, py_code_lines: List[str], py_code_block: str) -> Optional[int]:
    """Find line number to insert assertion in Python file."""
    # Find the variable/object name from verification
    obj_name = verification_name.split('.')[0]
    
    # Look for where this object is assigned/created in the code block
    # Then find that line in the actual file
    lines = py_code_block.split('\n')
    for i, line in enumerate(lines):
        if obj_name in line and ('=' in line or 'await' in line):
            # Found the assignment, now find it in the actual file
            # Search for a similar pattern
            pattern = re.escape(line.strip())
            for j, file_line in enumerate(py_code_lines):
                if obj_name in file_line and ('=' in file_line or 'await' in file_line):
                    # Found a match, return the line after it (1-indexed)
                    return j + 2  # +1 for 1-indexed, +1 for next line
    
    # Fallback: find the test function and insert near the end
    for i, line in enumerate(py_code_lines):
        if 'async def test_' in line or 'def test_' in line:
            # Find the end of the function (next def or class)
            for j in range(i + 1, len(py_code_lines)):
                if py_code_lines[j].strip().startswith('def ') or py_code_lines[j].strip().startswith('class '):
                    return j  # Insert before next function/class
            return len(py_code_lines)  # End of file
    
    return None


def create_backup(file_path: Path) -> Path:
    """Create backup copy of file."""
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    shutil.copy2(file_path, backup_path)
    return backup_path


def apply_patches(file_path: Path, patches: List[Dict], dry_run: bool = False) -> bool:
    """Apply multiple patches to Python file with correct line number tracking."""
    if not patches:
        return True
    
    # Sort patches by line number (ascending) to apply in order
    sorted_patches = sorted(patches, key=lambda p: p['line_num'] or 0)
    
    lines = read_python_file(str(file_path))
    offset = 0  # Track cumulative offset from insertions
    
    for patch in sorted_patches:
        line_num = patch['line_num']
        assertion_code = patch['py_assertion']
        
        if line_num is None or line_num < 1:
            print(f"  Warning: Invalid line number {line_num} for {patch['verification']}, skipping")
            continue
        
        # Adjust line number for previous insertions
        adjusted_line = line_num + offset
        insert_idx = adjusted_line - 1  # Convert to 0-indexed
        
        if insert_idx < 0 or insert_idx > len(lines):
            print(f"  Warning: Adjusted line number {adjusted_line} out of range for {patch['verification']}, skipping")
            continue
        
        # Get indentation from the line before
        if insert_idx > 0:
            prev_line = lines[insert_idx - 1]
            # Get indentation
            indent = len(prev_line) - len(prev_line.lstrip())
            # Preserve indentation
            assertion_code = ' ' * indent + assertion_code.lstrip()
        else:
            assertion_code = assertion_code.lstrip()
        
        if dry_run:
            print(f"  Line {line_num} (adjusted to {adjusted_line}): Would insert:")
            print(f"    + {assertion_code}")
        else:
            # Insert the assertion
            lines.insert(insert_idx, assertion_code + '\n')
            print(f"  Line {adjusted_line}: Added {assertion_code.strip()}")
            offset += 1  # Increment offset for next patch
    
    if not dry_run:
        # Write back all changes at once
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    return True


def format_changes(test_num: int, test_name: str, py_file: str, patches: List[Dict]) -> None:
    """Format and display changes."""
    print(f"\nTest {test_num}: {test_name}")
    print(f"\nFile: {py_file}")
    
    if not patches:
        print("\nNo patches to apply (no missing verifications found).")
        return
    
    # Sort patches by line number for display
    sorted_patches = sorted(patches, key=lambda p: p['line_num'] or 0)
    
    print(f"\nPlanned Changes:")
    for i, patch in enumerate(sorted_patches, 1):
        print(f"\n{i}. {patch['verification']}")
        if patch.get('ts_assertion'):
            print(f"   TypeScript: {patch['ts_assertion']}")
        print(f"   Python: {patch['py_assertion']}")
        if patch.get('line_num'):
            print(f"   Insert at line {patch['line_num']}")


def run_comparison_test(test_number: int, compare_script: str = 'compare_tests_with_ai.py') -> Optional[Dict]:
    """Run comparison test script and parse results."""
    script_path = Path(compare_script)
    if not script_path.exists():
        script_path = Path.cwd() / compare_script
    
    if not script_path.exists():
        print(f"  Warning: Comparison script not found: {compare_script}")
        return None
    
    print(f"\nRunning comparison test to verify...")
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), '--test-number', str(test_number)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout + result.stderr
        
        # Parse output to find test result
        # Look for pattern like: [N/1] Analyzing: ... followed by ✓ PASS or ✗ FAIL
        status_match = re.search(rf'\[{test_number}/1\].*?(✓|✗)\s+(PASS|FAIL)', output)
        similarity_match = re.search(rf'\[{test_number}/1\].*?(✓|✗)\s+(PASS|FAIL):\s+([\d.]+)%', output)
        
        status = None
        similarity = None
        
        if status_match:
            status = status_match.group(2)
        if similarity_match:
            similarity = float(similarity_match.group(3))
        
        return {
            'status': status,
            'similarity': similarity,
            'output': output
        }
    except subprocess.TimeoutExpired:
        print(f"  Warning: Comparison test timed out")
        return None
    except Exception as e:
        print(f"  Warning: Error running comparison test: {e}")
        return None


def check_test_result(result: Optional[Dict], original_status: str = 'FAIL') -> None:
    """Check and report test result."""
    if not result:
        return
    
    status = result.get('status')
    similarity = result.get('similarity')
    
    if status:
        if status == 'PASS':
            if original_status == 'FAIL':
                print(f"Test now passes! (was FAIL, now PASS)")
            else:
                print(f"Test status: PASS")
        else:
            print(f"Test status: FAIL")
            if similarity:
                print(f"Similarity: {similarity:.1f}%")
    elif similarity:
        print(f"Similarity: {similarity:.1f}%")


def run_pytest(test_file: str, test_function: str = None) -> Optional[Dict]:
    """Run pytest on the test file and parse results."""
    # Build pytest command
    test_file_path = Path(test_file)
    if not test_file_path.is_absolute():
        test_file_path = Path.cwd() / test_file
    
    # Determine working directory (usually the py-wallet-toolbox directory)
    if 'py-wallet-toolbox' in str(test_file_path):
        # Extract py-wallet-toolbox directory
        parts = test_file_path.parts
        py_wallet_idx = None
        for i, part in enumerate(parts):
            if part == 'py-wallet-toolbox':
                py_wallet_idx = i
                break
        if py_wallet_idx is not None:
            cwd = Path(*parts[:py_wallet_idx + 1])
        else:
            cwd = Path.cwd()
    else:
        cwd = Path.cwd()
    
    pytest_args = [sys.executable, '-m', 'pytest', str(test_file_path.relative_to(cwd)), '-v']
    if test_function:
        pytest_args.extend(['-k', test_function])
    
    print(f"\nRunning pytest to verify test execution...")
    try:
        result = subprocess.run(
            pytest_args,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=cwd
        )
        
        output = result.stdout + result.stderr
        
        # Parse pytest output
        # Look for: PASSED, FAILED, SKIPPED, ERROR
        passed_match = re.search(r'(\d+)\s+passed', output, re.IGNORECASE)
        failed_match = re.search(r'(\d+)\s+failed', output, re.IGNORECASE)
        skipped_match = re.search(r'(\d+)\s+skipped', output, re.IGNORECASE)
        error_match = re.search(r'(\d+)\s+error', output, re.IGNORECASE)
        
        # Also check for specific test result
        test_passed = 'PASSED' in output or 'passed' in output.lower()
        test_failed = 'FAILED' in output or 'failed' in output.lower()
        test_skipped = 'SKIPPED' in output or 'skipped' in output.lower()
        test_error = 'ERROR' in output or 'error' in output.lower()
        
        return {
            'passed': int(passed_match.group(1)) if passed_match else 0,
            'failed': int(failed_match.group(1)) if failed_match else 0,
            'skipped': int(skipped_match.group(1)) if skipped_match else 0,
            'error': int(error_match.group(1)) if error_match else 0,
            'test_passed': test_passed,
            'test_failed': test_failed,
            'test_skipped': test_skipped,
            'test_error': test_error,
            'output': output
        }
    except subprocess.TimeoutExpired:
        print(f"  Warning: pytest timed out")
        return None
    except Exception as e:
        print(f"  Warning: Error running pytest: {e}")
        return None


def check_pytest_result(pytest_result: Optional[Dict]) -> None:
    """Check and report pytest result."""
    if not pytest_result:
        return
    
    if pytest_result.get('test_skipped'):
        print(f"Pytest: Test is SKIPPED (marked with @pytest.mark.skip)")
        return
    
    if pytest_result.get('test_passed'):
        print(f"Pytest: ✓ Test PASSED")
    elif pytest_result.get('test_failed'):
        print(f"Pytest: ✗ Test FAILED")
        # Show error if available
        output = pytest_result.get('output', '')
        error_lines = [line for line in output.split('\n') if 'FAILED' in line or 'Error' in line or 'AssertionError' in line]
        if error_lines:
            print(f"  Error: {error_lines[0][:100]}")
    elif pytest_result.get('test_error'):
        print(f"Pytest: ✗ Test ERROR")
    else:
        passed = pytest_result.get('passed', 0)
        failed = pytest_result.get('failed', 0)
        if passed > 0:
            print(f"Pytest: {passed} test(s) passed")
        if failed > 0:
            print(f"Pytest: {failed} test(s) failed")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Apply patches to Python test files based on AI comparison report'
    )
    parser.add_argument(
        '-n', '--test-number', type=int, metavar='N',
        help='Process only test N (1-indexed)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--no-backup', action='store_true',
        help='Skip creating backup file'
    )
    parser.add_argument(
        '--no-verify', action='store_true',
        help='Skip running comparison test after patching'
    )
    parser.add_argument(
        '--report', type=str, default='ai_test_comparison_report.md',
        help='Path to comparison report (default: ai_test_comparison_report.md)'
    )
    parser.add_argument(
        '--compare-script', type=str, default='compare_tests_with_ai.py',
        help='Path to compare_tests_with_ai.py script (default: compare_tests_with_ai.py)'
    )
    
    args = parser.parse_args()
    
    # Parse report
    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Error: Report file not found: {report_path}")
        return
    
    tests = parse_report(report_path)
    
    # Filter to specific test if requested
    if args.test_number:
        tests = [t for t in tests if t['test_num'] == args.test_number]
        if not tests:
            print(f"Error: Test {args.test_number} not found or is not a FAIL test.")
            return
    
    if not tests:
        print("No failing tests found to process.")
        return
    
    # Process each test
    for test in tests:
        # Filter to only verification issues
        verif_issues = filter_verification_issues(test['issues'])
        
        if not verif_issues:
            print(f"\nTest {test['test_num']}: {test['test_name']}")
            print("No missing verifications found (only operations issues, which are ignored).")
            continue
        
        # Read Python file
        py_file_path = Path(test['py_file'])
        if not py_file_path.exists():
            # Try relative to current directory
            py_file_path = Path.cwd() / test['py_file']
        
        if not py_file_path.exists():
            print(f"\nTest {test['test_num']}: {test['test_name']}")
            print(f"Error: Python file not found: {test['py_file']}")
            continue
        
        # Process each missing verification
        patches = []
        for issue in verif_issues:
            verif_name = issue['name']
            
            # Find TS assertion
            ts_assertion = find_ts_assertion(verif_name, test['ts_code'])
            
            # Convert to Python
            py_assertion = convert_to_python_assertion(ts_assertion) if ts_assertion else None
            
            if not py_assertion:
                print(f"  Warning: Could not convert verification '{verif_name}' to Python assertion")
                continue
            
            # Find insertion point
            py_lines = read_python_file(str(py_file_path))
            line_num = find_insertion_point(verif_name, py_lines, test['py_code'])
            
            patches.append({
                'verification': verif_name,
                'ts_assertion': ts_assertion,
                'py_assertion': py_assertion,
                'line_num': line_num
            })
        
        # Show planned changes or apply patches
        if args.dry_run:
            format_changes(test['test_num'], test['test_name'], str(py_file_path), patches)
            print("\n[DRY RUN] No files modified. Use without --dry-run to apply changes.")
        else:
            # Create backup before applying
            if not args.no_backup:
                backup_path = create_backup(py_file_path)
                print(f"\nTest {test['test_num']}: {test['test_name']}")
                print(f"File: {py_file_path}")
                print(f"Backup: {backup_path}")
            else:
                print(f"\nTest {test['test_num']}: {test['test_name']}")
                print(f"File: {py_file_path}")
            
            print(f"\nApplied {len(patches)} patch(es):")
            apply_patches(py_file_path, patches, dry_run=False)
            
            # Run comparison test to verify if requested
            if not args.no_verify:
                result = run_comparison_test(test['test_num'], args.compare_script)
                check_test_result(result, original_status=test['status'])
                
                # Also run pytest to verify the test actually executes
                # Try to get function name from test_ranges.json first
                test_function_name = None
                try:
                    import json
                    test_ranges_path = Path('test_ranges.json')
                    if test_ranges_path.exists():
                        with open(test_ranges_path, 'r') as f:
                            test_ranges = json.load(f)
                            # Find matching test by test number
                            for entry in test_ranges:
                                # Match by test name (approximate)
                                if entry.get('test_name') == test['test_name']:
                                    test_function_name = entry.get('py_function_name')
                                    break
                except Exception:
                    pass
                
                # Fallback: extract from Python code block
                if not test_function_name:
                    py_code = test.get('py_code', '')
                    func_match = re.search(r'(?:async\s+)?def (test_\w+)', py_code)
                    if func_match:
                        test_function_name = func_match.group(1)
                
                if test_function_name:
                    pytest_result = run_pytest(str(py_file_path), test_function_name)
                    check_pytest_result(pytest_result)
                else:
                    # Fallback: run pytest on the whole file with test name pattern
                    test_name_words = test['test_name'].lower().replace(' ', '_')
                    pytest_result = run_pytest(str(py_file_path), test_name_words)
                    check_pytest_result(pytest_result)


if __name__ == '__main__':
    main()

