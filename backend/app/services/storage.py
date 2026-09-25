import os

import boto3
from dotenv import load_dotenv

load_dotenv()


def get_storage_client():

    client = boto3.client(
        "s3",
        endpoint_url=os.getenv("B2_ENDPOINT"),
        aws_access_key_id=os.getenv("B2_KEY_ID"),
        aws_secret_access_key=os.getenv("B2_APPLICATION_KEY")
    )

    return client


def upload_file(file_path, object_name):

    client = get_storage_client()

    client.upload_file(
        file_path,
        os.getenv("B2_BUCKET_NAME"),
        object_name
    )

    return True


def delete_file(object_name):

    client = get_storage_client()

    client.delete_object(
        Bucket=os.getenv("B2_BUCKET_NAME"),
        Key=object_name
    )

    return True