from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List
from app.middleware.auth import get_current_user, AuthUser
from app.services.storage import StorageService
from app.services.firestore import FirestoreService
from app.models.file import FileResponse, FileUploadResponse, BatchUploadResponse, FileListResponse
from datetime import datetime
import os

router = APIRouter()
storage_service = StorageService()
firestore_service = FirestoreService()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: AuthUser = Depends(get_current_user)
):
    """Upload a single file"""
    try:
        # Check file limit
        if current_user.file_count >= current_user.file_limit:
            raise HTTPException(
                status_code=400, 
                detail=f"File limit reached ({current_user.file_count}/{current_user.file_limit}). Contact admin to increase limit."
            )
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Upload to GCS
        gcs_path = storage_service.upload_file(
            file_content=file_content,
            file_name=file.filename,
            content_type=file.content_type,
            user_id=current_user.uid
        )
        
        # Create file record in Firestore
        file_data = {
            'user_id': current_user.uid,
            'file_name': file.filename,
            'file_size': file_size,
            'content_type': file.content_type,
            'gcs_path': gcs_path,
            'uploaded_at': datetime.utcnow()
        }
        
        file_id = firestore_service.create_file_record(file_data)
        
        # Update user's file count
        firestore_service.update_user_file_count(current_user.uid, 1)
        
        return FileUploadResponse(
            file_id=file_id,
            file_name=file.filename,
            file_size=file_size,
            message="File uploaded successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload-batch", response_model=BatchUploadResponse)
async def upload_batch_files(
    files: List[UploadFile] = File(...),
    current_user: AuthUser = Depends(get_current_user)
):
    """Upload multiple files at once"""
    try:
        # Check if adding these files would exceed limit
        if current_user.file_count + len(files) > current_user.file_limit:
            raise HTTPException(
                status_code=400,
                detail=f"Uploading {len(files)} files would exceed limit. Current: {current_user.file_count}/{current_user.file_limit}"
            )
        
        successful_uploads = []
        failed_uploads = []
        
        for file in files:
            try:
                # Read file content
                file_content = await file.read()
                file_size = len(file_content)
                
                # Upload to GCS
                gcs_path = storage_service.upload_file(
                    file_content=file_content,
                    file_name=file.filename,
                    content_type=file.content_type,
                    user_id=current_user.uid
                )
                
                # Create file record
                file_data = {
                    'user_id': current_user.uid,
                    'file_name': file.filename,
                    'file_size': file_size,
                    'content_type': file.content_type,
                    'gcs_path': gcs_path,
                    'uploaded_at': datetime.utcnow()
                }
                
                file_id = firestore_service.create_file_record(file_data)
                
                successful_uploads.append(FileUploadResponse(
                    file_id=file_id,
                    file_name=file.filename,
                    file_size=file_size,
                    message="Uploaded successfully"
                ))
                
            except Exception as e:
                failed_uploads.append({
                    'file_name': file.filename,
                    'error': str(e)
                })
        
        # Update user's file count with successful uploads
        if successful_uploads:
            firestore_service.update_user_file_count(current_user.uid, len(successful_uploads))
        
        return BatchUploadResponse(
            successful_uploads=successful_uploads,
            failed_uploads=failed_uploads,
            total_files=len(files),
            successful_count=len(successful_uploads),
            failed_count=len(failed_uploads)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch upload failed: {str(e)}")

@router.get("/my-files", response_model=FileListResponse)
async def get_my_files(current_user: AuthUser = Depends(get_current_user)):
    """Get current user's files"""
    try:
        files_data = firestore_service.get_user_files(current_user.uid)
        
        files = []
        for file_data in files_data:
            # Generate signed URL for each file
            try:
                download_url = storage_service.generate_signed_url(file_data['gcs_path'])
            except:
                download_url = None
            
            files.append(FileResponse(
                id=file_data['id'],
                file_name=file_data['file_name'],
                file_size=file_data['file_size'],
                content_type=file_data['content_type'],
                uploaded_at=file_data['uploaded_at'],
                download_url=download_url
            ))
        
        return FileListResponse(
            files=files,
            total_count=len(files),
            user_file_limit=current_user.file_limit,
            user_file_count=current_user.file_count
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get files: {str(e)}")

@router.delete("/{file_id}")
async def delete_file(file_id: str, current_user: AuthUser = Depends(get_current_user)):
    """Delete a file (user can only delete their own files)"""
    try:
        # Get file record
        file_data = firestore_service.get_file_by_id(file_id)
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Check if user owns this file
        if file_data['user_id'] != current_user.uid:
            raise HTTPException(status_code=403, detail="You can only delete your own files")
        
        # Delete from GCS
        storage_service.delete_file(file_data['gcs_path'])
        
        # Delete from Firestore
        firestore_service.delete_file_record(file_id)
        
        # Update user's file count
        firestore_service.update_user_file_count(current_user.uid, -1)
        
        return {"message": "File deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@router.get("/{file_id}/download")
async def get_download_url(file_id: str, current_user: AuthUser = Depends(get_current_user)):
    """Get signed download URL for a file"""
    try:
        # Get file record
        file_data = firestore_service.get_file_by_id(file_id)
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Check if user owns this file
        if file_data['user_id'] != current_user.uid:
            raise HTTPException(status_code=403, detail="You can only download your own files")
        
        # Generate signed URL
        download_url = storage_service.generate_signed_url(file_data['gcs_path'])
        
        # Update the file record with the new download URL
        firestore_service.update_file_download_url(file_id, download_url)
        
        return {"download_url": download_url}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {str(e)}")
