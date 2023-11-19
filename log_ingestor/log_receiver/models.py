# models.py
from django.db import models
import json

class LogEntry(models.Model):
    level = models.CharField(max_length=50)
    message = models.TextField()
    resource_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    trace_id = models.CharField(max_length=100)
    span_id = models.CharField(max_length=100)
    commit = models.CharField(max_length=100)
    metadata = models.TextField()  # Storing metadata as JSON text

    def set_metadata(self, metadata):
        self.metadata = json.dumps(metadata)

    def get_metadata(self):
        return json.loads(self.metadata)
