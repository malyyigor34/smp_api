import logging
import os
import random
import tempfile

import boto3
import requests
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None):
    s3_client = boto3.client('s3',
                               aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                               aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))


    if object_name is None:
        object_name = file_name


#    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    bucket_location = s3_client.get_bucket_location(Bucket=os.environ.get('BUCKET_NAME'))

    return f'https://s3.{bucket_location.get("LocationConstraint")}.amazonaws.com/{os.environ.get("BUCKET_NAME")}/{object_name}'


def upload_image(key, value):
    try:
        if key.find('_url') != -1:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                response = requests.get(value)
                if response.status_code == 200:
                    temp.write(response.content)
                    response = requests.get(value)
                    temp.write(response.content)
                    temp.write(requests.get(value).content)
                temp.flush()
                object_name = f'{random.randint(0,9999999)}.png'
                url = upload_file(temp.name, os.environ.get('BUCKET_NAME'), object_name)
                return url
    except Exception as err:
        return value
    return value