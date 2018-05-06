import boto3
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
athena  = boto3.client('athena')

with open(sys.argv[1], 'r') as f:
    result = athena.start_query_execution(
        QueryString = f.read(),
        QueryExecutionContext = {
            'Database': 'codeforces_analysis'
        },
        ResultConfiguration = {
            'OutputLocation': 's3://codeforces-analysis/athena/'
        }
    )
    logger.info(result)
