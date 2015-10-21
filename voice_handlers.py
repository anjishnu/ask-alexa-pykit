from lib.dialog_utils import VoiceHandler, ResponseBuilder
"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015

Each VoiceHandler function receives a ResponseBuilder object as input and outputs a Response object 
A response object is defined as the output of ResponseBuilder.create_response()
"""

r = ResponseBuilder()

def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return r.create_response(message="Just ask")


@VoiceHandler(request_type="LaunchRequest")
def launch_request_handler(request):
    """
    Annoatate functions with @VoiceHandler so that they can be automatically mapped 
    to request types.
    Use the 'request_type' field to map them to non-intent requests
    """
    return r.create_response(message="Hello Welcome to My Recipes!")


@VoiceHandler(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return r.create_response(message="Goodbye!")


@VoiceHandler(intent='GetRecipeIntent')
def get_recipe_intent_handler(request):
    """
    Use the 'intent' field in the VoiceHandler to map to the respective intent.
    You can insert arbitrary business logic code here    
    """

    # Get variables like userId, slots, intent name etc from the 'Request' object
    ingredient = request.get_slot_value("Ingredient") 
    ingredient = ingredient if ingredient else ""

    #Use ResponseBuilder object to build responses and UI cards
    card = r.create_card(title="GetRecipeIntent activated",
                         subtitle=None,
                         content="asked alexa to find a recipe using {}"
                         .format(ingredient))
    
    return r.create_response(message="Finding a recipe with the ingredient {}".format(ingredient),
                             end_session=False,
                             card_obj=card)


@VoiceHandler(intent="NextRecipeIntent")
def call_back_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    return r.create_response(message="Getting Next Recipe ...")
