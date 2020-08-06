import logging
import time
import uuid

from .eswrapper import index_audit_to_es

log = logging.getLogger('file')

# Method to log and index INFO level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
def log_info(message, entity_id):
    log.info(message)
    audit = {
        "auditID": generate_error_id(),
        "corelationId": entity_id,
        "message": message,
        "timeStamp": eval(str(time.time()).replace('.', '')),
        "auditType": "INFO"
    }
    index_audit_to_es(audit)


# Method to log and index DEBUG level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
def log_debug(message, entity_id):
    log.debug(message)
    audit = {
        "auditID": generate_error_id(),
        "corelationId": entity_id,
        "message": message,
        "timeStamp": eval(str(time.time()).replace('.', '')),
        "auditType": "DEBUG"
    }
    index_audit_to_es(audit)


# Method to log and index EXCEPTION level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
# exc: Exception object
def log_exception(message, entity_id, exc):
    log.exception(message)
    audit = {
        "auditID": generate_error_id(),
        "corelationId": entity_id,
        "message": message,
        "timeStamp": eval(str(time.time()).replace('.', '')),
        "auditType": "EXCEPTION"
    }
    if exc is not None:
        audit["cause"] = str(exc)

    index_audit_to_es(audit)


# Method to log and index EXCEPTION level logs
# message: The message to be logged
# entity_id: Any ID that can be used for co-relation. jobID in case of wf, unique Ids in case of normal flow.
# exc: Exception object
def log_error(message, entity_id, exc):
    log.error(message)
    audit = {
        "auditID": generate_error_id(),
        "corelationId": entity_id,
        "message": message,
        "timeStamp": eval(str(time.time()).replace('.', '')),
        "auditType": "ERROR"
    }
    if exc is not None:
        audit["cause"] = str(exc)

    index_audit_to_es(audit)


# Audit ID generator
def generate_error_id():
    return str(uuid.uuid4())
