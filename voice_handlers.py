from alexa.ask import voice, Request, ResponseBuilder as r

"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015

Each VoiceHandler function receives a Request object as input and outputs a Response object 
A response object is defined as the output of ResponseBuilder.create_response()
"""


def lambda_function(request_obj, context={}):

    '''      
    This is the main function to enter to enter into this code. 
    If you are hosting this code on AWS Lambda, this should be the entry point. 
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.        
    '''

    request = Request(request_obj)

    ''' inject user relevant metadata into the request if you want to, here.
    
    e.g. Something like : 
    ... request.meta_data['user_name'] = some_database.query_user_name(request.get_user_id()) 
    
    Then in the handler function you can do something like -
    ... return r.create_response('Hello there {}!'.format(request.meta_data['user_name']))
    '''    
    return voice.route_request(request)

    
@voice.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return r.create_response(message="Just ask")


@voice.request_handler("LaunchRequest")
def launch_request_handler(request):
    """
    Annoatate functions with @VoiceHandler so that they can be automatically mapped 
    to request types.
    Use the 'request_type' field to map them to non-intent requests
    """
    return r.create_response(message="Hello Welcome to My Recipes!")


@voice.request_handler(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return r.create_response(message="Goodbye!")


@voice.intent_handler(intent='GetRecipeIntent')
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



@voice.intent_handler(intent="NextRecipeIntent")
def next_recipe_intent_handler(request):
    """
    You can insert arbitrary business logic code here
    """
    return r.create_response(message="Getting Next Recipe ... 123")
