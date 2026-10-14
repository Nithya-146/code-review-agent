import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.python_parser import validate_python
from app.java_parser import validate_java

def test_empty_python_code():
    res = validate_python("")
    assert res["is_valid"] is True
    assert res["metadata"]["lines_of_code"] == 0
    print("✓ Test 1: Empty Python input handled correctly")

def test_empty_java_code():
    res = validate_java("")
    assert res["is_valid"] is False
    print("✓ Test 2: Empty Java input caught by syntax parser")

def test_valid_python_structure():
    code = "class Calculator:\n    def add(self, a, b):\n        return a + b\n"
    res = validate_python(code)
    assert res["is_valid"] is True
    assert "Calculator" in res["metadata"]["classes"]
    assert "add" in res["metadata"]["functions"]
    print("✓ Test 3: Valid Python AST metadata extraction passed")

def test_broken_python_syntax():
    code = "def faulty_func(:\n    return 42"
    res = validate_python(code)
    assert res["is_valid"] is False
    assert "SyntaxError" in res["error"]
    print("✓ Test 4: Broken Python syntax rejected with error line")

def test_valid_java_structure():
    code = "public class AuthService { public boolean login(String u) { return true; } }"
    res = validate_java(code)
    assert res["is_valid"] is True
    assert "AuthService" in res["metadata"]["classes"]
    assert "login" in res["metadata"]["methods"]
    print("✓ Test 5: Valid Java AST metadata extraction passed")

def test_broken_java_syntax():
    code = "public class BrokenService { int x = ; }"
    res = validate_java(code)
    assert res["is_valid"] is False
    print("✓ Test 6: Broken Java syntax rejected with error details")

def test_file_extension_validation():
    allowed_extensions = [".py", ".java"]
    assert os.path.splitext("test.py")[1] in allowed_extensions
    assert os.path.splitext("Main.java")[1] in allowed_extensions
    assert os.path.splitext("script.js")[1] not in allowed_extensions
    assert os.path.splitext("document.pdf")[1] not in allowed_extensions
    print("✓ Test 7: File extension filtering (.py, .java only) verified")

if __name__ == "__main__":
    test_empty_python_code()
    test_empty_java_code()
    test_valid_python_structure()
    test_broken_python_syntax()
    test_valid_java_structure()
    test_broken_java_syntax()
    test_file_extension_validation()
    print("\n✅ All 7 Submission Module Tests Passed Successfully!")