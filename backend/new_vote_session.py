import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', 'us-east-2')
table_users = dynamodb.Table('stardew_weather_state')

def lambda_handler(event, context):
    
    channel_id = event['queryStringParameters']['channel_id']
    
    
    resp = table_users.update_item(
        Key={'channel_id': channel_id},
        UpdateExpression="ADD vote_id :incr",
        ExpressionAttributeValues={":incr": 1},
        ReturnValues="ALL_NEW"
    )
    
    new_vote_id= int(resp['Attributes']['vote_id'])

    return {
        'statusCode': 200,
        'body': json.dumps({'new_vote_id': new_vote_id}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*'
        }
    }
