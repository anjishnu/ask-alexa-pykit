import cherrypy
import json
import dialog
from lib.validation_utils import valid_alexa_request
from urllib.parse import urlparse
import os
import subprocess
import requests
from config.config import SERVER_CONFIG, ALL_REQUESTS_VALID


class SkillServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        content_length = int(cherrypy.request.headers['Content-Length'])
        raw_body = cherrypy.request.body.read(content_length)
        input_json = json.loads(raw_body.decode("utf-8"))
        is_valid_request = valid_alexa_request(cherrypy.request.headers, 
                                               raw_body) if not ALL_REQUESTS_VALID else True
        if is_valid_request:
            print ("New Request Body:", json.dumps(input_json, indent=4))
            output_json = dialog.route_intent(input_json)
            return output_json    


if __name__ == "__main__":
    """
    Load the server config and launch the server
    """
    print (json.dumps(SERVER_CONFIG, indent=4))    
    config = {"global": SERVER_CONFIG}    
    cherrypy.config.update(SERVER_CONFIG)
    cherrypy.quickstart(SkillServer(), config=config)
