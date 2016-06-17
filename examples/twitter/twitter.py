import requests
import jsonpickle
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs, urlencode
import cherrypy 
from collections import defaultdict 
import json
import os
import re
from collections import defaultdict

# For readable serializations
jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)


class LocalCache(object):
    """ Generic class for encapsulating twitter credential caching """
    server_data_template = "{}.server"
    user_data_template = "{0}.user.{1}"

    def __init__(self, backup = "tmp/twitter.cache"):
        self.backup = backup #Unique identifier for the backup of this cache
        self.memcache = {
            "users" : defaultdict(lambda : {}),
            "server": defaultdict(lambda : {})
        }
        self.deserialize()

    def users(self):
        return self.memcache['users']

    def set_user_state(self, user_id, state):
        self.memcache['users'][user_id] = state

    def update_user_state(self, user_id, state = {}):
        self.memcache['users'][user_id].update(state)
        
    def get_user_state(self, user_id):
        return self.memcache['users'][user_id]

    def clear_user_state(self, user_id):
        return self.memcache['users'][user_id].clear()

    def update_server_state(self, state_dict):
        self.memcache['server'].update(state_dict)
        
    def get_server_state(self):
        return self.memcache['server']

    def clear_server_state(self):
        return self.memcache['server'].clear()    

    def initialize_user_queue(self, user_id, queue):
        self.memcache['users'][user_id]['user_queue'] = ReadableQueue(queue)        
        
    def user_queue(self, user_id):
        if 'user_queue' in self.memcache['users'][user_id]:
            return self.memcache['users'][user_id]['user_queue']
            
    def server_fname(self):
        return self.server_data_template.format(self.backup)
        
    def user_fname(self, user):
        return self.user_data_template.format(self.backup, user)

    def deserialize(self):
        cache_loaded = False
        if os.path.exists(self.server_fname()) and not os.path.isdir(self.backup):
            try:
                self.memcache = { "server" : {},
                                  "users" : {} }
                
                with open(self.server_fname()) as backupfile:
                    print ("Attempting to reload cache")
                    self.memcache['server'] = jsonpickle.decode(backupfile.read())

                print ("Server cache loaded", json.dumps(self.memcache, indent=4))
                for user in self.memcache['server']['user_list']:
                    # Try to load as much user data as possible
                    if os.path.exists(self.user_fname(user)):
                        print ("found path for user", user)
                        with open(self.user_fname(user)) as userfile:
                            user_data = jsonpickle.decode(userfile.read())
                        self.memcache['users'][user] = user_data
                cache_loaded = True
            except Exception as e:
                print ("Cache file corrupted...")
                raise e
        if not cache_loaded:
            print ("Cache could not be loaded")
            pass
        else:
            print ("CACHE LOADED SUCCESSFULLY!")


    def serialize(self):
        json_to_serialize = self.memcache['server']
        user_list = list(self.users().keys())
        json_to_serialize.update({"user_list" : user_list})
        with open(self.server_fname(), 'w') as backup_server:
            # Serialize Server:
            json_encoded = jsonpickle.encode(json_to_serialize)
            backup_server.write(json_encoded)
            
        for user in user_list:
            user_data = self.get_user_state(user)
            json_encoded = jsonpickle.encode(user_data)
            with open(self.user_fname(user), 'w') as userfile:
                userfile.write(json_encoded)


    
class ReadableQueue(object):    
    def __init__(self, queue=[], pos=0):
        self.hashmap = { "queue" : [(i, e) for i,e in enumerate(queue)],
                         "pos" : pos }
        return 

    def queue(self):
        return self.hashmap['queue']
    
    def is_empty(self):
        return len(self.queue()) == 0

    def is_finished(self):
        return self.pos() == len(self.queue())

    def pos(self):
        return self.hashmap['pos']

    def set_pos(self, val):
        self.hashmap['pos'] = val

    def get_next(self, offset=1):
        
        if self.pos() < len(self.queue()):
            temp_queue =  self.queue()[self.pos(): self.pos() + offset]
            self.set_pos(self.pos() + offset)    
            if self.pos() > len(self.queue()): self.set_pos(len(self.queue()))
            return temp_queue

            
    def read_out_next(self, offset=1):
         return " ".join([readable.read_out(index) for index,readable in self.get_next(offset)])

    def has_prev(self):
        return self.pos() > 0

    def get_prev(self, offset=1):
         if self.pos() > 0:
             self.set_pos(self.pos() - offset)
             if self.pos() < 0: 
                 offset = offset + self.pos() 
                 # [1, current(2), 3] get_prev(offeset=3) 
                 # pos :=> -2, offset :=> 3-2 = 1, pos :=> 0, then read 0 to 1
                 self.set_pos(0)
             return self.queue()[self.pos() : offset]
         return None
         
    def read_out_prev(self, offset=1):
         return " ".join([readable.read_out() for readable in self.get_prev(offset)])


#Local cache caches tokens for different users 
local_cache = LocalCache()



def strip_html(text):
    """ Get rid of ugly twitter html """
    def reply_to(text):
        replying_to = []
        split_text = text.split()
        for index, token in enumerate(split_text):
            if token.startswith('@'): replying_to.append(token[1:])
            else:
                message = split_text[index:]
                break
        rply_msg = ""
        if len(replying_to) > 0:
            rply_msg = "Replying to "
            for token in replying_to[:-1]: rply_msg += token+","                
            if len(replying_to)>1: rply_msg += 'and '
            rply_msg += replying_to[-1]+". "
        return rply_msg + " ".join(message)
        
    text = reply_to(text)      
    text = text.replace('@', ' ')
    return " ".join([token for token in text.split() 
                     if  ('http:' not in token) and ('https:' not in token)])


class Tweet(object):
    def __init__(self, json_obj):
        self.tweet = json_obj

    def get_id(self):
        return self.tweet['id']
        
    def get_raw_text(self):
        return self.tweet['text']
        
    def _process_text(self):
        text = strip_html(self.tweet['text'])
        user_mentions = self.tweet['entities']['user_mentions']
        text = text.replace('@', 'at ')
        for user in user_mentions:            
            text = text.replace(user['screen_name'], user['name'])
        return text
        
    def get_screen_name(self):
        return self.tweet['user']['screen_name']

    def get_user_name(self):
        return self.tweet['user']['name']
        
    def read_out(self, index):
        text = self._process_text()
        return "tweet number {num} by {user} : {text} ,".format(num=index+1, 
                                                              user=self.get_user_name(),
                                                              text = text)
    
    def detailed_description(self):
        response_builder = ["This tweet was posted by {user_name} whose twitter handle is {screen_name} the account description reads: {description}."
                            .format(screen_name=self.tweet['user']['screen_name'],
                                    user_name=self.tweet['user']['name'],
                                    description=self.tweet['user']['description'])]
        if self.tweet['retweeted']:
            response_builder += ["It's been retweeted {} times.".format(self.tweet['retweet_count'])]
        if self.tweet['favorited']:
            response_builder += ["{} people have favorited it.".format(self.tweet['favorites_count'])]
        if self.tweet["in_reply_to_screen_name"]:
            response_builder += ["it was posted in response to user {}.".format(self.tweet['in_reply_to_screen_name'])]
        response_builder += ["the text of the tweet is, {}.".format(self._process_text())]
        return " ".join(response_builder)

    def user_mentions(self):
        return self.tweet['user_mentions']


def get_cached_access_pair(uid):
    if uid in local_cache.users():
        access_token = local_cache.get_user_state(uid)['access_token']
        access_secret = local_cache.get_user_state(uid)['access_secret']
        return access_token, access_secret
    else:
        raise ValueError


def get_request_token(callback_url=None):
    url = "https://api.twitter.com/oauth/request_token"
    consumer_key, consumer_secret = local_cache.get_server_state()['twitter_keys']

    auth = OAuth1(consumer_key, consumer_secret)
    params = { "oauth_callback" : callback_url } 
    r = requests.post(url, auth=auth, params=params)
    response_obj = parse_qs(r.text)    
    local_cache.update_server_state({ "request_token" : response_obj['oauth_token'][0],
                                      "request_secret": response_obj['oauth_token_secret'][0] })
    return response_obj['oauth_token_secret'], response_obj['oauth_token']
    

def authenticate_user_page(callback_url="", metadata=None):
    url = "https://api.twitter.com/oauth/authenticate"
    oauth_secret, oauth_token = get_request_token(callback_url)
    local_cache.update_server_state({'metadata' : metadata })

    params = { "force_login" : True,
               "oauth_token": oauth_token }
    r = requests.get(url, params=params)
    return r.text
    

def post_tweet(user_id, message, additional_params={}):
    """
    Helper function to post a tweet 
    """
    url = "https://api.twitter.com/1.1/statuses/update.json"    
    params = { "status" : message }
    params.update(additional_params)
    r = make_twitter_request(url, user_id, params, request_type='POST')
    print (r.text)
    return "Successfully posted a tweet {}".format(message)


def get_access_token(oauth_token, oauth_verifier):
    url = "https://api.twitter.com/oauth/access_token"
    params = {"oauth_verifier" : oauth_verifier}

    server_state = local_cache.get_server_state()
    request_token  = server_state['request_token']
    request_secret = server_state['request_secret']
    consumer_key, consumer_secret = server_state['twitter_keys']

    auth = OAuth1(consumer_key, consumer_secret, request_token, request_secret)

    r = requests.post(url, params = params, auth=auth)
    response_obj = parse_qs(r.text)

    uid = response_obj['oauth_token'][0]    
    print ("Access token", uid)


    local_cache.set_user_state(user_id = uid,
                               state = { "access_token" : response_obj['oauth_token'][0],
                                         "access_secret" : response_obj['oauth_token_secret'][0],
                                         'twitter_user_id': response_obj['user_id'][0],
                                         'screen_name' : response_obj ['screen_name'][0] 
                               })
    local_cache.serialize()

    fragments = {
        "state" : local_cache.get_server_state()['metadata']['state'],
        "access_token" : uid,
        "token_type" : "Bearer"
    }
    return urlencode(fragments)



    
def get_twitter_auth(user_id):
    consumer_key, consumer_secret = local_cache.get_server_state()['twitter_keys']
    access_token, access_secret = get_cached_access_pair(user_id)
    return OAuth1(consumer_key, consumer_secret, access_token, access_secret)


def process_tweets(tweet_list):
    """ Clean tweets and enumerate, preserving only things that we are interested in """  
    return [Tweet(tweet) for tweet in tweet_list]
    

def make_twitter_request(url, user_id, params={}, request_type='GET'):
    """ Generically make a request to twitter API using a particular user's authorization """
    if request_type == "GET":
        return requests.get(url, auth=get_twitter_auth(user_id), params=params)
    elif request_type == "POST":
        return requests.post(url, auth=get_twitter_auth(user_id), params=params)



def get_user_twitter_details(user_id, params={}):
    url  = "https://api.twitter.com/1.1/users/lookup.json"    
    user_cache = local_cache.get_user_state(user_id)    
    params.update({"user_id": user_cache['twitter_user_id'] })
    response = make_twitter_request(url, user_id, params)
    return response.json()


def geo_search(user_id, search_location):
    """
    Search for a location - free form
    """
    url = "https://api.twitter.com/1.1/geo/search.json"
    params =  {"query" : search_location }
    response = make_twitter_request(url, user_id, params).json()
    return response


def closest_trend_search(user_id, params={}):
    #url = "https://api.twitter.com/1.1/trends/place.json"
    url = "https://api.twitter.com/1.1/trends/closest.json"
    response = make_twitter_request(url, user_id, params).json()
    return response


def list_trends(user_id, woe_id):
    url = "https://api.twitter.com/1.1/trends/place.json"
    params = { "id" : woe_id }
    response = make_twitter_request(url, user_id, params).json()
    return response


def read_out_tweets(processed_tweets, speech_convertor=None):
    """
    Input - list of processed 'Tweets'
    output - list of spoken responses
    """
    return ["tweet number {num} by {user}. {text}.".format(num=index+1, user=user, text=text)
               for index, (user, text) in enumerate(processed_tweets)]


def request_tweet_list(url, user_id, params={}):
    return process_tweets(make_twitter_request(url, user_id).json())


def get_home_tweets(user_id, input_params={}):
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    print ("Trying to get home tweets")
    response = request_tweet_list(url, user_id)
    return response


def get_retweets_of_me(user_id, input_params={}):
    """ returns recently retweeted  tweets """
    url = "https://api.twitter.com/1.1/statuses/retweets_of_me.json"
    print ("trying to get retweets")
    return request_tweet_list(url, user_id)


def get_my_favourite_tweets(user_id, input_params = {}):
    """ Returns a user's favourite tweets """
    url = "https://api.twitter.com/1.1/favorites/list.json"
    return request_tweet_list(url, user_id)


def get_user_latest_tweets(user_id, params={}):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
    return request_tweet_list(url, user_id, params)
    

def get_latest_twitter_mentions(user_id):
    url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"
    return request_tweet_list(url, user_id)


def search_for_tweets_about(user_id, params):
    """ Search twitter API """
    url = "https://api.twitter.com/1.1/search/tweets.json"
    response = make_twitter_request(url, user_id, params)
    return process_tweets(response.json()["statuses"]) 
