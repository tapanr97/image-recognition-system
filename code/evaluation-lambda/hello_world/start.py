import json
import base64
import os
import boto3
import time
import eval_face_recognition

student_information = {
    'Onkar': {
        'id': '1222405119',
        'name': 'Onkar Pandit',
        'course': 'Computer Science'
    },
    'Tapan': {
        'id': '1222405119',
        'name': 'Tapan Rajnikanth Modi',
        'course': 'Computer Science'
    },
    'Shreemad': {
        'id': '1222405119',
        'name': 'Shreemad Sanskarbhai Patel',
        'course': 'Computer Science'
    }
}

student_information_dynamo = {
    'Onkar': {
        'id': {'S': '1222405119'},
        'name': {'S': 'Onkar Pandit'},
        'course': {'S': 'Computer Science'}
    },
    'Tapan': {
        'id': {'S': '1222405119'},
        'name': {'S': 'Tapan Rajnikanth Modi'},
        'course': {'S': 'Computer Science'}
    },
    'Shreemad': {
        'id': {'S': '1222405119'},
        'name': {'S': 'Shreemad Sanskarbhai Patel'},
        'course': {'S': 'Computer Science'}
    }
}


def lambda_handler(event, context):
    # creating clients for further invocations
    lambdaClient = boto3.client('lambda')
    s3 = boto3.resource('s3')

    # receving image from request
    decodedBody = json.loads(event['body'])
    image = decodedBody['image']

    # calling function for evaluation
    # evalResponse = lambdaClient.invoke(
    #     FunctionName='***',
    #     InvocationType='***',
    #     Payload=json.dumps({'image': image})
    # )
    startTime = time.time()
    result = eval_face_recognition.evaluate_image(image)
    endTime = time.time()
    print('Total time taken', endTime - startTime)
    # evaluation = json.loads(evalResponse['Payload'].read().decode('utf-8'))
    student_info = student_information[result]
    student_info_dynamo_db = student_information_dynamo[result]

    # getting response from dynamoDB
    # lambdaClient.invoke(
    #     FunctionName='***',
    #     InvocationType='***',
    #     Payload=json.dumps({'value': student_info_dynamo_db})
    # )

    return {
        'statusCode': 200,
        'body': json.dumps(student_info)
    }

# startTime = time.time()
# result = eval_face_recognition.evaluate_image('./data/real_images/train/Shreemad/1.jpg')
# endTime = time.time()
# print('Total time taken', endTime - startTime)
# print(result)