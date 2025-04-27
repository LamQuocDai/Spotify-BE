import boto3
import uuid
from botocore.exceptions import ClientError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class S3Uploader:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file, file_type):
        if not file:
            return None

        file_extension = file.name.split('.')[-1].lower()
        random_filename = f"{file_type}/{uuid.uuid4()}.{file_extension}"

        try:
            # Upload file to S3
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                random_filename,
                ExtraArgs={
                    'ContentType': file.content_type,
                }
            )

            url = f"https://{self.bucket_name}.s3.amazonaws.com/{random_filename}"
            return url

        except ClientError as e:
            logger.error(f"Error uploading to S3: {e}")
            return None

    def delete_file(self, url):
        if not url:
            return True

        try:
            key = url.split('.com/')[-1]

            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return True

        except ClientError as e:
            logger.error(f"Error deleting from S3: {e}")
            return False