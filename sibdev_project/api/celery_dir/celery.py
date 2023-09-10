import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sibdev_project.sibdev_root.settings')

import django

django.setup()

from celery.schedules import crontab
from celery import Celery
from environs import Env

env = Env()
env.read_env()

app = Celery('celery',
             broker=f"amqp://{env.str('RABBITMQ_DEFAULT_USER')}:{env.str('RABBITMQ_DEFAULT_PASS')}@{env.str('RABBITMQ_HOST')}:{env.str('RABBITMQ_PORT')}//")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'add-every-15-seconds': {
        'task': 'sibdev_project.api.services.tasks.run_task',
        'schedule': crontab(hour='12', minute='0'),
    },
}
