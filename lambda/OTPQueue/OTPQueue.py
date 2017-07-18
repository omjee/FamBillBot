"""
This is a lamda function for reading from the SQS and return the latest message.
"""

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def readFromQueue(queueName):
    messageText = ''
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=queueName)
        messages = queue.receive_messages(WaitTimeSeconds=20)
        # Process messages
        for message in messages:
            messageText = message.body
            logger.debug("message text = "+ messageText)
    
            #Let the queue know that the message is processed
            message.delete()
    except:
        logger.debug('Inside exception block')
        
    return messageText

def lambda_handler(event, context):
    #Get queueName from event
    queueName = ''
    return readFromQueue('DelayQueue.fifo')