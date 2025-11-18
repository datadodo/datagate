<template>
  <div class="space-y-6">
    <!-- Users Table -->
    <div class="overflow-hidden">
      <table class="min-w-full divide-y divide-white/10">
        <thead>
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              User
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              Type
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              Files
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              File Limit
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              Size Limit
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/10">
          <tr 
            v-for="user in users" 
            :key="user.uid" 
            class="hover:bg-white/5 transition-colors cursor-pointer"
            @click="viewUserFiles(user)"
          >
            <!-- User Info -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-8 w-8">
                  <div class="h-8 w-8 bg-primary-500/20 rounded-full flex items-center justify-center">
                    <svg class="h-4 w-4 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-white">
                    {{ user.email }}
                  </div>
                  <div class="text-sm text-white/60">
                    ID: {{ user.uid.substring(0, 8) }}...
                  </div>
                </div>
              </div>
            </td>

            <!-- User Type -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                :class="[
                  'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                  user.user_type === 'admin'
                    ? 'bg-primary-500/20 text-primary-400'
                    : 'bg-white/10 text-white/70'
                ]"
              >
                {{ user.user_type }}
              </span>
            </td>

            <!-- File Count -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/70">
              {{ user.file_count }}
            </td>

            <!-- File Limit -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/70">
              {{ user.file_limit }}
            </td>

            <!-- File Size Limit -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/70">
              {{ formatFileSizeLimit(user.file_size_limit) }}
            </td>

            <!-- Actions -->
            <td class="px-6 py-4 whitespace-nowrap text-sm" @click.stop>
              <div class="flex items-center space-x-2">
                <button
                  @click="editUser(user)"
                  class="text-primary-400 hover:text-primary-300 transition-colors"
                  title="Edit User"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click="viewUserFiles(user)"
                  class="text-white/70 hover:text-white transition-colors"
                  title="View Files"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit User Modal -->
    <div v-if="editingUser" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="glass-card rounded-xl p-6 max-w-md w-full mx-4">
        <div class="space-y-4">
          <h3 class="text-lg font-medium text-white">Edit User</h3>
          
          <div>
            <label class="block text-sm font-medium text-white/70 mb-2">Email</label>
            <input
              :value="editingUser.email"
              disabled
              class="input-field w-full opacity-50"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-white/70 mb-2">User Type</label>
            <select
              v-model="editForm.user_type"
              class="input-field w-full"
            >
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-white/70 mb-2">File Limit (number of files)</label>
            <input
              v-model.number="editForm.file_limit"
              type="number"
              min="0"
              class="input-field w-full"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-white/70 mb-2">File Size Limit (MB)</label>
            <input
              v-model.number="editForm.file_size_limit_mb"
              type="number"
              min="1"
              class="input-field w-full"
              placeholder="e.g., 100"
            />
            <p class="text-xs text-white/50 mt-1">Maximum size per file in megabytes</p>
          </div>

          <div class="flex space-x-3 pt-4">
            <button
              @click="editingUser = null"
              class="btn-secondary flex-1"
            >
              Cancel
            </button>
            <button
              @click="saveUserChanges"
              :disabled="loading"
              class="btn-primary flex-1"
            >
              {{ loading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- User Files Modal -->
    <div v-if="viewingUser" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="glass-card rounded-xl p-6 max-w-4xl w-full mx-4 max-h-[80vh] overflow-hidden">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-white">Files for {{ viewingUser.email }}</h3>
            <button
              @click="viewingUser = null"
              class="text-white/70 hover:text-white transition-colors"
            >
              <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <!-- User Info -->
          <div class="bg-white/5 rounded-lg p-4">
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="text-white/70">User Type:</span>
                <span class="ml-2 text-white">{{ viewingUser.user_type }}</span>
              </div>
              <div>
                <span class="text-white/70">File Count:</span>
                <span class="ml-2 text-white">{{ viewingUser.file_count }}</span>
              </div>
              <div>
                <span class="text-white/70">File Limit:</span>
                <span class="ml-2 text-white">{{ viewingUser.file_limit }}</span>
              </div>
              <div>
                <span class="text-white/70">File Size Limit:</span>
                <span class="ml-2 text-white">{{ formatFileSizeLimit(viewingUser.file_size_limit) }}</span>
              </div>
              <div>
                <span class="text-white/70">User ID:</span>
                <span class="ml-2 text-white font-mono text-xs">{{ viewingUser.uid.substring(0, 8) }}...</span>
              </div>
            </div>
          </div>

          <!-- Files List -->
          <div class="max-h-96 overflow-y-auto">
            <div v-if="userFilesLoading" class="flex items-center justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent"></div>
            </div>
            
            <div v-else-if="userFiles.length === 0" class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-white/30 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p class="text-white/70">No files uploaded yet</p>
            </div>
            
            <div v-else class="space-y-2">
              <div 
                v-for="file in userFiles" 
                :key="file.id"
                class="flex items-center justify-between bg-white/5 rounded-lg p-3 hover:bg-white/10 transition-colors"
              >
                <div class="flex items-center space-x-3">
                  <div class="h-8 w-8 bg-primary-500/20 rounded-lg flex items-center justify-center">
                    <svg class="h-4 w-4 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-white">{{ file.file_name }}</div>
                    <div class="text-xs text-white/60">{{ formatFileSize(file.file_size) }} • {{ formatDate(file.uploaded_at) }}</div>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <button
                    @click="downloadUserFile(file)"
                    class="text-primary-400 hover:text-primary-300 transition-colors"
                    title="Download"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </button>
                  <button
                    @click="deleteUserFile(file)"
                    class="text-red-400 hover:text-red-300 transition-colors"
                    title="Delete"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useAdminStore } from '@/stores/adminStore'

const props = defineProps({
  users: {
    type: Array,
    default: () => []
  }
})

const adminStore = useAdminStore()

// Refs
const editingUser = ref(null)
const viewingUser = ref(null)
const userFiles = ref([])
const userFilesLoading = ref(false)
const editForm = reactive({
  user_type: 'user',
  file_limit: 500,
  file_size_limit_mb: 100  // Default 100MB
})

// Computed properties
const loading = computed(() => adminStore.loading)

// Methods
const editUser = (user) => {
  editingUser.value = user
  editForm.user_type = user.user_type
  editForm.file_limit = user.file_limit
  // Convert bytes to MB for display
  editForm.file_size_limit_mb = Math.round((user.file_size_limit || 100 * 1024 * 1024) / (1024 * 1024))
}

const saveUserChanges = async () => {
  if (!editingUser.value) return
  
  try {
    // Update user type if changed
    if (editForm.user_type !== editingUser.value.user_type) {
      await adminStore.updateUserType(editingUser.value.uid, editForm.user_type)
    }
    
    // Update file limit if changed
    if (editForm.file_limit !== editingUser.value.file_limit) {
      await adminStore.updateUserFileLimit(editingUser.value.uid, editForm.file_limit)
    }
    
    // Update file size limit if changed
    const currentSizeLimitMb = Math.round((editingUser.value.file_size_limit || 100 * 1024 * 1024) / (1024 * 1024))
    if (editForm.file_size_limit_mb !== currentSizeLimitMb) {
      await adminStore.updateUserFileSizeLimit(editingUser.value.uid, editForm.file_size_limit_mb)
    }
    
    // Refresh users list to show updated values
    await adminStore.fetchUsers()
    
    editingUser.value = null
  } catch (error) {
    console.error('Error updating user:', error)
  }
}

const viewUserFiles = async (user) => {
  console.log('viewUserFiles called with user:', user)
  console.log('user.uid:', user.uid)
  
  viewingUser.value = user
  userFilesLoading.value = true
  
  try {
    const files = await adminStore.fetchUserFiles(user.uid)
    console.log('Fetched files:', files)
    userFiles.value = files
  } catch (error) {
    console.error('Error fetching user files:', error)
    userFiles.value = []
  } finally {
    userFilesLoading.value = false
  }
}

const formatFileSize = (bytes) => {
  return adminStore.formatFileSize(bytes)
}

const formatFileSizeLimit = (bytes) => {
  if (!bytes) return '100 MB'  // Default
  const mb = Math.round(bytes / (1024 * 1024))
  return `${mb} MB`
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

const downloadUserFile = async (file) => {
  try {
    await adminStore.downloadFile(file)
  } catch (error) {
    console.error('Download error:', error)
  }
}

const deleteUserFile = async (file) => {
  if (confirm(`Are you sure you want to delete "${file.file_name}"?`)) {
    try {
      await adminStore.deleteAnyFile(file.id)
      // Remove from local list
      userFiles.value = userFiles.value.filter(f => f.id !== file.id)
      // Update user's file count
      viewingUser.value.file_count -= 1
    } catch (error) {
      console.error('Delete error:', error)
    }
  }
}
</script>
