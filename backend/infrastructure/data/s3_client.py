import boto3
from botocore.config import Config
from config import s3Config


class S3Client:
    """S3 Client for file uploads."""

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=s3Config.ENDPOINT_URL,
            aws_access_key_id=s3Config.S3_ACCESS_KEY,
            aws_secret_access_key=s3Config.S3_SECRET_KEY,
            config=Config(signature_version="s3v4"),
        )

    def generate_presigned_url(
        self,
        file_name: str,
        client_method: str = "put_object",
        file_type: str = "image/jpeg",
        expiration: int = 120,
    ) -> str:
        """Generate a presigned URL for uploading a file to S3.

        :param filename: Name of the file to be uploaded
        :param content_type: Content type of the file
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string
        """
        try:
            params = {
                "Bucket": s3Config.S3_BUCKET_NAME,
                "Key": file_name,
            }

            if client_method == "put_object":
                params["ContentType"] = file_type
            presigned_url = self.s3.generate_presigned_url(
                ClientMethod=client_method,
                Params=params,
                ExpiresIn=expiration,
            )

            return presigned_url
        except Exception as e:
            print(f"Error_generating_presigned_URL: {e}")
            return ""

    def upload_file(self, file_name: str, bucket: str, object_name: str = None):
        """Upload a file to an S3 bucket.

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        try:
            res = self.s3.upload_file(file_name, "appifytask", object_name)
            print("res_s3_upload", res)
            return True
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return False
