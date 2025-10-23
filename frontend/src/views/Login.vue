<template>
  <div class="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 bg-gradient-to-r from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mb-6">
          <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-white mb-2">DataGate</h2>
        <p class="text-white/70">Secure file management system</p>
      </div>

      <!-- Login Form -->
      <div class="glass-card p-8">
        <div class="space-y-6">
          <!-- Google Sign In Button -->
          <button
            @click="handleGoogleSignIn"
            :disabled="loading"
            class="w-full flex items-center justify-center px-4 py-3 border border-white/20 rounded-lg bg-white/10 hover:bg-white/20 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="!loading" class="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <div v-else class="w-5 h-5 mr-3 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
            <span class="text-white font-medium">
              {{ loading ? 'Signing in...' : 'Sign in with Google' }}
            </span>
          </button>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-500/20 border border-red-500/30 rounded-lg p-4">
            <p class="text-red-200 text-sm">{{ error }}</p>
          </div>

          <!-- Features -->
          <div class="mt-8 space-y-4">
            <h3 class="text-lg font-semibold text-white mb-4">Features</h3>
            <div class="space-y-3">
              <div class="flex items-center text-white/70">
                <svg class="w-5 h-5 mr-3 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Secure file uploads</span>
              </div>
              <div class="flex items-center text-white/70">
                <svg class="w-5 h-5 mr-3 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Drag & drop interface</span>
              </div>
              <div class="flex items-center text-white/70">
                <svg class="w-5 h-5 mr-3 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span>Admin management tools</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')

const handleGoogleSignIn = async () => {
  try {
    loading.value = true
    error.value = ''
    
    await authStore.signInWithGoogle()
    router.push('/')
  } catch (err) {
    error.value = err.message || 'Sign in failed'
  } finally {
    loading.value = false
  }
}
</script>
