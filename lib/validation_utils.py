from urllib.parse import urlparse
import os
import subprocess
import requests
import urllib
import json
import requests
from datetime import datetime
import base64
import shlex

from Crypto.Signature import PKCS1_v1_5 as Verifier
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


def linux_cmd(cmd_str):
    return str(subprocess.check_output(shlex.split(cmd_str))).replace("\\n","\n")


def valid_alexa_request(headers_map, request_body, disable_timestamp_validation=True):
    '''                                                                                                                                                                  
    Utility function to validate headers                                                                                                                                     '''
    if not os.path.isdir("tmp"):
        os.makedirs("tmp")

    cert_file = "tmp/echo_cert.pem"
    public_key_file = "tmp/pubkey.pem"
    files_to_be_cleaned =  [cert_file, public_key_file]

    cert_chain_url = headers_map["Signaturecertchainurl"]    

    is_url_valid =  valid_cert_url(cert_chain_url)
    is_cert_valid = valid_certificate(cert_chain_url, cert_file)    

    if disable_timestamp_validation:
        is_valid_timestamp = True
    else:
        is_valid_timestamp = valid_timestamp(json.loads(request_body.decode('utf-8'))['request']['timestamp'])
    extract_public_key(cert_file, public_key_file)
    signature = headers_map["Signature"]
    decoded_signature = base64.b64decode(signature)
    is_signature_verified = verify_signature(request_body, public_key_file, decoded_signature)    

    #Cleanup
    for fname in files_to_be_cleaned:
        os.remove(fname)

    return (is_valid_timestamp and is_url_valid 
            and is_cert_valid and is_signature_verified)

def valid_timestamp(timestamp_str):
    """ Validate the timestamp to ensure that it is valid
    timestamp_str format: '2015-08-29T22:22:37Z' """

    #No idea why my time is offset by this amount... server time drift?
    mysterious_delta = 296

    timestamp = datetime.strptime(timestamp_str,"%Y-%m-%dT%H:%M:%SZ")
    dt = datetime.utcnow() - timestamp
    print (dt, dt.seconds)
    return False if dt.seconds-mysterious_delta> 150 else True


def verify_signature(request_body, public_key_file, signature):
    """
    Given a public key, a request body and a signature - verifies that the signature is valid.
    """
    public_key = RSA.importKey(open(public_key_file).read())
    h = SHA.new(request_body)
    verifier = Verifier.new(public_key)
    return verifier.verify(h, signature)


def valid_cert_url(cert_chain_url):
    """
    Validate the URL location of the certificate
    """
    parsed_url = urlparse(cert_chain_url)
    if parsed_url.scheme == 'https':
        if parsed_url.hostname == "s3.amazonaws.com":
            if os.path.normpath(parsed_url.path).startswith("/echo.api/"):
                return True
    return False


def valid_certificate(cert_url, cert_file):
    """
    Download and Validate the ceritifcate provided by the requestor
    """
    r = requests.get(cert_url)
    with open(cert_file, 'wb') as cfile:
        cfile.write(r.content)
    get_cert_text = lambda cert: linux_cmd("openssl x509 -text -noout -in {}".format(cert))    
    cert_text = get_cert_text(cert_file)
    if valid_cert_text(cert_text):
        return True
    else:
        return False


def extract_public_key(cert_file, public_key_file):
    """
    Extract the public key 
    """
    os.system("openssl x509 -pubkey -noout -in {cert_file}  > {public_key_file}".format(cert_file=cert_file,
                                                                                        public_key_file=public_key_file))

def valid_cert_text(cert_text):
    """
    Validate the text of the certificate
    """
    cert_lines = cert_text.split("\n")    
    certificate_not_expired = False
    certificate_has_dns = False

    for index, line in enumerate(cert_lines):
        if line.strip().startswith("Not After"):
            def parse_time(text):
                """Not After : Oct 31 23:59:59 2015 GMT"""
                expiry_time_text = text.partition(":")[-1].strip()
                expiry_datetime = datetime.strptime(expiry_time_text,"%b %d %H:%M:%S %Y GMT")
                if datetime.utcnow() < expiry_datetime:
                    return True
                else:
                    return False
            certificate_not_expired = parse_time(line)            
        if line.strip().startswith("X509v3 Subject Alternative Name:"):
             certificate_has_dns = cert_lines[index+1].strip() == "DNS:echo-api.amazon.com"

    return (certificate_not_expired and certificate_has_dns)
         


            
