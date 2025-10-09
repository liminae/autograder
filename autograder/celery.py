import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autograder.settings")

app = Celery("proj")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(task_concurrency=4, worker_prefetch_multiplier=1)

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
