import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

// Firebase configuration
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyAFAg5iLtdBUffQgz6wYHw1gZl35PAQTPc",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "globaldashboard-4598e.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "globaldashboard-4598e",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "globaldashboard-4598e.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "815382375083",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:815382375083:web:2ab02864ed655ab97fe5ee"
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)

// Initialize Firebase services
export const auth = getAuth(app)
export const db = getFirestore(app)

export default app
