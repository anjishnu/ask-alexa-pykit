"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking! 
"""

from ask import alexa
import useful_science

def lambda_handler(request_obj, context={}):
    ''' All requests start here '''    
    return alexa.route_request(request_obj)

@alexa.default
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask")


@alexa.request("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="Welcome to Useful Science. We summarize complicated "
                                 "scientific publications in easy to understand forms!",
                                 reprompt_message='What would you like to know more about? '
                                 'You can ask for the latest posts or posts about a particular topic')


@alexa.request(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")

@alexa.intent('GetPosts')
def get_posts_intent_handler(request):    

    def resolve_slots(text):
        if text in useful_science.categories:
            return text        
        return 'new'
    
    category_text = request.slots['Category']
    category = resolve_slots(category_text)
    post = useful_science.post_cache.get_post(category)

    card_content = "{0} Link: {1}".format(post['summary'],
                                          post['permalink'])

    card = alexa.create_card(title=post['meta_title'],
                             subtitle=post['categories'],
                             content=card_content)
    
    return alexa.create_response(message=post['summary'],
                                 end_session=True,
                                 card_obj=card)


@alexa.intent('AMAZON.HelpIntent')
def help_intent_handler(request):
    cat_list = [cat for cat in useful_science.categories]
    pre = cat_list[:-1]
    post = cat_list[-1:]
    formatted = " ".join(map(lambda x : x+",", pre) + ['and'] + post)
    message = ["You can ask for posts in the following categories - ",
               formatted]          
    return alexa.create_response(message=' '.join(message))

                                 
@alexa.intent('AMAZON.StopIntent')
def stop_intent_handler(request):
    return alexa.create_response(message="Goodbye!")
