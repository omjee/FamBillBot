"""
This is a lamda function for reading direct messages.
"""

import tweepy
import boto3
import os
from base64 import b64decode

# Keys used for OAUTH communication. They have been encrypted using KMS and decrypted for usage
consumer_key_encrypted = os.environ['consumer_key']
consumer_key = boto3.client('kms').decrypt(CiphertextBlob=b64decode(consumer_key_encrypted))['Plaintext'].decode('utf-8')
consumer_secret_encrypted = os.environ['consumer_secret']
consumer_secret = boto3.client('kms').decrypt(CiphertextBlob=b64decode(consumer_secret_encrypted))['Plaintext'].decode('utf-8')
access_token_encrypted = os.environ['access_token']
access_token = boto3.client('kms').decrypt(CiphertextBlob=b64decode(access_token_encrypted))['Plaintext'].decode('utf-8')
access_token_secret_encrypted = os.environ['access_token_secret']
access_token_secret = boto3.client('kms').decrypt(CiphertextBlob=b64decode(access_token_secret_encrypted))['Plaintext'].decode('utf-8')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#The screen name of the twitter account to which direct messsages are sent. In this case, it is the screen name of ICICI bank.
account_screen_name = 'ICICIBank'

def parse_only_particular_message(dir_messages):
    return [x for x in dir_messages if x.sender_screen_name == account_screen_name]

def get_recent_message(list_msg):
    recent_txt = ''
    if len(list_msg) > 0:
        recent_txt = list_msg[0].text
    return recent_txt

def lambda_handler(event, context):
    api = tweepy.API(auth)
    #TODO : Pass the last read message sequence ID
    dir_message2 = api.direct_messages(include_entities=False, skip_status=True, count=5, full_text=True)
    list_msg = parse_only_particular_message(dir_message2)
    
    return get_recent_message(list_msg)
