"""
This is the basic config file, encapsulating all configuration options
ALL FILES SHOULD LOAD THEIR CONFIGURATIONS FROM THIS CENTRAL LOCATION
"""
from __future__ import print_function
import os
import json

# ---- Helper Functions ----

# Get path relative to the current file 
path_relative_to_file = lambda rel_path: os.path.normpath(os.path.join(os.path.dirname(__file__), rel_path))

# Load a json file as an object
load_json_schema = lambda schema_location : json.load(open(schema_location))


def read_from_user(input_type, *args, **kwargs):
    '''
    Helper function to prompt user for input of a specific type 
    e.g. float, str, int 
    Designed to work with both python 2 and 3 
    Yes I know this is ugly.
    '''

    def _read_in(*args, **kwargs):
        while True:
            try: tmp =  raw_input(*args, **kwargs)
            except NameError: tmp =  input(*args, **kwargs)
            try: return input_type(tmp)
            except: print ('Expected type', input_type)

    return _read_in(*args, **kwargs)

# Location of AMAZON.BUILTIN slot types
BUILTIN_SLOTS_LOCATION = path_relative_to_file(os.path.join('..', 'data', 'amazon_builtin_slots.tsv'))

def load_builtin_slots():
    '''
    Helper function to load builtin slots from the data location
    '''
    builtin_slots = {}
    for index, line in enumerate(open(BUILTIN_SLOTS_LOCATION)):
        o =  line.strip().split('\t')
        builtin_slots[index] = {'name' : o[0],
                                'description' : o[1] } 
    return builtin_slots

