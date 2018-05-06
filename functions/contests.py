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
    for s in ret['result']:
        chunk.append({
            'contest_id': s['id'],
            'contest_name': s['name'],
            'contest_type': s['type'],
            'contest_phase': s['phase'],
            'contest_duration': s['durationSeconds'],
            'contest_start_time': s['startTimeSeconds']
        })

        if len(chunk) >= 500:
            yield chunk
            chunk = []

    if len(chunk) > 0:
        yield chunk

    return ()

def handler(event, context):
    url = 'http://codeforces.com/api/contest.list'
    logger.info('GET: {}'.format(url))
    res = requests.get(url)

    for chunk in parse(res.text):
        firehose.put_record_batch(
            DeliveryStreamName='codeforces-analysis-contests',
            Records=[{ 'Data': json.dumps(status) + "\n" } for status in chunk]
        )

    return 'OK'
