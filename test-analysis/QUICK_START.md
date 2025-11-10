# Quick Start Guide - Automated Test Fixer

## TL;DR

```bash
# Fix all tests from the beginning
python auto_test_fixer.py

# Start from test #25 (resume after interruption)
python auto_test_fixer.py --start-from 25

# Increase retry attempts for difficult tests
python auto_test_fixer.py --max-attempts 10
```

## What This Does

1. Reads `test_comparison_detailed_report.md` (496 failing tests)
2. For each test:
   - Runs the test
   - Analyzes the failure
   - Modifies the test file to fix issues
   - Re-runs until it passes (or max attempts reached)
3. Generates `test_fixer_report.md` with results

## Common Commands

### Start Fresh
```bash
python auto_test_fixer.py
```

### Resume from Test #50
```bash
python auto_test_fixer.py --start-from 50
```

### Try Harder (10 attempts per test)
```bash
python auto_test_fixer.py --max-attempts 10
```

### Custom Report File
```bash
python auto_test_fixer.py --report my_report.md
```

## Output You'll See

```
🔧 Processing Test 15: Throws if not authenticated
📍 Attempt 1/5
  ▶️  Running test...
  ❌ Test FAILED
  🤖 AI Analysis:
     ✓ Found potential fix (confidence: 80%)
     ℹ️  Updated error match pattern
  🔧 Applying modification...
  ✅ Test PASSED on attempt 2!
```

## What Gets Modified

The script modifies:
- `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

It automatically creates:
- `.backup` file (original test file)
- `test_fixer_report.md` (results report)

## Safety Features

1. **Automatic Backup**: Original file saved as `.backup`
2. **Auto-Restore**: Reverts changes if no fix found
3. **Resume Support**: Can restart from any test number
4. **Max Attempts**: Won't loop forever (default: 5 attempts)

## When It Works Best

✅ **Good for**:
- Mock configuration issues
- Assertion count mismatches
- Missing await keywords
- Error message pattern fixes
- Attribute errors

❌ **Needs manual help**:
- Complex logic errors
- Architecture issues
- Import problems
- Test design flaws

## Quick Status Check

After running, check your results:

```bash
# View summary
head -20 test_fixer_report.md

# Check how many tests were fixed
grep -c "✅ PASSED" test_fixer_report.md

# See which tests still need work
grep "❌ FAILED" test_fixer_report.md
```

## If Something Goes Wrong

```bash
# Restore original test file
cp py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py.backup \
   py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py

# Run just one test manually to see what's wrong
cd py-wallet-toolbox
pytest tests/integration/test_cwi_style_wallet_manager.py::test_name -v
```

## Pro Tips

1. **Start with low attempts**: Use `--max-attempts 3` first to see what can be fixed easily
2. **Process in batches**: Fix 50-100 tests at a time, commit, then continue
3. **Monitor output**: Watch for patterns in what's failing
4. **Review before commit**: Always review the actual changes made

## Example Session

```bash
# Start fixing tests
python auto_test_fixer.py --max-attempts 3 --start-from 1

# ... wait for completion ...

# Check results
cat test_fixer_report.md | head -50

# If you're happy with changes, commit
git add py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py
git commit -m "Auto-fix tests 1-100"

# Continue with next batch
python auto_test_fixer.py --max-attempts 3 --start-from 101
```

## Expected Results

Based on the 496 failing tests, you can expect:

- **~30-50%** will be auto-fixed (pattern-based issues)
- **~20-30%** may need multiple attempts
- **~20-40%** will require manual intervention

## Next Steps After Auto-Fixing

1. Review `test_fixer_report.md`
2. Run full test suite: `pytest tests/integration/test_cwi_style_wallet_manager.py`
3. Manually fix remaining failures using insights from the report
4. Commit working tests

## Need More Help?

See `AUTO_TEST_FIXER_README.md` for:
- Detailed architecture
- How to extend the AI analyzer
- Advanced configuration options
- Troubleshooting guide
