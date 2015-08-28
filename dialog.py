import json
from collections import defaultdict as ddict
from lib.dialog_utilities import RequestHandler, SimpleIntentHandler, Request

DEFAULT_INTENT_SCHEMA_LOCATION = "config/intent_schema.json"
NON_INTENT_REQUESTS = ["LaunchRequest", "SessionEndedRequest"]

def load_intent_schema(schema_location = DEFAULT_INTENT_SCHEMA_LOCATION):
    with open(schema_location, 'r') as intentfile:
                return json.load(intentfile)

            
def set_up_handlers_for_intents():
    """
    Sets up handlers for intents based on an intent schema
    """
    handler_for_intent = {}
    intent_schema = load_intent_schema()
    for intent in intent_schema["intents"]:
        intent_name = intent["intent"]
        slots = {slot["name"] for slot in intent["slots"]}        
        intent_handler = SimpleIntentHandler(intent_name=intent_name,
                                             response_text="Hello World!",
                                             slots=slots)
        handler_for_intent[intent_name] = intent_handler
    return handler_for_intent


def set_up_handlers():
    handlers_map = {}
    handlers_map["IntentRequest"] = set_up_handlers_for_intents()
    #Handlers for LaunchAppRequest and SessionEndedRequest
    for request_type in NON_INTENT_REQUESTS:
        handlers_map[request_type] = RequestHandler(request_type=request_type,
                                                    response_text = "Just ask.")
    return handlers_map


def update_handlers(all_handlers):
    """
    # This is an example of how modify intent handlers

    #This gives you access to the handler for ExitIntent
    handler = all_handlers["IntentRequest"]["ExitIntent"]    

    #This changes the message of the handler!
    handler.set_message("Goodbye")
    
    # This sets the voice response of alexa to "GoodBye" whenever it sees an "ExitIntent"    
    return handler_for_intent
    """
    return all_handlers


"""
The HANDLERS global variable contains a python dict 
which contains mappings from the intent name to the handler
e.g. 
handler = HANDLERS["IntentRequest"][INTENT_NAME]
gives you the appropriate handler.
"""    

HANDLERS = set_up_handlers()


def route_intent(request_json):
    """
    This code routes requests to the appropriate handler
    """
    request = Request(request_json)    
    handler = HANDLERS[request.request_type()]
    if request.intent_name():
        handler = handler[request.intent_name()]
    return handler.get_response(request)

