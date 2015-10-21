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
    return r.create_response(message="Hello Welcome to My Recipes!")


@VoiceHandler(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return r.create_response(message="Goodbye!")


@VoiceHandler(intent='GetRecipeIntent')
def get_recipe_intent_handler(request):

    ingredient = request.get_slot("Ingredient")
    ingredient = ingredient if ingredient else ""
    card = r.create_card(title="CallDadIntent Activated",
                         subtitle=None,
                         content="used echo to call dad on {}"
                         .format(ingredient))
    
    return response_builder.create_response(message="Calling dad now...",
                                            end_session=False,
                                            card_obj=card)


@VoiceHandler(intent="NextRecipeIntent")
def call_back_intent_handler(request):
    return r.create_response(message="Getting Next Recipe")
