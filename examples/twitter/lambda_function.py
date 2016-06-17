from ask import alexa 
from config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from twitter import local_cache as twitter_cache
from twitter import (post_tweet, get_home_tweets, get_retweets_of_me, 
                     get_my_favourite_tweets, get_my_favourite_tweets, 
                     get_latest_twitter_mentions, search_for_tweets_about,
                     get_user_latest_tweets, get_user_twitter_details,
                     geo_search, closest_trend_search, list_trends)


# Run this code once on startup to load twitter keys into credentials
server_cache_state = twitter_cache.get_server_state()
if 'twitter_keys' not in server_cache_state:
    server_cache_state['twitter_keys'] = (TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)


def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return launch_request_handler(request)


@alexa.request(request_type="LaunchRequest")
def launch_request_handler(request):
    """ Annotate functions with @VoiceHandler so that they can be automatically mapped 
    to request types. Use the 'request_type' field to map them to non-intent requests """

    user_id = request.access_token()
    if user_id in twitter_cache.users():

        user_cache = twitter_cache.get_user_state(user_id)        
        user_cache["amzn_id"]= request.user_id()
        base_message = "Welcome to Twitter, {} . How may I help you today ?".format(user_cache["screen_name"])
        print (user_cache)        
        if 'pending_action' in user_cache:
            base_message += " You have one pending action . "
            print ("Found pending action")
            if 'description' in user_cache['pending_action']:
                print ("Found description")
                base_message += user_cache['pending_action']['description']
        return r.create_response(base_message)

    card = r.create_card(title="Please log into twitter", card_type="LinkAccount")
    return r.create_response(message="Welcome to twitter, looks like you haven't logged in!"
                             " Log in via the alexa app.", card_obj=card,
                             end_session=True)


@alexa.request("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")


@alexa.intent(intent='PostTweet')
def post_tweet_intent_handler(request):
    """
    Use the 'intent' field in the VoiceHandler to map to the respective intent.
    """
    tweet = request.get_slot_value("Tweet")
    tweet = tweet if tweet else ""    
    if tweet:
        user_state = twitter_cache.get_user_state(request.access_token())
        def action():
            return post_tweet(request.access_token(), tweet)

        message = "I am ready to post the tweet, {} ,\n Please say yes to confirm or stop to cancel .".format(tweet)
        user_state['pending_action'] = {"action" : action,
                                        "description" : message} 
        return r.create_response(message=message, end_session=False)
    else:
        # No tweet could be disambiguated
        message = " ".join(
            [
                "I'm sorry, I couldn't understand what you wanted to tweet .",
                "Please prepend the message with either post or tweet ."
            ]
        )
        return alexa.create_response(message=message, end_session=False)


@alexa.intent(intent="SearchTrends")
def find_trends_handler(request):

    uid = request.access_token()
    user_cache = twitter_cache.get_user_state(uid)
    resolved_location = False
    message = ""
    location = request.get_slot_value("Location")
    should_end_session = True

    if not location:
        # Get trends for user's current location
        user_details = get_user_twitter_details(uid)        
        location = user_details[0]['location'] 
        if location:
            message += "Finding trends near you . "
        else:
            message += "I could not figure out where you are, please set it up on your twitter account . "

    if location:

        response = geo_search(request.access_token(), location) # convert natural language text to location
        top_result = response['result']['places'][0]
        lon, lat = top_result['centroid'] 
        trend_params = {"lat" : lat, "long" : lon}
        trend_location = closest_trend_search(request.access_token(), trend_params) # find closest woeid which has trends
        woeid = trend_location[0]['woeid']
        trends = list_trends(request.access_token(), trend_location[0]['woeid']) # List top trends
        trend_lst = [trend['name'] for trend in trends[0]['trends']]
        message += "The top trending topics near {0} are, ".format(trend_location[0]['name'])
        message += "\n".join(["{0}, {1}, ".format(index+1, trend) for index, trend in enumerate(trend_lst)])

    return alexa.create_response(message=message, end_session=should_end_session)


@alexa.intent(intent="AMAZON.HelpIntent")
def help_intent_handler(request):
    msg = ("I can do several things for you on twitter! "
           "I can tell you about the top tweets on your home page, or the last tweets you favourited . "
           "I can also tell you about recent tweets that mention you, or were posted by you . "
           "When I am reading out a list of tweets, you can stop me and ask me to tell you about the tweet in more detail, or ask me to post a reply to it . " 
           "And of course, whenever post a tweet, say 'post hello world' or 'tweet hello world'. I am not good with hashtags or trending topics just yet, but I'm working on it! ")
    return r.create_response(message=msg)


@alexa.intent(intent="AMAZON.StopIntent")
def stop_intent__handler(request):
    return cancel_action_handler(request)


@alexa.intent(intent="AMAZON.CancelIntent")
def cancel_intent_handler(request):
    return cancel_action_handler(request)


MAX_RESPONSE_TWEETS = 3

def tweet_list_handler(request, tweet_list_builder, msg_prefix=""):

    """ This is a generic function to handle any intent that reads out a list of tweets"""
    # tweet_list_builder is a function that takes a unique identifier and returns a list of things to say
    tweets = tweet_list_builder(request.access_token())
    print (len(tweets), 'tweets found')
    if tweets:
        twitter_cache.initialize_user_queue(user_id=request.access_token(),
                                            queue=tweets)
        text_to_read_out = twitter_cache.user_queue(request.access_token()).read_out_next(MAX_RESPONSE_TWEETS)        
        message = msg_prefix + text_to_read_out + ", say 'next' to hear more, or reply to a tweet by number."
        return alexa.create_response(message=message,
                                     end_session=False)
    else:
        return alexa.create_response(message="Sorry, no tweets found, please try something else", 
                                 end_session=False)


@alexa.intent(intent="SearchTweets")
def search_tweets_handler(request):
    search_topic = request.get_slot_value("Topic")
    max_tweets = 3
    if search_topic:
        message = "Searching twitter for tweets about {} . ".format(search_topic)
        def search_tweets_builder(uid):
            params = {
                "q" : search_topic,
                "result_type" : "popular"
            }
            return search_for_tweets_about(request.access_token(), params)           
        return tweet_list_handler(request, tweet_list_builder=search_tweets_builder, msg_prefix=message)
    else:
         return r.create_response("I couldn't find a topic to search for in your request")


@alexa.intent(intent="FindLatestMentions")
def list_mentions_handler(request):
    return tweet_list_handler(request, tweet_list_builder=get_latest_twitter_mentions, msg_prefix="Looking for tweets that mention you.")


@alexa.intent(intent="ListHomeTweets")
def list_home_tweets_handler(request):
    return tweet_list_handler(request, tweet_list_builder=get_home_tweets)


@alexa.intent(intent="UserTweets")
def list_user_tweets_handler(request):
    """ by default gets tweets for current user """
    return tweet_list_handler(request, tweet_list_builder=get_user_latest_tweets, msg_prefix="Looking for tweets posted by you.")


@alexa.intent(intent="RetweetsOfMe")
def list_retweets_of_me_handler(request):
    return tweet_list_handler(request, tweet_list_builder=get_retweets_of_me, msg_prefix="Looking for retweets.")


@alexa.intent(intent="FindFavouriteTweets")
def find_my_favourites_handler(request):
    return tweet_list_handler(request, tweet_list_builder=get_my_favourite_tweets, msg_prefix="Finding your favourite tweets.")


def focused_on_tweet(request):
    """
    Return index if focused on tweet False if couldn't
    """
    slots = request.get_slot_map()
    if "Index" in slots and slots["Index"]:
        index = int(slots['Index'])

    elif "Ordinal" in slots and slots["Index"]:
        parse_ordinal = lambda inp : int("".join([l for l in inp if l in string.digits]))
        index = parse_ordinal(slots['Ordinal'])
    else:
        return False
        
    index = index - 1 # Going from regular notation to CS notation
    user_state = twitter_cache.get_user_state(request.access_token())
    queue = user_state['user_queue'].queue()
    if index < len(queue):
        # Analyze tweet in queue
        tweet_to_analyze = queue[index]
        user_state['focus_tweet'] = tweet_to_analyze
        return index + 1 # Returning to regular notation
        twitter_cache.serialize()
    return False

"""
Definining API for executing pending actions:
action = function that does everything you want and returns a 'message' to return.
description = read out in case there is a pending action at startup. 
other metadata will be added as time progresses
"""

@alexa.intent("ReplyIntent")
def reply_handler(request):
    message = "Sorry, I couldn't tell which tweet you want to reply to. "
    slots = request.get_slot_map()
    user_state = twitter_cache.get_user_state(request.access_token())
    should_end_session = True
    if not slots["Tweet"]:
        return reply_focus_handler(request)
    else:
        can_reply = False
        if slots['Tweet'] and not (slots['Ordinal'] or slots['Index']):
            user_state = twitter_cache.get_user_state(request.access_token())
            if 'focus_tweet' in user_state: # User is focused on a tweet
                can_reply = True
        else:
            index = focused_on_tweet(request)
            if index: can_reply = True

        if can_reply: # Successfully focused on a tweet
            index, focus_tweet = user_state['focus_tweet']
            tweet_message = "@{0} {1}".format(focus_tweet.get_screen_name(),
                                          slots['Tweet'])
            params = {"in_reply_to_status_id": focus_tweet.get_id()}
            
            def action():
                print ("Performing action! lambda functions are awesome!")
                message = post_tweet(request.access_token(), tweet_message, params)
                del user_state['focus_tweet']
                return message

            should_end_session = False
            message = "I am ready to post the tweet, {}. Please say yes to confirm or stop to cancel.".format(slots['Tweet'])
            user_state['pending_action'] = {"action" : action,
                                            "description" : message }

    return alexa.create_response(message=message, end_session=should_end_session)


@alexa.intent("YesIntent")
def confirm_action_handler(request):
    message = "okay."
    user_state = twitter_cache.get_user_state(request.access_token())
    should_end_session = True
    if 'pending_action' in user_state:
        params = user_state['pending_action']
        # Perform action
        message = params['action']()
        if 'message' in params:
            message = params['message']
        if 'callback' in params:
            params['callback']()
        del user_state['pending_action']
        print ("successfully executed command")
        message = message + " would you like me to do anything else ? "
        should_end_session = False
    return alexa.create_response(message, end_session=should_end_session)


@alexa.intent("AMAZON.CancelIntent")
def cancel_action_handler(request):
    message = "okay."
    user_state = twitter_cache.get_user_state(request.access_token())
    should_end_session = True
    if 'pending_action' in user_state:
        del user_state['pending_action'] # Clearing out the user's pending action
        print ("cleared user_state")
        message += " i won't do it. would you like me to do something else ? "
        should_end_session = False
    return r.create_response(message, end_session=should_end_session)


@alexa.intent("ReplyFocus")
def reply_focus_handler(request):    
    msg = "Sorry, I couldn't tell which tweet you wanted to reply to."
    index = focused_on_tweet(request)
    if index:
        return alexa.create_response(message="Do you want to reply to tweet {} ? If so say reply, followed by your message".format(index))
    return alexa.create_response(message=msg, end_session=False)


@alexa.intent("MoreInfo")
def more_info_handler(request):
    index = focused_on_tweet(request)
    if index:
        user_state = twitter_cache.get_user_state(request.access_token())
        index, tweet = user_state['focus_tweet']
        message = " ".join(["details about tweet number {}.".format(index+1), tweet.detailed_description(), 
                            "To reply, say 'reply' followed by your message"])
        return alexa.create_response(message=message, end_session=False)
    return reply_focus_handler(request)

@alexa.intent("NextIntent")
def next_intent_handler(request):
    """
    Takes care of things whenver the user says 'next'
    """

    message = "Sorry, couldn't find anything in your next queue"
    end_session = True
    if True:
        user_queue = twitter_cache.user_queue(request.access_token())
        if not user_queue.is_finished():
            message = user_queue.read_out_next(MAX_RESPONSE_TWEETS)
            if not user_queue.is_finished():
                end_session = False
                message = message + ". Please, say 'next' if you want me to read out more. "
    return alexa.create_response(message=message,
                                 end_session=end_session)
        

@alexa.intent(intent="PreviousIntent")
def previous_intent_handler(request):
    user_queue = twitter_cache.user_queue(request.access_token())
    if user_queue and user_queue.has_prev():
        message = user_queue.read_out_prev()
    else:
        message = "I couldn't find anything to repeat"
    return alexa.create_response(message=message)
