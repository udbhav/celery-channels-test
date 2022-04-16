from __future__ import absolute_import, unicode_literals
import asyncio
import os

import channels.layers
from celery import Celery
from asgiref.sync import async_to_sync

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_channels_test.settings")

app = Celery("celery_channels_test")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def sync_send(self):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)("foo", {"bar": 1})


@app.task(bind=True)
def detect_event_loop(self):
    try:
        event_loop = asyncio.get_event_loop()
    except RuntimeError:
        pass
    else:
        if event_loop.is_running():
            raise ValueError("event loop running")
