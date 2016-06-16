'''
Contains classes to help in interpreting dialogue 
'''


class Dialog(object):

    EXPECTED_INTENTS =  "dialog.expected_intents" # List of valid intents expected 
    ON_ERROR_LABEL = "dialog.on_error_label" # On unexpected intent - route to this function

    def __init__(self, expected_intents=[], error_label=None):
        self.expected_intents = expected_intents
        self.error_label = error_label
                
    def to_json(self):
        return { self.EXPECTED_INTENTS : self.expected_intents,
                 self.ON_ERROR_LABEL : self.error_label}

    @classmethod
    def from_session(self, session):

        expected_intents = session[self.EXPECTED_INTENTS] if self.EXPECTED_INTENTS in session else []
        error_label = session[self.ON_ERROR_LABEL] if self.ON_ERROR_LABEL in session else None            
        return Dialog(expected_intents, error_label)
        
