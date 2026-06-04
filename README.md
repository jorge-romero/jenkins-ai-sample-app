# Buggy Sample Application

This is a deliberately buggy FastAPI application created for demonstrating AI-powered automated fixing in Jenkins pipelines.

## 🐛 Intentional Bugs

### Bug #1: SQL Injection (CRITICAL - Security)
**File**: `src/database.py:41`
```python
query = f"SELECT * FROM users WHERE id = {user_id}"  # Vulnerable!
```
**Fix**: Use parameterized queries

### Bug #2: Hardcoded Secrets (CRITICAL - Security)
**File**: `src/auth.py:7-9`
```python
API_KEY = "AIzaSyDemoKey12345_THIS_IS_HARDCODED"
SECRET_TOKEN = "super-secret-token-123-hardcoded"
DATABASE_PASSWORD = "admin123password"
```
**Fix**: Use environment variables

### Bug #3: Code Quality Issues (MEDIUM - Quality)
**File**: `src/utils.py`
- Unused variables
- High cyclomatic complexity
- Deep nesting (6 levels)
- Too many parameters

**Fix**: Simplify code, remove unused variables

### Bug #4: Logic Errors (HIGH - Logic)
**File**: `src/calculator.py`
- Division by zero (no error handling)
- Off-by-one error in `get_first_n_items()`

**Fix**: Add error handling, fix slice logic

### Bug #5: Failing Tests (HIGH - Tests)
**Files**: `tests/test_app.py`, `tests/test_calculator.py`
- Wrong status code assertion (expects 201, gets 200)
- Tests that trigger unhandled exceptions
- Tests that fail due to bugs in source code

**Fix**: Correct assertions or fix source code bugs

## 🚀 Running Locally

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests (will fail)
pytest -v

# Run the app
uvicorn src.app:app --reload

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/users/1
curl "http://localhost:8000/calculate/divide?a=10&b=2"
```

## 🤖 AI Agents Will Fix

When you run this through the Jenkins pipeline:

1. **Test AI Agent** will:
   - Detect 3-4 failing tests
   - Use Gemini to analyze failures
   - Generate and apply fixes
   - Create a PR with test fixes

2. **Quality AI Agent** will:
   - Detect 5+ security/quality issues
   - Use Gemini to analyze issues
   - Generate and apply fixes
   - Create a PR with quality improvements

## 📊 Expected Results

### Before AI Fixes
- ❌ 3-4 tests failing
- ❌ 2 CRITICAL security issues
- ❌ 3+ code quality issues

### After AI Fixes (via PRs)
- ✅ All tests passing
- ✅ Security issues resolved
- ✅ Code quality improved

---

**Note**: This app is intentionally buggy for demonstration. Never deploy to production!
