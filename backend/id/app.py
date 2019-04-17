# Stardew Dev Tour Demo

import json
import os
import boto3


def get_env_var(name):
    return os.environ[name] if name in os.environ else None


WEATHER_TABLE_NAME = get_env_var('WEATHER_TABLE')

dynamodb = boto3.resource('dynamodb', get_env_var('AWS_REGION'))
table_users = dynamodb.Table(WEATHER_TABLE_NAME)


def lambda_handler(event, context):
    channel_id = event['queryStringParameters']['channel_id']
    response_dynamo = table_users.get_item(Key={'channel_id': channel_id})

    vote_id = str(response_dynamo['Item']['vote_id'])
    resp = {
        'vote_id': vote_id
    }
    return {
        'statusCode': 200,
        'body': json.dumps(resp),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
