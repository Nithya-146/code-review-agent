import sys
sys.path.append(".")

from app.python_parser import validate_python
from app.java_parser import validate_java

def test_python_valid():
    sample_code = """
import os

def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
"""
    result = validate_python(sample_code)
    assert result["is_valid"] is True
    assert "calculate_total" in result["metadata"]["functions"]
    assert "os" in result["metadata"]["imports"]
    print("✓ Python valid syntax check passed")

def test_python_invalid():
    sample_code = """
def broken_function(
    x = 10
"""
    result = validate_python(sample_code)
    assert result["is_valid"] is False
    assert "SyntaxError" in result["error"]
    print("✓ Python invalid syntax handling passed")

def test_java_valid():
    sample_code = """
public class AccountService {
    public void deposit(double amount) {
        System.out.println("Amount deposited");
    }
}
"""
    result = validate_java(sample_code)
    assert result["is_valid"] is True
    assert "AccountService" in result["metadata"]["classes"]
    assert "deposit" in result["metadata"]["methods"]
    print("✓ Java valid syntax check passed")

def test_java_invalid():
    sample_code = """
public class BrokenClass {
    public void brokenMethod( {
}
"""
    result = validate_java(sample_code)
    assert result["is_valid"] is False
    print("✓ Java invalid syntax handling passed")

if __name__ == "__main__":
    test_python_valid()
    test_python_invalid()
    test_java_valid()
    test_java_invalid()
    print("\nAll submission parser tests completed successfully!")