import boto3
from botocore.vendored import requests
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
firehose = boto3.client('firehose')

def fetch(path):
    return requests.get('http://codeforces.com/api/{}'.format(path))

def parse_contest_submissions(text):
    ret = json.loads(text)
    
    if ret['status'] != 'OK':
        raise 'ERROR: api status = {}'.format(ret['status'])

    chunk = []
    for s in ret['result']:
        chunk.append({
            'status_id': s['id'],
            'contest_id': s['contestId'],
            'create_time': s['creationTimeSeconds'],
            'relative_time': s['relativeTimeSeconds'],
            'problem_index': s['problem']['index'],
            'user_name': s['author']['members'][0]['handle'],
            'language': s['programmingLanguage'],
            'verdict': s['verdict'],
            'participant_type': s['participantType'],
            'passed_test_count': s['passedTestCount'],
            'execution_time': s['timeConsumedMillis'],
            'execution_memory': s['memoryConsumedBytes']
        })
        if len(chunk) >= 500:
            yield chunk
            chunk = []

    if len(chunk) > 0:
        yield chunk

    return ()

def put_firehose(stream, records):
    firehose.put_record_batch(
        DeliveryStreamName='codeforces-analysis-{}'.format(stream),
        Records=[{'Data': record} for record in records]
    )

def handler(event, context):
    contest_id = event['Records'][0]['dynamodb']['Keys']['contest_id']['N']
    logger.info('fetch: contest_id = {}'.format(contest_id))

    res = fetch('contest.status?contestId={}&from=1&count=100000'.format(contest_id))
    for chunk in parse_contest_submissions(res.text):
        put_firehose('contest-submissions', [json.dumps(status) + "\n" for status in chunk])
    return 'Hello'
