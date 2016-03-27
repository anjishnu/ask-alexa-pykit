'''
This is a helper function to run ask-alexa-pykit locally to debug etc
It is not intended to be used as a 
'''

from flask import Flask, request
from lambda_function import lambda_handler

server = Flask(__name__)

@server.route('/')
def alexa_skills_kit_requests():
    request_obj = request.get_json()
    return lambda_handler(request_obj)

if __name__ == '__main__':
    server.run()
