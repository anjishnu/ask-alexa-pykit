import os
from collections import OrderedDict
import json

RAW_RESPONSE = """
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
    """
    Decorator to store function metadata
    """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, function):
        function.voice_handler = self.kwargs
        return function

    
class Request(object):
    """
    Simple wrapper around the JSON request
    received by the module
    """    
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

    def get_slot_map(self):
        return {slot_name : request.get_slot_value(slot_name) for slot_name in self.get_slot_names}

    
class ResponseBuilder(object):
    """
    Simple class to help users to build responses
    """
    base_response = eval(RAW_RESPONSE)
        
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

    def set_response_text(self, response_text):
        self.response_text = response_text

    def set_card_info(self, card_info):
        raise NotImplementedError


class VoiceQueue(object):
    """
    Encapsulates voice interaction metadata for a single user
    """
    def __init__(self, raw_queue = []):
        self.queue = raw_queue[::-1]
        self.prev = None

    def is_empty(self):
        return True if self.queue else False

    def next_response(self):
        self.prev = self.queue.pop()
        return self.prev

    def previous_response(self):
        return self.prev

    def extend(self, text_lst):
        self.queue = text_lst[::-1].extend(self.queue)

    def append(self, text):
        self.queue = [text] + self.queue


class VoiceCache(object):
    """
    Dictionary like cache to encapsulate retrieval of voice
    interaction metadata for all users
    Over time this can evolve under the hood to become more like LRU 
    with some kind of filesystem backing. 
    """
    def __init__(self):
        self.queues = defaultdict(lambda : NextQueue())

    def __setitem__(self, key, item):
        self.queues[key] = NextQueue(item)

    def __getitem__(self, key):
        return self.queues[key]

    def __repr__(self):
        return repr(self.queues)

    def __len__(self):
        return len(self.queues)

    def __delitem__(self, key):
        del self.queues[key]

    def clear(self):
        return self.queues.clear()
