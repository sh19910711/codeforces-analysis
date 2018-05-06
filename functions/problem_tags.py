import boto3
from botocore.vendored import requests
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
firehose = boto3.client('firehose')

def parse(text):
    ret = json.loads(text)

    if ret['status'] != 'OK':
        raise 'ERROR: api status = {}'.format(ret['status'])

    chunk = []
    for s in ret['result']['problems']:
        # "contestId", "index", "name", "type", "tags"
        for t in s['tags']:
            chunk.append({
                'contest_id': s['contestId'],
                'problem_index': s['index'],
                'problem_tag': t
            })

            if len(chunk) >= 500:
                yield chunk
                chunk = []

    if len(chunk) > 0:
        yield chunk

    return ()

def handler(event, context):
    url = 'http://codeforces.com/api/problemset.problems'
    logger.info('GET: {}'.format(url))
    res = requests.get(url)

    for chunk in parse(res.text):
        firehose.put_record_batch(
            DeliveryStreamName='codeforces-analysis-problem-tags',
            Records=[{ 'Data': json.dumps(status) + "\n" } for status in chunk]
        )

    return 'OK'
