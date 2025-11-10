#!/usr/bin/env python3
"""Automated Test Fixer for CWI Style Wallet Manager Tests.

This script:
1. Parses test_comparison_detailed_report.md for FAIL tests
2. Runs each failing test and captures output
3. Analyzes critical issues using Claude AI
4. Modifies the test file to improve similarities
5. Retries until test passes or max attempts reached
6. Supports jumping to specific test numbers and skipping fixed tests
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Import the test comparator
try:
    from compare_test_implementations_hybrid import TestComparator, DEFAULT_TS_BASE_DIR, DEFAULT_PY_BASE_DIR
    COMPARATOR_AVAILABLE = True
except ImportError:
    COMPARATOR_AVAILABLE = False
    print("⚠️  Warning: Test comparator not available")


@dataclass
class TestCase:
    """Represents a test case (both PASS and FAIL)."""

    test_number: int
    test_name: str
    status: str  # "PASS" or "FAIL"
    ts_file: str
    ts_line: int
    ts_start: int
    ts_end: int
    py_file: str
    py_line: int
    py_start: int
    py_end: int
    py_function_name: str  # Actual Python function name for pytest
    ts_code: str
    py_code: str
    structural_score: float
    semantic_score: float
    total_score: float
    comparison_results: str
    critical_issues: list  # List of critical issues from comparison
    comparison_differences: list = None  # Structural differences from comparison
    comparison_suggestions: list = None  # Suggestions from comparison
    comparison_result: dict = None  # Full comparison result


class TestFixerReport:
    """Manages the fixing progress report."""

    def __init__(self, output_file: str = "test_fixer_report.md"):
        self.output_file = output_file
        self.fixed_tests = []
        self.failed_attempts = []

    def add_success(
        self, test_num: int, test_name: str, attempts: int, final_output: str
    ):
        """Record a successful test fix."""
        self.fixed_tests.append(
            {
                "test_number": test_num,
                "test_name": test_name,
                "attempts": attempts,
                "final_output": final_output,
            }
        )
        self._write_report()

    def add_failure(
        self, test_num: int, test_name: str, attempts: int, last_error: str
    ):
        """Record a failed fix attempt."""
        self.failed_attempts.append(
            {
                "test_number": test_num,
                "test_name": test_name,
                "attempts": attempts,
                "last_error": last_error,
            }
        )
        self._write_report()

    def _write_report(self):
        """Write the current report to file."""
        with open(self.output_file, "w") as f:
            f.write("# Automated Test Fixer Report\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Tests Fixed**: {len(self.fixed_tests)}\n")
            f.write(f"- **Tests Failed**: {len(self.failed_attempts)}\n\n")

            if self.fixed_tests:
                f.write("## Fixed Tests\n\n")
                for test in self.fixed_tests:
                    f.write(
                        f"### Test {test['test_number']}: {test['test_name']}\n\n"
                    )
                    f.write(f"- **Attempts**: {test['attempts']}\n")
                    f.write(f"- **Status**: ✅ PASSED\n\n")

            if self.failed_attempts:
                f.write("## Failed Fix Attempts\n\n")
                for test in self.failed_attempts:
                    f.write(
                        f"### Test {test['test_number']}: {test['test_name']}\n\n"
                    )
                    f.write(f"- **Attempts**: {test['attempts']}\n")
                    f.write(f"- **Status**: ❌ FAILED\n")
                    f.write(f"- **Last Error**:\n```\n{test['last_error']}\n```\n\n")


class TestParser:
    """Parses the detailed test comparison report."""

    def __init__(self, report_file: str):
        self.report_file = report_file

    def parse_all_tests(self) -> list[TestCase]:
        """Extract all tests (both PASS and FAIL) from the report to maintain test number alignment."""
        with open(self.report_file, "r", encoding="utf-8") as f:
            content = f.read()

        all_tests = []
        
        # Split content by test sections
        # Pattern matches both PASS and FAIL tests
        # Format: ## Test N: name **STATUS**
        test_section_pattern = r"## Test (\d+): (.+?) \*\*(PASS|FAIL)\*\*"
        
        # Find all test sections
        test_matches = list(re.finditer(test_section_pattern, content))
        
        for i, match in enumerate(test_matches):
            test_num = int(match.group(1))
            test_name = match.group(2).strip()
            status = match.group(3)
            
            # Get the section content (from this match to next match or end)
            start_pos = match.end()
            end_pos = test_matches[i + 1].start() if i + 1 < len(test_matches) else len(content)
            section_content = content[start_pos:end_pos]
            
            # Parse TS test info
            ts_match = re.search(r"### TS Test: \[(.+?)\]\((.+?)#L(\d+)\)", section_content)
            if not ts_match:
                continue
            ts_rel_path = ts_match.group(1)
            ts_full_path = ts_match.group(2)
            ts_line = int(ts_match.group(3))
            
            # Parse PY test info
            py_match = re.search(r"### PY Test: \[(.+?)\]\((.+?)#L(\d+)\)(?: - `([^`]+)`)?", section_content)
            if not py_match:
                continue
            py_rel_path = py_match.group(1)
            py_full_path = py_match.group(2)
            py_line = int(py_match.group(3))
            py_function_name = py_match.group(4) if py_match.group(4) else None
            
            # If Python function name not found in report, try to extract from file
            if not py_function_name:
                py_function_name = self._extract_py_function_name(py_full_path, py_line)
            
            # Read code from files (for PASS tests, code is not in report)
            ts_code = self._read_code_from_file(ts_full_path, ts_line)
            py_code = self._read_code_from_file(py_full_path, py_line)
            
            # Extract scores and critical issues (only present for FAIL tests)
            structural, semantic, total = 0.0, 0.0, 0.0
            critical_issues = []
            comparison_text = ""
            
            if status == "FAIL":
                # Extract scores from comparison results
                score_match = re.search(
                    r"Structural: ([\d.]+)% \| Semantic: ([\d.]+)% \| Total: ([\d.]+)%",
                    section_content,
                )
                if score_match:
                    structural, semantic, total = map(float, score_match.groups())
                
                # Extract critical issues
                critical_issues_match = re.search(r"\*\*Critical Issues:\*\*\n(.*?)(?=\n\n|\Z)", section_content, re.DOTALL)
                if critical_issues_match:
                    issues_text = critical_issues_match.group(1)
                    # Parse each issue line (starts with -)
                    for issue_line in issues_text.split('\n'):
                        issue_line = issue_line.strip()
                        if issue_line.startswith('-'):
                            critical_issues.append({'message': issue_line[1:].strip()})
                
                # Get comparison results text
                comparison_match = re.search(r"### Comparison Results\n\n(.*?)(?=\n---\n|\Z)", section_content, re.DOTALL)
                if comparison_match:
                    comparison_text = comparison_match.group(1).strip()
            
            # Get line ranges from test_ranges.json if available
            ts_start, ts_end, py_start, py_end = self._get_test_ranges(test_num)
            
            all_tests.append(
                TestCase(
                    test_number=test_num,
                    test_name=test_name,
                    status=status,
                    ts_file=ts_full_path,
                    ts_line=ts_line,
                    ts_start=ts_start or ts_line,
                    ts_end=ts_end or ts_line,
                    py_file=py_full_path,
                    py_line=py_line,
                    py_start=py_start or py_line,
                    py_end=py_end or py_line,
                    py_function_name=py_function_name or test_name.strip(),
                    ts_code=ts_code,
                    py_code=py_code,
                    structural_score=structural,
                    semantic_score=semantic,
                    total_score=total,
                    comparison_results=comparison_text,
                    critical_issues=critical_issues,
                )
            )

        return all_tests
    
    def _extract_py_function_name(self, py_file: str, py_line: int) -> str:
        """Extract Python function name from file at given line."""
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # Look backwards from the line number to find the function definition
            for i in range(py_line - 1, max(-1, py_line - 50), -1):
                if i < len(lines):
                    func_match = re.match(r'^\s*(?:async\s+)?def\s+(test_[a-zA-Z0-9_]+)\s*\(', lines[i])
                    if func_match:
                        return func_match.group(1)
        except Exception:
            pass
        return ""
    
    def _read_code_from_file(self, file_path: str, line_num: int) -> str:
        """Read code from file, looking for test function around the given line."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            is_typescript = file_path.endswith('.ts') or file_path.endswith('.tsx')
            
            # Find the test function start
            start_line = line_num - 1
            for i in range(line_num - 1, max(-1, line_num - 50), -1):
                if i >= len(lines):
                    continue
                line = lines[i]
                if is_typescript:
                    # TypeScript: test('...', async () => { or it('...', async () => {
                    if re.search(r'^\s*(?:test|it)\s*\(', line):
                        start_line = i
                        break
                else:
                    # Python: def test_ or async def test_
                    if re.match(r'^\s*(?:async\s+)?def\s+test_', line):
                        start_line = i
                        break
            
            # Find the test function end
            if start_line < len(lines):
                if is_typescript:
                    # TypeScript: find matching closing brace for the test function
                    # Look for the opening brace of the test function (after async () => {)
                    brace_count = 0
                    found_test_brace = False
                    end_line = len(lines)
                    for i in range(start_line, len(lines)):
                        line = lines[i]
                        for char in line:
                            if char == '{':
                                brace_count += 1
                                if brace_count == 1:
                                    found_test_brace = True
                            elif char == '}':
                                brace_count -= 1
                                if found_test_brace and brace_count == 0:
                                    end_line = i + 1
                                    return ''.join(lines[start_line:end_line])
                    return ''.join(lines[start_line:end_line])
                else:
                    # Python: next function or class at same or lower indent
                    start_indent = len(lines[start_line]) - len(lines[start_line].lstrip())
                    end_line = len(lines)
                    for i in range(start_line + 1, len(lines)):
                        current_indent = len(lines[i]) - len(lines[i].lstrip())
                        stripped = lines[i].strip()
                        if stripped and current_indent <= start_indent:
                            if re.match(r'(?:async\s+)?def\s+|class\s+|@', stripped):
                                end_line = i
                                break
                    
                    return ''.join(lines[start_line:end_line])
        except Exception as e:
            print(f"     ⚠️  Error reading code from {file_path}: {e}")
        return ""
    
    def _get_test_ranges(self, test_number: int) -> tuple:
        """Get test line ranges from test_ranges.json if available."""
        try:
            json_path = Path('test_ranges.json')
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    test_data = json.load(f)
                # Find test by number (assuming test_data is a list and test_number is 1-indexed)
                if isinstance(test_data, list) and test_number <= len(test_data):
                    entry = test_data[test_number - 1]
                    if entry.get('test_number') == test_number or entry.get('test_name'):
                        return (
                            entry.get('ts_start', 0),
                            entry.get('ts_end', 0),
                            entry.get('py_start', 0),
                            entry.get('py_end', 0),
                        )
        except Exception:
            pass
        return (0, 0, 0, 0)


class TestRunner:
    """Runs individual pytest tests and captures output."""

    def __init__(self, test_file: str, base_dir: str = "."):
        self.test_file = test_file
        self.base_dir = base_dir

    def run_test(
        self, test_name: str, timeout: int = 60
    ) -> tuple[bool, str, str]:
        """
        Run a specific test and return (success, stdout, stderr).

        Args:
            test_name: The test function name or test class::method
            timeout: Maximum time to wait for test completion

        Returns:
            Tuple of (success: bool, stdout: str, stderr: str)
        """
        try:
            # Construct pytest command
            cmd = [
                "pytest",
                self.test_file,
                "-v",
                "-k",
                test_name,
                "--tb=short",
                "--no-header",
            ]

            # Run the test
            result = subprocess.run(
                cmd,
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            success = result.returncode == 0
            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return False, "", f"Test timed out after {timeout} seconds"
        except Exception as e:
            return False, "", f"Error running test: {str(e)}"


class TestModifier:
    """Handles test file modifications based on AI analysis."""

    def __init__(self, test_file: str):
        self.test_file = test_file
        self.original_content = None

    def backup_original(self):
        """Create a backup of the original test file."""
        if self.original_content is None:
            with open(self.test_file, "r") as f:
                self.original_content = f.read()
            backup_file = f"{self.test_file}.backup"
            with open(backup_file, "w") as f:
                f.write(self.original_content)

    def restore_original(self):
        """Restore the original test file from backup."""
        if self.original_content:
            with open(self.test_file, "w") as f:
                f.write(self.original_content)

    def apply_modification(self, old_code: str, new_code: str) -> bool:
        """
        Apply a modification to the test file.

        Args:
            old_code: The code to replace
            new_code: The new code to insert

        Returns:
            True if modification was successful
        """
        try:
            with open(self.test_file, "r") as f:
                content = f.read()

            if old_code not in content:
                print(f"  ⚠️  Warning: Could not find exact match for code to replace")
                return False

            modified_content = content.replace(old_code, new_code, 1)

            with open(self.test_file, "w") as f:
                f.write(modified_content)

            return True
        except Exception as e:
            print(f"  ❌ Error applying modification: {e}")
            return False


class AIAnalyzer:
    """AI-powered test analysis using intelligent pattern matching."""

    def __init__(self):
        # Import the AI analyzer
        try:
            from ai_test_analyzer import CursorCodeIntegration

            self.ai = CursorCodeIntegration()
            self.available = True
        except ImportError:
            print("⚠️  Warning: AI analyzer not available, using basic mode")
            self.ai = None
            self.available = False

    def analyze_test_failure(
        self, test: TestCase, test_output: str, test_error: str, attempt: int = 1
    ) -> Optional[dict]:
        """
        Analyze test failure and suggest modifications based on comparison data.

        Args:
            test: The test case with comparison data
            test_output: stdout from test run
            test_error: stderr from test run
            attempt: Current attempt number

        Returns:
            Dictionary with 'old_code' and 'new_code' or None if no fix available
        """
        print("\n  🤖 AI Analysis:")

        # First, try to use comparison data (critical issues, differences, suggestions)
        if test.critical_issues or test.comparison_differences or test.comparison_suggestions:
            modification = self._analyze_from_comparison(test)
            if modification:
                return modification

        # Fall back to pattern-based analysis from test output
        if not self.available:
            print("     ⚠️  AI analyzer not available")
            return None

        # Use the AI analyzer for pattern-based fixes
        modification = self.ai.analyze_and_fix(
            test.test_name, test.py_code, test.ts_code, test_output, test_error, attempt
        )

        if modification:
            print(f"     ✓ Found potential fix (confidence: {modification.confidence:.0%})")
            print(f"     ℹ️  {modification.explanation}")
            return {
                "old_code": modification.old_code,
                "new_code": modification.new_code,
            }
        else:
            explanation = self.ai.explain_failure(test_output, test_error)
            print(f"     ✗ No automatic fix available")
            print(f"     ℹ️  {explanation}")
            return None
    
    def _analyze_from_comparison(self, test: TestCase) -> Optional[dict]:
        """Analyze test based on comparison data - focus on assertions only."""
        print("     🔍 Using comparison data for alignment...")
        
        # Focus on assertion-related critical issues only
        assertion_issues = []
        if test.critical_issues:
            for issue in test.critical_issues:
                issue_msg = issue.get('message', '') if isinstance(issue, dict) else str(issue)
                issue_type = issue.get('type', '') if isinstance(issue, dict) else ''
                
                # Only handle assertion-related issues
                if 'assertion' in issue_msg.lower() or issue_type in ['operator_mismatch', 'value_mismatch', 'missing_assertions', 'extra_assertions']:
                    assertion_issues.append(issue)
                    print(f"     📋 Found assertion issue: {issue_type} - {issue_msg[:60]}")
        
        # Try to fix assertion issues
        if assertion_issues:
            for issue in assertion_issues[:3]:  # Try first 3 assertion issues
                issue_msg = issue.get('message', '') if isinstance(issue, dict) else str(issue)
                issue_type = issue.get('type', '') if isinstance(issue, dict) else ''
                
                # Handle missing assertions
                if 'missing' in issue_msg.lower() and 'assertion' in issue_msg.lower():
                    result = self._add_missing_assertions(test, issue)
                    if result:
                        print(f"     ✓ Generated fix for missing assertions")
                        return result
                
                # Handle assertion mismatches
                if issue_type == 'operator_mismatch' or issue_type == 'value_mismatch':
                    result = self._fix_assertion_mismatch(test, issue)
                    if result:
                        print(f"     ✓ Generated fix for assertion mismatch")
                        return result
        
        # If no assertion fixes available, use AI analyzer to align the full test
        print("     🤖 No assertion-specific fixes found - using AI to align full test...")
        return self._align_test_with_ai(test)
    
    def _add_missing_assertions(self, test: TestCase, issue: dict) -> Optional[dict]:
        """Add missing assertions based on TypeScript test."""
        # Get TS steps to see what assertions are missing
        if not test.comparison_result:
            return None
        
        ts_steps = test.comparison_result.get('ts_steps_detailed', [])
        py_steps = test.comparison_result.get('py_steps_detailed', [])
        
        # Find assertions in TS that might be missing in PY
        ts_assertions = [s for s in ts_steps if s.get('type') == 'assertion']
        py_assertions = [s for s in py_steps if s.get('type') == 'assertion']
        
        if len(ts_assertions) > len(py_assertions):
            # Find the missing assertion(s)
            missing_idx = len(py_assertions)
            if missing_idx < len(ts_assertions):
                ts_assert = ts_assertions[missing_idx]
                # Try to convert TS assertion to Python
                new_assertion = self._convert_ts_assertion_to_py(ts_assert, test.ts_code)
                if new_assertion:
                    # Find insertion point (after last assertion in PY code)
                    lines = test.py_code.split('\n')
                    insert_line = self._find_assertion_insertion_point(lines)
                    if insert_line is not None:
                        new_lines = lines[:insert_line] + [new_assertion] + lines[insert_line:]
                        return {
                            "old_code": test.py_code,
                            "new_code": "\n".join(new_lines),
                        }
        return None
    
    def _fix_assertion_mismatch(self, test: TestCase, issue: dict) -> Optional[dict]:
        """Fix assertion operator or value mismatch."""
        ts_step = issue.get('ts_step', {})
        py_step = issue.get('py_step', {})
        
        if not ts_step or not py_step:
            return None
        
        # Find the assertion in Python code and replace it
        py_code_lines = test.py_code.split('\n')
        for i, line in enumerate(py_code_lines):
            # Look for assertion lines
            if 'assert' in line.lower():
                # Try to match this line with the py_step
                # This is a simplified approach - could be improved
                ts_op = ts_step.get('operator', '')
                py_op = py_step.get('operator', '')
                
                # If operators differ, try to fix
                if ts_op != py_op and self._are_operators_equivalent(ts_op, py_op):
                    # Operators are equivalent, no change needed
                    continue
                
                # Try to update the assertion based on TS
                # This is a placeholder - would need more sophisticated matching
                pass
        
        return None
    
    def _align_test_with_ai(self, test: TestCase) -> Optional[dict]:
        """Use AI analyzer to align Python test with TypeScript test."""
        if not self.available:
            print("     ⚠️  AI analyzer not available for alignment")
            return None
        
        # Create a prompt for the AI analyzer to align the tests
        # The AI analyzer should compare TS and PY code and suggest alignment
        print("     📤 Sending TS and PY code to AI analyzer for alignment...")
        
        # Use the AI analyzer with a focus on alignment
        # Pass the comparison context (critical issues, differences) as part of the "error" message
        alignment_context = []
        if test.critical_issues:
            alignment_context.append(f"Critical issues: {len(test.critical_issues)}")
        if test.comparison_differences:
            alignment_context.append(f"Structural differences: {len(test.comparison_differences)}")
        if test.total_score > 0:
            alignment_context.append(f"Current similarity: {test.total_score:.2%}")
        
        context_msg = "Test alignment needed. " + "; ".join(alignment_context) if alignment_context else "Test alignment needed."
        
        modification = self.ai.analyze_and_fix(
            test.test_name, 
            test.py_code, 
            test.ts_code, 
            context_msg,  # Use context as "stdout"
            "",  # Empty stderr
            1  # First attempt
        )
        
        if modification:
            print(f"     ✓ AI generated alignment fix (confidence: {modification.confidence:.0%})")
            print(f"     ℹ️  {modification.explanation}")
            return {
                "old_code": modification.old_code,
                "new_code": modification.new_code,
            }
        else:
            print("     ⚠️  AI analyzer could not generate alignment fix")
            return None
    
    def _convert_ts_assertion_to_py(self, ts_assert: dict, ts_code: str) -> Optional[str]:
        """Convert a TypeScript assertion to Python."""
        # This is a placeholder - would need to parse TS assertion and convert
        # For now, return None to indicate we can't auto-convert
        return None
    
    def _find_assertion_insertion_point(self, lines: list) -> Optional[int]:
        """Find where to insert a new assertion in Python code."""
        # Look for the last assertion in the code
        for i in range(len(lines) - 1, -1, -1):
            if 'assert' in lines[i].lower():
                return i + 1
        # If no assertions found, look for the end of the test function
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith('def ') or lines[i].strip().startswith('async def '):
                # Find the end of this function
                indent = len(lines[i]) - len(lines[i].lstrip())
                for j in range(i + 1, len(lines)):
                    current_indent = len(lines[j]) - len(lines[j].lstrip())
                    if lines[j].strip() and current_indent <= indent:
                        return j
                return len(lines)
        return None
    
    def _are_operators_equivalent(self, op1: str, op2: str) -> bool:
        """Check if two operators are equivalent (e.g., '==' and 'toBe')."""
        equivalents = {
            '==': ['toBe', 'toEqual', '=='],
            '!=': ['not.toBe', 'not.toEqual', '!='],
            'is': ['toBe', '=='],
            'is not': ['not.toBe', '!='],
        }
        for key, values in equivalents.items():
            if op1 in values and op2 in values:
                return True
        return op1 == op2


class TestComparatorWrapper:
    """Wrapper for the test comparator to measure alignment scores."""
    
    def __init__(self):
        if COMPARATOR_AVAILABLE:
            self.comparator = TestComparator()
        else:
            self.comparator = None
    
    def compare_test(self, test: TestCase) -> dict:
        """Compare a test and return scores and critical issues."""
        if not self.comparator:
            return {'similarity': 0.0, 'critical_issues': []}
        
        try:
            ts_file = test.ts_file
            py_file = test.py_file
            ts_range = f"{test.ts_start}-{test.ts_end}"
            py_range = f"{test.py_start}-{test.py_end}"
            
            result = self.comparator.compare_test_files(ts_file, ts_range, py_file, py_range)
            analysis = result.get('analysis', {})
            
            # Extract critical issues - they're in the analysis dict
            critical_issues = analysis.get('critical_issues', [])
            
            # Debug: print what we got
            if not critical_issues:
                # Check if analysis has the data we need
                print(f"  🔍 Debug: analysis keys: {list(analysis.keys())}")
                print(f"  🔍 Debug: critical_issues type: {type(critical_issues)}, value: {critical_issues}")
                # Also check differences and suggestions
                differences = result.get('differences', [])
                suggestions = analysis.get('suggestions', [])
                if differences:
                    print(f"  🔍 Debug: Found {len(differences)} differences")
                if suggestions:
                    print(f"  🔍 Debug: Found {len(suggestions)} suggestions")
            
            # Also get differences and suggestions for alignment
            differences = result.get('differences', [])
            suggestions = analysis.get('suggestions', [])
            
            return {
                'similarity': result.get('similarity', 0.0),
                'structural_score': result.get('structural_score', 0.0),
                'semantic_score': result.get('semantic_score', 0.0),
                'critical_issues': critical_issues,
                'differences': differences,
                'suggestions': suggestions,
                'status': analysis.get('status', 'UNKNOWN'),
                'analysis': analysis,
                'ts_steps_detailed': result.get('ts_steps_detailed', []),
                'py_steps_detailed': result.get('py_steps_detailed', []),
            }
        except Exception as e:
            print(f"  ⚠️  Error comparing test: {e}")
            return {'similarity': 0.0, 'critical_issues': [], 'status': 'ERROR'}


class AutomatedTestFixer:
    """Main orchestrator for automated test fixing."""

    def __init__(
        self,
        report_file: str,
        test_file: str,
        max_attempts: int = 5,
        start_from: int = 1,
        skip_fixed: bool = True,
        max_tests: int = None,
        similarity_threshold: float = 0.70,
    ):
        self.parser = TestParser(report_file)
        self.runner = TestRunner(test_file)
        self.modifier = TestModifier(test_file)
        self.analyzer = AIAnalyzer()
        self.comparator = TestComparatorWrapper()
        self.report = TestFixerReport()
        self.max_attempts = max_attempts
        self.start_from = start_from
        self.skip_fixed = skip_fixed
        self.max_tests = max_tests  # Limit number of tests to process
        self.similarity_threshold = similarity_threshold  # Threshold for PASS (default 70%)

    def fix_test(self, test: TestCase) -> bool:
        """
        Attempt to align and fix a single test based on critical issues.
        Works on both PASS and FAIL tests to improve alignment.

        Returns:
            True if test alignment was improved or test passes
        """
        print(f"\n{'='*80}")
        print(f"🔧 Processing Test {test.test_number}: {test.test_name}")
        print(f"{'='*80}")
        print(f"Status: {test.status}")
        if test.status == "FAIL":
            print(f"Current Score: {test.total_score}%")
        print(f"File: {test.py_file}:{test.py_line}")
        
        # Check if we should attempt improvements
        # Always attempt improvements for FAIL tests
        # For PASS tests, attempt if there are critical issues or similarity < 100%
        should_improve = False
        if test.status == "FAIL":
            should_improve = True
            print(f"  ⚠️  Test is FAILING - will attempt fixes")
        elif test.critical_issues:
            should_improve = True
            print(f"  ℹ️  Test PASSES but has {len(test.critical_issues)} critical issue(s) - will attempt alignment")
        elif test.total_score > 0 and test.total_score < 100.0:
            should_improve = True
            print(f"  ℹ️  Test PASSES but similarity is {test.total_score}% - will attempt alignment improvements")
        
        if not should_improve:
            print(f"  ✓ Test PASSES with no issues - skipping")
            return True

        # Backup original file before modifications
        self.modifier.backup_original()
        
        # Initial comparison to get baseline score
        print(f"  📊 Measuring initial alignment...")
        comparison_result = self.comparator.compare_test(test)
        current_score = comparison_result.get('similarity', test.total_score)
        current_critical_issues = comparison_result.get('critical_issues', test.critical_issues)
        current_differences = comparison_result.get('differences', [])
        current_suggestions = comparison_result.get('suggestions', [])
        print(f"  📈 Initial similarity score: {current_score:.2%}")
        if current_critical_issues:
            print(f"  ⚠️  Found {len(current_critical_issues)} critical issue(s):")
            for issue in current_critical_issues[:3]:
                issue_msg = issue.get('message', 'Unknown issue') if isinstance(issue, dict) else str(issue)
                print(f"     - {issue_msg}")
        if current_differences:
            print(f"  📋 Found {len(current_differences)} structural difference(s)")
        if current_suggestions:
            print(f"  💡 Found {len(current_suggestions)} suggestion(s) for improvement")

        for attempt in range(1, self.max_attempts + 1):
            print(f"\n📍 Attempt {attempt}/{self.max_attempts}")

            # Re-measure alignment after modifications
            if attempt > 1:
                print(f"  📊 Re-measuring alignment after modification...")
                comparison_result = self.comparator.compare_test(test)
                current_score = comparison_result.get('similarity', current_score)
                current_critical_issues = comparison_result.get('critical_issues', current_critical_issues)
                current_differences = comparison_result.get('differences', [])
                current_suggestions = comparison_result.get('suggestions', [])
                print(f"  📈 Current similarity score: {current_score:.2%}")
                
                # Check if we've reached the threshold
                if current_score >= self.similarity_threshold:
                    print(f"  ✅ Alignment score ({current_score:.2%}) meets threshold ({self.similarity_threshold:.2%})!")
                    # Verify test still passes
                    test_identifier = test.py_function_name if test.py_function_name else test.test_name
                    success, stdout, stderr = self.runner.run_test(test_identifier)
                    if success:
                        print(f"  ✅ Test also PASSES!")
                        self.report.add_success(
                            test.test_number, test.test_name, attempt, 
                            f"Alignment improved to {current_score:.2%}"
                        )
                        return True
                    else:
                        print(f"  ⚠️  Alignment improved but test fails - continuing...")

            # Show critical issues
            if current_critical_issues:
                print(f"  📋 Critical Issues ({len(current_critical_issues)}):")
                for issue in current_critical_issues[:5]:  # Show first 5
                    issue_msg = issue.get('message', 'Unknown issue') if isinstance(issue, dict) else str(issue)
                    print(f"     - {issue_msg}")
            else:
                if current_score >= self.similarity_threshold:
                    print(f"  ✓ No critical issues - alignment is good")
                    # Verify test passes
                    test_identifier = test.py_function_name if test.py_function_name else test.test_name
                    success, stdout, stderr = self.runner.run_test(test_identifier)
                    if success:
                        self.report.add_success(
                            test.test_number, test.test_name, attempt,
                            f"Alignment score: {current_score:.2%}"
                        )
                        return True

            # Analyze and suggest fix based on critical issues, differences, or suggestions
            if current_critical_issues or current_differences or current_suggestions:
                print(f"  🔍 Analyzing for alignment improvement...")
                # Update test object with current comparison data
                test.critical_issues = current_critical_issues
                # Store additional comparison data in test for analyzer
                test.comparison_differences = current_differences
                test.comparison_suggestions = current_suggestions
                test.comparison_result = comparison_result
                
                modification = self.analyzer.analyze_test_failure(
                    test, "", "", attempt
                )
            else:
                modification = None
                if current_score >= self.similarity_threshold:
                    print(f"  ✓ Alignment is acceptable - no modifications needed")
                    return True

            if modification is None:
                print(f"  ⚠️  No automatic fix available based on critical issues")
                if attempt == self.max_attempts:
                    self.modifier.restore_original()
                    self.report.add_failure(
                        test.test_number, test.test_name, attempt,
                        f"Final score: {current_score:.2%}, threshold: {self.similarity_threshold:.2%}"
                    )
                    return False
                continue

            # Apply modification
            print(f"  🔧 Applying modification...")
            if not self.modifier.apply_modification(
                modification["old_code"], modification["new_code"]
            ):
                print(f"  ❌ Failed to apply modification")
                if attempt == self.max_attempts:
                    self.modifier.restore_original()
                    self.report.add_failure(
                        test.test_number,
                        test.test_name,
                        attempt,
                        "Failed to apply modification",
                    )
                    return False
                continue

        # Final comparison
        print(f"\n  📊 Final alignment measurement...")
        final_comparison = self.comparator.compare_test(test)
        final_score = final_comparison.get('similarity', current_score)
        print(f"  📈 Final similarity score: {final_score:.2%}")
        
        if final_score >= self.similarity_threshold:
            print(f"  ✅ Alignment improved to threshold!")
            # Verify test passes
            test_identifier = test.py_function_name if test.py_function_name else test.test_name
            success, stdout, stderr = self.runner.run_test(test_identifier)
            if success:
                self.report.add_success(
                    test.test_number, test.test_name, self.max_attempts,
                    f"Final alignment: {final_score:.2%}"
                )
                return True
        
        print(f"\n  ❌ Max attempts ({self.max_attempts}) reached")
        print(f"  📊 Final score: {final_score:.2%} (threshold: {self.similarity_threshold:.2%})")
        self.modifier.restore_original()
        self.report.add_failure(
            test.test_number, test.test_name, self.max_attempts,
            f"Final alignment: {final_score:.2%}, threshold: {self.similarity_threshold:.2%}"
        )
        return False

    def run(self):
        """Run the automated test fixer."""
        print("🚀 Automated Test Fixer Starting...")
        print(f"📄 Report File: {self.parser.report_file}")
        print(f"📝 Test File: {self.runner.test_file}")
        print(f"🔢 Max Attempts per Test: {self.max_attempts}")
        print(f"⏭️  Starting from Test: {self.start_from}")

        # Parse all tests (both PASS and FAIL) to maintain test number alignment
        print("\n📊 Parsing all tests from report...")
        all_tests = self.parser.parse_all_tests()
        print(f"Found {len(all_tests)} total tests")
        
        # Count by status
        pass_count = sum(1 for t in all_tests if t.status == "PASS")
        fail_count = sum(1 for t in all_tests if t.status == "FAIL")
        print(f"  - PASS: {pass_count}")
        print(f"  - FAIL: {fail_count}")

        # Filter based on start_from
        tests_to_process = [t for t in all_tests if t.test_number >= self.start_from]
        
        # Limit number of tests if max_tests is set
        if self.max_tests is not None:
            tests_to_process = tests_to_process[:self.max_tests]
            print(f"Processing {len(tests_to_process)} tests (starting from #{self.start_from}, limited to {self.max_tests})")
        else:
            print(f"Processing {len(tests_to_process)} tests (starting from #{self.start_from})")

        # Process each test
        total_fixed = 0
        total_failed = 0

        for test in tests_to_process:
            if self.fix_test(test):
                total_fixed += 1
            else:
                total_failed += 1

        # Final summary
        print(f"\n{'='*80}")
        print("📊 FINAL SUMMARY")
        print(f"{'='*80}")
        print(f"✅ Tests Fixed: {total_fixed}")
        print(f"❌ Tests Failed: {total_failed}")
        print(f"📈 Success Rate: {total_fixed / len(tests_to_process) * 100:.1f}%")
        print(f"\n📄 Detailed report saved to: {self.report.output_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated Test Fixer for CWI Style Wallet Manager Tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fix all tests starting from the beginning
  python auto_test_fixer.py

  # Start from test number 10
  python auto_test_fixer.py --start-from 10

  # Use custom report file and test file
  python auto_test_fixer.py --report custom_report.md --test-file custom_test.py

  # Increase max attempts per test
  python auto_test_fixer.py --max-attempts 10
        """,
    )

    parser.add_argument(
        "--report",
        default="test_comparison_detailed_report.md",
        help="Path to the detailed test comparison report (default: test_comparison_detailed_report.md)",
    )

    parser.add_argument(
        "--test-file",
        default="py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py",
        help="Path to the test file to modify (default: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py)",
    )

    parser.add_argument(
        "--max-attempts",
        type=int,
        default=5,
        help="Maximum number of fix attempts per test (default: 5)",
    )

    parser.add_argument(
        "--start-from",
        type=int,
        default=1,
        help="Test number to start from (useful for resuming) (default: 1)",
    )

    parser.add_argument(
        "--no-skip-fixed",
        action="store_true",
        help="Re-process tests that were previously fixed",
    )

    parser.add_argument(
        "--max-tests",
        type=int,
        default=None,
        help="Maximum number of tests to process (default: None, process all)",
    )

    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.70,
        help="Similarity threshold for PASS (default: 0.70 = 70%%)",
    )

    args = parser.parse_args()

    # Validate files exist
    if not os.path.exists(args.report):
        print(f"❌ Error: Report file not found: {args.report}")
        sys.exit(1)

    if not os.path.exists(args.test_file):
        print(f"❌ Error: Test file not found: {args.test_file}")
        sys.exit(1)

    # Create and run fixer
    fixer = AutomatedTestFixer(
        report_file=args.report,
        test_file=args.test_file,
        max_attempts=args.max_attempts,
        start_from=args.start_from,
        skip_fixed=not args.no_skip_fixed,
        max_tests=args.max_tests,
        similarity_threshold=args.similarity_threshold,
    )

    try:
        fixer.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        print("💾 Progress has been saved to test_fixer_report.md")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
