#!/usr/bin/env python3
"""
Script to create an admin user in Firestore
"""
import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_admin_user():
    # Initialize Firebase Admin SDK
    cred_path = os.path.join(os.path.dirname(__file__), 'globaldashboard-4598e-firebase-adminsdk-fbsvc-8820178d65.json')
    cred = credentials.Certificate(cred_path)
    
    # Initialize Firebase Admin (only if not already initialized)
    try:
        firebase_admin.initialize_app(cred)
    except ValueError:
        # App already initialized
        pass
    
    db = firestore.client()
    
    email = "test@gmail.com"
    password = "test123456"  # Minimum 6 characters for Firebase Auth
    
    try:
        # Create user in Firebase Auth
        user_record = auth.create_user(
            email=email,
            password=password,
            email_verified=True
        )
        
        print(f"✅ Created Firebase Auth user: {user_record.uid}")
        
        # Create user profile in Firestore
        user_data = {
            'email': email,
            'userType': 'admin',
            'fileLimit': 1000,  # Higher limit for admin
            'fileCount': 0,
            'createdAt': datetime.now(),
            'isAdmin': True,
            'permissions': {
                'canViewAllFiles': True,
                'canDeleteAnyFile': True,
                'canManageUsers': True,
                'canChangeUserTypes': True
            }
        }
        
        # Add to Firestore
        db.collection('users').document(user_record.uid).set(user_data)
        
        print(f"✅ Created admin user profile in Firestore")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"👑 User Type: admin")
        print(f"🆔 User ID: {user_record.uid}")
        
        return True
        
    except auth.EmailAlreadyExistsError:
        print(f"⚠️  User {email} already exists in Firebase Auth")
        
        # Try to get the existing user
        try:
            user_record = auth.get_user_by_email(email)
            print(f"📧 Found existing user: {user_record.uid}")
            
            # Update user profile in Firestore to make them admin
            user_data = {
                'email': email,
                'userType': 'admin',
                'fileLimit': 1000,
                'fileCount': 0,
                'createdAt': datetime.now(),
                'isAdmin': True,
                'permissions': {
                    'canViewAllFiles': True,
                    'canDeleteAnyFile': True,
                    'canManageUsers': True,
                    'canChangeUserTypes': True
                }
            }
            
            db.collection('users').document(user_record.uid).set(user_data)
            print(f"✅ Updated user profile to admin in Firestore")
            print(f"📧 Email: {email}")
            print(f"👑 User Type: admin")
            print(f"🆔 User ID: {user_record.uid}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating existing user: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Creating admin user: test@gmail.com")
    print("=" * 50)
    
    success = create_admin_user()
    
    if success:
        print("=" * 50)
        print("✅ Admin user created successfully!")
        print("🌐 You can now sign in at: https://datagate.web.app")
        print("📧 Email: test@gmail.com")
        print("🔑 Password: test123456")
    else:
        print("=" * 50)
        print("❌ Failed to create admin user")
        sys.exit(1)
