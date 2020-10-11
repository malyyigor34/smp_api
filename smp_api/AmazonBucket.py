import boto3
from botocore.exceptions import ClientError
import logging
import os

def upload_file(file_name, bucket, object_name=None):
    s3_client = boto3.client('s3',
                               aws_access_key_id='AKIAJ4MQQBD35KLDSI5Q',
                               aws_secret_access_key='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')


    if object_name is None:
        object_name = file_name


#    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    bucket_location = s3_client.get_bucket_location(Bucket='twitterimagies')

    return f'https://s3.{bucket_location.get("LocationConstraint")}.amazonaws.com/{os.environ.get("BUCKET_NAME")}/{object_name}'




