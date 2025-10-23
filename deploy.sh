#!/bin/bash

# DataGate Deployment Script
echo "🚀 Starting DataGate deployment..."

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Check if user is logged in
if ! firebase projects:list &> /dev/null; then
    echo "❌ Not logged in to Firebase. Please run 'firebase login' first."
    exit 1
fi

# Set project
echo "📋 Setting Firebase project..."
firebase use globaldashboard-4598e

# Install dependencies
echo "📦 Installing dependencies..."

# Backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Build frontend
echo "🏗️ Building frontend..."
cd frontend
npm run build
cd ..

# Deploy backend to App Hosting
echo "🚀 Deploying backend to Firebase App Hosting..."
firebase deploy --only apphosting

# Deploy frontend to Hosting
echo "🌐 Deploying frontend to Firebase Hosting..."
firebase deploy --only hosting

echo "✅ Deployment complete!"
echo ""
echo "🔗 Your application is now live at:"
echo "Frontend: https://globaldashboard-4598e.web.app"
echo "Backend API: Check Firebase Console for App Hosting URL"
echo ""
echo "📝 Next steps:"
echo "1. Configure Firebase Authentication in the Firebase Console"
echo "2. Set up your Firebase web app configuration"
echo "3. Update frontend/src/firebase.js with your actual Firebase config"
echo "4. Test the application!"
