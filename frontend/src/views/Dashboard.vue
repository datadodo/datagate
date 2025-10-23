<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-primary-900">
    <!-- Header -->
    <header class="glass-card m-4 rounded-xl">
      <div class="flex items-center justify-between p-6">
        <!-- Logo and Title -->
        <div class="flex items-center space-x-4">
          <div class="h-10 w-10 bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">DataGate</h1>
            <p class="text-white/70 text-sm">File Management System</p>
          </div>
        </div>

        <!-- User Info and Actions -->
        <div class="flex items-center space-x-4">
          <!-- File Limit Indicator -->
          <div class="text-right">
            <p class="text-white/70 text-sm">Files</p>
            <p class="text-white font-medium">{{ userFileCount }}/{{ userFileLimit }}</p>
          </div>

          <!-- Admin Toggle (if admin) -->
          <AdminToggle v-if="isAdmin" />

          <!-- User Menu -->
          <div class="flex items-center space-x-3">
            <div class="text-right">
              <p class="text-white font-medium">{{ user?.email }}</p>
              <p class="text-white/70 text-sm capitalize">{{ userType }}</p>
            </div>
            <button
              @click="handleSignOut"
              class="btn-secondary text-sm"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-4 pb-8">
      <div class="max-w-7xl mx-auto space-y-6">
        <!-- File Upload Zone -->
        <FileUploadZone />

        <!-- Files List -->
        <div class="glass-card rounded-xl">
          <div class="p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-white">Your Files</h2>
              <button
                @click="refreshFiles"
                :disabled="loading"
                class="btn-secondary text-sm"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Refresh
              </button>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex items-center justify-center py-12">
              <div class="animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent"></div>
            </div>

            <!-- Empty State -->
            <div v-else-if="filesCount === 0" class="text-center py-12">
              <svg class="mx-auto h-16 w-16 text-white/30 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 class="text-lg font-medium text-white mb-2">No files yet</h3>
              <p class="text-white/70">Upload your first file to get started</p>
            </div>

            <!-- Files List -->
            <FileList v-else />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useFilesStore } from '@/stores/filesStore'
import FileUploadZone from '@/components/FileUploadZone.vue'
import FileList from '@/components/FileList.vue'
import AdminToggle from '@/components/AdminToggle.vue'

const router = useRouter()
const authStore = useAuthStore()
const filesStore = useFilesStore()

// Computed properties
const user = computed(() => authStore.user)
const userType = computed(() => authStore.userType)
const isAdmin = computed(() => authStore.isAdmin)
const userFileCount = computed(() => authStore.fileCount)
const userFileLimit = computed(() => authStore.fileLimit)
const filesCount = computed(() => filesStore.filesCount)
const loading = computed(() => filesStore.loading)

// Methods
const handleSignOut = async () => {
  await authStore.signOutUser()
  router.push('/login')
}

const refreshFiles = async () => {
  try {
    await filesStore.fetchFiles()
  } catch (error) {
    console.error('Error refreshing files:', error)
  }
}

// Lifecycle
onMounted(async () => {
  try {
    await filesStore.fetchFiles()
  } catch (error) {
    console.error('Error loading files:', error)
  }
})
</script>
