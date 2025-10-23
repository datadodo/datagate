import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

// Firebase configuration
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "your-api-key",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "globaldashboard-4598e.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "globaldashboard-4598e",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "globaldashboard-4598e.appspot.com",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "your-sender-id",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "your-app-id"
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)

// Initialize Firebase services
export const auth = getAuth(app)
export const db = getFirestore(app)
export const googleProvider = new GoogleAuthProvider()

// Configure Google provider
googleProvider.setCustomParameters({
  prompt: 'select_account'
})

export default app
