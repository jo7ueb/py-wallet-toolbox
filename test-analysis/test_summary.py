#!/usr/bin/env python3
"""Generate test coverage summary statistics."""

from pathlib import Path
import re

def count_lines_in_file(filepath):
    """Count lines in markdown file."""
    content = Path(filepath).read_text()
    lines = content.split('\n')
    
    # Count table rows (exclude header and separator)
    test_rows = [l for l in lines if l.startswith('| ') and 'Test Name' not in l and '|---' not in l and 'Total missing' not in l]
    
    return len(test_rows)

def extract_file_stats(filepath):
    """Extract statistics by file."""
    content = Path(filepath).read_text()
    lines = content.split('\n')
    
    file_stats = {}
    
    for line in lines:
        if line.startswith('| ') and '|---' not in line and 'Test Name' not in line and 'Total missing' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                ts_file = parts[2]
                if ts_file:
                    file_stats[ts_file] = file_stats.get(ts_file, 0) + 1
    
    return file_stats

def main():
    md_file = Path('/tmp/missing_python_tests.md')
    
    total_missing = count_lines_in_file(md_file)
    file_stats = extract_file_stats(md_file)
    
    print("=" * 80)
    print("TEST COVERAGE SUMMARY")
    print("=" * 80)
    print()
    print(f"Total missing Python test cases: {total_missing}")
    print()
    print("Top 10 TypeScript files with most missing Python tests:")
    print("-" * 80)
    
    sorted_files = sorted(file_stats.items(), key=lambda x: x[1], reverse=True)
    
    for i, (file, count) in enumerate(sorted_files[:10], 1):
        print(f"{i:2}. {file:60} ({count:3} tests)")
    
    print()
    print("=" * 80)
    print(f"Full report available at: missing_python_tests.md")
    print("=" * 80)

if __name__ == '__main__':
    main()
