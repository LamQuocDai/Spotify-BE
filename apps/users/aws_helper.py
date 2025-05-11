# apps/users/aws_helper.py
import boto3
import uuid
import logging
from django.conf import settings
from botocore.config import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class UserS3Uploader:
    def __init__(self):
        """Initialize S3 client with explicit credentials and configuration"""
        try:
            # Configure boto3 to avoid EC2 metadata service timeouts
            boto_config = Config(
                region_name=settings.AWS_S3_REGION_NAME,
                signature_version='s3v4',
                connect_timeout=5,
                read_timeout=5,
                retries={'max_attempts': 2}
            )

            # Create S3 client with explicit credentials
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
                config=boto_config
            )
            self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {str(e)}")
            raise

    def upload_file(self, file_obj, folder='profiles'):
        """Upload a file to S3 and return the URL"""
        if not file_obj:
            return None

        try:
            # Generate unique filename to prevent overwrites
            file_extension = file_obj.name.split('.')[-1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            s3_key = f"{folder}/{unique_filename}"

            # Upload file to S3
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs={'ContentType': file_obj.content_type}
            )

            # Return the public URL
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            logger.info(f"Successfully uploaded file to {s3_key}")
            return url

        except ClientError as e:
            logger.error(f"S3 upload error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during upload: {str(e)}")
            return None

    def delete_file(self, file_url):
        """Delete a file from S3 using its URL or key"""
        if not file_url or not isinstance(file_url, str):
            logger.warning("Cannot delete file: URL is None or not a string")
            return True  # Return True to avoid errors in calling code

        try:
            # Extract key from URL if needed
            if 's3.amazonaws.com/' in file_url:
                s3_key = file_url.split('s3.amazonaws.com/')[1]
            elif file_url.startswith('profiles/'):
                s3_key = file_url
            else:
                logger.warning(f"Invalid S3 URL format: {file_url}")
                return False

            # Delete the object
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            logger.info(f"Successfully deleted file: {s3_key}")
            return True

        except ClientError as e:
            logger.error(f"S3 deletion error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during deletion: {str(e)}")
            return False