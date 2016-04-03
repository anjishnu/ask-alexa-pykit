'''
Script for testing out the response for any given request
'''
from __future__ import print_function
from lambda_function import lambda_handler
import json
import sys
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_json', required=True)
    args = parser.parse_args()
    request_obj = json.load(open(args.input_json))
    print ('Request JSON')
    print (json.dumps(request_obj, indent=2))
    response = lambda_handler(request_obj)
    print ('Response JSON')
    print (json.dumps(response, indent=2))
    
