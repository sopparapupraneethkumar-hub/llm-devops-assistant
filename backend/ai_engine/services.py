from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_build_summary(console_log):
    prompt = f"""
You are an experienced DevOps engineer.

Analyze the following Jenkins console log.

Return your response in this format:

Root Cause:
...

Summary:
...

Suggested Fix:
...

Console Log:
{console_log}
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error generating AI summary: {str(e)}"