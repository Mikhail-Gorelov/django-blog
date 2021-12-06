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
