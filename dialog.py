import json
from collections import defaultdict as ddict


"""
REQUEST BODY SYNTAX:
{
"session": {
        "new": true,
        "user": {
            "userId": "amzn1.account.AGBATYSC32Y2QVDQKOWJUUJNEYFA"
        },
        "sessionId": "amzn1.echo-api.session.9ac857e7-6d4b-402a-be34-fc8f76057379"
    },
    "version": "1.0",
    "request": {
        "requestId": "amzn1.echo-api.request.4b79477a-5097-4a10-9d6f-bec24f9d92f1",
        "type": "LaunchRequest"
    }
}
"""

raw_response = """{
    "version": "1.0",
    "response": {
        "outputSpeech": {
            "type": "PlainText",
            "text": "Welcome to your recipes. I am ready to serve."
                },
        "card": {
            "type": "Simple",
            "title": "string",
            "subtitle": "string",
            "content": "string"
        }
        "shouldEndSession": False
    }
}"""


def create_response(message=None, end_session=False, card_obj=None):
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
    response = json.loads(raw_response)
    if message:
        response['response']['outputSpeech']['text'] = message
    response['response']['shouldEndSession'] = end_session
    if card_obj:
        
    return response

request_type_of  = lambda r : r['request']['type']
intent_name_of = lambda r : r['request']['intent']['name']
userId_of  = lambda r : r["session"]['user']['userId']

dialog_cache = ddict(lambda : ddict(list))

def route_intent(intent):
    if req_of(intent)=="LaunchRequest":
        return create_response()

    if req_of(intent)=="IntentRequest":

        if type_of(intent)=="FindRecipe":
            return find_recipe(intent)

        if type_of(intent)=="AddIngredient":
            return add_ingredient(intent)            
        
        if type_of(intent)=="ChooseRecipe":
            return choose_recipe(intent)

    return ""

