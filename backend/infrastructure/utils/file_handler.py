from pathlib import Path
from uuid import uuid4

from config import s3Config
from fastapi import UploadFile
from infrastructure.data.s3_client import S3Client


async def storefile(file: UploadFile, user_id: int) -> str:
    """
    Upload file to S3 bucket and return the file URL.

    Args:
        file: FastAPI UploadFile object
        user_id: ID of the user uploading the file

    Returns:
        str: URL of the uploaded file
    """
    s3_client = S3Client()
    unique_filename = f"user_{user_id}_{uuid4().hex}.{file.filename.split('.')[-1]}"
    UPLOAD_DIR = Path("uploads/posts")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    temp_file_path = UPLOAD_DIR / unique_filename
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    success = s3_client.upload_file(
        str(temp_file_path), s3Config.S3_BUCKET_NAME, unique_filename
    )
    print(f"Upload_success: {success}")
    temp_file_path.unlink(missing_ok=True)

    if not success:
        raise Exception("File upload failed")

    return f"https://{s3Config.S3_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"
