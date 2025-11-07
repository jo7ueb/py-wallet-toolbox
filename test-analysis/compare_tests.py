#!/usr/bin/env python3
"""
Compare TypeScript and Python tests to find missing Python test cases.
Uses fuzzy matching to identify similar test names across languages.
"""

import re
import subprocess
from pathlib import Path
from difflib import SequenceMatcher
from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class TestCase:
    """Represents a single test case."""
    file_path: str
    test_name: str
    full_name: str  # including describe blocks for TS


@dataclass
class MissingTest:
    """Represents a test present in TS but missing in Python."""
    ts_test_name: str
    ts_file_path: str
    proposed_py_file: str
    similarity_score: float


def normalize_name(name: str) -> str:
    """Normalize test names for comparison."""
    # Convert from camelCase/PascalCase to snake_case
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    # Remove common prefixes
    name = re.sub(r'^(test_|Test)', '', name, flags=re.IGNORECASE)
    # Remove special characters
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Lowercase
    name = name.lower()
    # Remove multiple underscores
    name = re.sub(r'_+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    return name


def extract_ts_file_base(ts_path: str) -> str:
    """Extract base name from TypeScript test file path."""
    # e.g., "WalletPermissionsManager.callbacks.test.ts" -> "wallet_permissions_manager_callbacks"
    basename = Path(ts_path).name
    # Remove .test.ts or .spec.ts
    basename = re.sub(r'\.(test|spec)\.ts$', '', basename)
    # Remove Test suffix if present
    basename = re.sub(r'Tests?$', '', basename, flags=re.IGNORECASE)
    return normalize_name(basename)


def extract_py_file_base(py_path: str) -> str:
    """Extract base name from Python test file path."""
    # e.g., "test_wallet_permissions_manager_callbacks.py" -> "wallet_permissions_manager_callbacks"
    basename = Path(py_path).name
    # Remove test_ prefix and .py
    basename = re.sub(r'^test_', '', basename)
    basename = re.sub(r'\.py$', '', basename)
    return normalize_name(basename)


def similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


def find_python_test_file(ts_file_path: str, py_test_files_with_paths: dict) -> str:
    """Find the most likely corresponding Python test file with full path."""
    ts_base = extract_ts_file_base(ts_file_path)

    best_match = None
    best_score = 0.0

    for py_file, full_path in py_test_files_with_paths.items():
        py_base = extract_py_file_base(py_file)
        score = similarity(ts_base, py_base)

        if score > best_score:
            best_score = score
            best_match = full_path

    # Only return if similarity is reasonable (> 0.4)
    if best_score > 0.4:
        return best_match
    return "-"


def parse_ts_tests(ts_root: Path) -> List[TestCase]:
    """Parse TypeScript test files and extract test cases."""
    test_cases = []

    # Find all test files
    test_files = []
    for pattern in ['**/*.test.ts', '**/*.spec.ts']:
        for f in ts_root.glob(pattern):
            # Skip node_modules
            if 'node_modules' not in str(f):
                test_files.append(f)

    for test_file in test_files:
        rel_path = str(test_file.relative_to(ts_root))

        try:
            content = test_file.read_text(encoding='utf-8')

            # Extract test names using regex
            # Pattern for: it('test name', ...) or test('test name', ...)
            test_pattern = r"(?:it|test)\s*\(\s*['\"]([^'\"]+)['\"]"
            describe_pattern = r"describe\s*\(\s*['\"]([^'\"]+)['\"]"

            for match in re.finditer(test_pattern, content):
                test_name = match.group(1)
                test_cases.append(TestCase(
                    file_path=rel_path,
                    test_name=test_name,
                    full_name=test_name
                ))
        except Exception as e:
            print(f"Error reading {test_file}: {e}")

    return test_cases


def parse_py_tests(py_test_output: str, py_root: Path) -> tuple[List[TestCase], dict]:
    """Parse pytest output to extract test cases and file paths with full paths."""
    test_cases = []
    test_files_with_paths = {}  # filename -> full relative path

    current_file = None
    current_dir_stack = []

    for line in py_test_output.split('\n'):
        # Match directory lines: <Dir dirname>
        dir_match = re.search(r'<(?:Dir|Package) ([^>]+)>', line)
        if dir_match:
            dirname = dir_match.group(1)
            # Determine depth by leading spaces
            indent = len(line) - len(line.lstrip())
            depth = indent // 2

            # Adjust stack to current depth
            current_dir_stack = current_dir_stack[:depth]
            current_dir_stack.append(dirname)
            continue

        # Match module lines: <Module test_something.py>
        module_match = re.search(r'<Module (test_[^>]+\.py)>', line)
        if module_match:
            current_file = module_match.group(1)
            # Build full path from directory stack
            if current_dir_stack:
                # Skip the root project dir name
                path_parts = [p for p in current_dir_stack if p not in ['py-wallet-toolbox', 'tests']]
                if path_parts:
                    full_path = '/'.join(path_parts) + '/' + current_file
                else:
                    full_path = current_file
            else:
                full_path = current_file

            test_files_with_paths[current_file] = full_path
            continue

        # Match function lines: <Function test_something>
        func_match = re.search(r'<(?:Function|Coroutine) (test_[^>]+)>', line)
        if func_match and current_file:
            test_name = func_match.group(1)
            test_cases.append(TestCase(
                file_path=current_file,
                test_name=test_name,
                full_name=test_name
            ))

    return test_cases, test_files_with_paths


def find_missing_tests(
    ts_tests: List[TestCase],
    py_tests: List[TestCase],
    py_test_files_with_paths: dict
) -> List[MissingTest]:
    """Find TypeScript tests that don't have corresponding Python tests."""

    # Create normalized Python test set for quick lookup
    py_normalized = {}
    for py_test in py_tests:
        normalized = normalize_name(py_test.test_name)
        if normalized not in py_normalized:
            py_normalized[normalized] = []
        py_normalized[normalized].append(py_test)

    missing_tests = []

    for ts_test in ts_tests:
        ts_normalized = normalize_name(ts_test.test_name)

        # Check if there's an exact normalized match
        if ts_normalized in py_normalized:
            continue

        # Check if there's a similar match (fuzzy)
        best_similarity = 0.0
        for py_norm in py_normalized.keys():
            sim = similarity(ts_normalized, py_norm)
            if sim > best_similarity:
                best_similarity = sim

        # If similarity is high enough (> 0.8), consider it a match
        if best_similarity > 0.8:
            continue

        # This is a missing test
        proposed_py_file = find_python_test_file(ts_test.file_path, py_test_files_with_paths)

        missing_tests.append(MissingTest(
            ts_test_name=ts_test.test_name,
            ts_file_path=ts_test.file_path,
            proposed_py_file=proposed_py_file,
            similarity_score=best_similarity
        ))

    return missing_tests


def generate_markdown_table(missing_tests: List[MissingTest]) -> str:
    """Generate a markdown table of missing tests."""

    # Sort by file path, then by test name
    missing_tests.sort(key=lambda x: (x.ts_file_path, x.ts_test_name))

    lines = [
        "# Missing Python Test Cases",
        "",
        "This table shows TypeScript test cases that don't have corresponding Python tests.",
        "",
        "| Test Name | TS File Path | Proposed Python Test File Path |",
        "|-----------|--------------|--------------------------------|",
    ]

    for test in missing_tests:
        test_name = test.ts_test_name.replace('|', '\\|')
        ts_path = test.ts_file_path.replace('|', '\\|')
        py_file = test.proposed_py_file.replace('|', '\\|')

        lines.append(f"| {test_name} | {ts_path} | {py_file} |")

    lines.append("")
    lines.append(f"**Total missing tests: {len(missing_tests)}**")

    return '\n'.join(lines)


def main():
    # Paths
    ts_root = Path('/mnt/c/Users/honoh/YenPoint/toolbox/wallet-toolbox')
    py_root = Path('/mnt/c/Users/honoh/YenPoint/toolbox/py-wallet-toolbox')
    py_test_output_file = Path('/mnt/c/Users/honoh/YenPoint/toolbox/py_tests.txt')

    print("Parsing TypeScript tests...")
    ts_tests = parse_ts_tests(ts_root)
    print(f"Found {len(ts_tests)} TypeScript tests")

    print("\nParsing Python tests...")
    if py_test_output_file.exists():
        py_test_output = py_test_output_file.read_text()
    else:
        # Run pytest to collect tests
        result = subprocess.run(
            ['python', '-m', 'pytest', 'tests/', '--collect-only', '-q'],
            cwd=str(py_root),
            capture_output=True,
            text=True
        )
        py_test_output = result.stdout

    py_tests, py_test_files_with_paths = parse_py_tests(py_test_output, py_root)
    print(f"Found {len(py_tests)} Python tests in {len(py_test_files_with_paths)} files")

    print("\nFinding missing tests...")
    missing_tests = find_missing_tests(ts_tests, py_tests, py_test_files_with_paths)
    print(f"Found {len(missing_tests)} missing Python tests")

    print("\nGenerating markdown table...")
    markdown = generate_markdown_table(missing_tests)

    # Write to file
    output_file = Path('/mnt/c/Users/honoh/YenPoint/toolbox/missing_python_tests.md')
    output_file.write_text(markdown)
    print(f"\nMarkdown table written to: {output_file}")

    # Also print to console
    print("\n" + markdown)


if __name__ == '__main__':
    main()
