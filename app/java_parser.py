import javalang
from typing import Dict, Any, List

def validate_java(code: str) -> Dict[str, Any]:
    """
    Parses Java source code using javalang to verify syntax
    and extracts declared classes and methods.
    """
    try:
        tokens = javalang.tokenizer.tokenize(code)
        parser = javalang.parser.Parser(tokens)
        tree = parser.parse()
        
        classes: List[str] = []
        methods: List[str] = []
        
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            classes.append(node.name)
            
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            methods.append(node.name)

        return {
            "is_valid": True,
            "error": None,
            "metadata": {
                "classes": classes,
                "methods": methods,
                "lines_of_code": len(code.splitlines())
            }
        }
    except (javalang.parser.JavaSyntaxError, javalang.tokenizer.LexerError) as err:
        return {
            "is_valid": False,
            "error": f"Java Parsing Error: {str(err)}",
            "metadata": {}
        }
    except Exception as err:
        return {
            "is_valid": False,
            "error": f"Unexpected Java parse failure: {str(err)}",
            "metadata": {}
        }