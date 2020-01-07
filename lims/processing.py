import os
import logging

from .lims_celery import celery_app
from .models import Task

# Background Processing Steps
# 1. Specify postpone time
# 2. After time has elapsed, query the database for all existing Tasks.
# 3. For each workflow in workflow, check if a new file exists in the associated folder
# 3a. If file exists, launch the corresponding processor and return the pandas data frame to output the Excel template file.
# task.status values = [PENDING, EXECUTING, COMPLETED, FAILED]


class BackgroundProcessing:

    def __init__(self, delay=30):
        self.delay = delay * 60         # default delay is 30 minutes
        self.run_checks.apply_async(countdown=self.delay, queue='lims')

    @celery_app.task(name="lims-background-processor", bind=True)
    def run_checks(self):
        logging.info("Starting LIMS workflow check")
        tasks = Task.objects.all()
        for t in tasks:
            if t.status is "PENDING" and os.path.exists(t.workflow.input_path):
                BackgroundWorker(t)
        logging.info("Completed LIMS workflow check")
        self.run_checks.apply_async(countdown=self.delay, queue='lims')


class BackgroundWorker:

    def __init__(self, task):
        self.task = task
        self.run_worker.apply_async(queue="lims")

    @celery_app.task(name="lims-background-worker", bind=True)
    def run_worker(self):
        logging.info("Launching processor to import data. Workflow: {}".format(self.task.workflow.name))
        update_status(self.task.workflow, "EXECUTING")

        success = False
        results = None

        try:
            results = self.task.workflow.processor.execute(self.task.input_file)
            success = True
        except Exception as e:
            logging.info("Error attempting to execute processor: {}".format(e))
            update_status(self.task.workflow, "FAILED")
        if success:
            df = results.df
            df.to_excel(self.task.workflow.output_path, index=False)
            if os.path.exists(self.task.workflow.output_path):
                os.remove(self.task.workflow.input_path)
                update_status(self.task.workflow, "COMPLETED")
            logging.info("Completed processor to import data. Workflow: {}".format(self.task.workflow.name))


def update_status(workflow, status):
    task = Task.objects.get(workflow=workflow)
    task.status = status
    task.save()
