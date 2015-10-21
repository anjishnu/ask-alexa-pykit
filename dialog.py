import json
from collections import defaultdict 
from lib.dialog_utils import ResponseBuilder, IntentResponseBuilder, Request
import pkgutil
import handlers
import inspect

DEFAULT_INTENT_SCHEMA_LOCATION = "config/intent_schema.json"
NON_INTENT_REQUESTS = ["LaunchRequest", "SessionEndedRequest"]

def load_intent_schema(schema_location = DEFAULT_INTENT_SCHEMA_LOCATION):
    with open(schema_location, 'r') as intentfile:
                return json.load(intentfile)

            
def set_up_handlers():
    #If no handler is specified, backoff to default handler 
    init_default_handler = lambda : handlers.default_handler
    all_handlers_map = defaultdict(init_default_handler)
    intent_handlers_map = defaultdict(init_default_handler)

    #Loading intent schema 
    intent_schema = load_intent_schema()
    all_intents = {intent["intent"] : { slot["name"] : slot["type"] for slot in intent['slots'] }
                   for intent in intent_schema['intents'] }

    print (json.dumps(all_intents, indent=4))    

    member_functions = inspect.getmembers(module, inspect.isfunction)

    for (name, function) in member_functions:
        if hasattr(function, 'voice_handler'): #Function has been decorated as a voice_handler

            if 'request_type' in function.voice_handler:
                if function.voice_handler['request_type'] in NON_INTENT_REQUESTS: 
                    all_handlers_map[f.voice_handler['request_type']] = function
                    
            elif 'intent' in function.voice_handler:
                if function.voice_handler['intent'] in all_intents:
                    intent_handler_map[function.voice_handler['intent']] = function 

    # Attach intent handler to main handlers map
    all_handlers_map['IntentRequest'] = intent_handlers_map                
    return all_handlers_map


"""
The HANDLERS global variable contains a python dict 
which contains mappings from the intent name to the handler
e.g. 
handler = HANDLERS["IntentRequest"][INTENT_NAME]
gives you the appropriate handler.
"""    

REGISTERED_HANDLERS = initialize_handlers()


def route_intent(request_json):
    """
    This code routes requests to the appropriate handler
    """
    request = Request(request_json)    
    handler = REGISTERED_HANDLERS[request.request_type()]
    if request.intent_name():
        handler = handler[request.intent_name()]
    return handler.get_response(request)

