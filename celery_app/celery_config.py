from celery import Celery

import os

from celery_app.celery_crontab import BEAT_SCHEDULE

BROKER_URL = os.environ.get("RABBITMQ_BROKER", "amqp://user:password@localhost:5672//")
BACKEND_URL = None

app = Celery(
    "celery_app",
    broker=BROKER_URL,
    backend=BACKEND_URL
)

app.conf.timezone = "Europe/Kiev"
app.conf.enable_utc = False

app.conf.beat_scheduler = "celery.beat.PersistentScheduler"
app.conf.beat_schedule_filename = "celerybeat-schedule.db"

app.conf.beat_schedule = BEAT_SCHEDULE

app.autodiscover_tasks(["celery_app.tasks"])
