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
You are an experienced DevOps Engineer.

Analyze the following Jenkins console log.

Return the answer in this exact format.

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

        if response and getattr(response, "text", None):

            return response.text

        return "Gemini returned an empty response."

    except Exception as e:

        error = str(e)

        if "429" in error or "RESOURCE_EXHAUSTED" in error:

            return (
                "Gemini API quota exceeded. "
                "Please try again later."
            )

        if "404" in error or "NOT_FOUND" in error:

            return (
                "Gemini model not found."
            )

        if "API key" in error.lower():

            return (
                "Invalid Gemini API Key."
            )

        return f"AI Analysis Error: {error}"


def generate_ai_summary(build):

    if not build.console_log:

        return

    summary = generate_build_summary(
        build.console_log
    )

    build.ai_summary = summary

    build.save()