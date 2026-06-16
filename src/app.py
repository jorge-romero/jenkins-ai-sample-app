"""Sample FastAPI application with intentional bugs for demonstration."""
from fastapi import FastAPI, HTTPException
# from typing import Optional
from .database import UserDatabase
from .auth import AuthService
from .calculator import Calculator

app = FastAPI(title="Buggy Sample App")

# Initialize services
db = UserDatabase()
auth = AuthService()
calc = Calculator()


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to the Buggy Sample App!"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Get user by ID (has SQL injection vulnerability)."""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users")
def create_user(name: str, email: str):
    """Create a new user."""
    user_id = db.create_user(name, email)
    return {"id": user_id, "name": name, "email": email}


@app.get("/calculate/divide")
def divide_numbers(a: float, b: float):
    """Divide two numbers (has division by zero bug)."""
    result = calc.divide(a, b)
    return {"result": result}


@app.get("/calculate/first-n")
def get_first_n(n: int):
    """Get first N items (has off-by-one bug)."""
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    result = calc.get_first_n_items(items, n)
    return {"items": result}


@app.get("/auth/check")
def check_auth(token: str):
    """Check authentication (has hardcoded secret)."""
    is_valid = auth.authenticate(token)
    return {"authenticated": is_valid}
