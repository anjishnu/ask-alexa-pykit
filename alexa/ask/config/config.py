"""
This is the basic config file, encapsulating all configuration options
ALL FILES SHOULD LOAD THEIR CONFIGURATIONS FROM THIS CENTRAL LOCATION
"""
from __future__ import print_function
import os
import json

# ---- Helper Functions ----

path_relative_to_file = lambda rel_path: os.path.join(os.path.dirname(__file__), rel_path)
load_json_schema = lambda schema_location : json.load(open(schema_location))
    
# --- AMAZON related configurations ---

# The redirect url is used in the account linking process to associate an amazon user account with your OAuth token

BASE_REDIRECT_URL = "<HARDCODE_IT_HERE>" # Different for each vendor 

DEFAULT_INTENT_SCHEMA_LOCATION = path_relative_to_file("intent_schema.json")

NON_INTENT_REQUESTS = ["LaunchRequest", "SessionEndedRequest"]

INTENT_SCHEMA = load_json_schema(DEFAULT_INTENT_SCHEMA_LOCATION)
