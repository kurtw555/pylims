from django.db import models

# Create your models here.


# class Processor(modeslModel):
#     name = models.CharField(max_length=250)


class Task(models.Model):
    id = models.UUIDField(primary_key='true')
    workflow = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    date = models.DateField()


class Workflow(models.Model):
    name = models.CharField(max_length=250)
    processor = models.CharField(max_length=250)
    inputPath = models.CharField(max_length=250)
    outputPath = models.CharField(max_length=250)
    frequency = models.PositiveIntegerField()
