from datetime import datetime, timedelta

from drf_api_logger.models import APILogsModel

from src.celery import app


@app.task(name="main.tasks.add", queue="blog")
def add(x, y):
    return x + y


@app.task(name="main.tasks.mul", queue="blog")
def mul(x, y):
    return x * y


@app.task(name="main.tasks.xsum", queue="blog")
def xsum(numbers):
    return sum(numbers)


@app.task(name="main.tasks.cleanup", queue="blog")
def cleanup():
    # Get the current date
    current_date = datetime.now()

    # Calculate the first day of the current month
    first_day_of_current_month = current_date.replace(day=1)

    # Calculate the last day of the previous month
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

    # Calculate the first day of the previous month
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    APILogsModel.objects.filter(
        added_on__gte=first_day_of_previous_month, added_on__lte=last_day_of_previous_month
    ).delete()
    return
