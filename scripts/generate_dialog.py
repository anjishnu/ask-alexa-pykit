import json
dialog_template = "dialog_template.txt"

intent_schema_location = "../configs/intent_schema.json"

def load_intent_schema():
    with open(intent_schema_location, 'r') as intentfile:
        return json.load(intentfile)

def name_func(inp_str):
    return inp_str.lower()+"_dialog"



if __name__ == "__main__":
    intent_schema = load_intent_schema()
    map_object = {intent: name_func(intent) for intent in intent_schema['intents']}
    
