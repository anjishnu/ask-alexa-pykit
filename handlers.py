"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015

Each VoiceHandler function receives a ResponseBuilder object as input and outputs a Response object
"""

from lib.dialog_utils import VoiceHandler


@VoiceHandler(request_type="LaunchRequest")
def launch_request_handler(response_builder):
    return response_builder.create_response(message="Hello world!")


@VoiceHandler(request_type="SessionEndedRequest")
def session_ended_request_handler(response_builder):
    return response_builder.create_response(message="Goodbye!")


@VoiceHandler(intent='CallDadIntent')
def call_dad_intent_handler(response_builder):
    request = response_builder.request

    #
    # Insert arbitrary business logic here
    # 

    slots = response_builder.get_slot_map()
    phone_number = slots['PhoneNo']
    card = response_builder.create_card(title="CallDadIntent Activated",
                                        subtitle=None,
                                        content="used echo to call dad on {phone_no}"
                                        .format(str(phone_number)))
    
    return response_builder.create_response(message="Calling dad now...",
                                            end_session=False,
                                            card_obj=card)


@VoiceHandler(intent="CallBack")
def call_back_intent_handler(response_builder):
    return response_builder
