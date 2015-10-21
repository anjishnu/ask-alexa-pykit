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

class VoiceHandler(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, f):
        f.voice_handler = self.kwargs
        return f

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
        try:
            return self.request["request"]["intent"]["slots"][slot_name]["value"]
        except:
            """Value not found"""
            return None

    def get_slot_names(self):
        try:
            return self.request['request']['intent']['slots'].keys()
        except:            
            return []
        
class ResponseBuilder(object):
    """
    This is a generic superclass to handle basic json operations for all response constructions
    """
    base_response = eval(raw_response)
    
    def __init__(self, request):
        self.request = request
        self.request_type = request.request_type()
    
    def create_response(self, message=None, end_session=False, card_obj=None):
        """
        message - text message to be spoken out by the Echo
        end_session - flag to determine whether this interaction should end the session
        card_obj = JSON card object to substitute the 'card' field in the raw_response
        """
        response = self.base_response
        if message:
            response['response']['outputSpeech']['text'] = message
        response['response']['shouldEndSession'] = end_session
        if card_obj:
            response['response']['card'] = card_obj
        return response

    def create_card(self, title=None, subtitle=None, content=None):
        """
        card_obj = JSON card object to substitute the 'card' field in the raw_response
        format: 
        {
          "type": "Simple", #COMPULSORY
          "title": "string", #OPTIONAL
          "subtitle": "string", #OPTIONAL
          "content": "string" #OPTIONAL
        }
        """
        card = {"type":"Simple"}
        if title: card["title"] = title
        if subtitle: card["subtitle"] = subtitle
        if content: card["content"] = content
        return card

    def set_response_text(self, response_text):
        self.response_text = response_text

    def set_card_info(self, card_info):
        raise NotImplementedError

    
class IntentResponseBuilder(ResponseBuilder):
    """ This class responds to an intent given a response """
    def __init__(self, request):
        self.request = request
        self.request_type = request.request_type()
        self.intent = request.intent_name()
        self.slots = request.get_slot_names()
        
    def get_slot_map(self, request):
        """"Utility function that returns a dictionary mapping slot type to its value for this intent """
        return {slot_name : request.get_slot_value(slot_name) for slot_name in self.slots}
    
