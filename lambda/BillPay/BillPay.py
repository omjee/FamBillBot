"""
This is the lamda function that the bot communicates with to get the slot information, to handle intents and return on fulfillment/error.
"""
import math
import dateutil.parser
import datetime
import time
import os
import logging
import requests
import tweepy
import boto3
from base64 import b64decode
import json
import re

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Keys used for OAUTH communication. They have been encrypted using KMS and decrypted for usage
consumer_key_encrypted = os.environ['consumer_key']
consumer_key = boto3.client('kms').decrypt(CiphertextBlob=b64decode(consumer_key_encrypted))['Plaintext'].decode('utf-8')
consumer_secret_encrypted = os.environ['consumer_secret']
consumer_secret = boto3.client('kms').decrypt(CiphertextBlob=b64decode(consumer_secret_encrypted))['Plaintext'].decode('utf-8')
access_token_encrypted = os.environ['access_token']
access_token = boto3.client('kms').decrypt(CiphertextBlob=b64decode(access_token_encrypted))['Plaintext'].decode('utf-8')
access_token_secret_encrypted = os.environ['access_token_secret']
access_token_secret = boto3.client('kms').decrypt(CiphertextBlob=b64decode(access_token_secret_encrypted))['Plaintext'].decode('utf-8')

#The screen name of the twitter account to which direct messsages are sent. In this case, it is the screen name of ICICI bank.
account_screen_name = 'ICICIBank'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

global direct_message
""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """

class DirectMessageStreamListener(tweepy.StreamListener):

    def on_direct_message(self, status):
        logger.debug ('on direct message : status = '+ str(status))
        if hasattr(status, 'direct_message'):
            if status.direct_message ['sender']['screen_name'] == account_screen_name :
             logger.debug ('only from '+account_screen_name)
             logger.debug(status.direct_message['text'])
             direct_message = status.direct_message['text']
             logger.debug('[TWITTER] Direct message = '+ direct_message)
             return False
        return True

    def on_error(self, status_code):
        logger.debug ("Error Code: " + str(status_code))
        if status_code == 420:
            return False
        else:
            return True

    def on_timeout(self):
        logger.debug('Timeout...')
        return True


def get_slots(intent_request):
    logger.debug('get_slots')
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    logger.debug('elicit_slot')
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }
    
def respond(err, res=None):
    logger.debug('err = '+ str(err))
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    

def readFromQueue(queueName):
    messageText = ''
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=queueName)
        #Wait for 20 seconds until the messages are in the queue
        messages = queue.receive_messages(WaitTimeSeconds=20)
        # Process messages in the queue
        for message in messages:
            messageText = message.body
            logger.debug("message text = "+ messageText)
            # Let the queue know that the message is processed
            message.delete()
    except:
        logger.debug('Inside exception block')
        
    return messageText
    
def listenToQueue():
    logger.debug('listenToQueue')
    
    messageText = ""
    tries = 0
    queueName = 'OTPQueue.fifo'
    
    #Read OTP from queue - Trial 1
    messageText = readFromQueue(queueName)
    if messageText == "":
        #Read OTP from queue - Trial 2
        messageText = readFromQueue(queueName)
    
    if messageText == "":
        #Read OTP from queue - Trial 3
        messageText = readFromQueue(queueName)

    return messageText
    
# Invoke the EmailSender lambda function
def sendEmail(slots):
    lambda_client = boto3.client('lambda')
    logger.debug('Before sendMail')
    payload = {'mobile_number' : slots['mobileNumber'], 'mobile_operator' : slots['operatorType'], 'amount' : slots['amount']}
    response = lambda_client.invoke(FunctionName='EmailSender',InvocationType='RequestResponse',LogType='Tail', Payload=json.dumps(payload))
    logger.debug('After sendMail ::  response = '+ str(response))
    

def sendToTwitter(slots):
    logger.debug('sendToTwitter')
    api = tweepy.API(auth)

    # Get the User object for twitter...
    user = api.get_user(account_screen_name)
    # Send #genotp direct message to twitter
    api.send_direct_message(screen_name=user.screen_name, text="#genotp")

    otp = listenToQueue()
    if otp == "":
        logger.debug('OTP is empty')
        raise ValueError("Request processing failed")
    
    reponse_message = ''
    
    # Populate the #TopUp command with information from the slots
    topup_text="#TopUp "+slots['mobileNumber']+" "+slots['operatorType'].upper()+" "+slots['amount']+" " +otp
    logger.debug('topup transaction triggering = '+ topup_text)
    
    # Send #TopUp direct message to twitter
    api.send_direct_message(screen_name=user.screen_name, text=topup_text)

    lambda_client = boto3.client('lambda')
    #Wait for the response from topup action
    response = lambda_client.invoke(FunctionName='OTPQueue',InvocationType='RequestResponse',LogType='Tail')
    response = lambda_client.invoke(FunctionName='OTPQueue',InvocationType='RequestResponse',LogType='Tail')
    
    response = lambda_client.invoke(FunctionName='DirectMessage',InvocationType='RequestResponse',LogType='Tail')
    logger.debug('DirectMessage :: response = '+ str(response))
    reponse_message = str(response['Payload'].read(),'utf-8')
    logger.debug('payload response = ' + response_message)

    #Handle error from twitter
    error_keywords = ['Error', 'Failed', 'Invalid']
    for word in words:
        if direct_message.lower().find(word.lower()) != -1:
           raise ValueError("Request processing failed")
           
    return 'Success'


def close(session_attributes, fulfillment_state, message, slots):
    logger.debug('close : '+ str(message))
    try:
        logger.debug('sendToTwitter : before')
        #Send direct messages to twitter
        sendToTwitter(slots)
        #Send email to account owner
        sendEmail(slots)
        logger.debug('sendToTwitter : after')
    except:
        logger.debug('sendToTwitter : In except block')
        message = {'contentType': 'PlainText',
                  'content': 'Sorry, your request could not be processed at the moment. Please try again.'}
	
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    logger.debug('delegate : '+ str(slots))
    
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

def validate_mobile_recharge(mobile_number, operator_type, amount):
    logger.debug('validate_mobile_recharge')
    operator_types = ['airtel', 'aircel', 'bsnl','idea','mts','vodafone', 'docomo']

    #Validate operator type
    if operator_type is not None and operator_type.lower() not in operator_types:
        return build_validation_result(False,
                                       'operatorType',
                                       'We do not provide services to the {} operator. Please enter a valid operator type.'.format(operator_type))
    
    #Validate mobile number
    if mobile_number is not None and re.match('^[0]?[789]\d{9}$', mobile_number) is None:
       return build_validation_result(False,
                                      'mobileNumber',
                                      'Please enter a valid mobile number.')
    #Validate recharge amount
    if amount is not None and not 1 <= int(amount) <= 1000:
        return build_validation_result(False,
                                      'amount',
                                      'Please enter an amount between 1 and 1000.')
    
    return build_validation_result(True, None, None)

# The function which contains the actions to be peformed for the MobileRecharge intent
def mobile_recharge(intent_request):
    logger.debug('mobile_recharge')
    mobile_number = get_slots(intent_request)["mobileNumber"]
    operator_type = get_slots(intent_request)["operatorType"]
    amount = get_slots(intent_request)["amount"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        validation_result = validate_mobile_recharge(mobile_number, operator_type, amount)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        return delegate(output_session_attributes, get_slots(intent_request))
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Thanks, your {} mobile number {} has been recharged successfully.'.format(operator_type, mobile_number)}, get_slots(intent_request))


""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('intent_request = '+ str(intent_request))
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'MobileRecharge':
        return mobile_recharge(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)