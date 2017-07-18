'''
This is lambda function which responds to the GreetUser intent (When the user typs Hi, Hello, etc..)
'''

def lambda_handler(event, context):
    response = {
        'sessionAttributes': None,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
             'message' : {'contentType': 'PlainText','content': 'Hi. I am here to help you with recharge of mobile numbers.'}
        }
    }

    return response