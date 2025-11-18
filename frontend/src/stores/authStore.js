import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut, 
  onAuthStateChanged
} from 'firebase/auth'
import { doc, getDoc, setDoc } from 'firebase/firestore'
import { auth, db } from '@/firebase'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const userProfile = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const authInitialized = ref(false)

  // Computed properties
  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => userProfile.value?.userType === 'admin')
  const userType = computed(() => userProfile.value?.userType || 'user')
  const fileLimit = computed(() => userProfile.value?.fileLimit || 500)
  const fileCount = computed(() => userProfile.value?.fileCount || 0)
  const fileSizeLimit = computed(() => userProfile.value?.fileSizeLimit || 100 * 1024 * 1024)

  // Initialize auth state
  const initializeAuth = () => {
    return new Promise((resolve) => {
      onAuthStateChanged(auth, async (firebaseUser) => {
        if (firebaseUser) {
          user.value = firebaseUser
          await fetchUserProfile(firebaseUser.uid)
        } else {
          user.value = null
          userProfile.value = null
        }
        authInitialized.value = true
        resolve()
      })
    })
  }

  // Fetch user profile from Firestore
  const fetchUserProfile = async (uid) => {
    try {
      const userDoc = await getDoc(doc(db, 'users', uid))
      if (userDoc.exists()) {
        userProfile.value = userDoc.data()
      } else {
        // Create user profile if it doesn't exist
        userProfile.value = {
          uid,
          email: user.value.email,
          userType: 'user',
          fileLimit: 500,
          fileCount: 0,
          createdAt: new Date()
        }
      }
    } catch (err) {
      console.error('Error fetching user profile:', err)
      error.value = 'Failed to fetch user profile'
    }
  }

  // Helper function to convert Firebase error codes to user-friendly messages
  const getErrorMessage = (error) => {
    const errorCode = error.code || error.message
    
    // Sign up errors
    if (errorCode.includes('email-already-in-use') || errorCode.includes('auth/email-already-in-use')) {
      return 'This email is already registered. Please sign in instead.'
    }
    
    // Sign in errors
    if (errorCode.includes('user-not-found') || errorCode.includes('auth/user-not-found')) {
      return 'No account found with this email. Please check your email or sign up.'
    }
    if (errorCode.includes('wrong-password') || errorCode.includes('auth/wrong-password')) {
      return 'Incorrect password. Please try again.'
    }
    if (errorCode.includes('invalid-credential') || errorCode.includes('auth/invalid-credential')) {
      return 'Invalid email or password. Please try again.'
    }
    
    // General errors
    if (errorCode.includes('invalid-email') || errorCode.includes('auth/invalid-email')) {
      return 'Invalid email address. Please enter a valid email.'
    }
    if (errorCode.includes('weak-password') || errorCode.includes('auth/weak-password')) {
      return 'Password should be at least 6 characters long.'
    }
    if (errorCode.includes('too-many-requests') || errorCode.includes('auth/too-many-requests')) {
      return 'Too many failed attempts. Please try again later.'
    }
    if (errorCode.includes('network-request-failed') || errorCode.includes('auth/network-request-failed')) {
      return 'Network error. Please check your internet connection and try again.'
    }
    
    // Default fallback
    return 'An error occurred. Please try again.'
  }

  // Sign up with email and password
  const signUpWithEmail = async (email, password) => {
    try {
      loading.value = true
      error.value = null
      
      const result = await createUserWithEmailAndPassword(auth, email, password)
      user.value = result.user
      
      // Create user profile in Firestore
      await setDoc(doc(db, 'users', result.user.uid), {
        email: email,
        userType: 'user',
        fileLimit: 500,
        fileCount: 0,
        createdAt: new Date()
      })
      
      await fetchUserProfile(result.user.uid)
      return result
    } catch (err) {
      console.error('Sign up error:', err)
      error.value = getErrorMessage(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Sign in with email and password
  const signInWithEmail = async (email, password) => {
    try {
      loading.value = true
      error.value = null
      
      const result = await signInWithEmailAndPassword(auth, email, password)
      user.value = result.user
      await fetchUserProfile(result.user.uid)
      
      return result
    } catch (err) {
      console.error('Sign in error:', err)
      error.value = getErrorMessage(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // Sign out
  const signOutUser = async () => {
    try {
      loading.value = true
      await signOut(auth)
      user.value = null
      userProfile.value = null
    } catch (error) {
      console.error('Sign out error:', error)
      error.value = error.message
    } finally {
      loading.value = false
    }
  }

  // Update user profile (for admin actions)
  const updateUserProfile = (updates) => {
    if (userProfile.value) {
      userProfile.value = { ...userProfile.value, ...updates }
    }
  }

  // Clear error
  const clearError = () => {
    error.value = null
  }

  return {
    // State
    user,
    userProfile,
    loading,
    error,
    authInitialized,
    
    // Computed
    isAuthenticated,
    isAdmin,
    userType,
    fileLimit,
    fileCount,
    fileSizeLimit,
    
    // Actions
    initializeAuth,
    signUpWithEmail,
    signInWithEmail,
    signOutUser,
    updateUserProfile,
    clearError
  }
})
