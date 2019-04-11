import decimal
import json
import os
import boto3

from boto3.dynamodb.conditions import Key

def get_env_var(name):
    return os.environ[name] if name in os.environ else None


VOTE_TABLE_NAME = get_env_var('VOTE_TABLE')
WEATHER_TABLE_NAME = get_env_var('WEATHER_TABLE')

dynamodb = boto3.resource('dynamodb', get_env_var('AWS_REGION'))
votes_table = dynamodb.Table(VOTE_TABLE_NAME)
table_weather_state = dynamodb.Table(WEATHER_TABLE_NAME)

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
    table_weather_state.update_item(Key={'channel_id': channel_id},
                                    UpdateExpression='SET change = :val1, weather_condition = :val2 ',
                                    ExpressionAttributeValues={':val1': True, ':val2': winning_weather})

    return {
        'statusCode': 200,
        'body': json.dumps({'winning_weather': winning_weather}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }


# helper
def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
