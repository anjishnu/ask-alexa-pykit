'''
Wrappers around useful science API calls
'''

import requests
from datetime import datetime
import random
import json

categories = {
    "new" : 0,
    "creativity": 1,
    "fitness": 2,
    "health": 3,
    "happiness": 4,
    "nutrition": 5,
    "productivity": 6,
    "sleep": 7,
    "persuasion": 8,
    "parenting": 9,
    "education": 10    
}


def most_recent_25_posts():
    end_point = 'http://www.usefulscience.org/api/posts'
    return requests.get(end_point).json()['posts']

def most_recent_25_posts_by_category(category_id):
    if not category_id:
        return most_recent_25_posts()
    end_point = "http://www.usefulscience.org/api/posts/{}".format(category_id)
    response = requests.get(end_point)
    return response.json()['posts']

    
''' Simple cache to keep updated with API '''
_1_DAY = 60 * 60 * 24
_1_MINUTE = 60

class SimplePostsCache(object):
    '''
    Seconds
    '''
    def __init__(self, refresh_rate=_1_MINUTE):
        
        self.cache = {cat_id : list()
                      for cat_name, cat_id in categories.items()}
        self.refresh_rate = refresh_rate # Seconds
        # Splitting refresh times by category so that one unlucky person doesn't
        # have to wait for 10 API calls to complete 
        self.last_refresh = {cat_id : datetime.now()
                             for cat_name, cat_id in categories.items()}
        for cat_id in self.last_refresh:
            self.refresh_cache(cat_id)
        
    def refresh_cache(self, cat_id):
        '''
        Repopulate cache
        '''        
        self.cache[cat_id] = most_recent_25_posts_by_category(cat_id)
        self.last_refresh[cat_id] = datetime.now()
        print ('Cache refresh at...', str(self.last_refresh[cat_id]))
        # print (json.dumps(self.cache, indent=4))

        
    def get_post(self, category):
        cat_id = categories[category]
        if ((datetime.now() - self.last_refresh[cat_id]).seconds
            > self.refresh_rate):
            # Time for a refresh ! 
            self.refresh_cache(cat_id)
        return random.choice(self.cache[cat_id])['post']

    
post_cache = SimplePostsCache(_1_MINUTE)
