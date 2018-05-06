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
        # "lastName", "country", "lastOnlineTimeSeconds", "city", "rating",
        # "friendOfCount", "titlePhoto", "handle", "avatar", "firstName",
        # "contribution", "organization", "rank", "maxRating",
        # "registrationTimeSeconds", "maxRank"
        chunk.append({
            'user_country': s.get('country'),
            'user_city': s.get('city'),
            'user_rating': s['rating'],
            'user_friend_count': s['friendOfCount'],
            'user_name': s['handle'],
            'user_contribution': s['contribution'],
            'user_organization': s.get('organization'),
            'user_rank': s['rank'],
            'user_registration_time': s['registrationTimeSeconds'],
            'user_max_rank': s['maxRank']
        })

        if len(chunk) >= 500:
            yield chunk
            chunk = []

    if len(chunk) > 0:
        yield chunk

    return ()

def handler(event, context):
    url = 'http://codeforces.com/api/user.ratedList'
    logger.info('GET: {}'.format(url))
    res = requests.get(url)

    for chunk in parse(res.text):
        firehose.put_record_batch(
            DeliveryStreamName='codeforces-analysis-users',
            Records=[{ 'Data': json.dumps(status) + "\n" } for status in chunk]
        )

    return 'OK'
