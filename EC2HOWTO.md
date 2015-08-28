Setting up ask-alexa-pykit on an EC2 instance
----

Go to console.aws.amazon.com

Click on EC2

Click on Launch Instance

#Matter of taste here
Choose Ubuntu (I tested on this, it should work on others as well)

Choose T2.micro (or higher if you’d like)

Click review and launch

Check your security group settings:

If you are new to this sort of thing, make sure your security group setting says this:
          Type     Protocol     port range     source
          All     All           All            0.0.0.0/0

Create a new security group if you have to - this allows any IP to access your host if they have the right credentials. 
If you are more well versed with web protocols then alter the security settings to make the server more secure.

click ‘launch'

You’ll be asked to choose an existing key pair or make a new one. 
Pick whatever you want. (Let’s call that key “askkey.pem")

Click Launch

Your EC2 instance is now launching. 

click View Instances.
Wait for the EC2 instance to launch.
Note down the public IP or DNS (I’ll call it $DNS)

Now we need to set up the skill:

First SSH into your host. 

<b>$ chmod 700 askkey.pem</b>  (Otherwise AWS will complain that your permissions are too lax and refuse to let you SSH into the box you just launched)

<b>$ ssh -i /path/to/askkey.pem ubuntu@$DNS</b>

Congrats! You are now in your host
Install git:

<b>$ sudo apt-get install git</b>

Install ask-alexa-pykit
<b>$ git clone https://github.com/anjishnu/ask-alexa-pykit.git</b>

Follow the instructions in the README.

Upload your intent schema and training utterances to the Amazon website. Go to https://developer.amazon.com/edw/home.html#/skills
Click ‘add a new skill'

In Skill Information
Enter the DNS address in 'endpoint'

In Interaction Model
paste the contents intent_schema.json in the Intent Schema box.
paste the contents of utterances.txt in Sample Utterances.
press Next

In SSL Certificate:
Copy and paste the contents keys/private-key.pem
press Next

Congratulations - your skill is now ready to be tested!
