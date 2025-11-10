# Automated Test Fixer

An intelligent, fully automated system for fixing failing Python tests by analyzing test comparison reports, running tests, and applying AI-powered modifications.

## Features

- **Automated Test Parsing**: Extracts all FAIL tests from `test_comparison_detailed_report.md`
- **Intelligent Test Running**: Executes individual tests and captures detailed output
- **AI-Powered Analysis**: Uses pattern matching and heuristics to identify issues
- **Automatic Code Modification**: Applies fixes directly to test files
- **Retry Logic**: Attempts multiple fixes with configurable max attempts
- **Resume Support**: Can restart from any test number, skipping already-fixed tests
- **Progress Tracking**: Generates detailed reports of all fixes and failures
- **Test Number Output**: Displays test numbers as they're processed
- **Exit Conditions**: Automatically stops if no solution can be found

## Installation

The scripts are standalone Python files with minimal dependencies:

```bash
# No additional installation required beyond Python 3.8+
# The scripts use only standard library plus pytest
```

## Usage

### Basic Usage

Fix all tests starting from the beginning:

```bash
python auto_test_fixer.py
```

### Start from Specific Test

Resume from test number 10 (useful if process was interrupted):

```bash
python auto_test_fixer.py --start-from 10
```

### Custom Configuration

```bash
python auto_test_fixer.py \
  --report custom_report.md \
  --test-file path/to/test_file.py \
  --max-attempts 10 \
  --start-from 1
```

### Command Line Options

- `--report FILE`: Path to detailed test comparison report (default: `test_comparison_detailed_report.md`)
- `--test-file FILE`: Path to test file to modify (default: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`)
- `--max-attempts N`: Maximum fix attempts per test (default: 5)
- `--start-from N`: Test number to start from (default: 1)
- `--no-skip-fixed`: Re-process previously fixed tests

## How It Works

### 1. Test Parsing

The script parses `test_comparison_detailed_report.md` to extract:
- Test number
- Test name
- TypeScript reference code
- Python test code
- File locations and line numbers
- Similarity scores
- Comparison results

### 2. Test Execution

For each failing test:
1. Backs up the original test file
2. Runs the specific test using pytest
3. Captures stdout and stderr
4. Analyzes the output

### 3. AI Analysis

The AI analyzer identifies common failure patterns:

- **Mock Attribute Errors**: Missing mock method/attribute configurations
- **Call Count Mismatches**: Incorrect assertion counts
- **Missing Await Keywords**: Async functions not awaited
- **Attribute Errors**: Missing object methods or attributes
- **Error Match Patterns**: Incorrect exception message patterns
- **Import Errors**: Module import issues

### 4. Code Modification

When a fix is identified:
1. Applies the modification to the test file
2. Re-runs the test
3. If successful: Marks test as FIXED and moves to next test
4. If failed: Tries again (up to max attempts)
5. If max attempts reached: Restores original and marks as FAILED

### 5. Reporting

Generates `test_fixer_report.md` with:
- Summary statistics
- List of fixed tests with attempt counts
- List of failed tests with error details

## Output Examples

### Console Output

```
🚀 Automated Test Fixer Starting...
📄 Report File: test_comparison_detailed_report.md
📝 Test File: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py
🔢 Max Attempts per Test: 5
⏭️  Starting from Test: 1

📊 Parsing failed tests...
Found 496 failed tests
Processing 496 tests (starting from #1)

================================================================================
🔧 Processing Test 1: All proxied methods call underlying with correct arguments
================================================================================
Current Score: 5.38%
File: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py:896

📍 Attempt 1/5
  ▶️  Running test...
  ❌ Test FAILED
  📋 Error Preview:
     FAILED tests/integration/test_cwi_style_wallet_manager.py::test_all_proxied_methods_call_underlying_with_correct_arguments

  🔍 Analyzing failure...
  🤖 AI Analysis:
     ✓ Found potential fix (confidence: 80%)
     ℹ️  Added missing mock attribute 'encrypt' to 'mock_underlying_wallet'

  🔧 Applying modification...
  ▶️  Running test...
  ✅ Test PASSED on attempt 1!

================================================================================
📊 FINAL SUMMARY
================================================================================
✅ Tests Fixed: 245
❌ Tests Failed: 251
📈 Success Rate: 49.4%

📄 Detailed report saved to: test_fixer_report.md
```

## Architecture

### File Structure

```
auto_test_fixer.py          # Main orchestrator script
ai_test_analyzer.py         # AI-powered test analysis engine
test_fixer_report.md        # Generated progress report
AUTO_TEST_FIXER_README.md   # This file
```

### Key Classes

#### `AutomatedTestFixer`
Main orchestrator that coordinates all components.

#### `TestParser`
Parses the detailed test comparison report to extract failing tests.

#### `TestRunner`
Executes pytest for specific tests and captures output.

#### `TestModifier`
Handles file backups and applies code modifications.

#### `AIAnalyzer`
Analyzes test failures using pattern matching and heuristics.

#### `IntelligentTestAnalyzer`
Core AI engine with pattern recognition and fix generation.

#### `TestFixerReport`
Manages progress reporting and statistics.

## Extending the AI Analyzer

To add new fix patterns, edit `ai_test_analyzer.py`:

```python
# Add to _load_common_patterns()
"your_pattern_name": {
    "pattern": r"your_regex_pattern",
    "fix_type": "your_fix_type",
}

# Add fix generator method
def _fix_your_pattern(self, test_name, py_code, output):
    # Analyze and generate fix
    return TestModification(
        old_code=old_code,
        new_code=new_code,
        explanation="What was fixed",
        confidence=0.8
    )
```

## Integration with Claude Code

The system is designed to integrate with Claude Code AI. To enable full AI capabilities:

1. The `AIAnalyzer` class can be extended to call Claude API
2. The `ClaudeCodeIntegration` class provides the integration point
3. Modifications can be provided by Claude based on the full context

Example integration point in `ai_test_analyzer.py`:

```python
def analyze_and_fix(self, test_name, py_code, ts_code, stdout, stderr, attempt):
    # First try pattern-based fixes
    modification = self.analyzer.analyze_failure(...)

    if modification and modification.confidence > 0.6:
        return modification

    # Fall back to Claude API for complex cases
    # return self._call_claude_api(test_name, py_code, ts_code, stdout, stderr)
```

## Limitations

1. **Pattern-Based Fixes**: Currently uses pattern matching; some complex issues may require manual intervention
2. **Test Isolation**: Each test is fixed independently; interactions between tests are not considered
3. **File Scope**: Only modifies test files, not implementation code
4. **Max Attempts**: Will give up after max attempts even if solution exists

## Best Practices

1. **Start Small**: Test on a subset of tests first using `--start-from` and `--max-attempts`
2. **Review Changes**: Always review the generated modifications before committing
3. **Backup**: The script automatically backs up files, but maintain your own version control
4. **Incremental**: Fix tests in batches and commit progress regularly
5. **Monitor Output**: Watch the console output for patterns in failures

## Troubleshooting

### Script Fails to Find Tests

- Verify `test_comparison_detailed_report.md` exists and has the correct format
- Check that test numbers start from 1

### Tests Don't Run

- Ensure pytest is installed: `pip install pytest`
- Verify test file path is correct
- Check that you're in the correct directory

### No Fixes Applied

- Check AI analyzer is properly imported (should show warning if not)
- Review console output for specific error messages
- Some tests may require manual intervention

### Import Errors

- Ensure all dependencies are available
- Check Python version (requires 3.8+)

## Example Workflow

1. **Initial Run**:
   ```bash
   python auto_test_fixer.py --max-attempts 3
   ```

2. **Review Results**:
   ```bash
   cat test_fixer_report.md
   ```

3. **Resume from Failures**:
   ```bash
   # If interrupted at test 50
   python auto_test_fixer.py --start-from 50
   ```

4. **Increase Attempts for Stubborn Tests**:
   ```bash
   python auto_test_fixer.py --start-from 200 --max-attempts 10
   ```

5. **Manual Review**:
   - Review the modifications in the test file
   - Run full test suite: `pytest path/to/test_file.py`
   - Commit successful fixes

## Future Enhancements

- [ ] Integration with actual Claude API for advanced analysis
- [ ] Multi-file support (fixing implementation code, not just tests)
- [ ] Parallel test execution for faster processing
- [ ] Machine learning from successful fixes
- [ ] Interactive mode for manual approval of modifications
- [ ] Diff preview before applying changes
- [ ] Test dependency graph analysis
- [ ] Automatic commit creation for each fix

## Support

For issues or questions:
1. Check the console output for error messages
2. Review `test_fixer_report.md` for detailed failure information
3. Examine the `.backup` file if modifications caused issues
4. Restore original: `cp test_file.py.backup test_file.py`

## License

Part of the YenPoint toolbox project.
