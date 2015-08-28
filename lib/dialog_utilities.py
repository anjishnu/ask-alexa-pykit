import os
from collections import OrderedDict
import json

raw_response = """
{
    "version": "1.0",
    "response": {
        "outputSpeech": {
            "type": "PlainText",
            "text": "Welcome to your recipes. I am ready to serve."
                },
        "shouldEndSession": False
    }
}"""


class Request(object):
    def __init__(self, request_dict):
        self.request = request_dict
        
    def request_type(self):
        return self.request["request"]["type"]

    def intent_name(self):
        if not "intent" in self.request["request"]:
            return None
        return self.request["request"]["intent"]["name"]

    def user_id(self):
        return self.request["session"]["user"]["userId"]

    def session_id(self):
        return self.request["session"]["sessionId"]

    def get_slot_value(self, slot_name):
        return self.request["request"]["intent"]["slots"][slot_name]["value"]

    
class RequestHandler(object):
    """
    This is a generic superclass to handle basic json operations for all response constructions
    """
    base_response = eval(raw_response)
    
    def __init__(self, request_type, response_text):
        self.request_type = request_type
        self.response_text = response_text
    
    def get_response(self, request):
        return self._process_request(request)

    def _process_request(self, request):
        """
        This is the function you should overload to 
        do all sorts of processing to generate the artifacts
        that are fed into self.create_response
        """
        return self.create_response(message=self.response_text)
    
    def create_response(self, message=None, end_session=False, card_obj=None):
        """
        message - text message to be spoken out by the Echo
        end_session - flag to determine whether this interaction should end the session
        card_obj = JSON card object to substitute the 'card' field in the raw_response
        format: 
        {
        "type": "Simple", #COMPULSORY
        "title": "string", #OPTIONAL
        "subtitle": "string", #OPTIONAL
        "content": "string" #OPTIONAL
        }
        """
        response = self.base_response
        if message:
            response['response']['outputSpeech']['text'] = message
        response['response']['shouldEndSession'] = end_session
        if card_obj:
            response['response']['card'] = card_obj
        return response

    def create_card(self, title=None, subtitle=None, content=None):
        card = {"type":"Simple"}
        if title: card["title"] = title
        if subtitle: card["subtitle"] = subtitle
        if content: card["content"] = content
        return card

    def set_response_text(self, response_text):
        self.response_text = response_text

    def set_card_info(self, card_info):
        raise NotImplementedError

    
class SimpleIntentHandler(RequestHandler):
    """ This class responds to an intent given a response """
    def __init__(self, intent_name, response_text = "Hello World", slots = []):
        self.request_type = "IntentRequest"
        self.intent = intent_name
        self.response_text = response_text
        self.slots = []
        
    def get_slot_map(self, request):
        return {slot_name : request.get_slot_value(slot_name) for slot_name in self.slots}


    
