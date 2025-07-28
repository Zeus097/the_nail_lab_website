import os
import django
import pytest

# Set up Django before tests are collected
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_nail_lab_website.settings")
django.setup()
