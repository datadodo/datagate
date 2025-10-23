from firebase_admin import firestore
from typing import List, Optional, Dict, Any
from datetime import datetime
import os

db = firestore.client()

class FirestoreService:
    
    @staticmethod
    def get_user_profile(uid: str) -> Optional[Dict[str, Any]]:
        """Get user profile from Firestore"""
        try:
            user_doc = db.collection('users').document(uid).get()
            if user_doc.exists:
                return user_doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    @staticmethod
    def update_user_file_count(uid: str, increment: int = 1) -> bool:
        """Update user's file count"""
        try:
            user_ref = db.collection('users').document(uid)
            user_ref.update({
                'fileCount': firestore.Increment(increment)
            })
            return True
        except Exception as e:
            print(f"Error updating file count: {e}")
            return False
    
    @staticmethod
    def update_user_file_limit(uid: str, new_limit: int) -> bool:
        """Update user's file upload limit"""
        try:
            user_ref = db.collection('users').document(uid)
            user_ref.update({
                'fileLimit': new_limit
            })
            return True
        except Exception as e:
            print(f"Error updating file limit: {e}")
            return False
    
    @staticmethod
    def update_user_type(uid: str, user_type: str) -> bool:
        """Update user's type (admin/user)"""
        try:
            user_ref = db.collection('users').document(uid)
            user_ref.update({
                'userType': user_type
            })
            return True
        except Exception as e:
            print(f"Error updating user type: {e}")
            return False
    
    @staticmethod
    def create_file_record(file_data: Dict[str, Any]) -> str:
        """Create a new file record in Firestore"""
        try:
            file_ref = db.collection('files').document()
            file_data['id'] = file_ref.id
            file_data['uploaded_at'] = datetime.utcnow()
            file_ref.set(file_data)
            return file_ref.id
        except Exception as e:
            print(f"Error creating file record: {e}")
            raise e
    
    @staticmethod
    def get_user_files(uid: str) -> List[Dict[str, Any]]:
        """Get all files for a specific user"""
        try:
            files = db.collection('files').where('user_id', '==', uid).order_by('uploaded_at', direction=firestore.Query.DESCENDING).stream()
            return [doc.to_dict() for doc in files]
        except Exception as e:
            print(f"Error getting user files: {e}")
            return []
    
    @staticmethod
    def get_all_files() -> List[Dict[str, Any]]:
        """Get all files across all users (admin only)"""
        try:
            files = db.collection('files').order_by('uploaded_at', direction=firestore.Query.DESCENDING).stream()
            return [doc.to_dict() for doc in files]
        except Exception as e:
            print(f"Error getting all files: {e}")
            return []
    
    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """Get all users (admin only)"""
        try:
            users = db.collection('users').stream()
            return [doc.to_dict() for doc in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
    
    @staticmethod
    def delete_file_record(file_id: str) -> bool:
        """Delete a file record from Firestore"""
        try:
            db.collection('files').document(file_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting file record: {e}")
            return False
    
    @staticmethod
    def get_file_by_id(file_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific file by ID"""
        try:
            file_doc = db.collection('files').document(file_id).get()
            if file_doc.exists:
                return file_doc.to_dict()
            return None
        except Exception as e:
            print(f"Error getting file: {e}")
            return None
    
    @staticmethod
    def update_file_download_url(file_id: str, download_url: str) -> bool:
        """Update file with signed download URL"""
        try:
            db.collection('files').document(file_id).update({
                'download_url': download_url
            })
            return True
        except Exception as e:
            print(f"Error updating download URL: {e}")
            return False
