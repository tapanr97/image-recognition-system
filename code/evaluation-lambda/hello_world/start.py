import json
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
    decodedBody = json.loads(event['body'])
    image = decodedBody['image']

    startTime = time.time()
    result = eval_face_recognition.evaluate_image(image)
    endTime = time.time()
    print('Total time taken', endTime - startTime)
    student_info = student_information[result]

    return {
        'statusCode': 200,
        'body': json.dumps(student_info)
    }
