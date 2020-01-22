import os
import logging
from celery import uuid
from django.utils import timezone

from .lims_celery import celery_app
from .models import Task, Workflow
from lims.plugins.plugin_collection import PluginCollection

processors = PluginCollection('lims.processors')


class GenerateTask:

    def __init__(self, workflow):
        self.workflow = workflow.name
        self.interval = workflow.interval
        self.input_file = None
        self.start_date = timezone.now() + timezone.timedelta(minutes=self.interval)
        self.status = "PENDING"
        self.id = uuid()
        self.task = Task.create(self.id, self.workflow, self.input_file, self.start_date, self.status, "")
        self.task.save()
        self.generate_task.apply_async(args=(self.id, workflow.id, self.interval), id=self.id, countdown=self.interval * 60, queue='lims')

    @celery_app.task(name="lims-background-processor", bind=True)
    def generate_task(self, id, workflow, interval):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            GenerateTask(workflow)
            return
        if task.status != "PENDING":                        # Only PENDING tasks are processed
            return
        logging.info("TASK: {} checking for files".format(id))
        workflow = Workflow.objects.get(id=workflow)
        if os.path.exists(workflow.v_input_path):               # Check if volume input directory exists
            input_file = os.listdir(workflow.v_input_path)
            if len(input_file) > 0:                             # Check if volume input directory contains any files
                for i in input_file:
                    completed = task_done(i)                    # Check if input file has an associated completed task
                    if not completed:
                        logging.info("TASK: {} executing processor for file: {}".format(id, i))
                        task.input_file = os.path.join(workflow.v_input_path, i)
                        task.status = "EXECUTING"
                        task.save()
                        success = run_processor(task, workflow.name, workflow.processor_name, i, workflow.v_input_path, workflow.v_output_path)
                        if success:
                            GenerateTask(workflow)              # Generate a new Task upon successfully completion of current task
            else:
                task.start_time = timezone.now() + timezone.timedelta(minutes=workflow.interval)
                task.save()
                self.retry(countdown=interval * 60)          # reschedule task because of no input files
        else:
            task.status = "FAILED"
            task.message = "Input path cannot be found. Input path: {}".format(workflow.v_input_path)
            task.save()


def run_processor(task, workflow_name, processor_name, input_file, input_path, output_path):
    input = os.path.join(input_path, input_file)
    try:
        processor = get_processor(processor_name)
        results = processor.execute(input)
    except Exception as e:
        logging.info("Error attempting to execute processor: {}".format(e))
        task.status = "FAILED"
        task.message = "Error executing process. {}".format(e)
        task.save()
        return False
    df = results.df
    output = input_file.split(".")[0] + "_output.xlsx"
    output_path = os.path.join(output_path, output)
    df.to_excel(output_path, index=False)
    if os.path.exists(output_path):
        os.remove(input)
        task.output_file = output_path
        task.status = "COMPLETED"
        task.save()
    else:
        task.status = "FAILED"
        task.message = "Output failed to be generated."
        task.save()
        return False
    logging.info("Completed processor to import data. Workflow: {}".format(workflow_name))
    return True


def task_done(file):
    try:
        tasks = Task.objects.get(input_file=file)
    except Task.DoesNotExist:
        tasks = None
    if tasks is None:
        return False
    else:
        if tasks.status == "COMPLETED":
            return True
        else:
            return False


def get_processor(name):
    processor = None
    for p in processors.plugins:
        if p.name == name:
            processor = p
    return processor
