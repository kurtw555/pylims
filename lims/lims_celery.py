# Celery setup and configuration for LIMS

import os
import logging
from celery import Celery


celery_tasks = [
    'lims.processing'
]

redis_server = os.environ.get('REDIS_HOSTNAME') if os.environ.get('REDIS_HOSTNAME') is not None else 'localhost'
redis_port = os.environ.get('REDIS_PORT') if os.environ.get('REDIS_PORT') is not None else '6379'

redis = 'redis://' + redis_server + ':' + redis_port + '/0'

logging.info("Celery connecting to redis server: {}".format(redis))

celery_app = Celery("lims", broker=redis, backend=redis, include=celery_tasks)
celery_app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_IGNORE_RESULT=False,
    CELERY_TRACK_STARTED=True,
    CELERYD_MAX_MEMORY_PER_CHILD=50000000
)
