from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth, firestore
from typing import Optional, Dict, Any
import os

security = HTTPBearer()
db = firestore.client()

class AuthUser:
    def __init__(self, uid: str, email: str, user_type: str, file_limit: int = 500, file_count: int = 0):
        self.uid = uid
        self.email = email
        self.user_type = user_type
        self.file_limit = file_limit
        self.file_count = file_count

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthUser:
    """
    Verify Firebase ID token and get user information from Firestore
    """
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(credentials.credentials)
        uid = decoded_token['uid']
        
        # Get user document from Firestore
        user_doc = db.collection('users').document(uid).get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found in database")
        
        user_data = user_doc.to_dict()
        
        # Extract user information with safe defaults
        email = user_data.get('email', '')
        user_type = user_data.get('userType', 'user')
        file_limit = user_data.get('fileLimit', 500)
        file_count = user_data.get('fileCount', 0)
        
        return AuthUser(
            uid=uid,
            email=email,
            user_type=user_type,
            file_limit=file_limit,
            file_count=file_count
        )
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication: {str(e)}")

async def get_admin_user(current_user: AuthUser = Depends(get_current_user)) -> AuthUser:
    """
    Ensure the current user is an admin
    """
    if current_user.user_type != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def get_optional_user(request: Request) -> Optional[AuthUser]:
    """
    Get current user if authenticated, otherwise return None
    """
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
            
        token = auth_header.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        user_doc = db.collection('users').document(uid).get()
        if not user_doc.exists:
            return None
            
        user_data = user_doc.to_dict()
        return AuthUser(
            uid=uid,
            email=user_data.get('email', ''),
            user_type=user_data.get('userType', 'user'),
            file_limit=user_data.get('fileLimit', 500),
            file_count=user_data.get('fileCount', 0)
        )
    except:
        return None
