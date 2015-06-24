#!/usr/bin/python3
# Generate an intent schema file by asking questions. 
import json 

empty_schema = """{"intents": []}"""

intent_schema_path = "../config/intent_schema.json"

slot_type_mappings = { 1 : ["LITERAL", "Description: " "passes the words for the slot value with no conversion"],
                       2 : ["NUMBER", "Description: " 'converts numeric words (five) into digits (such as 5)'],
                       3 : ["DATE", "Description: " 'converts words that indicate dates (today, tomorrow, or july) into a date format (such as 2015-07-00T9)'],
                       4 : ["TIME", "Description: " 'converts words that indicate time (four in the morning, two p m) into a time value (16:00).'],
                       5 : ["DURATION", "Description: " 'converts words that indicate durations (five minutes) into a numeric duration (5M).']}

def new_intent_schema():
    return append_to_schema(json.loads(empty_schema))

def add_to_existing_schema():
    with open(intent_schema_path, 'r') as infile:
        current_schema = infile.read()
    return append_to_schema(current_schema)

def append_to_schema(current_schema):
    print ("How many intents would you like to add")
    num = int(input())
    for i in range(num):
        current_schema["intents"]+= [add_intent(i)]
    return current_schema

def add_intent(index = 0):
    intent_json = {}
    print ("Name of intent no. ", index+1)
    intent_name = input()
    print ("How many slots?")
    no_slots = int(input())
    intent_json = {
        "intent": intent_name,
        "slots": [] 
    }
    for i in range(no_slots):
        print ("Slot name no.", i+1)
        slot_name = input().strip()
        print ("Slot type? Supported types listed below")
        print (json.dumps(slot_type_mappings, indent=True))
        slot_type = int(input())
        intent_json['slots'].append({'name': slot_name, 
                                      "type": slot_type_mappings[slot_type][0]})
    return intent_json

if __name__ == "__main__":
    print ("What would you like to do?")
    print ("1. Define new intent schema")
    print ("2. Add to current intent schema")
    print ("0. Exit program")

    opt = input()

    if int(opt)==1:
        output = new_intent_schema()
    elif int(opt)==2:
        output = add_to_existing_schema()

    print ("Schema created:")
    print (json.dumps(output, indent=2))

    print ("Write to file:", intent_schema_path,"? (y/n)")
    dec = input().strip().lower()
    if dec == "y":
        with open(intent_schema_path,'w') as outfile:
            outfile.write(json.dumps(output, indent=4))
    elif dec == "n":
        pass
