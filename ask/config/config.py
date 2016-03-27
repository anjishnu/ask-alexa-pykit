"""
This is the basic config file, encapsulating all configuration options
ALL FILES SHOULD LOAD THEIR CONFIGURATIONS FROM THIS CENTRAL LOCATION
"""
from __future__ import print_function
import os
import json

# ---- Helper Functions ----

def read_in(input_type, *args, **kwargs):
    def _read_in(*args, **kwargs):
        while True:
            try:
                tmp =  raw_input(*args, **kwargs)
            except NameError:
                tmp =  input(*args, **kwargs)
            try:
                return input_type(tmp)
            except:
                print ('Expected type', input_type)
    return _read_in(*args, **kwargs)


path_relative_to_file = lambda rel_path: os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path))
load_json_schema = lambda schema_location : json.load(open(schema_location))
    
