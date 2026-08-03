import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

print("\n========== AVAILABLE MODELS ==========\n")

for model in client.models.list():
    print(model.name)