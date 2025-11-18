<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-primary-900">
    <!-- Header -->
    <header class="glass-card m-4 rounded-xl">
      <div class="flex items-center justify-between p-6">
        <!-- Logo and Title -->
        <div class="flex items-center space-x-4">
          <button
            @click="$router.push('/')"
            class="text-white/70 hover:text-white transition-colors mr-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <img src="@/assets/kapsule-logo.svg" alt="Kapsule" class="h-8 w-auto mr-2" />
          <div>
            <h1 class="text-2xl font-bold text-white">My Files</h1>
            <p class="text-white/70 text-sm">Manage your uploaded files</p>
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
    <main class="px-4 pb-8" v-if="authInitialized">
      <div class="max-w-7xl mx-auto space-y-6">
        <!-- File Upload Zone -->
        <FileUploadZone />

        <!-- Filters -->
        <div class="glass-card rounded-xl p-4">
          <div class="flex flex-wrap items-center gap-4">
            <!-- Search -->
            <div class="flex-1 min-w-[200px]">
              <input
                v-model="filters.search"
                type="text"
                placeholder="Search files..."
                class="input-field w-full"
              />
            </div>

            <!-- File Type Filter -->
            <select
              v-model="filters.fileType"
              class="input-field"
            >
              <option value="">All Types</option>
              <option value="image">Images</option>
              <option value="video">Videos</option>
              <option value="document">Documents</option>
              <option value="audio">Audio</option>
              <option value="archive">Archives</option>
              <option value="other">Other</option>
            </select>

            <!-- Size Filter -->
            <select
              v-model="filters.sizeRange"
              class="input-field"
            >
              <option value="">All Sizes</option>
              <option value="small">Small (&lt; 1MB)</option>
              <option value="medium">Medium (1MB - 10MB)</option>
              <option value="large">Large (10MB - 100MB)</option>
              <option value="xlarge">Extra Large (&gt; 100MB)</option>
            </select>

            <!-- Date Filter -->
            <select
              v-model="filters.dateRange"
              class="input-field"
            >
              <option value="">All Time</option>
              <option value="today">Today</option>
              <option value="week">This Week</option>
              <option value="month">This Month</option>
              <option value="year">This Year</option>
            </select>

            <!-- Clear Filters -->
            <button
              @click="clearFilters"
              class="btn-secondary text-sm"
              v-if="hasActiveFilters"
            >
              Clear Filters
            </button>
          </div>
        </div>

        <!-- Files List -->
        <div class="glass-card rounded-xl">
          <div class="p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-white">
                Your Files 
                <span class="text-white/70 text-sm font-normal">({{ filteredFiles.length }})</span>
              </h2>
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
            <div v-else-if="filteredFiles.length === 0" class="text-center py-12">
              <svg class="mx-auto h-16 w-16 text-white/30 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 class="text-lg font-medium text-white mb-2">
                {{ hasActiveFilters ? 'No files match your filters' : 'No files yet' }}
              </h3>
              <p class="text-white/70 mb-4">
                {{ hasActiveFilters ? 'Try adjusting your filters' : 'Upload your first file to get started' }}
              </p>
              <button
                v-if="!hasActiveFilters"
                @click="refreshFiles"
                class="btn-primary"
              >
                Upload Files
              </button>
              <button
                v-else
                @click="clearFilters"
                class="btn-primary"
              >
                Clear Filters
              </button>
            </div>

            <!-- Files List -->
            <FileList :files="filteredFiles" v-else />
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
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useFilesStore } from '@/stores/filesStore'
import FileUploadZone from '@/components/FileUploadZone.vue'
import FileList from '@/components/FileList.vue'
import AdminToggle from '@/components/AdminToggle.vue'

const router = useRouter()
const authStore = useAuthStore()
const filesStore = useFilesStore()

// Filters
const filters = reactive({
  search: '',
  fileType: '',
  sizeRange: '',
  dateRange: ''
})

// Computed properties
const user = computed(() => authStore.user)
const userType = computed(() => authStore.userType)
const isAdmin = computed(() => authStore.isAdmin)
const userFileCount = computed(() => authStore.fileCount)
const userFileLimit = computed(() => authStore.fileLimit)
const loading = computed(() => filesStore.loading)
const authInitialized = computed(() => authStore.authInitialized)

// Filtered files
const filteredFiles = computed(() => {
  let result = [...filesStore.files]

  // Search filter
  if (filters.search) {
    const searchLower = filters.search.toLowerCase()
    result = result.filter(file => 
      file.file_name.toLowerCase().includes(searchLower)
    )
  }

  // File type filter
  if (filters.fileType) {
    result = result.filter(file => {
      const ext = file.file_name?.split('.').pop()?.toLowerCase() || ''
      const contentType = file.content_type?.toLowerCase() || ''
      
      switch (filters.fileType) {
        case 'image':
          return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext) || contentType.startsWith('image/')
        case 'video':
          return ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'].includes(ext) || contentType.startsWith('video/')
        case 'document':
          return ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'].includes(ext) || contentType.includes('document') || contentType.includes('pdf')
        case 'audio':
          return ['mp3', 'wav', 'flac', 'aac', 'ogg'].includes(ext) || contentType.startsWith('audio/')
        case 'archive':
          return ['zip', 'rar', '7z', 'tar', 'gz'].includes(ext) || contentType.includes('zip') || contentType.includes('archive')
        default:
          return true
      }
    })
  }

  // Size filter
  if (filters.sizeRange) {
    result = result.filter(file => {
      const sizeMB = file.file_size / (1024 * 1024)
      switch (filters.sizeRange) {
        case 'small':
          return sizeMB < 1
        case 'medium':
          return sizeMB >= 1 && sizeMB < 10
        case 'large':
          return sizeMB >= 10 && sizeMB < 100
        case 'xlarge':
          return sizeMB >= 100
        default:
          return true
      }
    })
  }

  // Date filter
  if (filters.dateRange) {
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    
    result = result.filter(file => {
      const fileDate = new Date(file.uploaded_at)
      
      switch (filters.dateRange) {
        case 'today':
          return fileDate >= today
        case 'week':
          const weekAgo = new Date(today)
          weekAgo.setDate(weekAgo.getDate() - 7)
          return fileDate >= weekAgo
        case 'month':
          const monthAgo = new Date(today)
          monthAgo.setMonth(monthAgo.getMonth() - 1)
          return fileDate >= monthAgo
        case 'year':
          const yearAgo = new Date(today)
          yearAgo.setFullYear(yearAgo.getFullYear() - 1)
          return fileDate >= yearAgo
        default:
          return true
      }
    })
  }

  return result
})

const hasActiveFilters = computed(() => {
  return filters.search || filters.fileType || filters.sizeRange || filters.dateRange
})

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

const clearFilters = () => {
  filters.search = ''
  filters.fileType = ''
  filters.sizeRange = ''
  filters.dateRange = ''
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

