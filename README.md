# ask-alexa-pykit

Version 0.3

Super simple Python starter code for developing apps for the Amazon Echo's  SDK - ASK:  Alexa Skills Kit.
Check the scripts in the scripts folder for utility code on how to get started with building the config files used by the ASK.
Run ./install.sh to download the python dependencies needed for this project. Currently the install.sh script is designed for a Ubuntu style Linux platform, but take a look inside, porting it over to Mac or Windows should be pretty trivial if you have python installed. 

Check out https://github.com/anjishnu/ask-alexa-pykit/blob/master/EC2_setup_tutorial.md for instructions on how to deploy this server on an EC2 instance. 

To use this code for your own skill, simply generate training data, security tokens and an intent schema definition using the scripts in the scripts/ folder (note, there's a README in that folder as well) and edit <b>voice_handlers.py</b> to add handler functions for the intents and requests that your skill supports - this should be enough to get started. This package is designed so that you can treat the code in utils, server.py and dialog.py as a black box as far as your application is concerned and work with a simple annotated-function interface.

# What's new?

ask-alexa-pykit is currently at version 0.3
  Latest changes:
- The main changes between v0.2 - v0.3 is the removal of the RequestHandler class, I started finding the design of that class was not very modular and didn't seem to lend itself well to easy use since it would have to be subclassed to add significantly new functionality. Instead I divided up the function of the RequestHandler into 3 simple APIs - the Request, the VoiceHandler function, and the ResponseBuilder.
    
- The Request object contains information about the Alexa request - such as intent, slots, userId etc.
    
- A VoiceHandler function (specified with an annotation) takes a request as an input, performs some arbitrary logic on top of it, and returns a Response.
    
- The ResponseBuilder is an encapsulated way to construct responses for a VoiceHandler. A Response can be constructed by called ResponseBuilder.create_response.
    
- This way each part of the code has an unambiguous responsbility, hopefully leading to an extremely easy API.
    
- I had to do a little magic using the inspect module in dialog.py to make it happen, hopefully the code is not too hard to understand. 
    
- Check out voice handlers for the new way to map a VoiceHandler to an intent - the new Handlers are more like AWS Lambda functions. When writing a new skill, you can simply copy this code, generate the intent schema and fill out some custom functions in the voice_handlers.py file.

Step 1:
-----
Install packages

<b>$ ./install.sh </b>

This command installs any python or linux packages needed by this code to run.

Step 2(a): Generate self-signed certificate
-----------
Generate self signed certificate (Only needed if you don't have a certificate from a valid hosting authority)

<b>
$ cd scripts

$ ./create_self_signed_certs.sh
</b>

This script takes you through the process of generating your own self signed certificate (note: needs openssl)
All you need to have with you are: 2 Letter US state, city, organization, skill name and web facing DNS address.
Remember that if the DNS address you enter here doesn't match your endpoint, your web app will not be able to communicate with Alexa.
Once the setup is complete, the private key and certificate produces are moved to the ask-alexa-pykit/keys folder.

Step 2(b): 
-----------
If you are using a certificate from a pre-authorized certification authority, move your private key to the keys/private-key.pem and certificate to keys/certificate.pem


Step 3: Create a intent schema for your app
----------

<b>
$ python3 generate_intent_schema.py
</b>

This script takes you through the process of generating an intent schema for your app- which defines how Alexa's language understanding system interprets results.
After the process is complete, it asks you whether you the intent schema moved to the appropriate location.

Step 4: Generate training data and upload to Amazon.
--------------
Create a file containing your training examples and upload to Amazon. 
I've created a script which loads in the intent schema and does some validation and prompting while you type utterances, but I haven't played around with it enough to know if it actually helps.

<b>$ python3 generate_training_data.py</b>

This script prompts you to enter valid training data in the format defined by the ASK (https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/defining-the-voice-interface). You toggle through the different intents by pressing enter with blank input. Play around with it and see if you find it intuitive.

Once you are done, this script generates a file called utterance.txt with all your training data in it, ready to be uploaded to your skill: https://developer.amazon.com/edw/home.html#/skills

Step 5: Add your business logic
--------------
Go to <b> voice_handlers.py </b> and add handler functions to the code for your specific request or intent.
This is what a handler function for NextRecipeIntent looks like. Note: a handler function will only be activated when the intent schema in the config/ folder is updated to include the intent it is handling. 

    @VoiceHandler(intent="NextRecipeIntent")
    def call_back_intent_handler(request):
      """
      You can insert arbitrary business logic code here
      """
      return r.create_response(message="Getting Next Recipe ...")



Step 6: Running your code as a server.
--------------
Start the server

<b>
$ sudo python3 server.py
</b>

This launches the cherrypy server to handle the apps. The server generates response handlers automatically from the intent schema.

Look into the code in dialog.py for details on how the intents are handled.

Notes:
--------------
Self signed certificates also cannot be used for app certification and launch.

Credits: Anjishnu Kumar 2015
