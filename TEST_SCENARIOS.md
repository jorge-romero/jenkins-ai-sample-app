# Sample Application Test Scenarios Documentation

**Purpose:** This document explains the intentional bugs and quality issues added to the sample application for testing the Jenkins AI agents (Test AI Agent and Quality AI Agent).

**Last Updated:** 2026-05-28  
**OpenSpec Change:** enhance-test-smart-agents  
**Task Group:** 9 - Expanded Sample Application Test Scenarios

---

## Overview

The sample application contains intentionally buggy code to validate that our AI agents can:
1. **Detect** failures and issues through automated tools (pytest, ruff, bandit)
2. **Analyze** the root cause of problems
3. **Propose** appropriate fixes
4. **Verify** that fixes resolve the issues

This enables realistic end-to-end testing of the agent workflows without relying on production code bugs.

---

## Test Failure Scenarios (Tasks 9.1-9.3)

**File:** `tests/test_intentional_failures.py`

These tests are designed to trigger various types of test failures that the **Test AI Agent** should detect and fix.

### 1. test_assertion_failure (Task 9.1)

**Type:** Assertion failure  
**Bug:** Wrong assertion (`2 + 2 == 5`)

**Expected Agent Behavior:**
- Detect assertion failure in pytest JSON report
- Analyze that expected (5) != actual (4)
- Propose fix: Change assertion to `2 + 2 == 4`
- Verify fix resolves the test failure

**Validation:** Confirms agent can handle simple logic errors

---

### 2. test_exception_failure (Task 9.2)

**Type:** Unhandled ValueError  
**Bug:** Attempting to convert non-numeric string to int

**Expected Agent Behavior:**
- Detect ValueError exception in test output
- Analyze that `int("not_a_number")` raises ValueError
- Propose fix: Add try-except block or input validation
- Verify fix prevents exception

**Validation:** Confirms agent can handle exception-based failures

---

### 3. test_import_error (Task 9.3)

**Type:** ImportError  
**Bug:** Importing non-existent module `nonexistent_module`

**Expected Agent Behavior:**
- Detect ImportError in test output
- Analyze that module doesn't exist
- Propose fix: Install package, fix import name, or remove import
- Verify fix resolves import error

**Validation:** Confirms agent can handle dependency issues

---

### Additional Test Failures

The file includes additional failure types for comprehensive testing:

- **test_type_error:** Type mismatch (`"hello" + 123`)
- **test_attribute_error:** Accessing non-existent attribute on dict
- **test_index_error:** List index out of bounds
- **test_key_error:** Dictionary key doesn't exist

These provide diverse failure scenarios for agent validation.

---

## Security Issues (Tasks 9.4-9.5)

**File:** `src/intentional_issues.py`

These code patterns trigger **Bandit** security warnings that the **Quality AI Agent** should detect and fix.

### 4. Hardcoded Secrets (Task 9.4)

**Bandit Rule:** B105 (HIGH severity)  
**Lines:** API_SECRET_KEY, DATABASE_PASSWORD

**Issue:**
```python
API_SECRET_KEY = "sk-1234567890abcdef-HARDCODED-SECRET"
DATABASE_PASSWORD = "admin123password"
```

**Expected Agent Behavior:**
- Detect hardcoded secret via Bandit B105
- Analyze security risk (secrets in version control)
- Propose fix: Use environment variables (`os.getenv()`)
- Verify secrets removed from code

**Threshold Trigger:** HIGH severity issues should trigger AI analysis

---

### 5. SQL Injection Vulnerability (Task 9.5)

**Bandit Rule:** B608 (CRITICAL severity)  
**Function:** `unsafe_sql_query()`

**Issue:**
```python
query = f"SELECT * FROM users WHERE username = '{user_input}'"
```

**Expected Agent Behavior:**
- Detect SQL injection via Bandit B608
- Analyze risk (arbitrary SQL execution)
- Propose fix: Use parameterized queries
- Verify fix prevents injection

**Threshold Trigger:** CRITICAL severity should trigger immediate AI analysis

---

### 6. Command Injection (Task 9.5)

**Bandit Rule:** B602, B607 (HIGH severity)  
**Function:** `unsafe_command_execution()`

**Issue:**
```python
subprocess.call(f"ls -la {user_input}", shell=True)
```

**Expected Agent Behavior:**
- Detect command injection via Bandit B602/B607
- Analyze risk (arbitrary command execution)
- Propose fix: Use subprocess without shell=True, validate input
- Verify fix prevents injection

---

### 7. Unsafe Deserialization (Task 9.5)

**Bandit Rule:** B301 (HIGH severity)  
**Function:** `unsafe_deserialization()`

**Issue:**
```python
return pickle.loads(data)
```

**Expected Agent Behavior:**
- Detect unsafe pickle usage via Bandit B301
- Analyze risk (arbitrary code execution)
- Propose fix: Use JSON or safer serialization
- Verify fix uses safe deserialization

---

### 8. Weak Cryptography (Task 9.4)

**Bandit Rule:** B324 (MEDIUM severity)  
**Function:** `weak_hash()`

**Issue:**
```python
return hashlib.md5(data.encode()).hexdigest()
```

**Expected Agent Behavior:**
- Detect weak MD5 usage via Bandit B324
- Analyze risk (collision attacks possible)
- Propose fix: Use SHA-256 or stronger
- Verify fix uses strong algorithm

---

## Code Quality Issues (Tasks 9.6-9.7)

**File:** `src/intentional_issues.py`

These patterns trigger **Ruff** code quality warnings that the **Quality AI Agent** should detect and fix.

### 9. Unused Variables (Task 9.6)

**Ruff Rule:** F841  
**Function:** `function_with_unused_variables()`

**Issue:**
```python
unused_variable = 100
another_unused = "hello"
temporary_value = x * 2  # Never used
```

**Expected Agent Behavior:**
- Detect unused variables via Ruff F841
- Analyze that variables are assigned but never read
- Propose fix: Remove unused variables or use them
- Verify fix removes warnings

**Threshold Trigger:** Should accumulate to trigger AI when count > threshold

---

### 10. Unused Imports (Task 9.6)

**Ruff Rule:** F401  
**Lines:** `import json`, `import sys`

**Issue:**
```python
import json  # Unused import
import sys   # Unused import
```

**Expected Agent Behavior:**
- Detect unused imports via Ruff F401
- Analyze that imports are never referenced
- Propose fix: Remove unused imports
- Verify fix removes warnings

---

### 11. Undefined Name (Task 9.6)

**Ruff Rule:** F821  
**Function:** `function_with_undefined_name()`

**Issue:**
```python
result = undefined_variable + 10  # undefined_variable not defined
```

**Expected Agent Behavior:**
- Detect undefined name via Ruff F821
- Analyze that variable is referenced before definition
- Propose fix: Define variable or fix reference
- Verify fix resolves undefined name

---

### 12. High Cyclomatic Complexity (Task 9.7)

**Ruff Rule:** C901  
**Function:** `high_complexity_function()`

**Issue:**
- 5 levels of nested if statements
- 13+ decision points
- Difficult to test and maintain

**Expected Agent Behavior:**
- Detect high complexity via Ruff C901
- Analyze that function has too many branches
- Propose fix: Refactor into smaller functions
- Verify fix reduces complexity below threshold

**Threshold Trigger:** High-complexity functions should trigger AI analysis

---

### 13. Additional Quality Issues (Task 9.6)

The file includes additional quality issues:

- **F811 (Redefinition):** `duplicate_function()` defined twice
- **B006 (Mutable default):** `function_with_mutable_default(items=[])`
- **E722 (Bare except):** `except:` without specific exception type
- **E501 (Line too long):** Line exceeding 88/100 character limit
- **E701 (Multiple statements):** Multiple statements on one line
- **E712 (Bool comparison):** `if flag == True:` instead of `if flag:`
- **E402 (Import not at top):** Import statement inside function

These provide comprehensive coverage of common code quality issues.

---

## Existing Bugs (Original Sample App)

The sample app already contains intentional bugs in these files:

### database.py (BUG #1)
- SQL injection in `get_user()` method
- Uses string formatting instead of parameterized queries

### auth.py (BUG #2)
- Hardcoded API keys and passwords
- Security credentials in source code

### calculator.py (BUG #4)
- Division by zero not handled in `divide()`
- Off-by-one error in `get_first_n_items()`

### test_calculator.py (BUG #5)
- `test_divide_by_zero()` - Expects function to handle zero division
- `test_get_first_n_items_edge_case()` - Expects correct list slicing

### test_app.py (BUG #5)
- `test_create_user_endpoint()` - Wrong HTTP status code expectation

---

## Testing Strategy

### For Test AI Agent

**Test Scenarios:**
1. Run pytest on `tests/test_intentional_failures.py`
2. Agent detects 7+ test failures
3. Agent analyzes each failure type
4. Agent proposes appropriate fixes
5. Agent re-runs tests to verify fixes

**Success Criteria:**
- All test failures detected
- Root causes correctly identified
- Fixes resolve failures
- No new failures introduced

---

### For Quality AI Agent

**Test Scenarios:**
1. Run bandit on `src/intentional_issues.py`
2. Agent detects CRITICAL + HIGH security issues (5+ issues)
3. Run ruff on `src/intentional_issues.py`
4. Agent detects quality issues (15+ issues)
5. Agent prioritizes by severity
6. Agent proposes fixes
7. Agent re-runs tools to verify improvements

**Success Criteria:**
- Security issues detected and prioritized
- Quality issues detected and counted
- Thresholds correctly evaluated
- AI triggered when thresholds breached
- Fixes improve metrics

---

## Threshold Configuration

These issues are designed to trigger AI analysis based on thresholds defined in `.env.test`:

```bash
# Security thresholds (Bandit)
SECURITY_THRESHOLD_CRITICAL=0  # Any CRITICAL issue triggers AI
SECURITY_THRESHOLD_HIGH=2      # 3+ HIGH issues trigger AI

# Quality thresholds (Ruff)
QUALITY_THRESHOLD_ERROR=5      # 6+ errors trigger AI
QUALITY_THRESHOLD_WARNING=20   # 21+ warnings trigger AI
```

**intentional_issues.py** contains:
- 1 CRITICAL security issue (SQL injection)
- 4+ HIGH security issues (command injection, hardcoded secrets, etc.)
- 15+ quality issues (unused variables, complexity, etc.)

This ensures thresholds are exceeded, triggering AI analysis.

---

## Usage

### Running Tests with Failures

```bash
# Run all intentional failure tests
pytest tests/test_intentional_failures.py -v

# Run specific failure type
pytest tests/test_intentional_failures.py::test_assertion_failure -v

# Skip intentional failures during normal testing
pytest -m "not intentional_failure"
```

### Running Quality Checks

```bash
# Security analysis
bandit -r src/intentional_issues.py -f json -o bandit_report.json

# Quality analysis
ruff check src/intentional_issues.py --output-format=json

# Both with thresholds
bandit -r src/ -ll  # Only HIGH and CRITICAL
ruff check src/ --select=F,E,W,C,B
```

### Expected Output

**Pytest failures:** 7 failures in test_intentional_failures.py  
**Bandit issues:** 5+ HIGH/CRITICAL severity issues  
**Ruff issues:** 15+ quality issues across multiple categories

---

## Maintenance

When adding new test scenarios:

1. Add intentional bug to appropriate file
2. Document the bug in this file
3. Specify expected agent behavior
4. Update threshold configuration if needed
5. Verify issue is detected by tools (pytest/ruff/bandit)
6. Update validation tests to check for new scenario

---

## Notes

- All intentional failures are clearly marked with comments
- Tests are marked with `@pytest.mark.intentional_failure` for filtering
- Security issues use real Bandit rules that would appear in production
- Quality issues use real Ruff rules from common coding standards
- Issues are diverse enough to test different AI analysis paths
- Each issue type should trigger distinct fix strategies

---

## Related Files

- `tests/test_intentional_failures.py` - Test failures (Tasks 9.1-9.3)
- `src/intentional_issues.py` - Security/quality issues (Tasks 9.4-9.7)
- `src/database.py` - SQL injection (BUG #1)
- `src/auth.py` - Hardcoded secrets (BUG #2)
- `src/calculator.py` - Logic bugs (BUG #4)
- `tests/test_calculator.py` - Test failures (BUG #5)
- `tests/test_app.py` - Test failures (BUG #5)

---

## Validation

To validate these scenarios work correctly:

```bash
# 1. Validate test failures are detected
bash scripts/quick_test.sh test-ai unit
# Expected: Multiple test failures detected

# 2. Validate security issues detected
docker run --rm -v $(pwd)/sample-app:/app test-ai-agent bandit -r /app/src/intentional_issues.py
# Expected: 5+ HIGH/CRITICAL issues

# 3. Validate quality issues detected
docker run --rm -v $(pwd)/sample-app:/app quality-ai-agent ruff check /app/src/intentional_issues.py
# Expected: 15+ quality issues

# 4. Validate full agent workflow
bash scripts/run_agent_tests.sh test-ai integration
# Expected: Agent detects, analyzes, proposes fixes, verifies
```

---

**Status:** ✓ Complete (Tasks 9.1-9.8)  
**Files Created:** 2 new files, 1 documentation file  
**Issues Added:** 7 test failures, 5+ security issues, 15+ quality issues
