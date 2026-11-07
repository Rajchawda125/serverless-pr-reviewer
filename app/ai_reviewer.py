
import os

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def review_with_ai(source_code):

    if not API_KEY:
        return "Error: Gemini API key not found."

    try:
        client = genai.Client(api_key=API_KEY)

        prompt = f"""
You are an experienced Python code reviewer.

Review the following Python code.

Check for:
1. Bugs
2. Security vulnerabilities
3. Performance issues
4. Coding best practices

For every issue, provide:
- Severity (HIGH, MEDIUM, LOW)
- Line number (if identifiable)
- Explanation
- Suggested fix

Python code:

{source_code}
"""

        response = client.models.generate_content(
           model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        return f"AI Review Error: {error}"
