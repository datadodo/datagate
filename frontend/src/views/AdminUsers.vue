<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-primary-900">
    <!-- Header -->
    <header class="glass-card m-4 rounded-xl">
      <div class="flex items-center justify-between p-6">
        <!-- Logo and Title -->
        <div class="flex items-center space-x-4">
          <button
            @click="$router.push('/admin')"
            class="text-white/70 hover:text-white transition-colors mr-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <div>
            <h1 class="text-2xl font-bold text-white">User Management</h1>
            <p class="text-white/70 text-sm">Manage all users</p>
          </div>
        </div>

        <!-- Navigation -->
        <div class="flex items-center space-x-4">
          <button
            @click="$router.push('/admin')"
            class="btn-secondary text-sm"
          >
            Dashboard
          </button>
          <button
            @click="$router.push('/admin/files')"
            class="btn-secondary text-sm"
          >
            Manage Files
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="px-4 pb-8">
      <div class="max-w-7xl mx-auto space-y-6">
        <!-- Filters -->
        <div class="glass-card rounded-xl p-4">
          <div class="flex flex-wrap items-center gap-4">
            <!-- Search -->
            <div class="flex-1 min-w-[200px]">
              <input
                v-model="filters.search"
                type="text"
                placeholder="Search users..."
                class="input-field w-full"
              />
            </div>

            <!-- User Type Filter -->
            <select
              v-model="filters.userType"
              class="input-field"
            >
              <option value="">All Types</option>
              <option value="admin">Admin</option>
              <option value="user">User</option>
            </select>

            <!-- File Count Filter -->
            <select
              v-model="filters.fileCount"
              class="input-field"
            >
              <option value="">All Users</option>
              <option value="hasFiles">Has Files</option>
              <option value="noFiles">No Files</option>
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

        <!-- Users List -->
        <div class="glass-card rounded-xl">
          <div class="p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-white">
                Users 
                <span class="text-white/70 text-sm font-normal">({{ filteredUsers.length }})</span>
              </h2>
              <button
                @click="refreshUsers"
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
            <div v-else-if="filteredUsers.length === 0" class="text-center py-12">
              <svg class="mx-auto h-16 w-16 text-white/30 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
              <h3 class="text-lg font-medium text-white mb-2">
                {{ hasActiveFilters ? 'No users match your filters' : 'No users found' }}
              </h3>
              <p class="text-white/70 mb-4">
                {{ hasActiveFilters ? 'Try adjusting your filters' : 'Users will appear here once they sign up' }}
              </p>
              <button
                v-if="hasActiveFilters"
                @click="clearFilters"
                class="btn-primary"
              >
                Clear Filters
              </button>
            </div>

            <!-- Users List -->
            <UsersManagement :users="filteredUsers" v-else />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, reactive, onMounted } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import UsersManagement from '@/components/admin/UsersManagement.vue'

const adminStore = useAdminStore()

// Filters
const filters = reactive({
  search: '',
  userType: '',
  fileCount: ''
})

// Computed properties
const allUsers = computed(() => adminStore.users)
const loading = computed(() => adminStore.loading)

// Filtered users
const filteredUsers = computed(() => {
  let result = [...allUsers.value]

  // Search filter
  if (filters.search) {
    const searchLower = filters.search.toLowerCase()
    result = result.filter(user => 
      user.email.toLowerCase().includes(searchLower) ||
      user.uid.toLowerCase().includes(searchLower)
    )
  }

  // User type filter
  if (filters.userType) {
    result = result.filter(user => user.user_type === filters.userType)
  }

  // File count filter
  if (filters.fileCount) {
    result = result.filter(user => {
      if (filters.fileCount === 'hasFiles') {
        return user.file_count > 0
      } else if (filters.fileCount === 'noFiles') {
        return user.file_count === 0
      }
      return true
    })
  }

  return result
})

const hasActiveFilters = computed(() => {
  return filters.search || filters.userType || filters.fileCount
})

// Methods
const refreshUsers = async () => {
  try {
    await adminStore.fetchUsers()
  } catch (error) {
    console.error('Error refreshing users:', error)
  }
}

const clearFilters = () => {
  filters.search = ''
  filters.userType = ''
  filters.fileCount = ''
}

// Lifecycle
onMounted(async () => {
  try {
    await adminStore.fetchUsers()
  } catch (error) {
    console.error('Error loading users:', error)
  }
})
</script>

