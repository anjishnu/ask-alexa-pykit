import cherrypy
import json
import dialog
from lib.validation_utils import valid_alexa_request

"""Verification"""
from urllib.parse import urlparse
import os
import subprocess

SERVER_CONFIG_PATH = "config/server_config.json"


class SkillResponse(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        content_length = int(cherrypy.request.headers['Content-Length'])
        raw_body = cherrypy.request.body.read(content_length)
        input_json = json.loads(raw_body.decode("utf-8"))

        if valid_alexa_request(cherrypy.request.headers, raw_body):
            print ("New Request Body:", json.dumps(input_json, indent=4))
            output_json = dialog.route_intent(input_json)
            return output_json

   
if __name__ == "__main__":
    """
    Load the server config and launch the server
    """
    with open(SERVER_CONFIG_PATH, 'r') as server_conf_file:
        server_config = json.load(server_conf_file)
        print ("Loaded server config file:")
    print (json.dumps(server_config, indent=4))    
    config = {"global": server_config}    
    cherrypy.config.update(server_config)
    cherrypy.quickstart(SkillResponse(), config=config)
