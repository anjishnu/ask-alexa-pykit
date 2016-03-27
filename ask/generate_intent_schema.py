#!/usr/bin/python3
# Generate an intent schema file by asking questions. 
from __future__ import print_function
import json 
import readline
import os
from .config.config import read_in

if __name__ == "__main__":

    parser = ArgumentParser()
    
    parser.add_argument('--intent_schema', '-i',
                        required=True) 
    parser.add_argument('--overwrite', '-o',
                        action='store_true',
                        default=False)
    args = parser.parse_args()

    if not args.overwrite:
        print ('In "Append", mode')
        intent_schema = IntentSchema.interactive_build(args.intent_schema)
    else:
        print ('In OVERWRITE mode')
        intent_schema = IntentSchema.interactive_build()        

    print ("Write to file:", args.intent_schema,"? (y/n)")
    dec = read_in(str).strip().lower()
    if dec == "y":
        intent_schema.save_to_file(args.intent_schema)
    elif dec == "n":
        pass

