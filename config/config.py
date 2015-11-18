"""
This is the basic config file, encapsulating all configuration options
ALL FILES SHOULD LOAD THEIR CONFIGURATIONS FROM THIS CENTRAL LOCATION
"""
from __future__ import print_function
import os
import json

# ---- Helper Functions ----
def path_relative_to_file(rel_path):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, rel_path)

def load_json_schema(schema_location):
    with open(schema_location, 'r') as json_file:
        return json.load(json_file)


# --- CherryPyServer related configurations ---

SERVER_CONFIG_PATH = path_relative_to_file("server_config.json")

SERVER_CONFIG = load_json_schema(SERVER_CONFIG_PATH)
print ("Loaded server config file:")


# --- AMAZON related configurations ---


ALL_REQUESTS_VALID = True # Declares all incoming requests valid - (switches off oauth validation - useful for debugging)

# The redirect url is used in the account linking process to associate an amazon user account with your OAuth token

BASE_REDIRECT_URL = "<HARDCODE_IT_HERE>" # Different for each vendor 

DEFAULT_INTENT_SCHEMA_LOCATION = path_relative_to_file("intent_schema.json")

NON_INTENT_REQUESTS = ["LaunchRequest", "SessionEndedRequest"]

INTENT_SCHEMA = load_json_schema(DEFAULT_INTENT_SCHEMA_LOCATION)


