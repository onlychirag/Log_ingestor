from elasticsearch import Elasticsearch
es_client = Elasticsearch(
    [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]
)
#es_client = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def index_log_in_elasticsearch(log_entry):
    es_data = {
        "level": log_entry.level,
        "message": log_entry.message,
        "resource_id": log_entry.resource_id,
        "timestamp": log_entry.timestamp,
        "trace_id": log_entry.trace_id,
        "span_id": log_entry.span_id,
        "commit": log_entry.commit,
        "metadata": log_entry.get_metadata(),
    }
    es_client.index(index="log_entries", body=es_data)

