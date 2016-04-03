import os
from collections import OrderedDict, defaultdict
import json
import pkgutil
import inspect

RAW_RESPONSE = """
{
    "version": "1.0",
    "response": {
        "outputSpeech": {
            "type": "PlainText",
            "text": "Some default text goes here."
                },
        "shouldEndSession": False
    }
}"""



class Request(object):
    """
    Simple wrapper around the JSON request
    received by the module
    """
    def __init__(self, request_dict, metadata=None):
        self.request = request_dict
        self.metadata = metadata or {}
        self.session = self.request.get('session',{}).get('attributes',{})     
        if self.intent_name():
            self.slots = self.get_slot_map()

    def request_type(self):
        return self.request["request"]["type"]

    def intent_name(self):
        if not "intent" in self.request["request"]:
            return None
        return self.request["request"]["intent"]["name"]

    def is_intent(self):
        if self.intent_name() == None:
            return False
        return True

    def user_id(self):
        return self.request["session"]["user"]["userId"]

    def access_token(self):
        try:
            return self.request['session']['user']['accessToken']
        except:
             return None

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

    def get_slot_map(self):
        return {slot_name : self.get_slot_value(slot_name) for slot_name in self.get_slot_names()}


class ResponseBuilder(object):
    """
    Simple class to help users to build responses
    """
    base_response = eval(RAW_RESPONSE)

    @classmethod
    def create_response(self, message=None, end_session=False, card_obj=None,
                        reprompt_message=None, is_ssml=None):
        """
        message - text message to be spoken out by the Echo
        end_session - flag to determine whether this interaction should end the session
        card_obj = JSON card object to substitute the 'card' field in the raw_response
        """
        response = dict(self.base_response)
        if message:
            response['response'] = self.create_speech(message, is_ssml)
        response['response']['shouldEndSession'] = end_session
        if card_obj:
            response['response']['card'] = card_obj
        if reprompt_message:
            response['response']['reprompt'] = self.create_speech(reprompt_message, is_ssml)
        return response

    @classmethod
    def create_speech(self, message=None, is_ssml=False):
        data = {}
        if is_ssml:
            data['type'] = "SSML"
            data['ssml'] = message
        else:
            data['type'] = "PlainText"
            data['text'] = message
        return {"outputSpeech" : data }

    @classmethod
    def create_card(self, title=None, subtitle=None, content=None, card_type="Simple"):
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
        card = {"type": card_type}
        if title: card["title"] = title
        if subtitle: card["subtitle"] = subtitle
        if content: card["content"] = content
        return card


class VoiceHandler(ResponseBuilder):
    """    Decorator to store function metadata
    Functions that are annotated with this label are
    treated as voice handlers """

    def __init__(self):
        self._handlers = { "IntentRequest" : {} }
        self._default = '_default_'

        
    def default_handler(self):
        ''' Decorator to register default handler '''

        def _handler(func):
            self._handlers[self._default] = func

        return _handler

    
    def intent_handler(self, intent):
        ''' Decorator to register intent handler'''

        def _handler(func):
            self._handlers['IntentRequest'][intent] = func

        return _handler


    def request_handler(self, request_type):
        ''' Decorator to register generic request handler '''

        def _handler(func):
            self._handlers[request_type] = func

        return _handler


    def route_request(self, request_json, metadata=None):
        ''' Route the request object to the right handler function '''
        request = Request(request_json)
        request.metadata = metadata        
        handler_fn = self._handlers[self._default] # Set default handling for noisy requests

        if not request.is_intent() and (request.request_type() in self._handlers):
            '''  Route request to a non intent handler '''
            handler_fn = self._handlers[request.request_type()]

        elif request.is_intent() and request.intent_name() in self._handlers['IntentRequest']:
            ''' Route to right intent handler '''
            handler_fn = self._handlers['IntentRequest'][request.intent_name()]

        response = handler_fn(request)
        response['sessionAttributes'] = request.session
        return response
