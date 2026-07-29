from google import genai
from django.conf import settings


def get_client():
    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


def generate_build_summary(console_log):

    if not console_log:
        return "No console log available."

    client = get_client()

    if client is None:
        return "Gemini API key is not configured."

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
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:
        return f"Error generating AI summary: {str(e)}"