#!/usr/bin/env python3
"""
Compare TypeScript and Python test implementations.

This script parses test code from both languages, extracts the sequence of operations,
and performs fuzzy matching to verify they implement the same test logic.
"""

import ast
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
import subprocess


@dataclass
class TestStep:
    """Represents a single step in a test."""
    type: str  # 'call', 'assignment', 'assertion', 'await', 'return'
    target: Optional[str] = None  # Variable being assigned to
    function: Optional[str] = None  # Function being called
    args: List[str] = None  # Argument names/values
    operator: Optional[str] = None  # For assertions: '==', '!=', etc.

    def __post_init__(self):
        if self.args is None:
            self.args = []

    def normalize(self) -> 'TestStep':
        """Normalize names for comparison (camelCase -> snake_case)."""
        normalized = TestStep(
            type=self.type,
            target=self._normalize_name(self.target) if self.target else None,
            function=self._normalize_name(self.function) if self.function else None,
            args=[self._normalize_name(arg) for arg in self.args],
            operator=self.operator
        )
        return normalized

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Convert camelCase/snake_case to normalized form."""
        if not name:
            return name

        # Convert camelCase to snake_case
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        name = name.lower()

        # Remove common prefixes/suffixes
        name = re.sub(r'^(test_|_test)', '', name)
        name = re.sub(r'(_test|test_)$', '', name)

        return name

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class PythonTestParser:
    """Parse Python test code and extract test steps."""

    def parse_test(self, code: str) -> List[TestStep]:
        """Parse Python test code and return list of steps."""
        # Dedent the code to handle indented methods
        import textwrap
        code = textwrap.dedent(code)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            print(f"Python syntax error: {e}")
            return []

        steps = []

        # Find test functions (including async)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith('test_'):
                steps.extend(self._parse_function(node))

        return steps

    def _parse_function(self, func_node: ast.FunctionDef) -> List[TestStep]:
        """Parse a function and extract steps."""
        steps = []

        for stmt in func_node.body:
            step = self._parse_statement(stmt)
            if step:
                steps.append(step)

        return steps

    def _parse_statement(self, stmt: ast.AST) -> Optional[TestStep]:
        """Parse a single statement."""
        # Assignment
        if isinstance(stmt, ast.Assign):
            target = self._get_name(stmt.targets[0]) if stmt.targets else None

            # Handle await expressions
            value = stmt.value
            if isinstance(value, ast.Await):
                value = value.value

            # Check if RHS is a function call
            if isinstance(value, ast.Call):
                func_name = self._get_name(value.func)
                args = [self._get_name(arg) for arg in value.args]

                return TestStep(
                    type='assignment',
                    target=target,
                    function=func_name,
                    args=args
                )
            else:
                return TestStep(
                    type='assignment',
                    target=target
                )

        # Function call (expression statement)
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            func_name = self._get_name(stmt.value.func)
            args = [self._get_name(arg) for arg in stmt.value.args]

            return TestStep(
                type='call',
                function=func_name,
                args=args
            )

        # Assert statement
        elif isinstance(stmt, ast.Assert):
            if isinstance(stmt.test, ast.Compare):
                left = self._get_name(stmt.test.left)
                op = self._get_operator(stmt.test.ops[0])
                right = self._get_name(stmt.test.comparators[0]) if stmt.test.comparators else None

                return TestStep(
                    type='assertion',
                    target=left,
                    operator=op,
                    args=[right] if right else []
                )

        # Await expression
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Await):
            return TestStep(type='await')

        return None

    def _get_name(self, node: ast.AST) -> str:
        """Extract name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            base = self._get_name(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return str(node.n)
        return ""

    def _get_operator(self, op: ast.AST) -> str:
        """Get operator as string."""
        op_map = {
            ast.Eq: '==',
            ast.NotEq: '!=',
            ast.Lt: '<',
            ast.LtE: '<=',
            ast.Gt: '>',
            ast.GtE: '>=',
            ast.Is: 'is',
            ast.IsNot: 'is not',
            ast.In: 'in',
            ast.NotIn: 'not in'
        }
        return op_map.get(type(op), str(op))


class TypeScriptTestParser:
    """Parse TypeScript test code and extract test steps."""

    def parse_test(self, code: str) -> List[TestStep]:
        """Parse TypeScript test code using regex patterns."""
        steps = []

        # Remove comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

        lines = code.split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('{') or line.startswith('}'):
                continue

            step = self._parse_line(line)
            if step:
                steps.append(step)

        return steps

    def _parse_line(self, line: str) -> Optional[TestStep]:
        """Parse a single line of TypeScript."""

        # Variable assignment with function call
        # const x = func(args)
        match = re.match(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:await\s+)?(\w+(?:\.\w+)*)\((.*?)\)', line)
        if match:
            target, func, args_str = match.groups()
            args = [a.strip() for a in args_str.split(',') if a.strip()]
            return TestStep(
                type='assignment',
                target=target,
                function=func,
                args=args
            )

        # Assignment without function call
        # const x = value
        match = re.match(r'(?:const|let|var)\s+(\w+)\s*=\s*(.+)', line)
        if match:
            target, value = match.groups()
            return TestStep(
                type='assignment',
                target=target,
                args=[value.rstrip(';')]
            )

        # Function call
        # func(args)
        match = re.match(r'(?:await\s+)?(\w+(?:\.\w+)*)\((.*?)\)', line)
        if match:
            func, args_str = match.groups()
            args = [a.strip() for a in args_str.split(',') if a.strip()]
            return TestStep(
                type='call',
                function=func,
                args=args
            )

        # Expect assertions
        # expect(x).toBe(y)
        match = re.match(r'expect\((.*?)\)\.(\w+)\((.*?)\)', line)
        if match:
            target, assertion, arg = match.groups()
            operator = self._jest_to_operator(assertion)
            return TestStep(
                type='assertion',
                target=target.strip(),
                operator=operator,
                args=[arg.strip()] if arg.strip() else []
            )

        return None

    def _jest_to_operator(self, jest_assertion: str) -> str:
        """Convert Jest assertion to operator."""
        mapping = {
            'toBe': '==',
            'toEqual': '==',
            'toStrictEqual': '==',
            'not.toBe': '!=',
            'not.toEqual': '!=',
            'toBeGreaterThan': '>',
            'toBeGreaterThanOrEqual': '>=',
            'toBeLessThan': '<',
            'toBeLessThanOrEqual': '<=',
            'toBeTruthy': '== true',
            'toBeFalsy': '== false',
            'toBeNull': '== null',
            'toBeUndefined': '== undefined',
            'toBeDefined': '!= undefined',
        }
        return mapping.get(jest_assertion, jest_assertion)


class TestComparator:
    """Compare test implementations."""

    def __init__(self):
        self.py_parser = PythonTestParser()
        self.ts_parser = TypeScriptTestParser()

    def compare_tests(self, ts_code: str, py_code: str) -> Dict[str, Any]:
        """Compare TypeScript and Python test implementations."""

        # Parse both tests
        ts_steps = self.ts_parser.parse_test(ts_code)
        py_steps = self.py_parser.parse_test(py_code)

        # Normalize steps
        ts_normalized = [step.normalize() for step in ts_steps]
        py_normalized = [step.normalize() for step in py_steps]

        # Compare sequences
        similarity = self._calculate_similarity(ts_normalized, py_normalized)

        # Find matching and differing steps
        matches, differences = self._align_steps(ts_normalized, py_normalized)

        return {
            'ts_steps': len(ts_steps),
            'py_steps': len(py_steps),
            'similarity': similarity,
            'matches': matches,
            'differences': differences,
            'ts_steps_detailed': [step.to_dict() for step in ts_steps],
            'py_steps_detailed': [step.to_dict() for step in py_steps],
        }

    def _calculate_similarity(self, ts_steps: List[TestStep], py_steps: List[TestStep]) -> float:
        """Calculate similarity score between 0 and 1."""
        if not ts_steps and not py_steps:
            return 1.0
        if not ts_steps or not py_steps:
            return 0.0

        # Convert steps to comparable strings
        ts_strings = [self._step_to_string(step) for step in ts_steps]
        py_strings = [self._step_to_string(step) for step in py_steps]

        # Use SequenceMatcher for sequence comparison
        matcher = SequenceMatcher(None, ts_strings, py_strings)
        return matcher.ratio()

    def _step_to_string(self, step: TestStep) -> str:
        """Convert step to comparable string."""
        parts = [step.type]
        if step.target:
            parts.append(f"target:{step.target}")
        if step.function:
            parts.append(f"func:{step.function}")
        if step.operator:
            parts.append(f"op:{step.operator}")
        if step.args:
            parts.append(f"args:{','.join(step.args)}")
        return '|'.join(parts)

    def _align_steps(self, ts_steps: List[TestStep], py_steps: List[TestStep]) -> Tuple[int, List[str]]:
        """Align steps and find matches/differences."""
        ts_strings = [self._step_to_string(step) for step in ts_steps]
        py_strings = [self._step_to_string(step) for step in py_steps]

        matcher = SequenceMatcher(None, ts_strings, py_strings)

        matches = 0
        differences = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                matches += (i2 - i1)
            elif tag == 'replace':
                differences.append(f"REPLACE: TS[{i1}:{i2}] <-> PY[{j1}:{j2}]")
            elif tag == 'delete':
                differences.append(f"DELETE: TS[{i1}:{i2}] (missing in Python)")
            elif tag == 'insert':
                differences.append(f"INSERT: PY[{j1}:{j2}] (extra in Python)")

        return matches, differences

    def compare_test_files(self, ts_file: str, ts_line_range: str,
                           py_file: str, py_line_range: str) -> Dict[str, Any]:
        """Compare tests from files using line ranges."""

        # Read TypeScript code
        ts_start, ts_end = map(int, ts_line_range.split('-'))
        with open(ts_file, 'r', encoding='utf-8') as f:
            ts_lines = f.readlines()
        ts_code = ''.join(ts_lines[ts_start-1:ts_end])

        # Read Python code
        py_start, py_end = map(int, py_line_range.split('-'))
        with open(py_file, 'r', encoding='utf-8') as f:
            py_lines = f.readlines()
        py_code = ''.join(py_lines[py_start-1:py_end])

        return self.compare_tests(ts_code, py_code)


def main():
    """Main function to demonstrate usage."""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python compare_test_implementations.py <mode> [args...]")
        print()
        print("Modes:")
        print("  test - Run on sample tests from matching_tests.md")
        print("  compare <ts_file> <ts_range> <py_file> <py_range> - Compare specific test")
        print()
        print("Example:")
        print("  python compare_test_implementations.py test")
        print("  python compare_test_implementations.py compare file.ts 10-20 file.py 30-40")
        return

    mode = sys.argv[1]
    comparator = TestComparator()

    if mode == 'test':
        # Load matching tests
        import json
        with open('/tmp/test_ranges.json', 'r') as f:
            test_data = json.load(f)

        print(f"Testing on {min(5, len(test_data))} sample tests...")
        print("="*80)

        for i, entry in enumerate(test_data[:5]):
            print(f"\nTest {i+1}: {entry['test_name']}")
            print("-"*80)

            ts_file = f"wallet-toolbox/{entry['ts_file']}"
            py_file = f"py-wallet-toolbox/tests/{entry['py_file']}"

            if 'ts_start' in entry and 'py_start' in entry:
                ts_range = f"{entry['ts_start']}-{entry['ts_end']}"
                py_range = f"{entry['py_start']}-{entry['py_end']}"

                try:
                    result = comparator.compare_test_files(ts_file, ts_range, py_file, py_range)

                    print(f"TypeScript steps: {result['ts_steps']}")
                    print(f"Python steps: {result['py_steps']}")
                    print(f"Similarity: {result['similarity']:.2%}")
                    print(f"Matching steps: {result['matches']}")

                    # Show TypeScript steps in detail
                    print("\nTypeScript steps:")
                    for idx, step in enumerate(result['ts_steps_detailed']):
                        step_str = f"{step['type']}"
                        if step.get('target'):
                            step_str += f" {step['target']}"
                        if step.get('function'):
                            step_str += f" = {step['function']}()"
                        if step.get('operator'):
                            step_str += f" {step['operator']}"
                        print(f"  [{idx}] {step_str}")

                    # Show Python steps in detail
                    print("\nPython steps:")
                    for idx, step in enumerate(result['py_steps_detailed']):
                        step_str = f"{step['type']}"
                        if step.get('target'):
                            step_str += f" {step['target']}"
                        if step.get('function'):
                            step_str += f" = {step['function']}()"
                        if step.get('operator'):
                            step_str += f" {step['operator']}"
                        print(f"  [{idx}] {step_str}")

                    if result['differences']:
                        print("\nDifferences:")
                        for diff in result['differences']:
                            print(f"  {diff}")

                except Exception as e:
                    print(f"Error: {e}")

    elif mode == 'compare' and len(sys.argv) == 6:
        ts_file, ts_range, py_file, py_range = sys.argv[2:6]

        result = comparator.compare_test_files(ts_file, ts_range, py_file, py_range)

        print(json.dumps(result, indent=2))

    else:
        print("Invalid arguments. Use --help for usage.")


if __name__ == '__main__':
    main()
