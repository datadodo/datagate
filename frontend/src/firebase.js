import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAFAg5iLtdBUffQgz6wYHw1gZl35PAQTPc",
  authDomain: "globaldashboard-4598e.firebaseapp.com",
  projectId: "globaldashboard-4598e",
  storageBucket: "globaldashboard-4598e.firebasestorage.app",
  messagingSenderId: "815382375083",
  appId: "1:815382375083:web:2ab02864ed655ab97fe5ee"
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)

// Initialize Firebase services
export const auth = getAuth(app)
export const db = getFirestore(app)

export default app
