from sibdev_project.api.celery_dir.celery import app
from sibdev_project.api.services.currency_service import CurrencyService


@app.task()
def run_task():
    CurrencyService().daily_add_currencies()
