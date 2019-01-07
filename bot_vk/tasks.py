# Create your tasks here
from celery.task import periodic_task
from celery.schedules import crontab
from bot_vk.post_to_wall import post_to_wall_best_in_genre
from bot_vk.send_message_to_all import send_message_all_members

# hour=7, minute=30, day_of_week=1
@periodic_task(ignore_result=True, run_every=crontab(minute=25, hour=13, day_of_week=4))
def celery_post_to_wall_best_in_genre():
    post_to_wall_best_in_genre(169943927, 22)

@periodic_task(ignore_result=True, run_every=crontab(minute=30, hour=13, day_of_week=4))
def celery_send_message_all_members():
    send_message_all_members(169943927, 22)
