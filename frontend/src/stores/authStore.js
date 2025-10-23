import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  signInWithPopup, 
  signOut, 
  onAuthStateChanged,
  GoogleAuthProvider 
} from 'firebase/auth'
import { doc, getDoc } from 'firebase/firestore'
import { auth, db } from '@/firebase'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const userProfile = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Computed properties
  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => userProfile.value?.userType === 'admin')
  const userType = computed(() => userProfile.value?.userType || 'user')
  const fileLimit = computed(() => userProfile.value?.fileLimit || 500)
  const fileCount = computed(() => userProfile.value?.fileCount || 0)

  // Initialize auth state
  const initializeAuth = () => {
    onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        user.value = firebaseUser
        await fetchUserProfile(firebaseUser.uid)
      } else {
        user.value = null
        userProfile.value = null
      }
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
    } catch (error) {
      console.error('Error fetching user profile:', error)
      error.value = 'Failed to fetch user profile'
    }
  }

  // Sign in with Google
  const signInWithGoogle = async () => {
    try {
      loading.value = true
      error.value = null
      
      const result = await signInWithPopup(auth, new GoogleAuthProvider())
      user.value = result.user
      await fetchUserProfile(result.user.uid)
      
      return result
    } catch (error) {
      console.error('Sign in error:', error)
      error.value = error.message
      throw error
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
    
    // Computed
    isAuthenticated,
    isAdmin,
    userType,
    fileLimit,
    fileCount,
    
    // Actions
    initializeAuth,
    signInWithGoogle,
    signOutUser,
    updateUserProfile,
    clearError
  }
})
