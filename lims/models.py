from django.db import models

# Create your models here.


class Processor(models.Model):
    FILE_TYPES = (
        (".csv", "comma separated value"),
        (".xlsx", "excel"),
        (".txt", "tab delimited")
    )
    # name needs to be unique across all processors
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=250)
    file_type = models.CharField(max_length=5, choices=FILE_TYPES)
    enabled = models.BooleanField(default=False)
    #input_file = models.CharField(max_length=50)
    #path = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Workflow(models.Model):
    name = models.CharField(max_length=20, default='')
    processor = Processor
    input_path = models.CharField(max_length=250)
    output_path = models.CharField(max_length=250, default='')
    # interval in seconds - limited to 32767 - roughly 22 days
    interval = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.name}'


class Task(models.Model):
    workflow = Workflow
    input_file = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    status = models.CharField(max_length=50, default='PENDING')
