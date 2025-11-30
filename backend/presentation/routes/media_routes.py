from uuid import uuid4

from config import s3Config
from fastapi import APIRouter, Body, Depends
from infrastructure.data.s3_client import S3Client
from presentation.routes.dependencies import get_current_user

mediaRouter = APIRouter(prefix="/media", tags=["Media"])


@mediaRouter.post("/s3/presigned-url")
async def s3_presigned_url(
    file_name: str = Body(), file_type: str = Body(), sender=Depends(get_current_user)
):
    """
    Generate a presigned URL for uploading media to S3.
    """
    s3_client = S3Client()
    user_id = sender["user_id"]
    unique_filename = f"user_{user_id}_{uuid4().hex}.{file_name.split('.')[-1]}"
    presigned_url = s3_client.generate_presigned_url(unique_filename, file_type)
    file_path = f"{s3Config.ENDPOINT_URL}/{s3Config.S3_BUCKET_NAME}/{unique_filename}"

    return {
        "presigned_url": presigned_url,
        "file_path": file_path,
    }
