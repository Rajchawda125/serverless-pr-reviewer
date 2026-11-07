
import ast


class CodeAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.issues = []

    def visit_Call(self, node):
        # Detect unsafe eval() and exec()
        if isinstance(node.func, ast.Name):
            if node.func.id in ("eval", "exec"):
                self.issues.append({
                    "severity": "HIGH",
                    "message": f"Unsafe use of {node.func.id}() detected.",
                    "line": node.lineno
                })

        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        # Detect bare except clause
        if node.type is None:
            self.issues.append({
                "severity": "LOW",
                "message": "Bare except clause detected. "
                           "Use a specific exception instead.",
                "line": node.lineno
            })

        self.generic_visit(node)

    def visit_Assign(self, node):
        # Detect hardcoded passwords and secrets
        sensitive_names = (
            "password", "secret", "api_key", "apikey"
        )

        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id.lower()

                if any(key in name for key in sensitive_names):
                    if isinstance(node.value, ast.Constant):
                        if isinstance(node.value.value, str):
                            if node.value.value.strip():
                                self.issues.append({
                                    "severity": "HIGH",
                                    "message": (
                                        f"Possible hardcoded secret "
                                        f"in variable '{target.id}'."
                                    ),
                                    "line": node.lineno
                                })

        self.generic_visit(node)


def analyze_code(source_code):
    """
    Analyze Python source code and return detected issues.
    """

    try:
        syntax_tree = ast.parse(source_code)

    except SyntaxError as error:
        return [{
            "severity": "ERROR",
            "message": f"Syntax error: {error.msg}",
            "line": error.lineno
        }]

    analyzer = CodeAnalyzer()
    analyzer.visit(syntax_tree)

    return analyzer.issues
