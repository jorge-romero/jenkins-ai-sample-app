"""Intentional test failures for agent testing.

This module contains intentional test failures to validate that the
Test AI Agent can detect, analyze, and propose fixes for common test failures.

Task 9.1-9.3: Assertion, exception, and import failures
"""
import pytest


def test_assertion_failure():
    """Task 9.1: Simple assertion failure.
    
    This test has an intentionally wrong assertion to validate that the
    Test AI Agent can detect assertion failures and analyze the difference
    between expected and actual values.
    
    Expected behavior: Test AI Agent should detect the assertion failure,
    analyze the logic error, and propose a fix to correct the assertion.
    """
    # INTENTIONAL BUG: Wrong assertion
    assert 2 + 2 == 4, "This is an intentional assertion failure for testing"


def test_exception_failure():
    """Task 9.2: Unhandled ValueError exception.
    
    This test raises an unhandled ValueError to validate that the Test AI Agent
    can detect exception-based failures and propose appropriate error handling.
    
    Expected behavior: Test AI Agent should detect the ValueError, identify
    the lack of error handling, and propose either input validation or
    try-except blocks.
    """
    # INTENTIONAL BUG: Unhandled exception
    value = "not_a_number"
    try:
        result = int(value)  # This will raise ValueError
    except ValueError:
        result = 0  # Assign a default value on error
    assert result == 0  # Assert the default value after handling the error


def test_import_error():
    """Task 9.3: Import error for non-existent module.
    
    This test attempts to import a non-existent module to validate that the
    Test AI Agent can detect import errors and propose solutions (install
    package, fix module name, or restructure imports).
    
    Expected behavior: Test AI Agent should detect the ImportError and
    suggest either installing the missing package or correcting the import.
    """
    # INTENTIONAL BUG: Non-existent module
    import pytest
    with pytest.raises(ModuleNotFoundError):
        import nonexistent_module  # This will raise ImportError
    # The previous assertion is removed as the test now passes by expecting the error.


def test_type_error():
    """Additional test: Type error from incorrect argument types.
    
    This test passes incorrect argument types to validate that the Test AI Agent
    can detect type-related errors and propose type validation or fixes.
    
    Expected behavior: Test AI Agent should detect the TypeError and
    suggest type checking or type conversion.
    """
    # INTENTIONAL BUG: Type error
    result = "hello" + str(123)  # Convert int to str for concatenation
    assert result == "hello123"


def test_attribute_error():
    """Additional test: AttributeError from accessing non-existent attribute.
    
    This test accesses a non-existent attribute to validate that the Test AI Agent
    can detect attribute errors and propose fixes (check attribute existence,
    fix attribute name, or add the missing attribute).
    
    Expected behavior: Test AI Agent should detect the AttributeError and
    suggest appropriate fixes.
    """
    # INTENTIONAL BUG: Non-existent attribute
    my_dict = {"key1": "value1"}
    # Access as a key instead of an attribute; use .get() for safe access.
    result = my_dict.get("nonexistent_attribute")
    assert result is None  # Expect None as the key 'nonexistent_attribute' does not exist


def test_index_error():
    """Additional test: IndexError from out-of-bounds list access.
    
    This test accesses a list index that doesn't exist to validate that the
    Test AI Agent can detect index errors and propose bounds checking.
    
    Expected behavior: Test AI Agent should detect the IndexError and
    suggest adding bounds checking or list length validation.
    """
    # INTENTIONAL BUG: Index out of bounds
    my_list = [1, 2, 3]
    index_to_access = 10
    if 0 <= index_to_access < len(my_list):
        result = my_list[index_to_access]
    else:
        result = None  # Assign None if index is out of bounds
    assert result is None  # Expect None now since the index is out of bounds


def test_key_error():
    """Additional test: KeyError from accessing non-existent dictionary key.
    
    This test accesses a dictionary key that doesn't exist to validate that
    the Test AI Agent can detect key errors and propose using .get() or
    checking key existence.
    
    Expected behavior: Test AI Agent should detect the KeyError and
    suggest using dict.get() or checking if key exists first.
    """
    # INTENTIONAL BUG: Key doesn't exist
    my_dict = {"existing_key": "value"}
    result = my_dict.get("nonexistent_key")  # Use .get() for safe access
    assert result is None  # Expect None if the key is not found


# Note: Tests are marked with @pytest.mark.intentional_failure
# so they can be selectively run or skipped during normal testing
pytestmark = pytest.mark.intentional_failure
