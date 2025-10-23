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
              Limit
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/10">
          <tr v-for="user in users" :key="user.uid" class="hover:bg-white/5 transition-colors">
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

            <!-- Actions -->
            <td class="px-6 py-4 whitespace-nowrap text-sm">
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
            <label class="block text-sm font-medium text-white/70 mb-2">File Limit</label>
            <input
              v-model.number="editForm.file_limit"
              type="number"
              min="0"
              class="input-field w-full"
            />
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
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useAdminStore } from '@/stores/adminStore'

const adminStore = useAdminStore()

// Refs
const editingUser = ref(null)
const editForm = reactive({
  user_type: 'user',
  file_limit: 500
})

// Computed properties
const users = computed(() => adminStore.users)
const loading = computed(() => adminStore.loading)

// Methods
const editUser = (user) => {
  editingUser.value = user
  editForm.user_type = user.user_type
  editForm.file_limit = user.file_limit
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
    
    editingUser.value = null
  } catch (error) {
    console.error('Error updating user:', error)
  }
}

const viewUserFiles = (user) => {
  // This could open a modal or navigate to a user files view
  console.log('View files for user:', user.email)
}
</script>
