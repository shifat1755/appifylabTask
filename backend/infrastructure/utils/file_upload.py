import uuid
from pathlib import Path

from fastapi import UploadFile

# Define upload directory
UPLOAD_DIR = Path("uploads/posts")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Base URL for serving static files
BASE_URL = "http://localhost:8000"


async def save_uploaded_file(file: UploadFile, user_id: int) -> str:
    """
    Save uploaded file to local storage and return the URL path.

    Args:
        file: FastAPI UploadFile object
        user_id: ID of the user uploading the file

    Returns:
        URL path to the saved file (e.g., "/uploads/posts/user_1_abc123.jpg")
    """
    # Generate unique filename
    file_extension = Path(file.filename).suffix if file.filename else ".jpg"
    unique_filename = f"user_{user_id}_{uuid.uuid4().hex}{file_extension}"

    # Create user-specific directory
    user_upload_dir = UPLOAD_DIR / f"user_{user_id}"
    user_upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = user_upload_dir / unique_filename
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Return URL path (relative to base URL)
    return f"/uploads/posts/user_{user_id}/{unique_filename}"
