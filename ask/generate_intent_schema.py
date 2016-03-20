#!/usr/bin/python3
# Generate an intent schema file by asking questions. 
from __future__ import print_function
import json 
import readline
import os
from .config import config

read_in = config.read_in
intent_schema_path = config.DEFAULT_INTENT_SCHEMA_LOCATION

empty_schema = """{"intents": []}"""


slot_type_mappings = {

    1 : ["AMAZON.LITERAL",
         "Description: " "passes the words for the slot value with no conversion"],
    2 : ["AMAZON.NUMBER",
         "Description: " 'converts numeric words (five) into digits (such as 5)'],
    3 : ["AMAZON.DATE", "Description: "
         'converts words that indicate dates (today, tomorrow, or july) into a date format (such as 2015-07-00T9)'],
    4 : ["AMAZON.TIME",
         "Description: " 'converts words that indicate time (four in the morning, two p m) into a time value (16:00).'],
    5 : ["AMAZON.DURATION",
         "Description: " 'converts words that indicate durations (five minutes) into a numeric duration (5M).'],
    6 : ["AMAZON.US_CITY",
         "Description: Improves slot performance on all major US cities"]
}


def new_intent_schema():
    return append_to_schema(json.loads(empty_schema))


def add_to_existing_schema():
    with open(intent_schema_path, 'r') as infile:
        current_schema = json.load(infile)
    return append_to_schema(current_schema)


def append_to_schema(current_schema):
    print ("How many intents would you like to add")
    num = int(read_in())
    for i in range(num):
        current_schema["intents"]+= [add_intent(i)]
    return current_schema


def add_intent(index = 0):
    intent_json = {}
    print ("Name of intent no. ", index+1)
    intent_name = read_in()
    print ("How many slots?")
    no_slots = int(read_in())
    intent_json = {
        "intent": intent_name,
        "slots": [] 
    }
    for i in range(no_slots):
        print ("Slot name no.", i+1)
        slot_name = read_in().strip()
        print ("Slot type? Enter a number for AMAZON supported types below, else enter a string for a Custom Slot")
        print (json.dumps(slot_type_mappings, indent=True))
        slot_type_str = read_in()
        try:
            # If the slot type is in the pre-filled list
            slot_type = slot_type_mappings[int(slot_type_str)][0] 
        except:
            # If it isn't. 
            slot_type = slot_type_str
        intent_json['slots'].append({'name': slot_name, 
                                      "type": slot_type_str})
    return intent_json


if __name__ == "__main__":
    print ("What would you like to do?")
    print ("1. Define new intent schema")
    print ("2. Add to current intent schema")
    print ("0. Exit program")

    opt = read_in()

    if int(opt)==1:
        output = new_intent_schema()
    elif int(opt)==2:
        output = add_to_existing_schema()

    print ("Schema created:")
    print (json.dumps(output, indent=2))

    print ("Write to file:", intent_schema_path,"? (y/n)")
    dec = read_in().strip().lower()
    if dec == "y":
        with open(intent_schema_path,'w') as outfile:
            outfile.write(json.dumps(output, indent=4))
    elif dec == "n":
        pass
