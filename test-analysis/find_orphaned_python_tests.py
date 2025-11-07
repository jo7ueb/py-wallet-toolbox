#!/usr/bin/env python3
"""
Find Python tests that don't have corresponding TypeScript tests.
These might be orphaned tests that can be deleted.
Generates clickable links with line ranges for easy deletion.
"""

import re
from pathlib import Path
from difflib import SequenceMatcher
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class TestCase:
    """Represents a single test case with location info."""
    file_path: str
    test_name: str
    line_number: int
    full_name: str


@dataclass
class TestWithContext:
    """Represents a test with its full context (including comments)."""
    file_path: str
    test_name: str
    start_line: int  # Start of comment block or decorator
    end_line: int    # End of test function
    full_path: str   # Absolute path for clickable link


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
            lines = content.split('\n')

            # Extract test names
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


def parse_py_tests_with_context(py_root: Path) -> List[TestWithContext]:
    """Parse Python test files and extract tests with their full context."""
    tests_with_context = []

    # Find all test files
    test_files = list(py_root.glob('tests/**/test_*.py'))

    for test_file in test_files:
        rel_path = str(test_file.relative_to(py_root / 'tests'))
        abs_path = str(test_file.absolute())

        try:
            content = test_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Pattern for test function definition
            test_pattern = r'^\s*(?:async\s+)?def\s+(test_[a-zA-Z0-9_]+)\s*\('

            i = 0
            while i < len(lines):
                line = lines[i]
                match = re.match(test_pattern, line)

                if match:
                    test_name = match.group(1)
                    test_def_line = i + 1  # 1-indexed

                    # Find start of context (comments, decorators above the test)
                    start_line = test_def_line

                    # Look backwards for comments and decorators
                    j = i - 1
                    while j >= 0:
                        prev_line = lines[j].strip()
                        # Check if it's a comment, decorator, or blank line
                        if (prev_line.startswith('#') or
                            prev_line.startswith('@') or
                            prev_line == ''):
                            start_line = j + 1  # 1-indexed
                            j -= 1
                        else:
                            break

                    # Find end of test function
                    end_line = test_def_line
                    indent_level = len(line) - len(line.lstrip())

                    # Look forward to find the end of the function
                    k = i + 1
                    while k < len(lines):
                        current_line = lines[k]
                        # Skip blank lines
                        if current_line.strip() == '':
                            k += 1
                            continue

                        current_indent = len(current_line) - len(current_line.lstrip())

                        # If we hit a line with same or less indentation (and not blank),
                        # the function has ended
                        if current_indent <= indent_level and current_line.strip():
                            end_line = k  # 1-indexed, this is the line AFTER the function
                            break

                        k += 1
                    else:
                        # Reached end of file
                        end_line = len(lines)

                    tests_with_context.append(TestWithContext(
                        file_path=rel_path,
                        test_name=test_name,
                        start_line=start_line,
                        end_line=end_line,
                        full_path=abs_path
                    ))

                i += 1

        except Exception as e:
            print(f"Error reading {test_file}: {e}")

    return tests_with_context


def find_orphaned_python_tests(
    ts_tests: List[TestCase],
    py_tests: List[TestWithContext]
) -> List[TestWithContext]:
    """Find Python tests that don't match any TypeScript tests."""

    # Create normalized TypeScript test set
    ts_normalized = set()
    for ts_test in ts_tests:
        normalized = normalize_name(ts_test.test_name)
        ts_normalized.add(normalized)

    orphaned_tests = []

    for py_test in py_tests:
        py_normalized = normalize_name(py_test.test_name)

        # Check for exact match
        if py_normalized in ts_normalized:
            continue

        # Check for fuzzy match (>0.8 similarity)
        best_similarity = 0.0
        for ts_norm in ts_normalized:
            sim = similarity(py_normalized, ts_norm)
            if sim > best_similarity:
                best_similarity = sim

        # If similarity is high enough (> 0.8), consider it a match
        if best_similarity > 0.8:
            continue

        # This is an orphaned Python test
        orphaned_tests.append(py_test)

    return orphaned_tests


def generate_markdown_report(orphaned_tests: List[TestWithContext], py_root: Path) -> str:
    """Generate a markdown report of orphaned Python tests with clickable links."""

    # Sort by file path, then by line number
    orphaned_tests.sort(key=lambda x: (x.file_path, x.start_line))

    lines = [
        "# Orphaned Python Tests",
        "",
        "These Python tests don't have corresponding TypeScript tests.",
        "They may be candidates for deletion if they're no longer needed.",
        "",
        f"**Total orphaned tests: {len(orphaned_tests)}**",
        "",
        "| Test Name | File Location | Line Range | Actions |",
        "|-----------|---------------|------------|---------|",
    ]

    for test in orphaned_tests:
        test_name = test.test_name.replace('|', '\\|')

        # Create clickable link to the file with line range
        # Format: file://path#LstartLine-LendLine
        link = f"[{test.file_path}](file://{test.full_path}#L{test.start_line}-L{test.end_line})"
        line_range = f"L{test.start_line}-L{test.end_line}"

        # VS Code command link to select range
        vscode_link = f"`{line_range}`"

        lines.append(f"| `{test_name}` | {link} | {vscode_link} | [View](file://{test.full_path}#L{test.start_line}) |")

    lines.extend([
        "",
        "---",
        "",
        "## How to Use",
        "",
        "1. **Click the File Location** link to open the file in your editor",
        "2. The link will highlight the full test including comments/decorators",
        "3. **Review the test** to determine if it should be deleted",
        "4. If deleting, select lines from the Line Range and delete",
        "",
        "## VS Code / Cursor / PyCharm",
        "",
        "The links use the format `file://path#L<start>-L<end>` which should work in:",
        "- VS Code (click or Ctrl/Cmd+click)",
        "- Cursor IDE",
        "- PyCharm (may need plugin)",
        "- Most modern IDEs",
        "",
        "## Why These Tests Might Be Orphaned",
        "",
        "Possible reasons:",
        "1. **Python-specific functionality** - Features unique to Python implementation",
        "2. **Deprecated TypeScript tests** - TS tests were removed but Python weren't",
        "3. **Renamed TypeScript tests** - Test was renamed in TS but not Python",
        "4. **Redundant tests** - Duplicate coverage that can be removed",
        "5. **Old test framework** - Legacy tests from previous testing approach",
        "",
        "**⚠️ Review carefully before deleting!** Some tests may be intentionally Python-specific.",
        "",
    ])

    # Add statistics by directory
    dir_stats = {}
    for test in orphaned_tests:
        directory = str(Path(test.file_path).parent)
        dir_stats[directory] = dir_stats.get(directory, 0) + 1

    lines.extend([
        "## Orphaned Tests by Directory",
        "",
        "| Directory | Count |",
        "|-----------|-------|",
    ])

    for directory, count in sorted(dir_stats.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {directory} | {count} |")

    return '\n'.join(lines)


def main():
    # Paths
    ts_root = Path('/mnt/c/Users/honoh/YenPoint/toolbox/wallet-toolbox')
    py_root = Path('/mnt/c/Users/honoh/YenPoint/toolbox/py-wallet-toolbox')

    print("Parsing TypeScript tests...")
    ts_tests = parse_ts_tests(ts_root)
    print(f"Found {len(ts_tests)} TypeScript tests")

    print("\nParsing Python tests with context...")
    py_tests = parse_py_tests_with_context(py_root)
    print(f"Found {len(py_tests)} Python tests with context")

    print("\nFinding orphaned Python tests...")
    orphaned_tests = find_orphaned_python_tests(ts_tests, py_tests)
    print(f"Found {len(orphaned_tests)} orphaned Python tests")

    print("\nGenerating markdown report...")
    markdown = generate_markdown_report(orphaned_tests, py_root)

    # Write to file
    output_file = Path('/mnt/c/Users/honoh/YenPoint/toolbox/orphaned_python_tests.md')
    output_file.write_text(markdown)
    print(f"\nMarkdown report written to: {output_file}")

    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total TypeScript tests: {len(ts_tests)}")
    print(f"Total Python tests: {len(py_tests)}")
    print(f"Orphaned Python tests: {len(orphaned_tests)}")
    print(f"Percentage orphaned: {len(orphaned_tests)/len(py_tests)*100:.1f}%")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
