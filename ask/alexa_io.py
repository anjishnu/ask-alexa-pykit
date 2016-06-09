import json

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
        self.session = self.request.get('session', {}).get('attributes', {})
        if self.intent_name():
            self.slots = self.get_slot_map()

    def request_type(self):
        return self.request["request"]["type"]

    def intent_name(self):
        if "intent" not in self.request["request"]:
            return None
        return self.request["request"]["intent"]["name"]

    def is_intent(self):
        if self.intent_name() is None:
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
        return {slot_name: self.get_slot_value(slot_name)
                for slot_name in self.get_slot_names()}


class Response(object):
    def __init__(self, json_obj):
        self.json_obj = json_obj

    def __repr__(self):
        return json.dumps(self.json_obj, indent=4)

    def with_card(self, title, content, subtitle, card_type='Simple'):
        new_obj = dict(self.json_obj)
        new_obj['response']['card'] = ResponseBuilder.create_card(title, content,
                                                                        subtitle, card_type)
        return Response(new_obj)

    def with_reprompt(self, message, is_ssml):
        new_obj = dict(self.json_obj)
        new_obj['response']['reprompt'] = ResponseBuilder.create_speech(message, is_ssml)
        return Response(new_obj)

    def set_session(self, session_attr):
        self.json_obj['sessionAttributes'] = session_attr

    def to_json(self):
        return dict(self.json_obj)


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
        return Response(response)

    @classmethod
    def respond(self, *args, **kwargs):
        return self.create_response(*args, **kwargs)

    @classmethod
    def create_speech(self, message=None, is_ssml=False):
        data = {}
        if is_ssml:
            data['type'], data['ssml'] = "SSML", message
        else:
            data['type'] = "PlainText"
            data['text'] = message
        return {"outputSpeech": data}

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
        """
        >>> alexa = VoiceHandler()
        >>> request =
        >>> @alexa.intent('HelloWorldIntent')
        ... def hello_world(request):
        ...   return alexa.create_response('hello world')
        >>> alexa.route_request(request)
        """
        self._handlers = { "IntentRequest" : {} }
        self._default = '_default_'

    def default(self, func):
        ''' Decorator to register default handler '''

        self._handlers[self._default] = func

        return func

    def intent(self, intent):
        ''' Decorator to register intent handler'''

        def _handler(func):
            self._handlers['IntentRequest'][intent] = func
            return func

        return _handler

    def request(self, request_type):
        ''' Decorator to register generic request handler '''

        def _handler(func):
            self._handlers[request_type] = func
            return func

        return _handler

    def route_request(self, request_json, metadata=None):

        ''' Route the request object to the right handler function '''
        request = Request(request_json)
        request.metadata = metadata
        # add reprompt handler or some such for default?
        handler_fn = self._handlers[self._default] # Set default handling for noisy requests

        if not request.is_intent() and (request.request_type() in self._handlers):
            '''  Route request to a non intent handler '''
            handler_fn = self._handlers[request.request_type()]

        elif request.is_intent() and request.intent_name() in self._handlers['IntentRequest']:
            ''' Route to right intent handler '''
            handler_fn = self._handlers['IntentRequest'][request.intent_name()]

        response = handler_fn(request)
        response.set_session(request.session)
        return response.to_json()
