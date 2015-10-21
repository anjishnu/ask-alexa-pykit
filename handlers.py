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
    return r.create_response(message="Hello world!")


@VoiceHandler(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return r.create_response(message="Goodbye!")


@VoiceHandler(intent='CallDadIntent')
def call_dad_intent_handler(request):

    phone_number = request.get_slot_value('PhoneNo')
    phone_number = phone_number if phone_number else "NULL"    

    card = r.create_card(title="CallDadIntent Activated",
                         subtitle=None,
                         content="used echo to call dad on {phone_no}"
                         .format(str(phone_number)))
    
    return response_builder.create_response(message="Calling dad now...",
                                            end_session=False,
                                            card_obj=card)


@VoiceHandler(intent="CallBack")
def call_back_intent_handler(r):
    return r.create_response(message="Initiating CallBack")
