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
            # Handle assert all(...) or assert any(...)
            if isinstance(stmt.test, ast.Call):
                func_name = self._get_name(stmt.test.func)
                if func_name in ['all', 'any']:
                    # Extract the comparison from generator expression
                    if stmt.test.args and isinstance(stmt.test.args[0], ast.GeneratorExp):
                        gen_exp = stmt.test.args[0]
                        if isinstance(gen_exp.elt, ast.Compare):
                            # Extract the comparison
                            left = self._get_name(gen_exp.elt.left)
                            op = self._get_operator(gen_exp.elt.ops[0])
                            right = self._get_name(gen_exp.elt.comparators[0]) if gen_exp.elt.comparators else None
                            # For all(), we can represent it as checking all elements match
                            target = f"all({left} {op} {right})" if right else f"all({left})"
                            return TestStep(
                                type='assertion',
                                target=target,
                                operator='==',
                                args=['true'] if func_name == 'all' else []
                            )
                        else:
                            # Just extract the element expression
                            condition = self._get_name(gen_exp.elt)
                            return TestStep(
                                type='assertion',
                                target=condition,
                                operator='==',
                                args=['true'] if func_name == 'all' else []
                            )
                    elif stmt.test.args:
                        # Simple condition
                        condition = self._get_name(stmt.test.args[0])
                        return TestStep(
                            type='assertion',
                            target=condition,
                            operator='==',
                            args=['true'] if func_name == 'all' else []
                        )
            
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
        elif isinstance(node, ast.Subscript):
            # Handle array indexing like r[i] or a[i]
            value = self._get_name(node.value)
            slice_val = self._get_name(node.slice) if hasattr(node, 'slice') and node.slice else ''
            return f"{value}[{slice_val}]" if slice_val else f"{value}[]"
        elif isinstance(node, ast.Call):
            # For call expressions, return the full call representation
            func_name = self._get_name(node.func)
            args = [self._get_name(arg) for arg in node.args]
            args_str = ', '.join(args) if args else ''
            return f"{func_name}({args_str})"
        elif isinstance(node, ast.Compare):
            # Handle comparisons like r[i] == a[i]
            left = self._get_name(node.left)
            op = self._get_operator(node.ops[0]) if node.ops else '=='
            right = self._get_name(node.comparators[0]) if node.comparators else ''
            return f"{left} {op} {right}" if right else left
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Dict):
            # Handle dictionary literals like {"partial": {}}
            # For comparison purposes, we'll represent it as a simplified form
            keys = [self._get_name(k) if k else '' for k in node.keys]
            values = [self._get_name(v) for v in node.values]
            pairs = [f"{k}:{v}" for k, v in zip(keys, values) if k]
            return '{' + ', '.join(pairs) + '}' if pairs else '{}'
        # Note: ast.Str and ast.Num were deprecated in Python 3.8 and removed in 3.14
        # ast.Constant handles all constant values (strings, numbers, etc.) in Python 3.8+
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

        # Expect assertions - check FIRST before generic function calls
        # expect(x).toBe(y) or expect(await x).toBe(y) or expect(x).not.toBe(y)
        # Strip await from inside expect() - it doesn't affect test logic
        match = re.match(r'expect\((.*?)\)\.(?:not\.)?(\w+)\((.*?)\)', line)
        if match:
            target, assertion, arg = match.groups()
            # Remove await keyword from target (async differences are whitelisted)
            target = re.sub(r'\bawait\s+', '', target).strip()
            # Handle 'not.toBe' case
            if 'not.' in line and line.find('not.') < line.find(assertion):
                assertion = f'not.{assertion}'
            operator = self._jest_to_operator(assertion)
            return TestStep(
                type='assertion',
                target=target,
                operator=operator,
                args=[arg.strip()] if arg.strip() else []
            )

        # Variable assignment with function call
        # const x = func(args) or const x = await func(args)
        # Note: await is stripped - async differences are whitelisted
        match = re.match(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:await\s+)?(\w+(?:\.\w+)*)\((.*?)\)', line)
        if match:
            target, func, args_str = match.groups()
            args = [a.strip() for a in args_str.split(',') if a.strip()]
            # Remove await from args if present (normalize async differences)
            args = [re.sub(r'\bawait\s+', '', arg) for arg in args]
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

        # Function call (but skip expect calls as they should be assertions)
        # func(args) or await func(args)
        # Note: await is stripped - async differences are whitelisted
        match = re.match(r'(?:await\s+)?(\w+(?:\.\w+)*)\((.*?)\)', line)
        if match:
            func, args_str = match.groups()
            # Skip expect() calls that weren't caught as assertions
            if func == 'expect':
                return None
            args = [a.strip() for a in args_str.split(',') if a.strip()]
            # Remove await from args if present (normalize async differences)
            args = [re.sub(r'\bawait\s+', '', arg) for arg in args]
            return TestStep(
                type='call',
                function=func,
                args=args
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

        # Filter out test framework calls (test(), describe(), etc.)
        ts_steps = [s for s in ts_steps if not (s.type == 'call' and s.function in ['test', 'describe', 'it', 'beforeEach', 'afterEach'])]
        py_steps = [s for s in py_steps if not (s.type == 'call' and s.function in ['pytest', 'fixture'])]
        
        # Filter out Python setup code (mock creation, fixtures, etc.)
        # This whitelists setup code so it doesn't affect similarity scores
        py_steps = [s for s in py_steps if not self._is_setup_code(s)]
        
        # Normalize async/await differences - remove async markers from arguments
        # This whitelists async differences so they don't affect similarity scores
        for step in ts_steps + py_steps:
            if step.args:
                step.args = [re.sub(r'\bawait\s+', '', arg) for arg in step.args]
                step.args = [re.sub(r'\basync\s+', '', arg) for arg in step.args]
            if step.target:
                step.target = re.sub(r'\bawait\s+', '', step.target)
                step.target = re.sub(r'\basync\s+', '', step.target)

        # Normalize steps
        ts_normalized = [step.normalize() for step in ts_steps]
        py_normalized = [step.normalize() for step in py_steps]

        # Normalize assignment+assertion patterns to match direct function calls in assertions
        # e.g., "count = func()" + "assert count == X" should match "expect(func()).toBe(X)"
        ts_normalized = self._normalize_assignment_assertion_patterns(ts_normalized)
        py_normalized = self._normalize_assignment_assertion_patterns(py_normalized)

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
        """Convert step to comparable string with normalized arguments."""
        parts = [step.type]
        if step.target:
            # Normalize semantically equivalent targets (r.length -> len(r), etc.)
            target = self._normalize_target(step.target)
            parts.append(f"target:{target}")
        if step.function:
            parts.append(f"func:{step.function}")
        if step.operator:
            parts.append(f"op:{step.operator}")
        if step.args:
            # Normalize args: strip quotes, normalize whitespace
            normalized_args = [self._normalize_arg(arg) for arg in step.args]
            parts.append(f"args:{','.join(normalized_args)}")
        return '|'.join(parts)

    def _normalize_assignment_assertion_patterns(self, steps: List[TestStep]) -> List[TestStep]:
        """Normalize assignment+assertion patterns to match direct function calls in assertions.
        
        Converts:
        - assignment: count = func(args)
        - assertion: count == value
        Into:
        - assertion: func(args) == value
        
        This makes Python's pattern match TypeScript's direct function call in expect().
        """
        normalized = []
        i = 0
        while i < len(steps):
            current = steps[i]
            
            # Check if this is an assignment followed by an assertion on the same variable
            if (i + 1 < len(steps) and 
                current.type == 'assignment' and 
                current.target and 
                current.function and
                steps[i + 1].type == 'assertion' and
                steps[i + 1].target == current.target):
                
                # This is assignment+assertion pattern - normalize to direct function call assertion
                next_step = steps[i + 1]
                
                # Create a new assertion with the function call as the target
                normalized_step = TestStep(
                    type='assertion',
                    target=f"{current.function}({','.join(current.args)})" if current.args else current.function,
                    operator=next_step.operator,
                    args=next_step.args
                )
                normalized.append(normalized_step)
                i += 2  # Skip both steps
            else:
                normalized.append(current)
                i += 1
        
        return normalized

    def _normalize_target(self, target: str) -> str:
        """Normalize semantically equivalent target expressions."""
        if not target:
            return target
        
        import re
        
        # Normalize r.length to len(r) for comparison
        match = re.match(r'(\w+)\.length', target)
        if match:
            return f"len({match.group(1)})"
        
        # Normalize r.every((v, i) => v === a[i]) to all(elements_match)
        # and all(r[i] == a[i]) to all(elements_match)
        # Both represent "check all elements match"
        if 'every' in target.lower() or target.startswith('all('):
            # Check if it's a comparison of array elements
            if '==' in target or '===' in target:
                return "all(elements_match)"
            return "all(elements_match)"
        
        # Normalize variable names: storage vs mock_storage are equivalent
        # Extract function calls and normalize the object name
        # e.g., "storage.countProvenTxs(...)" and "mock_storage.count_proven_txs(...)" should match
        # We normalize to just the function name for comparison
        func_call_match = re.match(r'(\w+)(?:\.|_)?(\w+)\(', target)
        if func_call_match:
            # Extract just the function name part, ignore the object name
            # This makes storage.func() and mock_storage.func() equivalent
            obj_name, func_name = func_call_match.groups()
            # Keep the full call but normalize object names
            normalized_obj = 'storage' if 'storage' in obj_name.lower() or 'mock' in obj_name.lower() else obj_name
            # Replace the object name with normalized version
            target = re.sub(r'^(\w+)(?:\.|_)?', f'{normalized_obj}.', target, count=1)
        
        # Normalize dictionary/object spacing in function call arguments
        # { partial: {} } should match {partial:{}} and { partial:{} }
        if '{' in target and '}' in target:
            # Remove all whitespace inside dictionaries (handles nested dicts)
            import re
            # Recursively remove whitespace from dictionary contents
            while True:
                new_target = re.sub(r'\{([^{}]*)\}', lambda m: '{' + re.sub(r'\s+', '', m.group(1)) + '}', target)
                if new_target == target:
                    break
                target = new_target
        
        return target

    def _normalize_arg(self, arg: str) -> str:
        """Normalize argument values for comparison."""
        if not arg:
            return arg
        
        # Strip surrounding quotes (single or double)
        arg = arg.strip()
        if (arg.startswith("'") and arg.endswith("'")) or (arg.startswith('"') and arg.endswith('"')):
            arg = arg[1:-1]
        
        # Normalize dictionary/object argument spacing
        # { partial: {} } should match {partial:{}} and { partial:{} }
        import re
        if arg.startswith('{') and arg.endswith('}'):
            # Remove all whitespace inside the dictionary
            arg = re.sub(r'\s+', '', arg)
        
        # Normalize string escape sequences
        # Both \x01\x02\x03\x04 (string representation) and actual bytes should match
        # Check if this looks like a hex escape sequence pattern
        # Convert both \x01\x02\x03\x04 and actual control characters to a normalized form
        if '\\x' in arg or any(ord(c) < 32 and c not in '\t\n\r' for c in arg):
            # Normalize escape sequences to a standard representation
            # Replace \xHH with normalized form, or actual control chars
            arg = re.sub(r'\\x([0-9a-fA-F]{2})', r'\\x\1', arg)
            # For actual control characters, convert to \x notation
            normalized = []
            for char in arg:
                if ord(char) < 32 and char not in '\t\n\r':
                    normalized.append(f'\\x{ord(char):02x}')
                else:
                    normalized.append(char)
            arg = ''.join(normalized)
            # Normalize to lowercase hex
            arg = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: f'\\x{m.group(1).lower()}', arg)
        
        # Lowercase for case-insensitive comparison
        arg = arg.lower()
        
        # Remove extra whitespace (but preserve structure for non-dict args)
        if not (arg.startswith('{') and arg.endswith('}')):
            arg = ' '.join(arg.split())
        
        return arg

    def _is_setup_code(self, step: TestStep) -> bool:
        """Check if a step is setup code that should be whitelisted.
        
        Setup code includes:
        - Mock object creation (type(), Mock(), etc.)
        - Test fixture creation
        - But NOT assignments that call methods on mocks (those are test operations)
        """
        if step.type == 'assignment':
            # Check if it's creating a mock or test fixture (not using one)
            if step.function:
                # Mock creation patterns: type(), Mock(), MagicMock(), etc.
                # The function might be parsed as 'type(...)' or just 'type'
                setup_functions = ['type', 'mock', 'magicmock', 'patch', 'fixture', 'setup']
                func_lower = step.function.lower()
                
                # Check if function name starts with or equals a setup function
                # e.g., 'type(...)' or 'type' or 'mock(...)'
                if any(func_lower.startswith(setup_func + '(') or func_lower == setup_func 
                       for setup_func in setup_functions):
                    return True
                # If it contains 'type(' in the function name, it's likely mock creation
                if 'type(' in func_lower:
                    return True
            
            # Check if target name suggests setup AND it's creating a mock
            # mock_storage = type(...) is setup
            # count = mock_storage.count_proven_txs(...) is NOT setup
            if step.target:
                setup_prefixes = ['mock_', 'test_', 'fixture_', 'setup_', 'given_']
                target_lower = step.target.lower()
                if any(target_lower.startswith(prefix) for prefix in setup_prefixes):
                    # Only filter if it's creating the mock, not using it
                    # Check if function name indicates setup
                    if step.function:
                        func_lower = step.function.lower()
                        if any(func_lower.startswith(setup_func + '(') or func_lower == setup_func 
                               for setup_func in ['type', 'mock', 'magicmock']):
                            return True
                        if 'type(' in func_lower:
                            return True
        
        return False

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
        test_json_path = Path('test_ranges.json')
        if not test_json_path.exists():
            # Try alternative locations
            alt_paths = [
                Path('/tmp/test_ranges.json'),
                Path('py-wallet-toolbox/test-analysis/test_ranges.json'),
            ]
            for alt_path in alt_paths:
                if alt_path.exists():
                    test_json_path = alt_path
                    break
            else:
                print(f"Error: test_ranges.json not found. Please create it in the current directory.")
                return
        
        with open(test_json_path, 'r', encoding='utf-8') as f:
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
