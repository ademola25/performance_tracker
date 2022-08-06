from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gt_hr.settings')

app = Celery('gt_hr')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# env_file = os.path.join(os.path.dirname(
#     os.path.dirname(os.path.realpath(__file__))), '.env')
# os.environ.get(env_file)
