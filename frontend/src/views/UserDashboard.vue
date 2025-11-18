<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-primary-900">
    <!-- Header -->
    <header class="glass-card m-4 rounded-xl">
      <div class="flex items-center justify-between p-6">
        <!-- Logo and Title -->
        <div class="flex items-center space-x-4">
          <img src="@/assets/kapsule-logo.svg" alt="Kapsule" class="h-10 w-auto" />
          <div>
            <h1 class="text-2xl font-bold text-white">Dashboard</h1>
            <p class="text-white/70 text-sm">Overview & Statistics</p>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex items-center space-x-4">
          <button
            @click="$router.push('/files')"
            class="btn-primary text-sm"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Manage Files
          </button>
          <AdminToggle v-if="isAdmin" />
          <button
            @click="handleSignOut"
            class="btn-secondary text-sm"
          >
            Sign Out
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-4 pb-8" v-if="authInitialized">
      <div class="max-w-7xl mx-auto space-y-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <!-- Total Files -->
          <div class="glass-card rounded-xl p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary-500/20 rounded-lg">
                <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-white/70 text-sm">Total Files</p>
                <p class="text-2xl font-bold text-white">{{ filesCount }}</p>
              </div>
            </div>
          </div>

          <!-- Storage Used -->
          <div class="glass-card rounded-xl p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary-500/20 rounded-lg">
                <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-white/70 text-sm">Storage Used</p>
                <p class="text-2xl font-bold text-white">{{ formatFileSize(totalSize) }}</p>
              </div>
            </div>
          </div>

          <!-- File Limit -->
          <div class="glass-card rounded-xl p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary-500/20 rounded-lg">
                <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-white/70 text-sm">File Limit</p>
                <p class="text-2xl font-bold text-white">{{ userFileCount }}/{{ userFileLimit }}</p>
              </div>
            </div>
          </div>

          <!-- File Size Limit -->
          <div class="glass-card rounded-xl p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary-500/20 rounded-lg">
                <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-white/70 text-sm">Max File Size</p>
                <p class="text-2xl font-bold text-white">{{ formatFileSizeLimit(userFileSizeLimit) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Files -->
        <div class="glass-card rounded-xl">
          <div class="p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-white">Recent Files</h2>
              <button
                @click="$router.push('/files')"
                class="btn-secondary text-sm"
              >
                View All
              </button>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex items-center justify-center py-12">
              <div class="animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent"></div>
            </div>

            <!-- Empty State -->
            <div v-else-if="recentFiles.length === 0" class="text-center py-12">
              <svg class="mx-auto h-16 w-16 text-white/30 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 class="text-lg font-medium text-white mb-2">No files yet</h3>
              <p class="text-white/70 mb-4">Upload your first file to get started</p>
              <button
                @click="$router.push('/files')"
                class="btn-primary"
              >
                Upload Files
              </button>
            </div>

            <!-- Recent Files List -->
            <div v-else class="space-y-2">
              <div 
                v-for="file in recentFiles" 
                :key="file.id"
                class="flex items-center justify-between bg-white/5 rounded-lg p-4 hover:bg-white/10 transition-colors"
              >
                <div class="flex items-center space-x-4 flex-1">
                  <div class="h-10 w-10 bg-primary-500/20 rounded-lg flex items-center justify-center">
                    <svg class="h-5 w-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-white truncate">{{ file.file_name }}</p>
                    <p class="text-xs text-white/60">{{ formatFileSize(file.file_size) }} • {{ formatDate(file.uploaded_at) }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <button
                    @click="downloadFile(file)"
                    class="text-primary-400 hover:text-primary-300 transition-colors"
                    title="Download"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Auth Loading State -->
    <main class="px-4 pb-8" v-else>
      <div class="max-w-7xl mx-auto flex items-center justify-center min-h-[60vh]">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-2 border-primary-500 border-t-transparent mx-auto mb-4"></div>
          <p class="text-white/70">Loading...</p>
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
const userFileSizeLimit = computed(() => authStore.fileSizeLimit)
const filesCount = computed(() => filesStore.filesCount)
const totalSize = computed(() => filesStore.totalSize)
const loading = computed(() => filesStore.loading)
const authInitialized = computed(() => authStore.authInitialized)

// Get recent files (last 5)
const recentFiles = computed(() => {
  return filesStore.files.slice(0, 5)
})

// Methods
const handleSignOut = async () => {
  await authStore.signOutUser()
  router.push('/login')
}

const formatFileSize = (bytes) => {
  return filesStore.formatFileSize(bytes)
}

const formatFileSizeLimit = (bytes) => {
  if (!bytes) return '100 MB'
  const mb = Math.round(bytes / (1024 * 1024))
  return `${mb} MB`
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const downloadFile = async (file) => {
  try {
    await filesStore.downloadFile(file)
  } catch (error) {
    console.error('Download error:', error)
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

