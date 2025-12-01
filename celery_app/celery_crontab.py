from celery.schedules import crontab

BEAT_SCHEDULE = {
    "make_report": {
        "task": "celery_app.tasks.make_report",
        "schedule": crontab(minute='*/1.5'),
    },
    "check_subscription": {
        "task": "celery_app.tasks.check_subscriptions_task",
        "schedule": crontab(minute='*/1'),
    }
}
# hour=18
