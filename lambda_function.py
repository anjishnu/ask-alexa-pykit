from __future__ import print_function
import json
from collections import defaultdict 
from alexa.ask.utils import Request, initialize_handlers
import voice_handlers
from config.config import INTENT_SCHEMA, NON_INTENT_REQUESTS

"""
The REGISTERED_HANDLERS global variable contains a python dict 
which contains mappings from the intent name to the handler
e.g. 
handler = REGISTERED_HANDLERS["IntentRequest"][INTENT_NAME]
gives you the appropriate handler.
"""    

REGISTERED_HANDLERS = initialize_handlers(voice_handlers,
                                          INTENT_SCHEMA,
                                          NON_INTENT_REQUESTS)

def lambda_handler(request_json, context):
    """
    This code routes requests to the appropriate handler
    request_json : This is the json received by the alexa skill
    context : event metadata provided by Amazon Web Services Lambda
    """
    request = Request(request_json)
    voice_handler = REGISTERED_HANDLERS[request.request_type()]
    if request.intent_name() in voice_handler:
        voice_handler = voice_handler[request.intent_name()]
    else:
        voice_handler = voice_handlers.default_handler
    return voice_handler(request)
