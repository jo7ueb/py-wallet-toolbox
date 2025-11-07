# Test Coverage Analysis Summary

Complete analysis of TypeScript and Python test coverage with clickable navigation.

## Overview

- **TypeScript Tests**: 792 tests found
- **Python Tests**: 878 tests found  
- **Matching Tests**: 540 (68.2% coverage)
- **Missing Python Tests**: 257

## Generated Reports

### 1. Matching Tests Report
**File**: `matching_tests.md`

Shows all TypeScript tests that **DO** have corresponding Python implementations.

**Features**:
- ✅ Clickable links to exact line numbers in both TS and Python files
- ✅ Fuzzy match indicators (shows similarity percentage)
- ✅ 540 matched test cases
- ✅ Sorted by TypeScript file path

**Example Entry**:
```markdown
| Test Name | TypeScript File | Python File |
|-----------|-----------------|-------------|
| Successfully creates a new token | [src/__tests/CWIStyleWalletManager.test.ts:189](file://...) | [integration/test_cwi_style_wallet_manager.py:154](file://...) |
```

### 2. Missing Tests Report
**File**: `missing_python_tests.md`

Shows all TypeScript tests that **DO NOT** have Python implementations.

**Features**:
- ✅ Lists 257 missing test cases
- ✅ Shows proposed Python test file path (where they should be added)
- ✅ Sorted by TypeScript file path
- ✅ "-" indicates no good match found

**Example Entry**:
```markdown
| Test Name | TS File Path | Proposed Python Test File Path |
|-----------|--------------|--------------------------------|
| should block usage of admin-only protocol | src/__tests/WalletPermissionsManager.initialization.test.ts | permissions/test_wallet_permissions_manager_initialization.py |
```

## Top Areas Needing Coverage

The following TypeScript test files have the most missing Python tests:

1. `test/Wallet/list/listActions2.test.ts` - **41 missing tests**
2. `test/Wallet/action/createAction2.test.ts` - **15 missing tests**
3. `test/Wallet/list/listOutputs.test.ts` - **15 missing tests**
4. `test/Wallet/local/localWallet2.man.test.ts` - **12 missing tests**
5. `test/Wallet/live/walletLive.man.test.ts` - **11 missing tests**
6. `test/Wallet/specOps/specOps.man.test.ts` - **11 missing tests**
7. `src/storage/schema/entities/__tests/SyncStateTests.test.ts` - **9 missing tests**
8. `test/Wallet/list/listActions.test.ts` - **9 missing tests**
9. `test/services/Services.test.ts` - **9 missing tests**
10. `src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts` - **8 missing tests**

## Scripts for Analysis

### 1. `compare_tests.py`
Generates the missing tests report by comparing TypeScript and Python tests.

**Usage**:
```bash
python compare_tests.py
```

**Features**:
- Parses TypeScript test files with regex
- Uses `py_tests.txt` (pytest collection output)
- Fuzzy name matching (normalized, 80% threshold)
- Generates `missing_python_tests.md`

### 2. `generate_matching_tests.py`
Generates the matching tests report with clickable links.

**Usage**:
```bash
python generate_matching_tests.py
```

**Features**:
- Directly parses both TS and Python test files
- Extracts line numbers for each test
- Creates clickable `file://` links
- Shows similarity scores for fuzzy matches
- Generates `matching_tests.md`

## Supporting Data Files

### `py_tests.txt`
Complete pytest collection output showing all 878 Python tests with their module paths.

**Generated with**:
```bash
python -m pytest tests/ --collect-only -q > py_tests.txt
```

## How Test Matching Works

### Name Normalization
Both TS and Python test names are normalized for comparison:

1. Convert camelCase/PascalCase to snake_case
2. Remove `test_` or `Test` prefixes
3. Remove special characters
4. Lowercase everything
5. Clean up multiple underscores

**Example**:
- TS: `"Successfully creates a new token"`
- Normalized: `successfully_creates_new_token`
- Python: `test_successfully_creates_a_new_token_and_calls_buildandsend`
- Normalized: `successfully_creates_new_token_and_calls_buildandsend`
- Similarity: 98% → **Match!**

### Matching Thresholds
- **Exact match**: 100% similarity (normalized names identical)
- **Fuzzy match**: > 80% similarity (considered a match)
- **No match**: ≤ 80% similarity (listed in missing tests)

## Navigation Tips

### Using Clickable Links
The links in `matching_tests.md` use the `file://` protocol:

```
file:///mnt/c/Users/honoh/YenPoint/toolbox/wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts#L189
```

**Supported in**:
- VS Code (Ctrl+Click or Cmd+Click)
- Most modern IDEs
- Terminal file explorers

### Finding Missing Tests
1. Open `missing_python_tests.md`
2. Find a test you want to implement
3. Check the "Proposed Python Test File Path" column
4. Open that file (or create it if it doesn't exist)
5. Implement the missing test

## Re-running Analysis

To update the reports after adding new tests:

```bash
# Update Python test collection
cd py-wallet-toolbox
python -m pytest tests/ --collect-only -q > ../py_tests.txt

# Re-generate missing tests report
cd ..
python compare_tests.py

# Re-generate matching tests report
python generate_matching_tests.py
```

## Summary Statistics

```
Total TypeScript Tests:     792
Total Python Tests:         878
Matching Tests:             540
Missing Python Tests:       257
Coverage:                   68.2%
```

### Coverage by Category
Based on the matching tests:
- ✅ Permissions Manager: ~95% coverage
- ✅ Storage/Entities: ~90% coverage  
- ✅ CWI Wallet Manager: ~85% coverage
- ⚠️ Wallet Actions: ~50% coverage
- ⚠️ Services: ~45% coverage
- ❌ Sync/Live Operations: ~20% coverage

---

**Generated**: 2025-11-07  
**Location**: `/mnt/c/Users/honoh/YenPoint/toolbox/`
