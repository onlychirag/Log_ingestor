from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LogEntry
#from .tasks import index_log_in_elasticsearch  
import json
from log_ingestor.elasticsearch_conf import index_log_in_elasticsearch
from django.utils.dateparse import parse_datetime
import logging
from django.shortcuts import render
from .forms import LogSearchForm
from elasticsearch import Elasticsearch
from django.shortcuts import render
from .forms import LogSearchForm
from django.shortcuts import render
from .forms import LogSearchForm
from elasticsearch import Elasticsearch
from django.conf import settings


def search_logs(request):
    form = LogSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        es = Elasticsearch(settings.ELASTICSEARCH_DSL)

        # Constructing the Elasticsearch query
        search_params = form.cleaned_data
        query = {
            "bool": {
                "must": [],
                "filter": []
            }
        }

        # Textual fields: level, message, resourceId, traceId, spanId, commit
        for field in ['level', 'message', 'resource_id', 'trace_id', 'span_id', 'commit']:
            value = search_params.get(field)
            if value:
                query['bool']['must'].append({"match": {field: value}})

        # Date range for timestamp
        timestamp = search_params.get('timestamp')
        if timestamp:
            query['bool']['filter'].append({"range": {"timestamp": {"gte": timestamp}}})

        # Nested field for metadata.parentResourceId
        parent_resource_id = search_params.get('parent_resource_id')
        if parent_resource_id:
            query['bool']['must'].append({"nested": {
                "path": "metadata",
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"metadata.parentResourceId": parent_resource_id}}
                        ]
                    }
                }
            }})

        response = es.search(index="log_entries", body={"query": query}, size=10)
        results = response['hits']['hits']

    return render(request, 'search.html', {'form': form, 'results': results})


def search_logs(request):
    form = LogSearchForm(request.GET or None)
    results = []

    if form.is_valid():
        es = Elasticsearch()
        query = {"query": {"bool": {"must": [], "filter": []}}}
        form_data = form.cleaned_data

        # Construct query based on form input
        for key, value in form_data.items():
            if value:
                query['query']['bool']['filter'].append({"term": {key: value}})

        # Execute query
        response = es.search(index="log_entries", body=query)
        results = response['hits']['hits']

    return render(request, 'search.html', {'form': form, 'results': results})


logger = logging.getLogger(__name__)  # Set up logging

@csrf_exempt 
def ingest_log(request):
    if request.method == 'POST':
        try:
            log_data = json.loads(request.body.decode('utf-8'))

            # Basic data validation (you can expand this as needed)
            if not log_data.get('level') or not log_data.get('message'):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            log_entry = LogEntry(
                level=log_data.get('level', ''),
                message=log_data.get('message', ''),
                resource_id=log_data.get('resourceId', ''),
                timestamp=parse_datetime(log_data.get('timestamp')),
                trace_id=log_data.get('traceId', ''),
                span_id=log_data.get('spanId', ''),
                commit=log_data.get('commit', ''),
                metadata=log_data.get('metadata', {})
            )
            log_entry.save()

            # Asynchronously index the log in Elasticsearch
            index_log_in_elasticsearch.delay(log_entry.id)  # Pass log entry ID or relevant data

            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f'Error ingesting log: {str(e)}')  # Log the exception
            return JsonResponse({"status": "error", "message": "Internal Server Error"}, status=500)
    else:
        return JsonResponse({'status': 'invalid request'}, status=400)
