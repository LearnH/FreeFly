
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreeFly.settings')

app = Celery('FreeFly')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()