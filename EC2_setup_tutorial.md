Setting up ask-alexa-pykit on an EC2 instance
----

1. Go to console.aws.amazon.com

2. Click on EC2

3. Click on Launch Instance

4. Matter of taste here
          Choose Ubuntu (I tested on this, it should work on others as well)
          Choose T2.micro (or higher if you’d like)
          Click review and launch

5. Check your security group settings:
          If you are new to this sort of thing, make sure your security group setting says this:
          Type     Protocol     port range     source
          All     All           All            0.0.0.0/0
          Create a new security group if you have to - this allows any IP to access your host if they have the right credentials. 
          If you are more well versed with web protocols then alter the security settings to make the server more secure.
          Click ‘launch'

6.        You’ll be asked to choose an existing key pair or make a new one. 
          Pick whatever you want. (Let’s call that key “askkey.pem")
          Click Launch

Your EC2 instance is now launching. 

7.        Click View Instances.
          Wait for the EC2 instance to launch.
          Copy the public IP or DNS somewhere (I’ll call it $DNS)

Now we need to set up the skill:

8.        First SSH into your host. 

<b>$ chmod 700 askkey.pem</b>  

(Otherwise AWS will complain that your permissions are too lax and refuse to let you SSH into the box you just launched)

<b>$ ssh -i /path/to/askkey.pem ubuntu@$DNS</b>

Congrats! You are now in your host

9.        Install git:        

<b>$ sudo apt-get install git</b>

10.       Install ask-alexa-pykit       

<b>$ git clone https://github.com/anjishnu/ask-alexa-pykit.git</b>

Follow the instructions in the README.

11.       Upload your intent schema and training utterances to the Amazon website. 
          Go to https://developer.amazon.com/edw/home.html#/skills and Click ‘add a new skill'

          a. In Skill Information
                    Fill out the miscellaneous information
                    Enter the DNS address in 'endpoint'
                    Press Next

          b. In Interaction Model
                    paste the contents intent_schema.json in the Intent Schema box.
                    paste the contents of utterances.txt in Sample Utterances.
                    Press Next

          c. In SSL Certificate:
                    Copy and paste the contents keys/private-key.pem
                    Press Next

Congratulations - your skill is now ready to be tested!
