# hydration_project/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hydration_project.settings')

app = Celery('hydration_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
