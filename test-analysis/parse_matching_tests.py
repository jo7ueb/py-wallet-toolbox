#!/usr/bin/env python3
"""Parse matching_tests.md and generate test_ranges.json with all entries."""

import re
import json
from pathlib import Path

def parse_matching_tests(md_file: str) -> list:
    """Parse matching_tests.md and extract all test entries."""
    entries = []
    
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the table start (after header row)
    in_table = False
    for line in lines:
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
            
            # Remove similarity percentage from test name if present (handles both formats)
            test_name = re.sub(r'\s*\(\d+%\)\s*$', '', test_name)  # (94%)
            test_name = re.sub(r'\s*\*\(\d+%\)\*\s*$', '', test_name)  # *(94%)*
            test_name = test_name.strip()
            
            # Parse TS file and line range
            # Format: [filename:start-end](file:///path#Lstart-Lend)
            ts_match = re.search(r'\[([^\]]+):(\d+)-(\d+)\]', ts_link)
            if not ts_match:
                continue
            ts_file = ts_match.group(1)
            ts_start = int(ts_match.group(2))
            ts_end = int(ts_match.group(3))
            
            # Parse PY file and line range
            py_match = re.search(r'\[([^\]]+):(\d+)-(\d+)\]', py_link)
            if not py_match:
                continue
            py_file = py_match.group(1)
            py_start = int(py_match.group(2))
            py_end = int(py_match.group(3))
            
            entries.append({
                "test_name": test_name,
                "ts_file": ts_file,
                "ts_start": ts_start,
                "ts_end": ts_end,
                "py_file": py_file,
                "py_start": py_start,
                "py_end": py_end
            })
    
    return entries

def main():
    md_file = Path('matching_tests.md')
    json_file = Path('test_ranges.json')
    
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return
    
    print(f"Parsing {md_file}...")
    entries = parse_matching_tests(str(md_file))
    
    print(f"Found {len(entries)} test entries")
    
    # Write to JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {json_file} with {len(entries)} entries")

if __name__ == '__main__':
    main()

