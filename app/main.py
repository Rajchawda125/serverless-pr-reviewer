
from pathlib import Path

from app.code_analyzer import analyze_code
from app.ai_reviewer import review_with_ai


def review_file(file_path):

    path = Path(file_path)

    if not path.exists():
        print("Error: File not found.")
        return

    if path.suffix != ".py":
        print("Error: Please provide a Python file.")
        return

    source_code = path.read_text(encoding="utf-8")

    # Static code analysis
    issues = analyze_code(source_code)

    print("\n========== STATIC CODE ANALYSIS ==========")
    print(f"File: {path.name}")
    print(f"Total issues found: {len(issues)}")

    for index, issue in enumerate(issues, start=1):
        print(f"\nIssue {index}")
        print(f"Severity: {issue['severity']}")
        print(f"Line: {issue['line']}")
        print(f"Message: {issue['message']}")

    # Gemini AI review
    print("\n========== GEMINI AI CODE REVIEW ==========")

    ai_result = review_with_ai(source_code)

    print(ai_result)

    print("\n========== REVIEW COMPLETED ==========")


if __name__ == "__main__":

    file_path = input("Enter Python file path to review: ")

    review_file(file_path)
