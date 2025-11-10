#!/usr/bin/env python3
"""Parse matching_tests.md and generate test_ranges.json with up to 4 entries."""

import re
import json
from pathlib import Path

def find_test_range(file_path: str, start_line: int) -> tuple:
    """
    Find the full range of a test function starting at start_line.
    Returns (start, end) line numbers (1-indexed).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Adjust to 0-indexed
        idx = start_line - 1
        if idx < 0 or idx >= len(lines):
            return (start_line, start_line)

        # Find the start of the test (look backwards for test declaration)
        test_start = idx
        for i in range(idx, max(-1, idx - 50), -1):
            line = lines[i].strip()
            # TypeScript: test('...', or it('...', or describe('...',
            # Python: def test_... or async def test_...
            if (re.match(r"(test|it|describe)\s*\(", line) or
                re.match(r"(async\s+)?def\s+test_", line)):
                test_start = i
                break

        # Find the end of the test (look for closing brace/dedent)
        test_end = test_start

        # Determine if it's TypeScript or Python
        is_python = file_path.endswith('.py')

        if is_python:
            # For Python, find the next function definition or end of file
            # by looking for the next line at the same or lower indentation level
            start_indent = len(lines[test_start]) - len(lines[test_start].lstrip())
            for i in range(test_start + 1, len(lines)):
                current_indent = len(lines[i]) - len(lines[i].lstrip())
                stripped = lines[i].strip()
                # Stop at next function/class definition at same or lower indent
                # Also stop at decorators (which precede the next function)
                if stripped and current_indent <= start_indent:
                    if re.match(r"(async\s+)?def\s+|class\s+|@", stripped):
                        test_end = i - 1
                        break
            else:
                test_end = len(lines) - 1
        else:
            # For TypeScript/JavaScript, count braces
            brace_count = 0
            started = False
            for i in range(test_start, len(lines)):
                line = lines[i]
                for char in line:
                    if char == '{':
                        brace_count += 1
                        started = True
                    elif char == '}':
                        brace_count -= 1
                        if started and brace_count == 0:
                            test_end = i
                            return (test_start + 1, test_end + 1)  # Convert back to 1-indexed
            test_end = min(test_start + 100, len(lines) - 1)  # Fallback

        return (test_start + 1, test_end + 1)  # Convert back to 1-indexed

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return (start_line, start_line)

def parse_matching_tests(md_file: str, max_tests: int = 4) -> list:
    """Parse matching_tests.md and extract up to max_tests entries with full ranges."""
    entries = []
    base_path = Path(__file__).parent

    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find the table start (after header row)
    in_table = False
    for line in lines:
        # if len(entries) >= max_tests:
        #     break

        line = line.strip()

        # Skip header and separator rows
        if line.startswith('|') and 'Test Name' in line:
            in_table = True
            continue
        if line.startswith('|') and '---' in line:
            continue
        if not in_table:
            continue

        # Parse table row
        if line.startswith('|') and line.endswith('|'):
            parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
            if len(parts) < 3:
                continue

            test_name = parts[0]
            ts_link = parts[1]
            py_link = parts[2]
            py_function = parts[3] if len(parts) > 3 else None  # Python function name from table

            # Remove similarity percentage from test name if present (handles both formats)
            test_name = re.sub(r'\s*\(\d+%\)\s*$', '', test_name)  # (94%)
            test_name = re.sub(r'\s*\*\(\d+%\)\*\s*$', '', test_name)  # *(94%)*
            test_name = test_name.strip()

            # Extract Python function name from markdown code block if present
            if py_function:
                py_function = re.sub(r'^`|`$', '', py_function).strip()  # Remove backticks

            # Parse TS file and line number
            # Format: [filename:line](file:///path#Lline)
            ts_match = re.search(r'\[([^\]]+):(\d+)\]', ts_link)
            if not ts_match:
                continue
            ts_file = ts_match.group(1)
            ts_line = int(ts_match.group(2))

            # Parse PY file and line number
            py_match = re.search(r'\[([^\]]+):(\d+)\]', py_link)
            if not py_match:
                continue
            py_file = py_match.group(1)
            py_line = int(py_match.group(2))

            # Find full paths
            ts_path = base_path / "wallet-toolbox" / ts_file
            py_path = base_path / "py-wallet-toolbox" / "tests" / py_file

            # If Python function name not in table, extract it from the file
            if not py_function:
                try:
                    with open(py_path, 'r', encoding='utf-8') as f:
                        py_lines = f.readlines()
                        # Look backwards from the line number to find the function definition
                        for i in range(py_line - 1, max(-1, py_line - 50), -1):
                            if i < len(py_lines):
                                func_match = re.match(r'^\s*(?:async\s+)?def\s+(test_[a-zA-Z0-9_]+)\s*\(', py_lines[i])
                                if func_match:
                                    py_function = func_match.group(1)
                                    break
                except Exception:
                    pass

            # Find full test ranges
            ts_start, ts_end = find_test_range(str(ts_path), ts_line)
            py_start, py_end = find_test_range(str(py_path), py_line)

            entries.append({
                "test_name": test_name,
                "ts_file": ts_file,
                "ts_start": ts_start,
                "ts_end": ts_end,
                "py_file": py_file,
                "py_start": py_start,
                "py_end": py_end,
                "py_function_name": py_function or ""  # Add Python function name
            })

            print(f"Found test {len(entries)}: {test_name}")
            print(f"  TS: {ts_file}:{ts_start}-{ts_end}")
            print(f"  PY: {py_file}:{py_start}-{py_end}")
            if py_function:
                print(f"  PY Function: {py_function}")

    return entries

def main():
    md_file = Path('matching_tests.md')
    json_file = Path('test_ranges.json')

    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return

    print(f"Parsing {md_file} (max 4 tests)...")
    entries = parse_matching_tests(str(md_file), max_tests=4)

    print(f"\nFound {len(entries)} test entries")

    # Write to JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"Generated {json_file} with {len(entries)} entries")

if __name__ == '__main__':
    main()

