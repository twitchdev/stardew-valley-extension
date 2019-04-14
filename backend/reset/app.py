
import json
import os
import boto3


def get_env_var(name):
    return os.environ[name] if name in os.environ else None


TABLE_NAME = get_env_var('WEATHER_TABLE')

dynamodb = boto3.resource('dynamodb', get_env_var('AWS_REGION'))
table_users = dynamodb.Table(TABLE_NAME)


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
