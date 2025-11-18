<template>
  <div class="space-y-4">
    <!-- Files Table -->
    <div class="overflow-hidden">
      <table class="min-w-full divide-y divide-white/10">
        <thead>
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              File Name
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              Size
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              Upload Date
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-white/70 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/10">
          <tr v-for="file in files" :key="file.id" class="hover:bg-white/5 transition-colors">
            <!-- File Name -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-8 w-8">
                  <div class="h-8 w-8 bg-primary-500/20 rounded-lg flex items-center justify-center">
                    <svg class="h-4 w-4 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-white truncate max-w-xs">
                    {{ file.file_name }}
                  </div>
                  <div class="text-sm text-white/60">
                    {{ file.content_type }}
                  </div>
                </div>
              </div>
            </td>

            <!-- File Size -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/70">
              {{ formatFileSize(file.file_size) }}
            </td>

            <!-- Upload Date -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/70">
              {{ formatDate(file.uploaded_at) }}
            </td>

            <!-- Actions -->
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <div class="flex items-center space-x-2">
                <button
                  @click="downloadFile(file)"
                  :disabled="loading"
                  class="text-primary-400 hover:text-primary-300 disabled:opacity-50 transition-colors"
                  title="Download"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </button>
                <button
                  @click="confirmDelete(file)"
                  :disabled="loading"
                  class="text-red-400 hover:text-red-300 disabled:opacity-50 transition-colors"
                  title="Delete"
                >
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="fileToDelete" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="glass-card rounded-xl p-6 max-w-md w-full mx-4">
        <div class="text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-500/20 mb-4">
            <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-white mb-2">Delete File</h3>
          <p class="text-white/70 mb-6">
            Are you sure you want to delete <strong>{{ fileToDelete.file_name }}</strong>? This action cannot be undone.
          </p>
          <div class="flex space-x-3">
            <button
              @click="fileToDelete = null"
              class="btn-secondary flex-1"
            >
              Cancel
            </button>
            <button
              @click="deleteFile"
              :disabled="loading"
              class="btn-danger flex-1"
            >
              {{ loading ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useFilesStore } from '@/stores/filesStore'

const props = defineProps({
  files: {
    type: Array,
    default: () => []
  }
})

const filesStore = useFilesStore()

// Refs
const fileToDelete = ref(null)

// Computed properties
const loading = computed(() => filesStore.loading)

// Methods
const formatFileSize = (bytes) => {
  return filesStore.formatFileSize(bytes)
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

const downloadFile = async (file) => {
  try {
    await filesStore.downloadFile(file)
  } catch (error) {
    console.error('Download error:', error)
  }
}

const confirmDelete = (file) => {
  fileToDelete.value = file
}

const deleteFile = async () => {
  if (!fileToDelete.value) return
  
  try {
    await filesStore.deleteFile(fileToDelete.value.id)
    fileToDelete.value = null
  } catch (error) {
    console.error('Delete error:', error)
  }
}
</script>
