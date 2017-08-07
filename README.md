# ask-alexa-pykit

Release Version : <b>Master</b> (Unstable! For a stable release, check out the 0.5.6 branch)

ask-alexa-pykit 0.5 is out!

A minimalist framework for developing apps (skills) for the Amazon Echo's  SDK: The Alexa Skills Kit (<b>ASK</b>).

<b>What does this library do?</b>
- Remove boiler plate from Alexa Skills Kit Code - maps intents directly to their handler functions.
- Provide utils to quickly and effectively generate and manipulate sample utterances and the intent schema. 
- Provides python objects to quickly build alexa responses. 
- Automatic session management using session variables - your code gets access to a really simple interface for session management, you just add key value pairs to, or delete things from, a python dictionary, and this library along with the ASK platform takes care of the rest. 

To use this code for your own skill, simply generate training data, and an intent schema definition and edit <b>lambda_function.py</b> to add handler functions for the intents and requests that your skill supports - this should be enough to get started.

<b>Note</b>: Unless someone asks me to reconsider - I am now only going to do further releases of this library for AWS Lambda - the core library is concise enough that it can be included into any python server framework with just a few imports. The old releases (for cherrypy) will contain the infuriating request validation parts of the library which can be useful for people who don't want to use the Lambda or LambdaProxy approach to skill development.

# What's new?

  Latest changes:

-  There's a <b>pypi repo</b> now https://pypi.python.org/pypi/ask-alexa-pykit/ - so you should be able to do `pip install ask-alexa-pykit` to use 'ask' as a standard python library or `pip install ask-alexa-pykit --target new_skill_folder` to install it into a directory (which will be your AWS Lambda Function directory). 

- Added an actual intent_schema.py module - thin wrapper around the JSON object which allows for easy manipulation, creation and serialization/deserialization. This module also doubles as the generate intent schema script now, with hooks to interactively generate the object. 

- The scripts folder is gone now - and the scripts themselves have been moved into the main alexa.ask module, which means that they can stay in sync with the Intent Schema and other config parameters without much fuss.

- The annotation API has changed (become simpler) and the intent map computation and routing now happens under the hood. As of version 0.4 the VoiceHandler object now maintains an internal mapping of handler functions and now takes on the responsibility of handing off incoming requests to the right function end point.

- Now there's only one module that a user has to be aware of. We've fully factored out the alexa specific bits into the <b>ask</b> library and you don't need to see how the mappings are computed.

- The Request class got a minor upgrade - the addition of a 'metadata' field, which allows the developer to easily extend code to inject session, user or device specific metadata (after, for instance, querying a database) into a request object before it gets passed to the annotated handler functions. 

- The interface to the ask library function is now uniformly exposed to developers. A voice handler is now a subclass of a ResponseBuilder so that as a user all your really need to do is `from ask import alexa`

- Improved session handling - no need to pass back the session attributes - just edit them in the dict and they'll automatically get propogated.

- Python 2/3 dual compatibility

Basic overview of Classes:

- The Request object contains information about the Alexa request - such as intent, slots, userId etc.

- A VoiceHandler is an object that internally stores a mapping from intents and requests to their corresponding handler functions. These mappings are specified by a simple annotation scheme (see <b>lambda_function.py</b> for an example)

- An alexa (VoiceHandler) annotated class (specified with an annotation) takes a request as an input, performs some arbitrary logic on top of it, and returns a Response.
    
- The ResponseBuilder is an encapsulated way to construct responses for a VoiceHandler. A Response can be constructed by called ResponseBuilder.create_response.


Step 1: Download Code
-----------

Method 1:

<b>$ git clone https://github.com/anjishnu/ask-alexa-pykit.git </b>

Make sure you're in a python lambda release branch. E.g

<b>
$ cd ask-alexa-pykit
<br>
$ git checkout python_lambda_0.5_release </b>
<br>
Otherwise your build my be broken since the master branch is not always stable. 
<br>
Method 2:
<br>
<b>
$ mkdir my_new_skill
<br>
$ pip install ask-alexa-pykit --target my_new_skill 
<br>
</b>

ask-alexa-pykit is now installed in your <b>my_new_skill</b> directory. Just import the library and start hacking. 

Step 2: Create a intent schema for your app
----------
Skip this if you're trying the included basic example and use  <b>sample_intent_schema.json</b> as your <b>INTENT_SCHEMA</b>.

<br><b>
$ python -m ask.intent_schema -i FILEPATH
</b>

This script takes you through the process of generating an intent schema for your app- which defines how Alexa's language understanding system interprets results.
After the process is complete, it asks you whether you the intent schema stored at the appropriate location.

Step 3: Generate training data and upload to Amazon.
--------------

3(a):
Create a file containing your training examples and upload to Amazon.
I've created a script which loads in the intent schema and does some validation and prompting while you type utterances, but I haven't played around with it enough to know if it actually helps.
<br>
<b>$ python -m ask.write_sample -i INTENT_SCHEMA -o TRAINING_DATA_OUTPUT_LOCATION</b>
<br>
This script prompts you to enter valid training data in the format defined by the ASK (https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/defining-the-voice-interface). You toggle through the different intents by pressing enter with blank input. Play around with it and see if you find it intuitive.

3(b):
Once you are done, this script generates a file called utterance.txt with all your training data in it, ready to be uploaded to your skill: https://developer.amazon.com/edw/home.html#/skills

Step 4: Add your business logic
--------------

Skip this if you're just trying to run the included basic example.

Go to <b> lambda_function.py </b> and add handler functions to the code for your specific request or intent.
This is what a handler function for NextRecipeIntent looks like. 

    @alexa.intent("NextRecipeIntent")
    def next_recipe_intent_handler(request):
      """
      You can insert arbitrary business logic code here
      """
      return alexa.create_response("Getting Next Recipe ...")

Step 5: Package your code for Lambda
----------------

Package the code folder for AWS Lambda. Detailed instructions are here: http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

For the basic  example included in the package simply zip the folder:
<b>
<br>
$ cd ask-alexa-pykit
<br>
$ zip -r ask-lambda.zip *
</b>

Step 6: Create a Lambda Function
-----
- Go to <b>console.aws.amazon.com</b>
- Click on Lambda
- Select [Virgina] on the top right. (ASK source is only available in Virginia)
- Click on Create Lambda Function
- Skip the Select Blueprint Section
- In the configure step: choose a name e.g. alexa-pykit-demo
- Choose Runtime as Python 2.7
- Code Entry Type - Upload a zip file.
- Upload ask-lambda.zip
- For Role : create a new basic execution role
- Press Next, and then Create Function
- In the event source configuration pick event source type - Alexa Skills Kit.

Step 7: Associate Lambda Function with Alexa Skill
------
Add the ARN code for the Lambda Function you've just created as the Lambda ARN (Amazon Resource Name) Endpoint in the Skill Information tab of your skill's information on https://developer.amazon.com/edw/home.html#/skills/list

Note an ARN code is at the top of you Lambda page and starts with something like: <b>arn:aws:lambda:us</b>...


Contributing
---------------

- The master branch is meant to be stable. I usually work on unstable stuff on a personal branch.
- Fork the master branch ( https://github.com/[my-github-username]/ask-alexa-pykit/fork )
- Create your branch (git checkout -b my-branch)
- Commit your changes (git commit -am 'added fixes for something')
- Push to the branch (git push origin my-branch)
- Create a new Pull Request
- And you're done!

- Bug fixes, bug reports and new documentation are all appreciated!

Projects that use this library
--------------

- Rap Battle Alexa - http://devpost.com/software/rapbattlealexa
- Twitter Reader (Official Twitter Skill for Alexa)
- How much is it worth - https://www.hackster.io/minus-et-cortex/how-much-it-worth-07e190
- Useful Science 
- University of Pennsylvania, Deep Learning Methods for Automated Discourse - (http://dialog-systems-class.org/assignment1.html) 

If this library helps you build some dialog systems or do some interesting research - please remember to cite it! 

```
  @Misc{kumarask2015,
  author =   {Anjishnu Kumar},
  title =    {ASK Alexa PyKit},
  howpublished = {\url{github.com/anjishnu/ask-alexa-pykit}},
  year = {2015}
  }
```
Let me know if you know any other projects that use or build on top of ask-alexa-pykit.

Credits: Anjishnu Kumar 2015
