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
    for request_type in NON_INTENT_REQUESTS:
        handlers_map[request_type] = RequestHandler(request_type=request_type,
                                                    response_text = "Just ask.")
    return handlers_map

def update_handlers(handlers):
    """
    # This is an example of how modify intent handlers

    #This gives you access to the handler for ExitIntent
    handler = handler_for_intent["IntentRequest"]["ExitIntent"]    

    #This changes the message of the handler!
    handler.set_message("Goodbye")
    
    # This sets the voice response of alexa to "GoodBye" whenever it sees an "ExitIntent"    
    return handler_for_intent
    """
    return handlers


"""
The HANDLER_FOR_INTENT variable contains a python dict 
which contains mappings from the intent name to the handler
e.g. 
handler = HANDLERS["IntentRequest"][INTENT_NAME]
gives you the appropriate handler
"""    

HANDLERS = set_up_handlers()

def route_intent(intent):
    """
    This code routes 
    """
    request = Request(intent)    
    if request.intent_name():
        handler = HANDLERS[request.request_type()][request.intent_name()]
    else:
        handler = HANDLERS[request.request_type()]
    return handler.get_response(request)

