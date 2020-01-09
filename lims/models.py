import datetime
from django.db import models

# Create your models here.


class Processor(models.Model):
    FILE_TYPES = (
        (".csv", "comma separated value"),
        (".xlsx", "excel"),
        (".txt", "tab delimited")
    )
    # name needs to be unique across all processors
    id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    version = models.CharField(max_length=20)
    description = models.CharField(max_length=250)
    file_type = models.CharField(max_length=5, choices=FILE_TYPES)
    enabled = models.BooleanField(default=False)
    #input_file = models.CharField(max_length=50)
    #path = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Workflow(models.Model):
    id = models.CharField(max_length=20)
    name = models.CharField(max_length=20, default='')
    processor = Processor
    input_path = models.CharField(max_length=250)
    output_path = models.CharField(max_length=250, default='')
    v_input_path = models.CharField(max_length=250, default='')
    v_output_path = models.CharField(max_length=250, default='')
    # interval in seconds - limited to 32767 - roughly 22 days
    interval = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.name}'


class Task(models.Model):
    id = models.CharField(max_length=20, default='')
    workflow = models.CharField(max_length=50)
    input_file = models.CharField(max_length=50)
    output_file = models.CharField(max_length=50)
    start_time = models.DateTimeField()     # scheduled to execute
    status = models.CharField(max_length=50, default='PENDING')
    message = models.CharField(max_length=120, default='')

    @classmethod
    def create(cls, task_id, workflow, input_file=None, start_time=None, status="PENDING", message=""):
        i_file = '' if input_file is None else input_file
        scheduled_time = datetime.datetime.now() + datetime.timedelta(minutes=30) if start_time is None else start_time
        task = cls(
            id=task_id,
            workflow=workflow,
            input_file=i_file,
            output_file='',
            start_time=scheduled_time,
            status=status,
            message=message
        )
        return task
