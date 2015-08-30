import os
from base64 import b64encode
import json
import urllib.request as request
from github import Github
import boto3

def getNewToken():
	random_bytes = os.urandom(64)
	token = b64encode(random_bytes).decode('utf-8')
	token = token[:64]
	return token

client = boto3.client('ec2')


response = client.describe_security_groups(
	Filters=[
		{
			'Name': 'tag-value',
			'Values': [
				'frontend'
			]
		}
	]
)


securityGroupId = response['SecurityGroups'][0]['GroupId']
print("SECURITY GROUP: ", response)
print()

response = client.describe_images(
    DryRun=False,
    Owners=[
        'self',
    ],
    Filters=[
        {
            'Name': 'name',
            'Values': [
                'TESTING2',
            ]
        },
    ]
)

print("Image ID: ", response['Images'][0]['ImageId'])
print()

print("Instance Description: ", response)
print()
#'t1.micro'|'m1.small'|'m1.medium'|'m1.large'|'m1.xlarge'|'m3.medium'|'m3.large'|'m3.xlarge'|'m3.2xlarge'|'m4.large'|'m4.xlarge'|'m4.2xlarge'|'m4.4xlarge'|'m4.10xlarge'|'t2.micro'|'t2.small'|'t2.medium'|'t2.large'|'m2.xlarge'|'m2.2xlarge'|'m2.4xlarge'|'cr1.8xlarge'|'i2.xlarge'|'i2.2xlarge'|'i2.4xlarge'|'i2.8xlarge'|'hi1.4xlarge'|'hs1.8xlarge'|'c1.medium'|'c1.xlarge'|'c3.large'|'c3.xlarge'|'c3.2xlarge'|'c3.4xlarge'|'c3.8xlarge'|'c4.large'|'c4.xlarge'|'c4.2xlarge'|'c4.4xlarge'|'c4.8xlarge'|'cc1.4xlarge'|'cc2.8xlarge'|'g2.2xlarge'|'cg1.4xlarge'|'r3.large'|'r3.xlarge'|'r3.2xlarge'|'r3.4xlarge'|'r3.8xlarge'|'d2.xlarge'|'d2.2xlarge'|'d2.4xlarge'|'d2.8xlarge',

imageId = response['Images'][0]['ImageId']

launchToken = getNewToken()
print("Launch Token: ", launchToken)

response = client.run_instances(
    DryRun=True,
    ImageId=imageId,
    MinCount=1,
    MaxCount=1,
    KeyName='MS_Test',
    SecurityGroupIds=[
        securityGroupId,
    ],
    UserData='echo loggin in',
    InstanceType='t1.micro',
    Placement= {
        'AvailabilityZone': 'us-west-1a',
        'Tenancy': 'default'
    },
    Monitoring={
        'Enabled': False
    },
    DisableApiTermination=False,
    InstanceInitiatedShutdownBehavior='stop',
    ClientToken=launchToken,
)




quit()

f = open("password.txt", "r")

password = f.readlines()[0]

g = Github("connorgorman", password)

repo_name = "Webhook"

repository = g.get_user().get_repo(repo_name)
    
hook_name = "test"
config = {"url": "http://example.com/webhook"}
events = [ "push"]
active = True

hook = repository.create_hook(name="web", config=config, events=events, active=active)

print(hook)
