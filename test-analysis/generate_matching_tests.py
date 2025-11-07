#!/usr/bin/env python3
"""
Generate a report of TypeScript tests that DO exist in Python.
Creates a markdown table with clickable links to implementation files and line numbers.
"""

import re
import subprocess
from pathlib import Path
from difflib import SequenceMatcher
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional


@dataclass
class TestCase:
    """Represents a single test case."""
    file_path: str
    test_name: str
    line_number: int
    full_name: str


@dataclass
class MatchedTest:
    """Represents a test that exists in both TS and Python."""
    test_name: str
    ts_file_path: str
    ts_line_number: int
    py_file_path: str
    py_line_number: int
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


def similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


def parse_ts_tests_with_lines(ts_root: Path) -> List[TestCase]:
    """Parse TypeScript test files and extract test cases with line numbers."""
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
            lines = content.split('\n')

            # Extract test names with line numbers using regex
            # Pattern for: it('test name', ...) or test('test name', ...)
            test_pattern = r"(?:it|test)\s*\(\s*['\"]([^'\"]+)['\"]"

            for line_idx, line in enumerate(lines, start=1):
                matches = re.finditer(test_pattern, line)
                for match in matches:
                    test_name = match.group(1)
                    test_cases.append(TestCase(
                        file_path=rel_path,
                        test_name=test_name,
                        line_number=line_idx,
                        full_name=test_name
                    ))
        except Exception as e:
            print(f"Error reading {test_file}: {e}")

    return test_cases


def parse_py_tests_with_lines(py_root: Path) -> Tuple[List[TestCase], Dict[str, str]]:
    """Parse Python test files directly to get line numbers."""
    test_cases = []
    test_files_with_paths = {}  # filename -> full relative path

    # Find all test files
    test_files = list(py_root.glob('tests/**/test_*.py'))

    for test_file in test_files:
        rel_path = str(test_file.relative_to(py_root / 'tests'))
        filename = test_file.name
        test_files_with_paths[filename] = rel_path

        try:
            content = test_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Pattern for: def test_something(...) or async def test_something(...)
            test_pattern = r'^\s*(?:async\s+)?def\s+(test_[a-zA-Z0-9_]+)\s*\('

            for line_idx, line in enumerate(lines, start=1):
                match = re.match(test_pattern, line)
                if match:
                    test_name = match.group(1)
                    test_cases.append(TestCase(
                        file_path=rel_path,
                        test_name=test_name,
                        line_number=line_idx,
                        full_name=test_name
                    ))
        except Exception as e:
            print(f"Error reading {test_file}: {e}")

    return test_cases, test_files_with_paths


def find_matching_tests(
    ts_tests: List[TestCase],
    py_tests: List[TestCase]
) -> List[MatchedTest]:
    """Find TypeScript tests that have corresponding Python tests."""

    # Create normalized Python test lookup with details
    py_normalized: Dict[str, List[TestCase]] = {}
    for py_test in py_tests:
        normalized = normalize_name(py_test.test_name)
        if normalized not in py_normalized:
            py_normalized[normalized] = []
        py_normalized[normalized].append(py_test)

    matched_tests = []

    for ts_test in ts_tests:
        ts_normalized = normalize_name(ts_test.test_name)

        # Check for exact normalized match
        if ts_normalized in py_normalized:
            for py_test in py_normalized[ts_normalized]:
                matched_tests.append(MatchedTest(
                    test_name=ts_test.test_name,
                    ts_file_path=ts_test.file_path,
                    ts_line_number=ts_test.line_number,
                    py_file_path=py_test.file_path,
                    py_line_number=py_test.line_number,
                    similarity_score=1.0
                ))
            continue

        # Check for fuzzy match (>0.8 similarity)
        best_match = None
        best_score = 0.0

        for py_norm, py_test_list in py_normalized.items():
            score = similarity(ts_normalized, py_norm)
            if score > best_score:
                best_score = score
                best_match = py_test_list[0]  # Take first match

        # If similarity is high enough (> 0.8), consider it a match
        if best_score > 0.8 and best_match:
            matched_tests.append(MatchedTest(
                test_name=ts_test.test_name,
                ts_file_path=ts_test.file_path,
                ts_line_number=ts_test.line_number,
                py_file_path=best_match.file_path,
                py_line_number=best_match.line_number,
                similarity_score=best_score
            ))

    return matched_tests


def generate_markdown_table(matched_tests: List[MatchedTest], ts_root: Path, py_root: Path) -> str:
    """Generate a markdown table of matching tests with clickable links."""

    # Sort by TS file path, then by test name
    matched_tests.sort(key=lambda x: (x.ts_file_path, x.test_name))

    lines = [
        "# Matching Test Cases (TypeScript ↔ Python)",
        "",
        "This table shows TypeScript test cases that have corresponding Python tests.",
        "",
        f"**Total matching tests: {len(matched_tests)}**",
        "",
        "| Test Name | TypeScript File | Python File |",
        "|-----------|-----------------|-------------|",
    ]

    for test in matched_tests:
        test_name = test.test_name.replace('|', '\\|')

        # Create clickable file:line links
        ts_link = f"[{test.ts_file_path}:{test.ts_line_number}](file://{ts_root}/{test.ts_file_path}#L{test.ts_line_number})"
        py_link = f"[{test.py_file_path}:{test.py_line_number}](file://{py_root}/tests/{test.py_file_path}#L{test.py_line_number})"

        # Add similarity indicator for fuzzy matches
        if test.similarity_score < 1.0:
            test_name += f" *({test.similarity_score:.0%})*"

        lines.append(f"| {test_name} | {ts_link} | {py_link} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**Legend:**")
    lines.append("- Percentages in parentheses indicate fuzzy matches (< 100% similarity)")
    lines.append("- Click on file paths to open them at the exact line number")
    lines.append("")

    return '\n'.join(lines)


def main():
    # Paths
    ts_root = Path('/mnt/c/Users/honoh/YenPoint/toolbox/wallet-toolbox')
    py_root = Path('/mnt/c/Users/honoh/YenPoint/toolbox/py-wallet-toolbox')

    print("Parsing TypeScript tests with line numbers...")
    ts_tests = parse_ts_tests_with_lines(ts_root)
    print(f"Found {len(ts_tests)} TypeScript tests")

    print("\nParsing Python tests with line numbers...")
    py_tests, py_test_files_with_paths = parse_py_tests_with_lines(py_root)
    print(f"Found {len(py_tests)} Python tests in {len(py_test_files_with_paths)} files")

    print("\nFinding matching tests...")
    matched_tests = find_matching_tests(ts_tests, py_tests)
    print(f"Found {len(matched_tests)} matching tests")

    print("\nGenerating markdown table...")
    markdown = generate_markdown_table(matched_tests, ts_root, py_root)

    # Write to file
    output_file = Path('/mnt/c/Users/honoh/YenPoint/toolbox/matching_tests.md')
    output_file.write_text(markdown)
    print(f"\nMarkdown table written to: {output_file}")

    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total TypeScript tests: {len(ts_tests)}")
    print(f"Total Python tests: {len(py_tests)}")
    print(f"Matching tests: {len(matched_tests)}")
    print(f"Coverage: {len(matched_tests)/len(ts_tests)*100:.1f}%")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
