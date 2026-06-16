"""Code with intentional quality and security issues.

This module contains intentional code quality and security issues to validate
that the Quality AI Agent can detect and propose fixes using ruff and bandit.

Task 9.4-9.7: Security issues and code quality issues
"""
# import os
import pickle
import subprocess


# Task 9.4: Hardcoded secret (Bandit HIGH severity: B105)
API_SECRET_KEY = "sk-1234567890abcdef-HARDCODED-SECRET"
DATABASE_PASSWORD = "admin123password"  # Hardcoded password


# Task 9.5: SQL injection vulnerability (Bandit CRITICAL severity: B608)
def unsafe_sql_query(user_input: str) -> str:
    """Execute SQL query with user input - SQL INJECTION VULNERABILITY.
    
    This function demonstrates a SQL injection vulnerability that Bandit
    should detect as CRITICAL severity.
    
    Expected behavior: Quality AI Agent should detect this as high-severity
    security issue and propose parameterized queries.
    """
    # INTENTIONAL SECURITY BUG: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    return query


# Task 9.5: Command injection vulnerability (Bandit HIGH severity: B602, B607)
def unsafe_command_execution(user_input: str):
    """Execute shell command with user input - COMMAND INJECTION.
    
    This function demonstrates command injection vulnerability using
    shell=True with user input.
    
    Expected behavior: Quality AI Agent should detect this as high-severity
    security issue and propose safer alternatives.
    """
    # INTENTIONAL SECURITY BUG: Command injection
    subprocess.call(f"ls -la {user_input}", shell=True)


# Task 9.5: Pickle deserialization (Bandit HIGH severity: B301)
def unsafe_deserialization(data: bytes):
    """Deserialize data using pickle - UNSAFE DESERIALIZATION.
    
    Pickle can execute arbitrary code during deserialization.
    
    Expected behavior: Quality AI Agent should detect unsafe deserialization
    and propose safer alternatives like JSON.
    """
    # INTENTIONAL SECURITY BUG: Unsafe deserialization
    return pickle.loads(data)


# Task 9.4: Use of weak cryptography (Bandit MEDIUM severity: B324)
def weak_hash(data: str) -> str:
    """Hash data using weak MD5 algorithm.
    
    Expected behavior: Quality AI Agent should detect weak cryptography
    and propose stronger alternatives like SHA-256.
    """
    import hashlib
    # INTENTIONAL SECURITY BUG: Weak cryptography
    return hashlib.md5(data.encode()).hexdigest()


# Task 9.6: Unused variables (Ruff F841)
def function_with_unused_variables(x: int, y: int) -> int:
    """Function with unused variables - CODE QUALITY ISSUE.
    
    Expected behavior: Quality AI Agent should detect unused variables
    and propose either using them or removing them.
    """
    # INTENTIONAL QUALITY BUG: Unused variables
    unused_variable = 100
    another_unused = "hello"
    temporary_value = x * 2  # Calculated but never used
    
    return x + y  # Only uses x and y, others are unused


# Task 9.6: Unused imports (Ruff F401)
# Removed unused import: 'json'  # Unused import
# import sys   # Unused import
Removed unused 'typing' import, Dict, Optional, Tuple  # Some unused


# Task 9.6: Undefined name (Ruff F821)
def function_with_undefined_name():
    """Function using undefined variable - CODE QUALITY ISSUE.
    
    Expected behavior: Quality AI Agent should detect undefined name
    and propose defining it or fixing the reference.
    """
    # INTENTIONAL QUALITY BUG: Undefined name
    result = Make sure that 'undefined_variable' has been defined before using it. + 10  # undefined_variable is not defined
    return result


# Task 9.7: High complexity function (Ruff C901)
def high_complexity_function(a, b, c, d, e):
    """Function with high cyclomatic complexity - CODE QUALITY ISSUE.
    
    This function has many nested conditions and branches, making it
    difficult to test and maintain.
    
    Expected behavior: Quality AI Agent should detect high complexity
    and propose refactoring into smaller functions.
    """
    # INTENTIONAL QUALITY BUG: High cyclomatic complexity
    result = 0
    
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        result = a + b + c + d + e
                    else:
                        result = a + b + c + d
                else:
                    result = a + b + c
            else:
                result = a + b
        else:
            result = a
    else:
        if b < 0:
            if c < 0:
                if d < 0:
                    if e < 0:
                        result = a - b - c - d - e
                    else:
                        result = a - b - c - d
                else:
                    result = a - b - c
            else:
                result = a - b
        else:
            result = 0
    
    return result


# Task 9.6: Redefined unused variable (Ruff F811)
def duplicate_function():
    """First definition."""
    pass


def duplicate_function():  # Redefinition - Ruff F811
    """Second definition - shadows first one."""
    pass


# Task 9.6: Mutable default argument (Ruff B006)
def function_with_mutable_default(items=[]):  # INTENTIONAL BUG
    """Function with mutable default argument - CODE QUALITY ISSUE.
    
    Mutable default arguments can cause unexpected behavior as they're
    shared across function calls.
    
    Expected behavior: Quality AI Agent should detect mutable default
    and propose using None with initialization inside function.
    """
    items.append(1)
    return items


# Task 9.6: Bare except (Ruff E722)
def function_with_bare_except():
    """Function with bare except clause - CODE QUALITY ISSUE.
    
    Bare except catches all exceptions including KeyboardInterrupt and
    SystemExit, which is usually not intended.
    
    Expected behavior: Quality AI Agent should detect bare except
    and propose catching specific exceptions.
    """
    try:
        risky_operation()
    except:  # INTENTIONAL BUG: Bare except
        pass


def risky_operation():
    """Placeholder for risky operation."""
    pass


# Task 9.6: Line too long (Ruff E501)
def function_with_long_line():
    """Function with line exceeding recommended length."""
    very_long_variable_name = "This is an intentionally very long string that exceeds the recommended line length limit of 88 or 100 characters depending on the configuration which should trigger a code quality warning from ruff"
    return very_long_variable_name


# Task 9.6: Multiple statements on one line (Ruff E701)
def function_with_multiple_statements(): x = 1; y = 2; return x + y  # INTENTIONAL BUG


# Task 9.6: Comparison to True/False (Ruff E712)
def function_with_comparison_to_bool(flag: bool) -> bool:
    """Function comparing to True/False directly - CODE QUALITY ISSUE.
    
    Expected behavior: Quality AI Agent should detect comparison to bool
    and propose using the value directly.
    """
    # INTENTIONAL QUALITY BUG: Comparison to True
    if flag:  # Should be: if flag:
        return True
    else:
        return False


# Task 9.6: Import not at top of file (Ruff E402)
def function_that_imports():
    """Function that imports inside - CODE QUALITY ISSUE."""
    import random  # INTENTIONAL BUG: Import not at top
    return random.randint(1, 100)
