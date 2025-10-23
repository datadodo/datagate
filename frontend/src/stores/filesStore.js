import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useFilesStore = defineStore('files', () => {
  const files = ref([])
  const loading = ref(false)
  const error = ref(null)
  const uploadProgress = ref({})
  const userFileLimit = ref(500)
  const userFileCount = ref(0)

  // Computed properties
  const filesCount = computed(() => files.value.length)
  const totalSize = computed(() => 
    files.value.reduce((total, file) => total + file.file_size, 0)
  )
  const canUploadMore = computed(() => 
    userFileCount.value < userFileLimit.value
  )
  const remainingSlots = computed(() => 
    userFileLimit.value - userFileCount.value
  )

  // Format file size
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  // Get user's files
  const fetchFiles = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await api.get('/api/files/my-files')
      files.value = response.data.files
      userFileLimit.value = response.data.user_file_limit
      userFileCount.value = response.data.user_file_count
      
      return response.data
    } catch (error) {
      console.error('Error fetching files:', error)
      error.value = error.response?.data?.detail || 'Failed to fetch files'
      throw error
    } finally {
      loading.value = false
    }
  }

  // Upload single file
  const uploadFile = async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await api.post('/api/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          uploadProgress.value[file.name] = progress
        }
      })
      
      // Remove from progress tracking
      delete uploadProgress.value[file.name]
      
      // Refresh files list
      await fetchFiles()
      
      return response.data
    } catch (error) {
      console.error('Error uploading file:', error)
      delete uploadProgress.value[file.name]
      error.value = error.response?.data?.detail || 'Failed to upload file'
      throw error
    }
  }

  // Upload multiple files
  const uploadBatchFiles = async (files) => {
    try {
      const formData = new FormData()
      files.forEach(file => {
        formData.append('files', file)
      })
      
      const response = await api.post('/api/files/upload-batch', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          files.forEach(file => {
            uploadProgress.value[file.name] = progress
          })
        }
      })
      
      // Clear progress tracking
      files.forEach(file => {
        delete uploadProgress.value[file.name]
      })
      
      // Refresh files list
      await fetchFiles()
      
      return response.data
    } catch (error) {
      console.error('Error uploading files:', error)
      files.forEach(file => {
        delete uploadProgress.value[file.name]
      })
      error.value = error.response?.data?.detail || 'Failed to upload files'
      throw error
    }
  }

  // Delete file
  const deleteFile = async (fileId) => {
    try {
      loading.value = true
      error.value = null
      
      await api.delete(`/api/files/${fileId}`)
      
      // Remove from local state
      files.value = files.value.filter(file => file.id !== fileId)
      userFileCount.value -= 1
      
      return true
    } catch (error) {
      console.error('Error deleting file:', error)
      error.value = error.response?.data?.detail || 'Failed to delete file'
      throw error
    } finally {
      loading.value = false
    }
  }

  // Get download URL
  const getDownloadUrl = async (fileId) => {
    try {
      const response = await api.get(`/api/files/${fileId}/download`)
      return response.data.download_url
    } catch (error) {
      console.error('Error getting download URL:', error)
      error.value = error.response?.data?.detail || 'Failed to get download URL'
      throw error
    }
  }

  // Download file
  const downloadFile = async (file) => {
    try {
      const downloadUrl = await getDownloadUrl(file.id)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = file.file_name
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    } catch (error) {
      console.error('Error downloading file:', error)
      throw error
    }
  }

  // Clear error
  const clearError = () => {
    error.value = null
  }

  // Clear upload progress
  const clearUploadProgress = () => {
    uploadProgress.value = {}
  }

  return {
    // State
    files,
    loading,
    error,
    uploadProgress,
    userFileLimit,
    userFileCount,
    
    // Computed
    filesCount,
    totalSize,
    canUploadMore,
    remainingSlots,
    
    // Actions
    fetchFiles,
    uploadFile,
    uploadBatchFiles,
    deleteFile,
    getDownloadUrl,
    downloadFile,
    formatFileSize,
    clearError,
    clearUploadProgress
  }
})
