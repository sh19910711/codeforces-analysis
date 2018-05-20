import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('sqs')
SQS_URL = os.getenv('SQS_URL')
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.getenv('DYNAMODB_TABLE')

def pop():
    res = client.receive_message(QueueUrl=SQS_URL)
    if 'Messages' in res:
        client.delete_message(
            QueueUrl=SQS_URL,
            ReceiptHandle=res['Messages'][0]['ReceiptHandle'])
        return json.loads(res['Messages'][0]['Body'])

def handler(event, context):
    item = pop()
    if item:
        logger.info('pop: {}'.format(json.dumps(item)))
        t = dynamodb.Table(TABLE_NAME)
        t.put_item(
            Item=item
        )
    return 'OK'
