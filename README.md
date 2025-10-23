# DataGate - File Management System

A modern, secure file management system built with Vue.js 3, FastAPI, and Firebase. Features role-based access control, drag-and-drop file uploads, and a beautiful Kapsule-inspired UI.

## 🚀 Features

### User Features
- **Google Authentication** - Secure sign-in with Google
- **Drag & Drop Upload** - Intuitive file upload interface
- **File Management** - View, download, and delete your files
- **File Limits** - Configurable upload limits (default: 500 files)
- **Batch Upload** - Upload multiple files at once
- **Progress Tracking** - Real-time upload progress

### Admin Features
- **User Management** - View all users and their file counts
- **File Management** - View and manage all files across users
- **Permission Control** - Change user types (admin/user)
- **File Limit Management** - Increase user file limits
- **Statistics Dashboard** - View system-wide statistics

## 🏗️ Architecture

- **Frontend**: Vue.js 3 + Vite + TailwindCSS
- **Backend**: FastAPI (Python)
- **Authentication**: Firebase Authentication
- **Database**: Firestore
- **Storage**: Google Cloud Storage
- **Deployment**: Firebase Hosting + App Hosting

## 🎨 Design

Inspired by [Kapsule](https://kapsuletech.com/) with:
- **Color Palette**: Teal/turquoise primary colors
- **Modern UI**: Glass-morphism effects and smooth animations
- **Responsive Design**: Works on all devices
- **Dark Theme**: Professional dark interface

## 📁 Project Structure

```
datagate/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── routes/            # API endpoints
│   │   ├── models/            # Pydantic models
│   │   ├── services/          # Business logic
│   │   └── middleware/         # Auth middleware
│   ├── requirements.txt
│   └── apphosting.yaml
├── frontend/                   # Vue.js frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── views/             # Page components
│   │   ├── stores/            # Pinia state management
│   │   ├── services/          # API service layer
│   │   └── assets/            # Styles and images
│   ├── package.json
│   └── firebase.json
├── deploy.sh                  # Deployment script
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.12+
- Firebase CLI
- Google Cloud account with Firebase project

### 1. Clone and Setup

```bash
git clone <repository-url>
cd datagate
```

### 2. Configure Firebase

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project or use existing: `globaldashboard-4598e`
3. Enable Authentication with Google provider
4. Create a Firestore database
5. Get your Firebase web app configuration

### 3. Configure Environment Variables

Create `frontend/.env` with your Firebase config:

```env
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=globaldashboard-4598e.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=globaldashboard-4598e
VITE_FIREBASE_STORAGE_BUCKET=globaldashboard-4598e.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_API_URL=http://localhost:8000
```

### 4. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 5. Run Locally

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit `http://localhost:3000` to see the application.

## 🚀 Deployment

### Automatic Deployment

```bash
# Make sure you're logged in to Firebase
firebase login

# Run the deployment script
./deploy.sh
```

### Manual Deployment

```bash
# Deploy backend
firebase deploy --only apphosting

# Deploy frontend
cd frontend
npm run build
firebase deploy --only hosting
```

## 🔧 Configuration

### Firebase Setup

1. **Authentication**: Enable Google Sign-In
2. **Firestore**: Create database with these collections:
   - `users` - User profiles with `userType` field
   - `files` - File metadata (created automatically)

3. **Storage**: Create GCS bucket: `globaldashboard-4598e-direct-user-uploads`

### Firestore Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own profile
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Files access rules
    match /files/{fileId} {
      allow read: if request.auth != null && 
        (resource.data.userId == request.auth.uid || 
         get(/databases/$(database)/documents/users/$(request.auth.uid)).data.userType == 'admin');
      allow create: if request.auth != null && request.resource.data.userId == request.auth.uid;
      allow delete: if request.auth != null && 
        (resource.data.userId == request.auth.uid || 
         get(/databases/$(database)/documents/users/$(request.auth.uid)).data.userType == 'admin');
    }
  }
}
```

## 📊 API Endpoints

### File Management
- `POST /api/files/upload` - Upload single file
- `POST /api/files/upload-batch` - Upload multiple files
- `GET /api/files/my-files` - Get user's files
- `DELETE /api/files/{file_id}` - Delete file
- `GET /api/files/{file_id}/download` - Get download URL

### Admin Endpoints
- `GET /api/admin/users` - Get all users
- `GET /api/admin/files` - Get all files
- `DELETE /api/admin/files/{file_id}` - Delete any file
- `PUT /api/admin/users/{user_id}/file-limit` - Update file limit
- `PUT /api/admin/users/{user_id}/user-type` - Change user type
- `GET /api/admin/stats` - Get system statistics

## 🎨 Customization

### Colors (TailwindCSS)
- Primary: `#2D8B8B` (teal)
- Secondary: `#3BABA5` (light teal)
- Dark: `#1A1A2E` (navy)
- Accent: `#E0F2F1` (light teal)

### Components
- `FileUploadZone` - Drag & drop upload area
- `FileList` - File management table
- `AdminToggle` - Admin view switcher
- `UsersManagement` - User administration
- `FilesManagement` - File administration

## 🔒 Security Features

- **Firebase Authentication** - Secure user authentication
- **Role-based Access** - Admin vs user permissions
- **File Validation** - Type and size validation
- **Signed URLs** - Secure file downloads
- **CORS Protection** - Cross-origin request security

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Check Firebase configuration
   - Verify Google Sign-In is enabled
   - Check Firestore security rules

2. **File Upload Issues**
   - Verify GCS bucket permissions
   - Check file size limits
   - Ensure user has upload permissions

3. **Admin Access Issues**
   - Verify user has `userType: 'admin'` in Firestore
   - Check admin toggle visibility

### Debug Mode

```bash
# Backend debug
cd backend
uvicorn app.main:app --reload --log-level debug

# Frontend debug
cd frontend
npm run dev -- --debug
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support, please contact the development team or create an issue in the repository.

---

**DataGate** - Secure, modern file management for the cloud era.
