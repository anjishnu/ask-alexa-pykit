'''
Abstractions around IntentSchema class. 
'''
from __future__ import print_function
import json
from collections import OrderedDict
from argparse import ArgumentParser
import os
from .config.config import read_from_user, load_builtin_slots


class IntentSchema(object):
    '''
    Wrapper class to manipulate Intent Schema
    '''
    def __init__(self, json_obj=None):
        if json_obj:
            # Use existing intent schema 
            self._obj = json_obj
        else:
            # Create one from scratch
            self._obj = OrderedDict({ "intents" : [] })

            # These intents are basically always needed
            # for certification 
            self.add_intent('AMAZON.HelpIntent')
            self.add_intent('AMAZON.StopIntent')
            self.add_intent('AMAZON.CancelIntent')
            
    def add_intent(self, intent_name, slots=None):
        if not slots: slots = []
        intent = OrderedDict()
        intent ['intent'], intent['slots'] = intent_name, slots        
        self._obj['intents'].append(intent)
        
        
    def build_slot(self, slot_name, slot_type):
        slot = OrderedDict()
        slot['name'], slot['type'] = slot_name, slot_type
        return slot
    
    def __str__(self):
        return json.dumps(self._obj, indent=2)

    
    def get_intents(self):
        return self._obj['intents']     

    def get_intent_names(self):
        return [intent['intent'] for intent in self.get_intents()]
    
    @classmethod
    def interactive_build(self, fpath=None):
        intent_schema = IntentSchema.from_filename(fpath)
        print ("How many intents would you like to add")
        num = read_from_user(int)
        for i in range(num):
            intent_schema._add_intent_interactive(intent_num=i+1)
        return intent_schema

    def save_to_file(self, filename):
        with open(filename, 'w') as fp:
            print(self, file=fp)
            
    def _add_intent_interactive(self, intent_num=0):        
        '''
        Interactively add a new intent to the intent schema object 
        '''
        print ("Name of intent number : ", intent_num)
        slot_type_mappings = load_builtin_slots()
        intent_name = read_from_user(str)
        print ("How many slots?")        
        num_slots = read_from_user(int)
        slot_list = []
        for i in range(num_slots):
            print ("Slot name no.", i+1)
            slot_name = read_from_user(str).strip()
            print ("Slot type? Enter a number for AMAZON supported types below,"
                   "else enter a string for a Custom Slot")
            print (json.dumps(slot_type_mappings, indent=True))
            slot_type_str = read_from_user(str)
            try: slot_type = slot_type_mappings[int(slot_type_str)]['name'] 
            except: slot_type = slot_type_str
            slot_list += [self.build_slot(slot_name, slot_type)]                    
        self.add_intent(intent_name, slot_list)                        

    
    @classmethod
    def from_filename(self, filename):
        '''
        Build an IntentSchema from a file path 
        creates a new intent schema if the file does not exist, throws an error if the file
        exists but cannot be loaded as a JSON
        '''
        if os.path.exists(filename):
            with open(filename) as fp:
                return IntentSchema(json.load(fp, object_pairs_hook=OrderedDict))
        else:
            print ('File does not exist')
            return IntentSchema()

def from_filename(fname):
    return IntentSchema.from_filename(fname)

        
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--intent_schema', '-i', required=True) 
    parser.add_argument('--overwrite', '-o', action='store_true',
                        default=False)
    args = parser.parse_args()

    if not args.overwrite:
        print ('In APPEND mode')
        intent_schema = IntentSchema.interactive_build(args.intent_schema)
    else:
        print ('In OVERWRITE mode')
        intent_schema = IntentSchema.interactive_build()        

    print ("Write to file:", args.intent_schema,"? (y/n)")
    dec = read_from_user(str).strip().lower()
    if dec == "y":
        intent_schema.save_to_file(args.intent_schema)
    elif dec == "n":
        pass
