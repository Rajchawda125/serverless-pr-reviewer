
import unittest

from app.code_analyzer import analyze_code


class TestCodeAnalyzer(unittest.TestCase):

    def test_eval_detection(self):
        code = "result = eval('2 + 2')"
        issues = analyze_code(code)

        self.assertTrue(
            any("eval()" in issue["message"] for issue in issues)
        )

    def test_exec_detection(self):
        code = "exec('print(hello)')"
        issues = analyze_code(code)

        self.assertTrue(
            any("exec()" in issue["message"] for issue in issues)
        )

    def test_bare_except_detection(self):
        code = """
try:
    print("Hello")
except:
    print("Error")
"""
        issues = analyze_code(code)

        self.assertTrue(
            any("Bare except" in issue["message"] for issue in issues)
        )

    def test_hardcoded_password_detection(self):
        code = 'password = "mypassword123"'
        issues = analyze_code(code)

        self.assertTrue(
            any("hardcoded secret" in issue["message"] for issue in issues)
        )

    def test_clean_code(self):
        code = 'print("Hello World")'
        issues = analyze_code(code)

        self.assertEqual(len(issues), 0)

    def test_syntax_error(self):
        code = "if True print('Hello')"
        issues = analyze_code(code)

        self.assertEqual(issues[0]["severity"], "ERROR")


if __name__ == "__main__":
    unittest.main()
