from django.db import models
import os
import abc
import lims.models

class MassLynx(Processor):
    def __init__(self):
        self.input_file = ""

    def execute(self, db_processor):
        
        

