import json
from argparse import ArgumentParser
import os

default_dialog_template_fpath = "dialog_template.txt"
default_intent_schema_location = "../config/intent_schema.json"

empty_dialog_template=('def {0}(intent_request):\n'
'    """\n'
'    The default dialog to be spoken on receipt of intent {1}.\n'
'    TODO:\n'
'      Fill in dialog logic\n'
'    """\n'
'    return create_response("Hello world!")\n')

def load_intent_schema(schema_location = default_intent_schema_location):
    with open(schema_location, 'r') as intentfile:
        return json.load(intentfile)

def name_dialog_func(inp_str):
    """
    Logic for deciding how to name a dialog 
    function given an intent_name    
    """
    return inp_str.lower()+"_dialog"


def generate_intent_to_func_str(intent_map):
    """
    Takes a map of form: { "IntentOne" : "func_name_1",
                           "IntentTwo" : "func_name_2" }
    and returns a string
    '{ "IntentOne" : func_name_1,
       "IntentTwo" : func_name_2 }'
    
    """
    raw_str = json.dumps(intent_map, indent=4)
    #print(raw_str)
    out_lst = []
    for line in raw_str.split('\n'):
        if '":' in line:
            before, it, after  = line.partition('":')
            after = after.replace('"', '')
            line = "".join([before, it, after, '\n'])
        else: line = "".join([line,'\n'])
        out_lst+=[line]
    return "".join(out_lst)

def generate_dialog_file(intent_map, dialog_template_path = default_dialog_template_fpath):
    with open(dialog_template_path, 'r') as dtfile:
        dialog_file_template = dtfile.read()

    #print(dialog_file_template)
    #inserting the dialog map str"

    dialog_map_str = generate_intent_to_func_str(intent_map)
    #print (dialog_map_str)
    dialog_file_template = dialog_file_template.replace('{0}', dialog_map_str)

    #Appending the dialog map functions.
    for intent_name, dialog_fn_name in intent_map.items():
        dialog_file_template+= "\n\n"
        dialog_file_template+= empty_dialog_template.format(dialog_fn_name,
                                                       intent_name)
    return dialog_file_template

def main(args):
    intent_schema = load_intent_schema(args.intent_schema)
    intent_map = {intent['intent']: name_dialog_func(intent['intent']) 
                   for intent in intent_schema['intents']}
    output = (generate_dialog_file(intent_map, dialog_template_path=args.dialog_template))
    with open(args.output_file, 'w') as outfile:
        outfile.write(output)
    return 

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i","--input_file", help="intent schema from which to generate output file, default = ../config/intent_schema.json", 
                        default=default_intent_schema_location, dest="intent_schema")
    parser.add_argument("-o", "--output_file", help = "output file location, by default it will be produced in current folder with name dialog.py", 
                        default="sample_dialog.py", dest="output_file")
    parser.add_argument("-dt", "--dialog_template", help = "template file from which to build the dialog file, default=dialog_template.txt, do not mess with this "
                        "unless you know what you are doing", default = default_dialog_template_fpath, dest= "dialog_template")
    args = parser.parse_args()
    print (args)
    main(args)
