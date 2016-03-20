from . import utils

''' 
Setting up some nice abstractions around good object oritented code.
'''

def create_response(*args, **kwargs):
    return utils.ResponseBuilder.create_response(*args, **kwargs)

ResponseBuilder = utils.ResponseBuilder
alexa = utils.VoiceHandler()
Request = utils.Request
