from django.db import models

# Create your models here.

class DBProcessor(models.Model):
    FILE_TYPES = (
        (".csv", "comma separated value"),
        (".xlsx", "excel"),
        (".txt", "tab delimited")
    )
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    file_type = models.CharField(max_length=5, choices=FILE_TYPES)
    input_file = models.CharField(max_length=50)
    path = models.CharField(max_length=50)


class DBTask(models.Model):
    processor = models.ForeignKey(DBProcessor)
    input_file = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class DBWorkflow(models.Model):
    processor = models.ForeignKey(DBProcessor)
