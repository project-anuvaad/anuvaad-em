import logging
import time
import uuid

from .eswrapper import index_audit_to_es

log = logging.getLogger('file')

# Method to log and index INFO level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
def log_info(method, message, entity_id):
    log.info(message)
    try:
        audit = {
            "auditID": generate_error_id(),
            "method_name": method,
            "message": message,
            "timeStamp": eval(str(time.time()).replace('.', '')),
            "auditType": "INFO"
        }
        if entity_id is None:
            audit["corelationId"] = "CO-ID-NA"
        else:
            audit["corelationId"] = entity_id
        index_audit_to_es(audit)
    except Exception as e:
        log.exception("Anuvaad Auditor INFO failed.")
        return None


# Method to log and index DEBUG level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
def log_debug(method, message, entity_id):
    log.debug(message)
    try:
        audit = {
            "auditID": generate_error_id(),
            "method_name": method,
            "message": message,
            "timeStamp": eval(str(time.time()).replace('.', '')),
            "auditType": "DEBUG"
        }
        if entity_id is None:
            audit["corelationId"] = "CO-ID-NA"
        else:
            audit["corelationId"] = entity_id
        index_audit_to_es(audit)
    except Exception as e:
        log.exception("Anuvaad Auditor DEBUG failed.")
        return None



# Method to log and index EXCEPTION level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
# exc: Exception object
def log_exception(method, message, entity_id, exc):
    log.exception(message)
    try:

        audit = {
            "auditID": generate_error_id(),
            "method_name": method,
            "message": message,
            "timeStamp": eval(str(time.time()).replace('.', '')),
            "auditType": "EXCEPTION"
        }
        if entity_id is None:
            audit["corelationId"] = "CO-ID-NA"
        else:
            audit["corelationId"] = entity_id
        if exc is not None:
            audit["cause"] = str(exc)
        index_audit_to_es(audit)
    except Exception as e:
        log.exception("Anuvaad Auditor EXCEPTION failed.")
        return None



# Method to log and index EXCEPTION level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
# exc: Exception object
def log_error(method, message, entity_id, exc):
    log.error(message)
    try:
        audit = {
            "auditID": generate_error_id(),
            "method_name": method,
            "message": message,
            "timeStamp": eval(str(time.time()).replace('.', '')),
            "auditType": "ERROR"
        }
        if entity_id is None:
            audit["corelationId"] = "CO-ID-NA"
        else:
            audit["corelationId"] = entity_id
        if exc is not None:
            audit["cause"] = str(exc)
        index_audit_to_es(audit)
    except Exception as e:
        log.exception("Anuvaad Auditor ERROR failed.")
        return None


# Audit ID generator
def generate_error_id():
    return str(uuid.uuid4())
