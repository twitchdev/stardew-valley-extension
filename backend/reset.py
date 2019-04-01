
import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', 'us-east-2')
table_users = dynamodb.Table('stardew_weather_state')

def lambda_handler(event, context):

    event_body = json.loads(event['body'])

    try: 
        weather_changed = event_body['weather_changed']
        channel_id = str(event_body['channel_id'])
    except:
        print('error')
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }

    table_users.update_item(Key={'channel_id': channel_id},
                            UpdateExpression='SET change = :val1',
                            ExpressionAttributeValues={':val1': False})
    return {
        'statusCode': 200,
        'body': json.dumps('Succesfully changed')
    }
