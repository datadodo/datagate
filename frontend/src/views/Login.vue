<template>
  <div class="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="mx-auto mb-6 flex justify-center">
          <img src="@/assets/kapsule-logo.svg" alt="Kapsule" class="h-20 w-auto" />
        </div>
        <p class="text-white/70">Secure file management system</p>
      </div>

      <!-- Login Form -->
      <div class="glass-card p-8">
        <div class="space-y-6">
          <!-- Toggle between Sign In and Sign Up -->
          <div class="flex bg-white/10 rounded-lg p-1">
            <button
              @click="isSignUp = false"
              :class="[
                'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all duration-300',
                !isSignUp ? 'bg-primary-500 text-white' : 'text-white/70 hover:text-white'
              ]"
            >
              Sign In
            </button>
            <button
              @click="isSignUp = true"
              :class="[
                'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all duration-300',
                isSignUp ? 'bg-primary-500 text-white' : 'text-white/70 hover:text-white'
              ]"
            >
              Sign Up
            </button>
          </div>

          <!-- Email and Password Form -->
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-white/70 mb-2">Email</label>
              <input
                v-model="email"
                type="email"
                required
                class="input-field w-full"
                placeholder="Enter your email"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-white/70 mb-2">Password</label>
              <input
                v-model="password"
                type="password"
                required
                class="input-field w-full"
                placeholder="Enter your password"
                minlength="6"
              />
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ loading ? 'Please wait...' : (isSignUp ? 'Create Account' : 'Sign In') }}
            </button>
          </form>

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
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const isSignUp = ref(false)
const email = ref('')
const password = ref('')

const loading = computed(() => authStore.loading)
const error = computed(() => authStore.error)

// Clear error when switching between Sign In and Sign Up
watch(isSignUp, () => {
  authStore.clearError()
})

const handleSubmit = async () => {
  try {
    authStore.clearError()
    
    if (isSignUp.value) {
      await authStore.signUpWithEmail(email.value, password.value)
    } else {
      await authStore.signInWithEmail(email.value, password.value)
    }
    
    router.push('/')
  } catch (err) {
    // Error is already set in the store, so it will be displayed automatically
    console.error('Authentication error:', err)
  }
}
</script>
