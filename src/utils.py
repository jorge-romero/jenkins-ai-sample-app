"""Utility module with code quality issues (BUG #3)."""


def process_data(a, b, c, d, e, f):
    """Process data with multiple parameters.
    
    BUG #3: High complexity, too many parameters, unused variables
    This function has OBVIOUS code quality issues.
    """
    # FIXED QUALITY BUG: Removed unused variables
    
    # OBVIOUS BUG: Deep nesting and high cyclomatic complexity!
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        if f > 0:
                            return a + b + c + d + e + f
                        else:
                            return a + b + c + d + e
                    else:
                        return a + b + c + d
                else:
                    return a + b + c
            else:
                return a + b
        else:
            return a
    else:
        return 0


def another_messy_function(x, y, z):
    """Another function with quality issues.
    
    BUG #3: More unused variables and complexity.
    """
    unused_1 = "not used"
    unused_2 = "also not used"
    unused_3 = "still not used"
    
    # This works but has unused variables above
    return x + y + z


class DataProcessor:
    """A class with code quality issues."""
    
    def __init__(self):
        # OBVIOUS BUG: Unused attributes
        self.unused_attr = "never accessed"
        self.another_unused = 123
    
    def process(self, data):
        """Process some data (ignores unused attributes)."""
        return data * 2
