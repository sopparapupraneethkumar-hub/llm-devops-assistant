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
        You are a Senior DevOps Engineer specializing in Jenkins CI/CD pipelines.

        Your task is to analyze ONLY the current Jenkins build execution.

        IMPORTANT RULES:

        1. Focus ONLY on the latest build execution.
        2. Ignore old log messages, printed source code, comments, or historical output.
        3. If the build ends with:
        Finished: SUCCESS
        then DO NOT invent failures.
        4. If the build ends with:
        Finished: FAILURE
        then identify the real failure from the log.
        5. Ignore informational messages that do not affect the build.
        6. Never report warnings as Root Cause unless they actually failed the build.
        7. Base your answer only on evidence present in the console log.

        Return EXACTLY in this format:

        Root Cause:
        - ...

        Summary:
        - ...

        Suggested Fix:
        1.
        2.
        3.

        If the build completed successfully, your answer should look similar to:

        Root Cause:
        - No build failure detected. The Jenkins pipeline completed successfully.

        Summary:
        - Repository checkout completed successfully.
        - Python virtual environment was created.
        - Dependencies were installed.
        - Django system checks passed.
        - Build metadata was processed successfully.

        Suggested Fix:
        1. No immediate action required.
        2. Continue monitoring future builds.
        3. Add automated tests or deployment stages for additional quality assurance.

        Jenkins Console Log:

        {console_log}
        """

    


    models = [
        "gemini-flash-latest",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
    ]

    last_error = None

    for model_name in models:

        try:

            print(f"Trying Gemini Model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            if response and getattr(response, "text", None):

                print(f"Success with {model_name}")

                return response.text.strip()

            print(f"{model_name} returned an empty response.")

        except Exception as e:

            print(f"{model_name} failed -> {e}")

            last_error = e

            continue

    if last_error:

        error = str(last_error)

        if "429" in error or "RESOURCE_EXHAUSTED" in error:
            return (
                "Gemini API quota exceeded.\n\n"
                "Please try again later."
            )

        if "404" in error or "NOT_FOUND" in error:
            return (
                "Unable to access a supported Gemini model.\n\n"
                f"Last Error:\n{error}"
            )

        return (
            "Gemini Error\n\n"
            f"{error}"
        )

    return "Gemini did not return any response."


def generate_ai_summary(build):

    if not build.console_log:
        return

    build.ai_summary = generate_build_summary(
        build.console_log
    )

    build.save()