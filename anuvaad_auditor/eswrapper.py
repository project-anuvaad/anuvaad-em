import logging
from datetime import datetime

from elasticsearch import Elasticsearch
from .config import es_url
from .config import es_core_error_index
from .config import es_wf_error_index
from .config import es_audit_index

log = logging.getLogger('file')

es_core_error_index_test = "anuvaad-etl-core-errors-test-v1"
es_wf_error_index_test = "anuvaad-etl-wf-errors-test-v1"
es_audit_index_test = "anuvaad-etl-audit-test-v1"

# Method to instantiate the elasticsearch client.
def instantiate_es_client():
    es_client = Elasticsearch([es_url])
    return es_client


# Method to index errors on to elasticsearch.
def index_error_to_es(index_obj):
    try:
        es = instantiate_es_client()
        id = index_obj["errorID"]
        if index_obj["errorType"] == "core-error":
            in_name = es_core_error_index
        else:
            in_name = es_wf_error_index
        index_obj = add_timestamp_field(index_obj)
        es.index(index=in_name, id=id, body=index_obj)
    except Exception as e:
        log.exception("Indexing FAILED for errorID: " + index_obj["errorID"], e)


# Method to index audit details onto elasticsearch
def index_audit_to_es(index_obj):
    try:
        es = instantiate_es_client()
        id = index_obj["auditID"]
        index_obj = add_timestamp_field(index_obj)
        es.index(index=es_audit_index, id=id, body=index_obj)
    except Exception as e:
        log.exception("Indexing FAILED for errorID: " + index_obj["auditID"], e)


# Method to generate timestamp in the format es expects per index object.
def add_timestamp_field(error):
    #date_format = "%Y-%m-%d'T'%H:%M:%S.%f'Z'"
    epoch = error["timeStamp"]
    epoch_short = eval((str(epoch)[:10]))
    error["@timestamp"] = datetime.fromtimestamp(epoch_short).isoformat()
    return error