<template>
  <div v-if="false"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  router.replace('/admin')
})
</script>

<!-- OLD ADMIN VIEW - REDIRECTED TO NEW STRUCTURE -->
<!--
<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-primary-900">
    <!-- Header -->
    <header class="glass-card m-4 rounded-xl">
      <div class="flex items-center justify-between p-6">
        <!-- Logo and Title -->
        <div class="flex items-center space-x-4">
          <div class="h-10 w-10 bg-gradient-to-r from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-white">Admin Panel</h1>
            <p class="text-white/70 text-sm">Manage users and files</p>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex items-center space-x-4">
          <button
            @click="$router.push('/')"
            class="btn-secondary text-sm"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Dashboard
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

        <!-- Tabs -->
        <div class="glass-card rounded-xl">
          <div class="border-b border-white/10">
            <nav class="flex space-x-8 px-6">
              <button
                @click="activeTab = 'users'"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                  activeTab === 'users'
                    ? 'border-primary-500 text-primary-400'
                    : 'border-transparent text-white/70 hover:text-white'
                ]"
              >
                Users Management
              </button>
              <button
                @click="activeTab = 'files'"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                  activeTab === 'files'
                    ? 'border-primary-500 text-primary-400'
                    : 'border-transparent text-white/70 hover:text-white'
                ]"
              >
                All Files
              </button>
            </nav>
          </div>

          <div class="p-6">
            <!-- Users Tab -->
            <div v-if="activeTab === 'users'">
              <UsersManagement />
            </div>

            <!-- Files Tab -->
            <div v-if="activeTab === 'files'">
              <FilesManagement />
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import UsersManagement from '@/components/admin/UsersManagement.vue'
import FilesManagement from '@/components/admin/FilesManagement.vue'

const adminStore = useAdminStore()

const activeTab = ref('users')

// Computed properties
const stats = computed(() => adminStore.stats)
const loading = computed(() => adminStore.loading)

// Methods
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
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
    console.error('Error loading admin data:', error)
  }
})
</script>
