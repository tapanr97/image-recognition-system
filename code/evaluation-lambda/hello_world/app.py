import os
import os.path

import torch
import torchvision.transforms as transforms
from PIL import Image
import json
import numpy as np
import build_custom_model
import base64
import time
import boto3

def lambda_handler(event, context):
    # parser = argparse.ArgumentParser(description='Evaluate your customized face recognition model')
    # parser.add_argument('--img_path', type=str, default="./data/test_me/val/angelina_jolie/1.png", help='the path of the dataset')
    # args = parser.parse_args()
    image = event['image']
    imgdata = base64.b64decode(image)
    current_time = time.time()
    filename = '/tmp/receivedImage' + str(current_time) + '.png'
    s3 = boto3.resource('s3')

    with open(filename, 'wb') as f:
        f.write(imgdata)

    object = s3.Object('cc-lambda-files', 'image.png')
    object.put(Body=filename)

    img_path = filename
    labels_dir = "./checkpoint/labels.json"
    model_path = "./checkpoint/model_vggface2_best.pth"

    print("The file model_vggface2 exists?", os.path.exists(model_path))

    # read labels
    with open(labels_dir) as f:
        labels = json.load(f)
    # print(f"labels: {labels}")
    print('JSON loaded')

    device = torch.device('cpu')
    model = build_custom_model.build_model(len(labels)).to(device)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))['model'])
    model.eval()
    # print(f"Best accuracy of the loaded model: {torch.load(model_path, map_location=torch.device('cpu'))['best_acc']}")
    print('Completed eval')

    img = Image.open(img_path)
    rgb_image = img.convert('RGB')
    img_tensor = transforms.ToTensor()(rgb_image).unsqueeze_(0).to(device)
    outputs = model(img_tensor)
    _, predicted = torch.max(outputs.data, 1)
    result = labels[np.array(predicted.cpu())[0]]
    # print(predicted.data, result)

    print('Obtained', result)
    # img_name = img_path.split("/")[-1]
    # img_and_result = f"({img_name}, {result})"
    # print(f"Image and its recognition result is: {img_and_result}")
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
