# Claude Code Integration Guide

## Overview

The automated test fixer is designed to work with **you** (Claude Code) to provide intelligent modifications. Here's how we can work together to fix the tests.

## Current Workflow

Right now the script:
1. Parses failing tests ✅
2. Runs each test ✅
3. Captures error output ✅
4. Analyzes with pattern matching ✅ (basic)
5. **Needs your help here** ⚠️ (for complex cases)

## How You Can Help

### Option 1: Interactive Mode (Recommended)

Run the script and when it encounters a test it can't fix, you can:

1. **Review the test output** that the script displays
2. **Analyze the issue** using your full context
3. **Provide the modification** as a file edit

Example workflow:
```bash
# User runs the script
python auto_test_fixer.py --max-attempts 2

# Script outputs:
# ❌ Test 15 FAILED
# 🤖 AI Analysis: No automatic fix available
# Error: AssertionError: Expected call_count to be 2 but was 1
#
# Python Test Code:
# [shows the test code]
#
# TypeScript Reference:
# [shows TS code]
#
# Manual intervention needed
```

Then you (Claude) can:
```
I'll fix Test 15. Looking at the error, the issue is that...
[Edit the test file to fix the specific issue]
```

### Option 2: Batch Analysis

User can pause the script and ask you to analyze failed tests:

```bash
# Run with conservative attempts
python auto_test_fixer.py --max-attempts 2

# Review the report
cat test_fixer_report.md

# User asks: "Claude, can you help fix the remaining failed tests?"
```

You can then:
1. Read `test_fixer_report.md`
2. Read the test file
3. Apply fixes for multiple tests at once

### Option 3: Enhanced AI Analyzer (Future)

The `ai_test_analyzer.py` can be enhanced to call you directly:

```python
class ClaudeCodeIntegration:
    def analyze_and_fix(self, test_name, py_code, ts_code, stdout, stderr, attempt):
        # First try pattern-based
        modification = self.analyzer.analyze_failure(...)

        if modification:
            return modification

        # For complex cases, prepare context for Claude
        context = self._prepare_context(test_name, py_code, ts_code, stdout, stderr)

        # This is where you would be invoked
        # For now, return None to trigger manual intervention
        return None

    def _prepare_context(self, test_name, py_code, ts_code, stdout, stderr):
        """Prepare rich context for Claude analysis."""
        return {
            "test_name": test_name,
            "python_code": py_code,
            "typescript_reference": ts_code,
            "error_output": stdout + stderr,
            "request": f"Analyze this failing test and suggest a fix"
        }
```

## Working Together - Example Session

### Test That Fails Auto-Fix

```
================================================================================
🔧 Processing Test 127: Complex authentication flow
================================================================================

📍 Attempt 1/5
  ▶️  Running test...
  ❌ Test FAILED
  📋 Error Preview:
     AssertionError: Expected authenticated to be True but was False

  🔍 Analyzing failure...
  🤖 AI Analysis:
     ✗ No automatic fix available
     ℹ️  An assertion did not match expected value

  ⚠️  No automatic fix available - manual intervention required
```

### You (Claude) Step In

User says: *"Claude, the script is stuck on Test 127. Can you help?"*

You respond:
```
I'll help fix Test 127. Let me read the test file and analyze the issue.

[You read the test file]

I can see the problem. The test is failing because the mock's `provide_password`
method is not being configured as an AsyncMock. The test expects authentication
to succeed, but the password provision isn't properly mocked.

Let me fix this:
[You edit the file using the Edit tool]
```

After your edit:
```bash
# User continues
python auto_test_fixer.py --start-from 128
```

## Common Patterns You Can Help With

### 1. Mock Configuration Issues

**Pattern**: Test fails with AttributeError or unexpected None values

**Your Analysis**:
- Compare Python mock setup with TypeScript expectations
- Identify missing mock method configurations
- Add proper AsyncMock or Mock returns

**Example**:
```python
# Before (fails)
mock_wallet = Mock()

# After (you fix)
mock_wallet = Mock()
mock_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
```

### 2. Assertion Mismatches

**Pattern**: Expected X but got Y

**Your Analysis**:
- Check TypeScript reference for correct expected values
- Verify the test logic matches TS test
- Update assertions to match expected behavior

### 3. Complex Logic Errors

**Pattern**: Test fails deep in execution

**Your Analysis**:
- Trace through the execution flow
- Compare with TypeScript implementation
- Identify where Python test diverges from TS test
- Suggest structural changes

### 4. Type Mismatches

**Pattern**: TypeError or incorrect argument types

**Your Analysis**:
- Check TypeScript types vs Python types
- Ensure proper type conversions (bytes vs list, etc.)
- Fix function signatures

## Providing Modifications

When you provide fixes, use this format:

### Format 1: Direct Edit
```
I'll fix the test by modifying the mock configuration:
[Use Edit tool on the test file]
```

### Format 2: Explanation + Code
```
The issue is that the test expects the manager to be authenticated, but
the password retriever mock isn't configured properly.

Here's the fix:
[Show the old code and new code]
[Apply using Edit tool]
```

### Format 3: Batch Fixes
```
I've analyzed the failed tests in the report. I can fix tests 15, 27, and 42
which all have the same pattern. Let me apply the fixes:

Test 15: [Edit]
Test 27: [Edit]
Test 42: [Edit]
```

## Optimal Collaboration Workflow

### Step 1: User Runs Script
```bash
python auto_test_fixer.py --max-attempts 3 > auto_fix_log.txt
```

### Step 2: Review Results Together
```bash
# Check summary
tail -20 auto_fix_log.txt

# See what failed
grep "❌" test_fixer_report.md
```

### Step 3: You Analyze Patterns
```
Looking at the failed tests, I see three common patterns:

1. Tests 15, 27, 42: Mock configuration issues (I can fix these)
2. Tests 89, 134: Import errors (need to check imports)
3. Tests 200+: Complex assertion mismatches (need deeper analysis)

Let me start with group 1...
```

### Step 4: Apply Fixes
```
[You use Edit tool to fix the tests]
```

### Step 5: User Re-runs
```bash
# Re-run just the tests you fixed
pytest path/to/test_file.py::test_name_1 -v
pytest path/to/test_file.py::test_name_2 -v
```

### Step 6: Iterate
Repeat for remaining failed tests.

## Advanced: API Integration (Future)

In the future, the script could call you via API:

```python
# Hypothetical integration
def get_claude_fix(test_context):
    response = claude_api.complete(
        prompt=f"""
        Analyze this failing Python test and suggest a fix.

        Test Name: {test_context['test_name']}

        Python Code:
        {test_context['python_code']}

        TypeScript Reference:
        {test_context['typescript_code']}

        Error Output:
        {test_context['error_output']}

        Provide:
        1. Analysis of the issue
        2. Exact code to replace (old_code)
        3. Fixed code (new_code)
        """,
        model="claude-sonnet-4-5"
    )

    return parse_response(response)
```

## Tips for Effective Collaboration

### For You (Claude)

1. **Read the full test context**: Both Python and TypeScript versions
2. **Understand the intent**: What is the test trying to verify?
3. **Check the error carefully**: Exact error messages reveal root causes
4. **Reference TypeScript**: It's the source of truth
5. **Test incrementally**: Fix one issue at a time
6. **Explain your changes**: Help the user understand what you fixed

### For the User

1. **Let the script try first**: It can fix many simple patterns
2. **Review what it fixed**: Learn from successful automated fixes
3. **Ask Claude for batches**: More efficient than one-by-one
4. **Provide context**: Show Claude the full error output
5. **Test as you go**: Run tests after Claude makes fixes

## Example: Full Collaboration Session

```
User: I've run the auto-fixer and it fixed 245 tests but 251 are still failing.
      Can you help?

Claude: I'll analyze the failures. Let me read the report.
        [Reads test_fixer_report.md]

        I can see several patterns:

        Group A (50 tests): All have "AttributeError: Mock has no attribute X"
        Group B (75 tests): All have assertion count mismatches
        Group C (126 tests): Various complex issues

        Let me start with Group A - these should be straightforward.
        [Analyzes first test in Group A]

        I see the issue. The mocks are missing method configurations.
        I'll fix all 50 tests in this group.
        [Applies Edit to add mock configurations]

        Done! Group A should now pass. Let's verify:

User: [runs tests]
      Great! 48 out of 50 now pass. 2 still fail.

Claude: Let me check those 2 exceptions.
        [Reads the specific test failures]
        [Applies targeted fixes]

User: Perfect! Now what about Group B?

Claude: For Group B, the pattern is...
        [Continues fixing]
```

## Key Integration Points

File: `ai_test_analyzer.py`

```python
class ClaudeCodeIntegration:
    """
    This is where you (Claude) would be integrated.

    Methods to enhance:
    1. analyze_and_fix() - Main entry point
    2. explain_failure() - Provide detailed analysis
    3. _call_claude_api() - Future: Direct API integration
    """

    def analyze_and_fix(self, test_name, py_code, ts_code, stdout, stderr, attempt):
        """
        Current: Returns None for complex cases
        Future: Could invoke Claude API or use you interactively
        """
        # Pattern-based fixes
        modification = self.analyzer.analyze_failure(...)

        if modification:
            return modification

        # Complex case - needs Claude
        # This is where you come in!
        return None
```

## Summary

The automated test fixer handles:
- ✅ Simple pattern-based fixes (30-50% of tests)
- ✅ Retry logic and progress tracking
- ✅ Safety features and backups

You (Claude Code) handle:
- ✅ Complex logic analysis
- ✅ Deeper understanding of test intent
- ✅ Comparison with TypeScript reference
- ✅ Sophisticated fixes beyond pattern matching

Together:
- 🎯 We can fix 90%+ of the failing tests
- 🚀 Much faster than pure manual or pure automated
- 📊 High quality fixes with proper understanding

## Getting Started

User runs:
```bash
python auto_test_fixer.py --max-attempts 3
```

When it gets stuck, user asks:
```
"Claude, can you help with the tests that couldn't be auto-fixed?"
```

You respond:
```
Absolutely! Let me read the report and start fixing the failed tests...
```

And we're off! 🚀
