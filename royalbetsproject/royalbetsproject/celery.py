from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ['DJANGO_SETTINGS_MODULE'] = 'royalbetsproject.settings'

app = Celery('royalbetsproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
