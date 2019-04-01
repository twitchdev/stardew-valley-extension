import json
import boto3
import decimal

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from operator import itemgetter

dynamodb = boto3.resource('dynamodb', 'us-east-2')
votes_table = dynamodb.Table('stardew_votes')
table_weather_state = dynamodb.Table('stardew_weather_state')

winning_weather = ''

def lambda_handler(event, context):
    
    channel_id = event['queryStringParameters']['channel_id']
    vote_id = str(event['queryStringParameters']['vote_id'])
    
    all_votes = votes_table.query(
        KeyConditionExpression=Key('channel_vote').eq(channel_id + ":" + vote_id)
    )

    sorted_votes = sorted(all_votes['Items'], key=lambda x: x['votes'], reverse=True)
    if len(sorted_votes) > 0:
        winning_weather = int(sorted_votes[0]['vote_item'])
    else:
        return {
        'statusCode': 500,
        'body': 'Error'
    }
        
    
    # set weather update to true
    table_weather_state.update_item(Key={'channel_id': channel_id},UpdateExpression='SET change = :val1, weather_condition = :val2 ',ExpressionAttributeValues={':val1': True, ':val2': winning_weather})
    

    return {
        'statusCode': 200,
        'body': json.dumps({'winning_weather': winning_weather}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*'
        }
    }

# helper
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
