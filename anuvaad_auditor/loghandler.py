import logging
import time
import uuid
import inspect

from .eswrapper import index_audit_to_es

log = logging.getLogger('file')
from .config import es_url

# Method to log and index INFO level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
def log_info(message, entity):
    log.info(message)
    if es_url != 'localhost':
        try:
            previous_frame = inspect.currentframe().f_back
            (filename, line_number,
             function_name, lines, index) = inspect.getframeinfo(previous_frame)
            audit = {
                "auditID": generate_error_id(),
                "methodName": function_name,
                "fileName": filename,
                "lineNo": line_number,
                "message": str(message),
                "timeStamp": eval(str(time.time()).replace('.', '')),
                "auditType": "INFO"
            }
            audit_enriched = enrich_entity_details(audit, entity)
            if audit_enriched is not None:
                audit = audit_enriched
            index_audit_to_es(audit)
        except Exception as e:
            log.exception("Anuvaad Auditor INFO failed.", e)
            return None


# Method to log and index DEBUG level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
def log_debug(message, entity):
    log.debug(message)
    if es_url != 'localhost':
        try:
            previous_frame = inspect.currentframe().f_back
            (filename, line_number,
             function_name, lines, index) = inspect.getframeinfo(previous_frame)
            audit = {
                "auditID": generate_error_id(),
                "methodName": function_name,
                "fileName": filename,
                "lineNo": line_number,
                "message": str(message),
                "timeStamp": eval(str(time.time()).replace('.', '')),
                "auditType": "DEBUG"
            }
            audit_enriched = enrich_entity_details(audit, entity)
            if audit_enriched is not None:
                audit = audit_enriched
            index_audit_to_es(audit)
        except Exception as e:
            log.exception("Anuvaad Auditor DEBUG failed.", e)
            return None



# Method to log and index EXCEPTION level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
# exc: Exception object
def log_exception(message, entity, exc):
    log.exception(message)
    if es_url != 'localhost':
        try:
            previous_frame = inspect.currentframe().f_back
            (filename, line_number,
             function_name, lines, index) = inspect.getframeinfo(previous_frame)
            audit = {
                "auditID": generate_error_id(),
                "methodName": function_name,
                "fileName": filename,
                "lineNo": line_number,
                "message": str(message),
                "timeStamp": eval(str(time.time()).replace('.', '')),
                "auditType": "EXCEPTION"
            }
            audit_enriched = enrich_entity_details(audit, entity)
            if audit_enriched is not None:
                audit = audit_enriched
            if exc is not None:
                audit["cause"] = str(exc)
            index_audit_to_es(audit)
        except Exception as e:
            log.exception("Anuvaad Auditor EXCEPTION failed.", e)
            return None



# Method to log and index EXCEPTION level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
# exc: Exception object
def log_error(message, entity, exc):
    log.error(message)
    if es_url != 'localhost':
        try:
            previous_frame = inspect.currentframe().f_back
            (filename, line_number,
             function_name, lines, index) = inspect.getframeinfo(previous_frame)
            audit = {
                "auditID": generate_error_id(),
                "methodName": function_name,
                "fileName": filename,
                "lineNo": line_number,
                "message": str(message),
                "timeStamp": eval(str(time.time()).replace('.', '')),
                "auditType": "ERROR"
            }
            audit_enriched = enrich_entity_details(audit, entity)
            if audit_enriched is not None:
                audit = audit_enriched
            if exc is not None:
                audit["cause"] = str(exc)
            index_audit_to_es(audit)
        except Exception as e:
            log.exception("Anuvaad Auditor ERROR failed.", e)
            return None

# Enriches the audit object with entity related data
def enrich_entity_details(audit, entity):
    try:
        if entity is not None:
            if 'jobID' in entity.keys():
                audit["entityID"] = entity["jobID"]
            else:
                audit["entityID"] = "JOB-ID-NA"
            if 'taskID' in entity.keys():
                audit["taskID"] = entity["taskID"]
            else:
                audit["taskID"] = "TASK-ID-NA"
            if 'metadata' in entity.keys():
                metadata = entity["metadata"]
                if 'sessionID' in metadata.keys():
                    audit["sessionID"] = metadata["sessionID"]
                else:
                    audit["sessionID"] = "SE-ID-NA"
                if 'userID' in metadata.keys():
                    audit["userID"] = metadata["userID"]
                else:
                    audit["userID"] = "USR-ID-NA"
                if 'module' in metadata.keys():
                    audit["module"] = metadata["module"]
                else:
                    audit["module"] = "MOD-NA"
            else:
                audit["sessionID"] = "SE-ID-NA"
                audit["userID"] = "USR-ID-NA"
                audit["module"] = "MOD-NA"
        return audit
    except Exception as e:
        log.exception("Exception while enriching with entity!", e)
        return None


# Audit ID generator
def generate_error_id():
    return str(uuid.uuid4())
