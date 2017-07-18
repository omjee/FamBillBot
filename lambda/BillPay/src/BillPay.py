"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages orders for flowers.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'OrderFlowers' template.

For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""
import math
import dateutil.parser
import datetime
import time
import os
import logging
import requests
import tweepy

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

consumer_key = 'gnWQYpvgBmGgPUPliwRj1kYbD'
consumer_secret = 'SqbSYwzG3Q3QSx9A0IP44Smqb8y0GK1GRNvzxpoL3w3GDUy4zk'
access_token = '208709888-ukeJxxZ7IgDM2wmAZhDRfjgOq5yuI6828NHlndBH'
access_token_secret = 'QHOkD467d2OPRm0eq20eufZCl2pQOip1VE9179beldzlr'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """

class DirectMessageStreamListener(tweepy.StreamListener):
    # def __init__(self):
    #     super(tweepy.StreamListener, self).__init__()
    #     self.status_count = 0

    def on_direct_message(self, status):
        logger.debug ('on direct message')
        if hasattr(status, 'direct_message'):
            if status.direct_message ['sender']['screen_name'] == account_screen_name :
             logger.debug ('only from '+account_screen_name)
             logger.debug(status.direct_message['text'])
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

def sendToTwitter():

    api = tweepy.API(auth)
    # Get the User object for twitter...
    # pass the user screen name
    user = api.get_user('ICICIBank')

    # api.send_direct_message(user.screen_name,"Hi "+user.screen_name+" this is from python code")
    api.send_direct_message(screen_name=user.screen_name, text="#genotp")
    listener = DirectMessageStreamListener()
    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, listener)
    stream.userstream()

def close(session_attributes, fulfillment_state, message):
    #logger.debug('close')
    #url = 'https://api.webmethodscloud.com/abs/apirepository/apis?tenant=rndapicloud'
    #headers = {"Accept": "application/json", "Authorization" : "Basic dGVzdGFkbWluOnRlc3RhZG1pbg=="}
    #apiResponse = requests.get(url, headers= headers)
    #logger.debug("apiResponse = "+ str(apiResponse))
    sendToTwitter()
	
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
    logger.debug('delegate')
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


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


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def validate_mobile_recharge(mobile_number, operator_type):
    logger.debug('validate_mobile_recharge')
    operator_types = ['Airtel', 'Vodafone', 'BSNL']
    if operator_type is not None and operator_type.lower() not in operator_types:
        return build_validation_result(False,
                                       'operatorType',
                                       'We do not provide services to the {} operator.'.format(operator_type))
    #TODO validate mobile number
    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def mobile_recharge(intent_request):
    """
    Performs dialog management and fulfillment for ordering flowers.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """
    logger.debug('mobile_recharge')
    mobile_number = get_slots(intent_request)["mobileNumber"]
    operator_type = get_slots(intent_request)["operatorType"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        validation_result = validate_mobile_recharge(mobile_number, operator_type)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        #if flower_type is not None:
            #output_session_attributes['Price'] = len(flower_type) * 5  # Elegant pricing model

        return delegate(output_session_attributes, get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Thanks, your mobile number {} of network {} has been recharged successfully.'.format(mobile_number, operator_type)})


""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

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
    for record in event.Records:
        logger.debug(record.dynamodb.Keys.username)
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    #time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)