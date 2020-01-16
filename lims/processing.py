import os
import logging
import datetime

from .lims_celery import celery_app
from .models import Task, Workflow, Processor


class GenerateTask:

    def __init__(self, workflow):
        self.workflow = workflow.name
        self.interval = workflow.interval
        self.input_file = None
        self.start_date = datetime.datetime.now() + datetime.timedelta(minutes=self.interval)
        self.status = "PENDING"
        self.id = self.generate_task.apply_async(countdown=self.interval * 60, queue='lims')
        self.task = Task.create(self.id, self.workflow, self.input_file, self.start_date, self.status, "")
        self.task.save()

    @celery_app.task(name="lims-background-processor", bind=True)
    def generate_task(self):
        _id = celery_app.current_task.request.id
        task = Task.objects.get(id=_id)
        if task.status != "PENDING":                        # Only PENDING tasks are processed
            return
        logging.info("TASK: {} checking for files".format(self.id))
        workflow = Workflow.objects.get(name=self.workflow)
        if os.path.exists(workflow.v_input_path):               # Check if volume input directory exists
            input_file = os.listdir(workflow.v_input_path)
            if len(input_file) > 0:                             # Check if volume input directory contains any files
                for i in input_file:
                    completed = task_done(i)                    # Check if input file has an associated completed task
                    if not completed:
                        logging.info("TASK: {} executing processor for file: {}".format(self.id, i))
                        task.input_file = i
                        task.status = "EXECUTING"
                        task.save()
                        success = self.run_processor(task, workflow.processor, i, workflow.v_input_path, workflow.v_output_path)
                        if success:
                            GenerateTask(workflow)              # Generate a new Task upon successfully completion of current task
            else:
                task.start_time = datetime.datetime.now() + datetime.timedelta(minutes=workflow.interval)
                task.save()
                self.generate_task.retry(countdown=self.interval * 60)          # reschedule task because of no input files
        else:
            task.status = "FAILED"
            task.message = "Input path cannot be found. Input path: {}".format(workflow.v_input_path)
            task.save()

    def run_processor(self, task, processor_name, input_file, input_path, output_path):
        input = os.path.join(input_path, input_file)
        try:
            processor = Processor.objects.get(name=processor_name)
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
            task.status = "COMPLETED"
            task.save()
        else:
            task.status = "FAILED"
            task.message = "Output failed to be generated."
            task.save()
            return False
        logging.info("Completed processor to import data. Workflow: {}".format(self.task.workflow.name))
        return True


def task_done(file):
    tasks = Task.objects.get(input_file=file)
    if len(tasks) > 0:
        return True
    else:
        return False
