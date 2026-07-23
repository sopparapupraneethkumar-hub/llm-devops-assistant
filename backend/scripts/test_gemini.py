import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from ai_engine.services import generate_build_summary

sample_log = """
Started by user Praneeth Kumar

Collecting packages...
Installing dependencies...

Traceback (most recent call last):
ModuleNotFoundError: No module named 'psycopg'

Finished: FAILURE
"""

summary = generate_build_summary(sample_log)

print("\n========== AI SUMMARY ==========\n")
print(summary)