from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.middleware.auth import get_admin_user, AuthUser
from app.services.firestore import FirestoreService
from app.services.storage import StorageService
from app.models.file import UserResponse, FileResponse, UpdateUserRequest
from datetime import datetime

router = APIRouter()
firestore_service = FirestoreService()
storage_service = StorageService()

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(current_user: AuthUser = Depends(get_admin_user)):
    """Get all users (admin only)"""
    try:
        users_data = firestore_service.get_all_users()
        
        users = []
        for user_data in users_data:
            users.append(UserResponse(
                uid=user_data.get('uid', ''),
                email=user_data.get('email', ''),
                user_type=user_data.get('userType', 'user'),
                file_limit=user_data.get('fileLimit', 500),
                file_count=user_data.get('fileCount', 0),
                created_at=user_data.get('createdAt')
            ))
        
        return users
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get users: {str(e)}")

@router.get("/files", response_model=List[FileResponse])
async def get_all_files(current_user: AuthUser = Depends(get_admin_user)):
    """Get all files across all users (admin only)"""
    try:
        files_data = firestore_service.get_all_files()
        
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
        
        return files
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get files: {str(e)}")

@router.delete("/files/{file_id}")
async def delete_any_file(file_id: str, current_user: AuthUser = Depends(get_admin_user)):
    """Delete any file (admin only)"""
    try:
        # Get file record
        file_data = firestore_service.get_file_by_id(file_id)
        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Delete from GCS
        storage_service.delete_file(file_data['gcs_path'])
        
        # Delete from Firestore
        firestore_service.delete_file_record(file_id)
        
        # Update the file owner's file count
        firestore_service.update_user_file_count(file_data['user_id'], -1)
        
        return {"message": "File deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@router.put("/users/{user_id}/file-limit")
async def update_user_file_limit(
    user_id: str, 
    new_limit: int,
    current_user: AuthUser = Depends(get_admin_user)
):
    """Update user's file upload limit (admin only)"""
    try:
        if new_limit < 0:
            raise HTTPException(status_code=400, detail="File limit must be non-negative")
        
        success = firestore_service.update_user_file_limit(user_id, new_limit)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update file limit")
        
        return {"message": f"File limit updated to {new_limit}"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update file limit: {str(e)}")

@router.put("/users/{user_id}/user-type")
async def update_user_type(
    user_id: str,
    user_type: str,
    current_user: AuthUser = Depends(get_admin_user)
):
    """Change user's type (admin/user) (admin only)"""
    try:
        if user_type not in ['admin', 'user']:
            raise HTTPException(status_code=400, detail="User type must be 'admin' or 'user'")
        
        # Prevent admin from demoting themselves
        if user_id == current_user.uid and user_type == 'user':
            raise HTTPException(status_code=400, detail="You cannot demote yourself")
        
        success = firestore_service.update_user_type(user_id, user_type)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update user type")
        
        return {"message": f"User type updated to {user_type}"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user type: {str(e)}")

@router.get("/users/{user_id}/files", response_model=List[FileResponse])
async def get_user_files(user_id: str, current_user: AuthUser = Depends(get_admin_user)):
    """Get files for a specific user (admin only)"""
    try:
        files_data = firestore_service.get_user_files(user_id)
        
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
        
        return files
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user files: {str(e)}")

@router.get("/stats")
async def get_admin_stats(current_user: AuthUser = Depends(get_admin_user)):
    """Get admin dashboard statistics"""
    try:
        users_data = firestore_service.get_all_users()
        files_data = firestore_service.get_all_files()
        
        total_users = len(users_data)
        total_files = len(files_data)
        total_storage = sum(file.get('file_size', 0) for file in files_data)
        
        admin_users = len([u for u in users_data if u.get('userType') == 'admin'])
        regular_users = total_users - admin_users
        
        return {
            "total_users": total_users,
            "admin_users": admin_users,
            "regular_users": regular_users,
            "total_files": total_files,
            "total_storage_bytes": total_storage,
            "total_storage_mb": round(total_storage / (1024 * 1024), 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
