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

    resp = table_users.update_item(
        Key={'channel_id': channel_id},
        UpdateExpression="ADD vote_id :incr",
        ExpressionAttributeValues={":incr": 1},
        ReturnValues="ALL_NEW"
    )

    new_vote_id = int(resp['Attributes']['vote_id'])

    return {
        'statusCode': 200,
        'body': json.dumps({'new_vote_id': new_vote_id}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
