# ANUVAAD AUDITOR

A python package that has been implemented to abstract out and standardize the process of logging and error handling for the anuvaad dataflow pipeline. This also serves as a service that enables features like Session tracing, Job tracing, Error debugging and troubleshoot features for the pipeline. The library has two parts to it:
1. Logging/Auditing.
2. Error Handling.

## Prerequisites
- python 3.7
- ubuntu 16.04

INSTALLATION:
```bash
pip install anuvaad-auditor==0.1.1
```
Versions Available:
```bash
anuvaad-auditor==0.1.1
anuvaad-auditor==0.1.0
anuvaad-auditor==0.0.7
anuvaad-auditor==0.0.3
```

## Logging/Auditing.
```bash
log_info(<str(message)>, <json(input object)>):
```
This function has to be used at places where the service wants to log INFO level information. The message to be logged and the input received from WFM either through Kafka or REST has to be passed as parameters as shown.

```bash
log_debug(<str(message)>, <json(input object)>):
```
This function has to be used at places where the service wants to log DEBUGlevel information. The message to be logged and the input received from WFM either through Kafka or REST has to be passed as parameters as shown.

```bash
log_error(<str(error_message)>, <json(input object)>, <exception_object>):
```
This function has to be used at places where the service wants to log ERROR level information. The message to be logged and the input received from WFM either through Kafka or REST has to be passed as parameters as shown. In case this method is called within an exception context in order to register a logical error, the exception object has to be passed.

```bash
log_exception(<str(exception_message)>, <json(input object)>, <exception_object>):
```
This function has to be used at places where the service wants to log EXCEPTIONlevel information. The message to be logged and the input received from WFM either through Kafka or REST has to be passed as parameters as shown. This should always be called within an exception context and the exception object has to be passed.
The difference between log_error and log_exception is that log_error should be used for logical errors like “File is not valid”, “File format not accepted” etc. Whereas, log_exception should be used in case of exceptions like “TypeError”, “KeyError” etc.

## Error Handling.
```bash
post_error(<str(error_code)>, <str(error_msg)>, <exception_object>):
```
This method returns a standard error object that can be used to reply back to the client during a SYNC call. The error at the same time is also indexed to an error index. This function should ideally be used when:
a. During a SYNC call, which means when the request comes directly from UI.

```bash
post_error_wf(<str(error_code)>, <str(error_msg)>, <json(input-obj)>, <exception_object>):
```
This method constructs a standard error object which will be indexed to a different error index and at the same time PUSHES THE ERROR TO WFM internally. This means, at any point due to a logical error or an exception if the module needs to inform WFM of the error, the module should use this function. 
So, for any flow that is triggered via kafka or REST through WFM, please use this function only. WFM is dependent on this function to understand if the job has failed somewhere downstream and acts accordingly.
The modules will construct and push the objects only in case of successful job completion, in any case of failure just use this method and avoid pushing custom error objects to the output topic.


## License
[MIT](https://choosealicense.com/licenses/mit/)
