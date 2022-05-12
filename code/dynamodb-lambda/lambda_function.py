import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('***')
    
    recognizedKey = event['value']
    print(recognizedKey)
    
    response = table.query(
        KeyConditionExpression=Key('id').eq(recognizedKey)
    )
    
    return {
        'body': response
    }
