from celery import shared_task
from django.utils.dateparse import parse_datetime
from .models import LogEntry
from log_ingestor.elasticsearch_conf import index_log_in_elasticsearch as es_index
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_log_entry(log_data):
    try:
        # Convert timestamp to a datetime object
        log_data['timestamp'] = parse_datetime(log_data['timestamp'])

        # Re-map keys to match the model fields
        log_data['resource_id'] = log_data.pop('resourceId', '')
        log_data['metadata'] = log_data.pop('metadata', {})

        # Create a new LogEntry object and save it to PostgreSQL
        log_entry = LogEntry(**log_data)
        log_entry.save()

        # Prepare data for Elasticsearch and index it
        es_data = {
            "level": log_entry.level,
            "message": log_entry.message,
            "resource_id": log_entry.resource_id,
            "timestamp": log_entry.timestamp,
            "trace_id": log_entry.trace_id,
            "span_id": log_entry.span_id,
            "commit": log_entry.commit,
            "metadata": log_entry.metadata
        }
        es_index(es_data)
    except Exception as e:
        logger.error(f'Error processing log entry: {str(e)}')
