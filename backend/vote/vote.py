# Stardew Dev Tour Demo
import json
import os
import boto3


def get_env_var(name):
    return os.environ[name] if name in os.environ else None


VOTE_TABLE_NAME = get_env_var('VOTE_TABLE')
VIEWERS_TABLE_NAME = get_env_var('VIEWERS_TABLE')

dynamodb = boto3.resource('dynamodb', get_env_var('AWS_REGION'))
votes_table = dynamodb.Table(VOTE_TABLE_NAME)
viewers_table = dynamodb.Table(VIEWERS_TABLE_NAME)


def lambda_handler(event, context):
    return_message = 'Vote recorded'
    event_body = json.loads(event['body'])
    try: 
        user_id = event_body['user_id']
        channel_id = str(event_body['channel_id'])
        vote_id = str(event_body['vote_id'])
        vote_item = str(event_body['vote_item'])
    except:
        print('Error')
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }
    try:
        resp = viewers_table.update_item(
            Key={"user_id": user_id, "channel_vote": channel_id + ":" + vote_id},
            UpdateExpression="SET vote_item = :vote_item",
            ExpressionAttributeValues={":vote_item": vote_item},
            ReturnValues="UPDATED_OLD"
        )
    except ClientError as e:
        print("There was an error: ", e)

    previous_vote = resp.get('Attributes', {}).get('vote_item')

    # Decrement the previous vote if it existed
    if previous_vote:
        # check if user is voting with same previous vote
        if previous_vote == vote_item:
            return
        try:
            votes_table.update_item(
                Key={"channel_vote": channel_id + ":" + vote_id, 'vote_item': previous_vote},
                UpdateExpression="ADD votes :incr",
                ExpressionAttributeValues={":incr": -1},
            )
        except ClientError as e:
            print("There was an error: ", e)
        return_message = 'Changed your vote'
  
    # we always add the new vote in
    try:
        votes_table.update_item(
            Key={'channel_vote': channel_id + ":" + vote_id, 'vote_item': vote_item},
            UpdateExpression="ADD votes :incr",
            ExpressionAttributeValues={":incr": 1},
            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        print("There was an error: ", e)

    return {
        'statusCode': 200,
        'body': json.dumps(return_message),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*'
        }
    }
