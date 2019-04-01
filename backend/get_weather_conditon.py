# Stardew Dev Tour Demo
# stardew_api

import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', 'us-east-2')
table_users = dynamodb.Table('stardew_weather_state')

def lambda_handler(event, context):
    channel_id = event['queryStringParameters']['channel_id']
    change = False
    weather_condition = 0


    response_dynamo = table_users.get_item(Key={'channel_id': channel_id})

    if 'Item' not in response_dynamo:
        table_users.put_item(Item={
        'channel_id': channel_id,
        'change': False,
        'weather_condition': 0,
        'vote_id': 0
        })
    else:
        change = response_dynamo['Item']['change']
        weather_condition = int(response_dynamo['Item']['weather_condition'])

    resp = {
        'channel_id': channel_id,
        'change': change,
        'weather_condition': weather_condition
    }

    return {
        'statusCode': 200,
        'body': json.dumps(resp)
    }
