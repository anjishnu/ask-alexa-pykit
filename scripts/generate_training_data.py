#!/usr/bin/python3
from __future__ import print_function
import readline
import json
import re

DEFAULT_INTENT_SCHEMA_LOCATION = "../alexa/ask/config/intent_schema.json"

def read_in(**kwargs):
    try:
        return raw_input(**kwargs)
    except NameError:
        return input(**kwargs)
            

"""
Usage - python3 generate_training_data.py
"""


def print_description(intent):
    print ("<> Enter data for <{intent}> OR Press enter with empty string to move onto next intent"
           .format(intent=intent["intent"]))
    print ("<> Enter '<' to delete last training utterance")
    print ("<> Sample utterance to remind you of the format:")
    print (">> what is the recipe for {ravioli|Food} ?")
    if len(intent["slots"]) > 0:
        print ("<> Available slots for this intent")
        for slot in intent["slots"]:
            print (" - - ", slot["name"], "<TYPE: {}>".format(slot["type"])) 

            
def validate_input_format(utterance, intent):
    """ TODO add handling for bad input"""
    slots = {slot["name"] for slot in intent["slots"]}
    split_utt = re.split("{(.*)}", utterance)

    banned = set("-/\\()^%$#@~`-_=+><;:")
    for token in split_utt:
        if (banned & set(token)):
            print (" - Banned character found in substring", token)
            print (" - Banned character list", banned)
            return False

        if "|" in token:
            split_token = token.split("|")
            if len(split_token)!=2:
                print (" - Error, token is incorrect in", token, split_token)
                return False

            word, slot = split_token
            if slot.strip() not in slots:
                print (" -", slot, "is not a valid slot for this Intent, valid slots are", slots)
                return False
    return True


def lowercase_utterance(utterance):
    split_utt = re.split("({.*})", utterance)
    def lower_case_split(token):
        if "|" in token:
            phrase, slot = token.split("|")
            return "|".join([phrase.strip().lower(), slot.strip()])
        else:
            return token.lower()
    return " ".join([lower_case_split(token) for token in split_utt])
    
        
def generate_training_data(intent_schema = DEFAULT_INTENT_SCHEMA_LOCATION):
    with open(intent_schema) as input_file:
        schema = json.load(input_file)
    print ("Loaded intent schema, populating intents")
    training_data = []
    for intent in schema["intents"]:
        utterance = "default"
        print_description(intent)
        keep_prompting = True
        while keep_prompting:            
            utterance = read_in(str(len(training_data))+". "+intent["intent"]+'\t')
            if utterance.strip() == "":
                keep_prompting = False
            elif utterance.strip() == "<":
                print (" - Discarded utterance: ", training_data.pop())
            elif validate_input_format(utterance, intent):
                training_data.append("\t".join([intent["intent"], lowercase_utterance(utterance)]))
            else:
                print (" - Discarded utterance:", utterance)
    return training_data                


with open("utterances.txt", 'w') as utterance_file:
    utterance_file.write("\n".join(generate_training_data()))
