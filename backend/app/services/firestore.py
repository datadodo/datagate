from firebase_admin import firestore
from typing import List, Optional, Dict, Any
from datetime import datetime
import os

def get_firestore_client():
    """Get Firestore client, initializing if needed"""
    try:
        return firestore.client()
    except Exception as e:
        print(f"Failed to get Firestore client: {e}")
        return None

class FirestoreService:
    
    @staticmethod
    def get_user_profile(uid: str) -> Optional[Dict[str, Any]]:
        """Get user profile from Firestore"""
        try:
            db = get_firestore_client()
            if not db:
                return None
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
            db = get_firestore_client()
            if not db:
                return False
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
            db = get_firestore_client()
            if not db:
                return False
            user_ref = db.collection('users').document(uid)
            user_ref.update({
                'fileLimit': new_limit
            })
            return True
        except Exception as e:
            print(f"Error updating file limit: {e}")
            return False
    
    @staticmethod
    def update_user_file_size_limit(uid: str, new_size_limit: int) -> bool:
        """Update user's file size limit (in bytes)"""
        try:
            db = get_firestore_client()
            if not db:
                return False
            user_ref = db.collection('users').document(uid)
            user_ref.update({
                'fileSizeLimit': new_size_limit
            })
            return True
        except Exception as e:
            print(f"Error updating file size limit: {e}")
            return False
    
    @staticmethod
    def update_user_type(uid: str, user_type: str) -> bool:
        """Update user's type (admin/user)"""
        try:
            db = get_firestore_client()
            if not db:
                return False
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
            db = get_firestore_client()
            if not db:
                raise Exception('Database connection failed')
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
            db = get_firestore_client()
            if not db:
                return []
            files = db.collection('files').where('user_id', '==', uid).stream()
            file_list = []
            for doc in files:
                file_data = doc.to_dict()
                file_data['id'] = doc.id  # Add the document ID as id
                file_list.append(file_data)
            # Sort by uploaded_at in Python instead of Firestore
            file_list.sort(key=lambda x: x.get('uploaded_at', datetime.min), reverse=True)
            return file_list
        except Exception as e:
            print(f"Error getting user files: {e}")
            return []
    
    @staticmethod
    def get_all_files() -> List[Dict[str, Any]]:
        """Get all files across all users (admin only)"""
        try:
            db = get_firestore_client()
            if not db:
                return []
            files = db.collection('files').stream()
            file_list = []
            for doc in files:
                file_data = doc.to_dict()
                file_data['id'] = doc.id  # Add the document ID as id
                file_list.append(file_data)
            # Sort by uploaded_at in Python instead of Firestore
            file_list.sort(key=lambda x: x.get('uploaded_at', datetime.min), reverse=True)
            return file_list
        except Exception as e:
            print(f"Error getting all files: {e}")
            return []
    
    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """Get all users (admin only)"""
        try:
            db = get_firestore_client()
            if not db:
                return []
            users = db.collection('users').stream()
            user_list = []
            for doc in users:
                user_data = doc.to_dict()
                user_data['uid'] = doc.id  # Add the document ID as uid
                user_list.append(user_data)
            return user_list
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
    
    @staticmethod
    def delete_file_record(file_id: str) -> bool:
        """Delete a file record from Firestore"""
        try:
            db = get_firestore_client()
            if not db:
                return False
            db.collection('files').document(file_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting file record: {e}")
            return False
    
    @staticmethod
    def get_file_by_id(file_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific file by ID"""
        try:
            db = get_firestore_client()
            if not db:
                return None
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
            db = get_firestore_client()
            if not db:
                return False
            db.collection('files').document(file_id).update({
                'download_url': download_url
            })
            return True
        except Exception as e:
            print(f"Error updating download URL: {e}")
            return False
    
    @staticmethod
    def sync_user_file_count(uid: str) -> bool:
        """Sync user's file count with actual files in database"""
        try:
            # Get actual file count
            actual_count = len(FirestoreService.get_user_files(uid))
            
            # Update user profile with actual count
            db = get_firestore_client()
            if not db:
                return False
            user_ref = db.collection('users').document(uid)
            user_ref.update({
                'fileCount': actual_count
            })
            return True
        except Exception as e:
            print(f"Error syncing file count: {e}")
            return False