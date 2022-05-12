import json
import base64
import os
import boto3
import time

student_information = {
    'Onkar': '1222405119',
    'Tapan': '1222325026',
    'Shreemad': '1222713687'
}

def lambda_handler(event, context):
    # creating clients for further invocations
    lambdaClient = boto3.client('lambda')
    s3 = boto3.resource('s3')
    
    # receving image from request
    decodedBody = json.loads(event['body'])
    image = decodedBody['image']
    
    starTime = time.time()
    #calling function for evaluation
    evalResponse = lambdaClient.invoke(
        FunctionName='***',
        InvocationType='***',
        Payload=json.dumps({'image': image})
    )
    endTime = time.time()
    
    evaluation = json.loads(evalResponse['Payload'].read().decode('utf-8'))
    print(evaluation)
    student_info = student_information[evaluation['body'][1:-1]]
    print(student_info)
    
    #getting response from dynamoDB
    dynamoRes = lambdaClient.invoke(
        FunctionName='***',
        InvocationType='***',
        Payload=json.dumps({'value': student_info })
    )
    
    response = json.loads(dynamoRes['Payload'].read().decode('utf-8'))
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
