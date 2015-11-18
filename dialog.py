from __future__ import print_function
import json
from collections import defaultdict 
from lib.dialog_utils import Request
import pkgutil
import voice_handlers
import inspect
from config.config import INTENT_SCHEMA, NON_INTENT_REQUESTS


            
def initialize_handlers():
    """
    Automatically populate function handlers from the handlers
    """
    # If no handler is specified, backoff to default handler 
    init_default_handler = lambda : voice_handlers.default_handler
    all_handlers_map = defaultdict(init_default_handler)
    intent_handlers_map = defaultdict(init_default_handler)
    
    # Load intent schema to verify that handlers are mapped to valid intents
    all_intents = {intent["intent"] : { slot["name"] : slot["type"] for slot in intent['slots'] }
                   for intent in INTENT_SCHEMA['intents'] }

    #Loaded functions in the handlers module
    member_functions = inspect.getmembers(voice_handlers, inspect.isfunction)

    for (name, function) in member_functions:
        if hasattr(function, 'voice_handler'): #Function has been decorated as a voice_handler
            if 'request_type' in function.voice_handler:
                if function.voice_handler['request_type'] in NON_INTENT_REQUESTS: 
                    # Function is a valid request voice handler
                    all_handlers_map[function.voice_handler['request_type']] = function                    

            elif 'intent' in function.voice_handler:
                if function.voice_handler['intent'] in all_intents:
                    # Function is a valid intent voice handler
                    intent_handlers_map[function.voice_handler['intent']] = function 

    all_handlers_map['IntentRequest'] = intent_handlers_map                
    return all_handlers_map


"""
The REGISTERED_HANDLERS global variable contains a python dict 
which contains mappings from the intent name to the handler
e.g. 
handler = REGISTERED_HANDLERS["IntentRequest"][INTENT_NAME]
gives you the appropriate handler.
"""    

REGISTERED_HANDLERS = initialize_handlers()


def route_intent(request_json):
    """
    This code routes requests to the appropriate handler
    """
    request = Request(request_json)    
    voice_handler = REGISTERED_HANDLERS[request.request_type()]
    if request.intent_name():
        voice_handler = voice_handler[request.intent_name()]
    return voice_handler(request)
