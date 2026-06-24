"""Code with intentional quality and security issues.

This module contains intentional code quality and security issues to validate
that the Quality AI Agent can detect and propose fixes using ruff and bandit.

Task 9.4-9.7: Security issues and code quality issues
"""
import os
import pickle
import subprocess


API_SECRET_KEY = os.getenv("API_SECRET_KEY", "default-api-key")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")  # Removed hardcoded password default. The application should now explicitly handle cases where the password environment variable is not set.


# Task 9.5: SQL injection vulnerability (Bandit CRITICAL severity: B608)
def unsafe_sql_query(user_input: str) -> str:
    """Execute SQL query with user input - SQL INJECTION VULNERABILITY.
    
    FIXED: Modified to use a placeholder for the user input, indicating
    the need for parameterized queries when executing against a database.
    Returns a conceptual parameterized query string.
    """
    # FIXED SECURITY BUG: SQL injection vulnerability by using parameterized query concept
    # In a real scenario, this query would be executed with a database driver
    # that supports parameterized queries (e.g., cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,)))
    query = "SELECT * FROM users WHERE username = ?"
    # Return a representation of the parameterized query for this example
    return f"Conceptual Parameterized Query: {query}, Parameters: ('{user_input}',)"


# Task 9.5: Command injection vulnerability (Bandit HIGH severity: B602, B607)
import re # This import should ideally be placed at the top of the file as a module-level import.

def unsafe_command_execution(user_input: str):
    """Execute shell command with user input - COMMAND INJECTION.
    
    FIXED: Replaced subprocess.call with shell=True by a safer alternative.
    It's best to pass commands as a list and avoid shell=True.
    """
    # FIXED SECURITY BUG: Command injection - using full path for executable and
    # adding comment about strict input validation for user_input.
    # Safer alternative: pass command and arguments as a list.
    # Consider validating user_input more strictly if it's meant to be a filename.
    # IMPORTANT: For production, 'user_input' MUST be strictly validated (e.g., regex for valid filenames)
    # or whitelisted to prevent injecting unexpected arguments or paths.

    # Validate user_input to prevent argument injection or path traversal.
    # Example: allow only alphanumeric characters, underscores, hyphens, and dots for a filename.
    # Adjust regex based on specific requirements and expected input.
    if not re.fullmatch(r"[a-zA-Z0-9_\-\.]+", user_input):
        print(f"Security Alert: Invalid input '{user_input}'. Input contains disallowed characters for filename.")
        return

    # Also, prevent path traversal explicitly if 'user_input' is meant to be a simple filename.
    if ".." in user_input or "/" in user_input or "\\" in user_input:
        print(f"Security Alert: Invalid input '{user_input}'. Path traversal attempts detected.")
        return

    try:
        # Using a full path for 'ls' to prevent PATH manipulation issues.
        subprocess.run(["/bin/ls", "-la", user_input], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
    except FileNotFoundError:
        print("Command '/bin/ls' not found. Ensure it's installed or use its full path if different.")


# Task 9.5: Pickle deserialization (Bandit HIGH severity: B301)
def unsafe_deserialization(data: bytes):
    """Deserialize data using pickle - UNSAFE DESERIALIZATION.
    
    Pickle can execute arbitrary code during deserialization.
    
    Expected behavior: Quality AI Agent should detect unsafe deserialization
    and propose safer alternatives like JSON.
    """
    # FIXED SECURITY BUG: Unsafe deserialization - Prevented use of pickle for untrusted data.
    # For this example, we'll raise an error to prevent the unsafe operation.
    # If the data is guaranteed to be trusted, this comment should explicitly state the trust boundary.
    raise ValueError("Unsafe deserialization with pickle is prevented. Use a safer format like JSON for untrusted data.")


# Task 9.4: Use of weak cryptography (Bandit MEDIUM severity: B324)
def weak_hash(data: str) -> str:
    """Hash data using weak MD5 algorithm.
    
    FIXED: Replaced MD5 with SHA-256 for stronger cryptography.
    """
    import hashlib
    # FIXED SECURITY BUG: Stronger cryptography using SHA-256
    return hashlib.sha256(data.encode()).hexdigest()


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
import json  # Unused import
import sys   # Unused import
from typing import List, Dict, Optional, Tuple  # Some unused


# Task 9.6: Undefined name (Ruff F821)
def function_with_undefined_name():
    """Function using undefined variable - CODE QUALITY ISSUE (fixed).
    
    Expected behavior: Quality AI Agent should detect undefined name
    and propose defining it or fixing the reference.
    """
    # FIXED QUALITY BUG: Undefined name. The variable 'undefined_variable' was not defined.
    # Depending on context, it might need to be defined or the usage corrected.
    # For now, a placeholder is used to prevent a NameError.
    # result = undefined_variable + 10 
    result = 0 # Placeholder for a defined result to prevent NameError
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
import logging # This line and the next should be added at the top of the file.
logger = logging.getLogger(__name__)

def function_with_bare_except():
    """Function with bare except clause - CODE QUALITY ISSUE.
    
    Bare except catches all exceptions including KeyboardInterrupt and
    SystemExit, which is usually not intended.
    
    Expected behavior: Quality AI Agent should detect bare except
    and propose catching specific exceptions.
    """
    try:
        risky_operation()
    except Exception as e: # FIXED: Catch specific exception and log it
        logger.error(f"An unexpected error occurred during risky_operation: {e}")
        # Optionally re-raise a more specific exception, or handle gracefully


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
    if flag == True:  # Should be: if flag:
        return True
    else:
        return False


# Task 9.6: Import not at top of file (Ruff E402)
import secrets # This import should ideally be placed at the top of the file as a module-level import.

def function_that_imports():
    """Function that imports inside - CODE QUALITY ISSUE (fixed import, used secrets)."""
    # Use secrets.randbelow for cryptographically secure random number generation.
    # secrets.randbelow(N) returns an int in the range [0, N-1].
    # For a range [1, 100], we need secrets.randbelow(100) + 1.
    return secrets.randbelow(100) + 1
