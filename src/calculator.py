"""Calculator module with logic bugs (BUG #4)."""
from typing import List, Any


class Calculator:
    """Calculator with OBVIOUS bugs."""
    
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers.
        
        BUG #4: No zero division check!
        This will raise ZeroDivisionError when b=0
        """
        if b == 0: raise ValueError("Cannot divide by zero")
        return a / b  # OBVIOUS BUG: What if b is 0?
    
    def get_first_n_items(self, items: List[Any], n: int) -> List[Any]:
        """Get first N items from a list.
        
        BUG #4: Off-by-one error when n > len(items)
        """
        if n > len(items):
            # OBVIOUS BUG: Should return all items, not items[0:n-1]
            return items[0:n-1]  # Wrong!
        return items[0:n]
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers (this one is correct)."""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers (this one is correct)."""
        return a - b
