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
            'status_id': s['id'],
            'contest_id': s['contestId'],
            'create_time': s['creationTimeSeconds'],
            'relative_time': s['relativeTimeSeconds'],
            'problem_index': s['problem']['index'],
            'user_name': s['author']['members'][0]['handle'],
            'participant_type': s['author']['participantType'],
            'language': s['programmingLanguage'],
            'verdict': s.get('verdict'),
            'testset': s['testset'],
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

def handler(event, context):
    contest_id = event['Records'][0]['dynamodb']['Keys']['contest_id']['N']

    version = firehose.describe_delivery_stream(DeliveryStreamName='codeforces-analysis-submissions')['DeliveryStreamDescription']['VersionId']
    firehose.update_destination(
        DeliveryStreamName='codeforces-analysis-submissions',
        CurrentDeliveryStreamVersionId=version,
        DestinationId='destinationId-000000000001',
        S3DestinationUpdate={
            'Prefix': 'data/parquet/submissions/'
        })

    url = 'http://codeforces.com/api/contest.status?contestId={}&from=1&count=100000'.format(contest_id)
    logger.info('GET: {}'.format(url))
    res = requests.get(url)

    for chunk in parse(res.text):
        firehose.put_record_batch(
            DeliveryStreamName='codeforces-analysis-submissions',
            Records=[{ 'Data': json.dumps(status) + "\n" } for status in chunk]
        )

    return 'OK'
