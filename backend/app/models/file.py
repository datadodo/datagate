from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FileUpload(BaseModel):
    file_name: str
    file_size: int
    content_type: str
    gcs_path: str

class FileResponse(BaseModel):
    id: str
    file_name: str
    file_size: int
    content_type: str
    uploaded_at: datetime
    download_url: Optional[str] = None

class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str
    file_size: int
    message: str

class BatchUploadResponse(BaseModel):
    successful_uploads: List[FileUploadResponse]
    failed_uploads: List[dict]
    total_files: int
    successful_count: int
    failed_count: int

class UserResponse(BaseModel):
    uid: str
    email: str
    user_type: str
    file_limit: int
    file_count: int
    created_at: Optional[datetime] = None

class UpdateUserRequest(BaseModel):
    user_type: Optional[str] = None
    file_limit: Optional[int] = None

class FileListResponse(BaseModel):
    files: List[FileResponse]
    total_count: int
    user_file_limit: int
    user_file_count: int
