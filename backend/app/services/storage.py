from google.cloud import storage
from typing import Optional, BinaryIO
import os
import uuid
from datetime import datetime, timedelta

class StorageService:
    def __init__(self):
        self.bucket_name = os.getenv('GCS_BUCKET_NAME', 'globaldashboard-4598e-direct-user-uploads')
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)
    
    def upload_file(self, file_content: bytes, file_name: str, content_type: str, user_id: str) -> str:
        """
        Upload file to Google Cloud Storage
        Returns the GCS path of the uploaded file
        """
        try:
            # Generate unique filename to avoid conflicts
            file_extension = os.path.splitext(file_name)[1]
            unique_filename = f"{user_id}/{uuid.uuid4()}{file_extension}"
            
            # Create blob and upload
            blob = self.bucket.blob(unique_filename)
            blob.upload_from_string(file_content, content_type=content_type)
            
            return unique_filename
        except Exception as e:
            print(f"Error uploading file: {e}")
            raise e
    
    def delete_file(self, gcs_path: str) -> bool:
        """
        Delete file from Google Cloud Storage
        """
        try:
            blob = self.bucket.blob(gcs_path)
            blob.delete()
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def generate_signed_url(self, gcs_path: str, expiration_hours: int = 1) -> str:
        """
        Generate a signed URL for file download
        """
        try:
            blob = self.bucket.blob(gcs_path)
            
            # Generate signed URL valid for specified hours
            expiration = datetime.utcnow() + timedelta(hours=expiration_hours)
            
            url = blob.generate_signed_url(
                version="v4",
                expiration=expiration,
                method="GET"
            )
            
            return url
        except Exception as e:
            print(f"Error generating signed URL: {e}")
            raise e
    
    def get_file_info(self, gcs_path: str) -> Optional[dict]:
        """
        Get file metadata from GCS
        """
        try:
            blob = self.bucket.blob(gcs_path)
            if blob.exists():
                blob.reload()
                return {
                    'size': blob.size,
                    'content_type': blob.content_type,
                    'created': blob.time_created,
                    'updated': blob.updated
                }
            return None
        except Exception as e:
            print(f"Error getting file info: {e}")
            return None
    
    def file_exists(self, gcs_path: str) -> bool:
        """
        Check if file exists in GCS
        """
        try:
            blob = self.bucket.blob(gcs_path)
            return blob.exists()
        except Exception as e:
            print(f"Error checking file existence: {e}")
            return False
