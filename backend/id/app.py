# Stardew Dev Tour Demo

import json
import boto3

dynamodb = boto3.resource('dynamodb', 'us-east-2')
table_users = dynamodb.Table('stardew_weather_state')


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
