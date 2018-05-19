import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('sqs')
SQS_URL = os.getenv('SQS_URL')

def push(item):
    client.send_message(
        QueueUrl=SQS_URL,
        MessageBody=json.dumps(item)
        )

def handler(event, context):
    push({
        'contest_id': 123
    })
    return 'OK'
