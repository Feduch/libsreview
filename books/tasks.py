# Create your tasks here
from celery.task import periodic_task
from celery.schedules import crontab
from books.views import update_ratings, import_from_litres


@periodic_task(ignore_result=True, run_every=crontab(hour=0, minute=1))
def celery_update_ratings():
    update_ratings()


@periodic_task(ignore_result=True, run_every=crontab(hour=1, minute=0))
def celery_import_from_litres():
    import_from_litres()
