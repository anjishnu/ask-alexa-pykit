from utils import ResponseBuilder, VoiceHandler

''' 
Setting up some nice abstractions around good object oritented code.
'''

def create_response(*args, **kwargs):
    return ResponseBuilder.create_response(*args, **kwargs)

voice = VoiceHandler()
