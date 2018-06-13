import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.getenv('DYNAMODB_TABLE')

def push(item):
    t = dynamodb.Table(TABLE_NAME)
    t.put_item(
        Item=item
    )

def handler(event, context):
    return 'OK'
