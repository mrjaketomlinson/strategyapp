import django
import os
import sys

sys.path.append("/app")

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "strategyapp.settings")
django.setup()

from account.models import Organization

Organization.objects.all().delete()