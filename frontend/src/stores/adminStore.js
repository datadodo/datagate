import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAdminStore = defineStore('admin', () => {
  const users = ref([])
  const allFiles = ref([])
  const stats = ref({})
  const loading = ref(false)
  const error = ref(null)

  // Computed properties
  const adminUsers = computed(() => 
    users.value.filter(user => user.user_type === 'admin')
  )
  const regularUsers = computed(() => 
    users.value.filter(user => user.user_type === 'user')
  )
  const totalUsers = computed(() => users.value.length)
  const totalFiles = computed(() => allFiles.value.length)
  const totalStorage = computed(() => 
    allFiles.value.reduce((total, file) => total + file.file_size, 0)
  )

  // Format file size
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  // Get all users
  const fetchUsers = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await api.get('/api/admin/users')
      users.value = response.data
      
      return response.data
    } catch (error) {
      console.error('Error fetching users:', error)
      error.value = error.response?.data?.detail || 'Failed to fetch users'
      throw error
    } finally {
      loading.value = false
    }
  }

  // Get all files
  const fetchAllFiles = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await api.get('/api/admin/files')
      allFiles.value = response.data
      
      return response.data
    } catch (error) {
      console.error('Error fetching all files:', error)
      error.value = error.response?.data?.detail || 'Failed to fetch files'
      throw error
    } finally {
      loading.value = false
    }
  }

  // Get admin stats
  const fetchStats = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await api.get('/api/admin/stats')
      stats.value = response.data
      
      return response.data
    } catch (error) {
      console.error('Error fetching stats:', error)
      error.value = error.response?.data?.detail || 'Failed to fetch stats'
      throw error
    } finally {
      loading.value = false
    }
  }

  // Get files for specific user
  const fetchUserFiles = async (userId) => {
    try {
      const response = await api.get(`/api/admin/users/${userId}/files`)
      return response.data
    } catch (error) {
      console.error('Error fetching user files:', error)
      error.value = error.response?.data?.detail || 'Failed to fetch user files'
      throw error
    }
  }

  // Update user file limit
  const updateUserFileLimit = async (userId, newLimit) => {
    try {
      loading.value = true
      error.value = null
      
      await api.put(`/api/admin/users/${userId}/file-limit`, null, {
        params: { new_limit: newLimit }
      })
      
      // Update local state
      const user = users.value.find(u => u.uid === userId)
      if (user) {
        user.file_limit = newLimit
      }
      
      return true
    } catch (error) {
      console.error('Error updating file limit:', error)
      error.value = error.response?.data?.detail || 'Failed to update file limit'
      throw error
    } finally {
      loading.value = false
    }
  }

  // Update user type
  const updateUserType = async (userId, userType) => {
    try {
      loading.value = true
      error.value = null
      
      await api.put(`/api/admin/users/${userId}/user-type`, null, {
        params: { user_type: userType }
      })
      
      // Update local state
      const user = users.value.find(u => u.uid === userId)
      if (user) {
        user.user_type = userType
      }
      
      return true
    } catch (error) {
      console.error('Error updating user type:', error)
      error.value = error.response?.data?.detail || 'Failed to update user type'
      throw error
    } finally {
      loading.value = false
    }
  }

  // Delete any file
  const deleteAnyFile = async (fileId) => {
    try {
      loading.value = true
      error.value = null
      
      await api.delete(`/api/admin/files/${fileId}`)
      
      // Remove from local state
      allFiles.value = allFiles.value.filter(file => file.id !== fileId)
      
      return true
    } catch (error) {
      console.error('Error deleting file:', error)
      error.value = error.response?.data?.detail || 'Failed to delete file'
      throw error
    } finally {
      loading.value = false
    }
  }

  // Get download URL for any file
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

  return {
    // State
    users,
    allFiles,
    stats,
    loading,
    error,
    
    // Computed
    adminUsers,
    regularUsers,
    totalUsers,
    totalFiles,
    totalStorage,
    
    // Actions
    fetchUsers,
    fetchAllFiles,
    fetchStats,
    fetchUserFiles,
    updateUserFileLimit,
    updateUserType,
    deleteAnyFile,
    getDownloadUrl,
    downloadFile,
    formatFileSize,
    clearError
  }
})
