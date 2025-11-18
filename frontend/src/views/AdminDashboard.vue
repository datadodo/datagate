<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-primary-900">
    <!-- Header -->
    <header class="glass-card m-4 rounded-xl">
      <div class="flex items-center justify-between p-6">
        <!-- Logo and Title -->
        <div class="flex items-center space-x-4">
          <div class="h-10 w-10 bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">Admin Dashboard</h1>
            <p class="text-white/70 text-sm">System Overview & Analytics</p>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex items-center space-x-4">
          <button
            @click="$router.push('/admin/files')"
            class="btn-primary text-sm"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Manage Files
          </button>
          <button
            @click="$router.push('/admin/users')"
            class="btn-primary text-sm"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
            </svg>
            Manage Users
          </button>
          <button
            @click="$router.push('/')"
            class="btn-secondary text-sm"
          >
            User View
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-4 pb-8">
      <div class="max-w-7xl mx-auto space-y-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="glass-card rounded-xl p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary-500/20 rounded-lg">
                <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-white/70 text-sm">Total Users</p>
                <p class="text-2xl font-bold text-white">{{ stats.total_users || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="glass-card rounded-xl p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary-500/20 rounded-lg">
                <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-white/70 text-sm">Total Files</p>
                <p class="text-2xl font-bold text-white">{{ stats.total_files || 0 }}</p>
              </div>
            </div>
          </div>

          <div class="glass-card rounded-xl p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary-500/20 rounded-lg">
                <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-white/70 text-sm">Storage Used</p>
                <p class="text-2xl font-bold text-white">{{ formatFileSize(stats.total_storage_bytes || 0) }}</p>
              </div>
            </div>
          </div>

          <div class="glass-card rounded-xl p-6">
            <div class="flex items-center">
              <div class="p-3 bg-primary-500/20 rounded-lg">
                <svg class="w-6 h-6 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-white/70 text-sm">Admin Users</p>
                <p class="text-2xl font-bold text-white">{{ stats.admin_users || 0 }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Additional Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- File Type Distribution -->
          <div class="glass-card rounded-xl p-6">
            <h3 class="text-lg font-semibold text-white mb-4">File Types</h3>
            <div v-if="loading" class="flex items-center justify-center py-8">
              <div class="animate-spin rounded-full h-6 w-6 border-2 border-primary-500 border-t-transparent"></div>
            </div>
            <div v-else class="space-y-3">
              <div 
                v-for="type in fileTypeStats" 
                :key="type.extension"
                class="flex items-center justify-between"
              >
                <div class="flex items-center space-x-2">
                  <span class="text-white/70 text-sm">{{ type.extension || 'Unknown' }}</span>
                </div>
                <div class="flex items-center space-x-3">
                  <div class="w-32 bg-white/10 rounded-full h-2">
                    <div 
                      class="bg-primary-500 h-2 rounded-full transition-all"
                      :style="{ width: `${(type.count / (stats.total_files || 1)) * 100}%` }"
                    ></div>
                  </div>
                  <span class="text-white text-sm font-medium w-8 text-right">{{ type.count }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="glass-card rounded-xl p-6">
            <h3 class="text-lg font-semibold text-white mb-4">Recent Files</h3>
            <div v-if="loading" class="flex items-center justify-center py-8">
              <div class="animate-spin rounded-full h-6 w-6 border-2 border-primary-500 border-t-transparent"></div>
            </div>
            <div v-else-if="recentFiles.length === 0" class="text-center py-8">
              <p class="text-white/70">No files uploaded yet</p>
            </div>
            <div v-else class="space-y-2 max-h-64 overflow-y-auto">
              <div 
                v-for="file in recentFiles" 
                :key="file.id"
                class="flex items-center justify-between bg-white/5 rounded-lg p-3 hover:bg-white/10 transition-colors"
              >
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-white truncate">{{ file.file_name }}</p>
                  <p class="text-xs text-white/60">{{ getOwnerEmail(file.user_id) }} • {{ formatDate(file.uploaded_at) }}</p>
                </div>
                <span class="text-xs text-white/70 ml-2">{{ formatFileSize(file.file_size) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '@/stores/adminStore'

const router = useRouter()
const adminStore = useAdminStore()

// Computed properties
const stats = computed(() => adminStore.stats)
const loading = computed(() => adminStore.loading)
const allFiles = computed(() => adminStore.allFiles)
const users = computed(() => adminStore.users)

// Get recent files (last 10)
const recentFiles = computed(() => {
  return allFiles.value.slice(0, 10)
})

// File type statistics
const fileTypeStats = computed(() => {
  const typeMap = {}
  allFiles.value.forEach(file => {
    const ext = file.file_name?.split('.').pop()?.toLowerCase() || 'unknown'
    typeMap[ext] = (typeMap[ext] || 0) + 1
  })
  
  return Object.entries(typeMap)
    .map(([extension, count]) => ({ extension: `.${extension}`, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
})

// Methods
const formatFileSize = (bytes) => {
  return adminStore.formatFileSize(bytes)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getOwnerEmail = (userId) => {
  const user = users.value.find(u => u.uid === userId)
  return user ? user.email : 'Unknown'
}

// Lifecycle
onMounted(async () => {
  try {
    await Promise.all([
      adminStore.fetchUsers(),
      adminStore.fetchAllFiles(),
      adminStore.fetchStats()
    ])
  } catch (error) {
    console.error('Error loading admin dashboard data:', error)
  }
})
</script>

