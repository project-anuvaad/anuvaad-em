import os

anu_etl_wf_error_topic = os.environ.get('ANU_DP_WF_ERROR_TOPIC', 'anuvaad-etl-wf-errors')
es_url = os.environ.get('ANUVAAD_DP_ES_URL', 'localhost')

es_core_error_index = os.environ.get('ANUVAAD_DP_ES_CORE_ERROR_INDEX', 'anuvaad-etl-errors-core-v1')
es_wf_error_index = os.environ.get('ANUVAAD_DP_ES_WF_ERROR_INDEX', 'anuvaad-etl-errors-wf-v1')
es_audit_index = os.environ.get('ANUVAAD_DP_ES_AUDIT_INDEX', 'anuvaad-etl-audit-test-v1')
