from os import environ
from kombu import Queue, Exchange

CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = environ.get('CELERY_RESULT_BACKEND')

CELERY_TIMEZONE = "Europe/Kiev"

CELERY_RESULT_PERSISTENT = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BROKER_HEARTBEAT_CHECKRATE = 10
CELERY_EVENT_QUEUE_EXPIRES = 10
CELERY_EVENT_QUEUE_TTL = 10
CELERY_TASK_SOFT_TIME_LIMIT = 60

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 4,
    'interval_start': 0,
    'interval_step': 0.5,
    'interval_max': 3,
}

# CELERY_TASK_QUEUES = (
#     Queue('blog', exchange='blog'),
# )

CELERY_TASK_DEFAULT_EXCHANGE = "celery"

CELERY_TASK_QUEUES = {
    "blog": {
        "binding_key": "blog",
    }
}

CELERY_TASK_ROUTES = {
    '*': {'queue': 'blog'},
    'main.tasks.*': {'queue': 'blog'}
}
