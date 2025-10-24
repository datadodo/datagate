import axios from 'axios'
import { auth } from '@/firebase'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://datagate--globaldashboard-4598e.us-central1.hosted.app',
  timeout: 30000
})

// Request interceptor to add Firebase ID token
api.interceptors.request.use(
  async (config) => {
    try {
      const user = auth.currentUser
      if (user) {
        const token = await user.getIdToken()
        config.headers.Authorization = `Bearer ${token}`
      }
    } catch (error) {
      console.error('Error getting Firebase token:', error)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      console.error('Authentication error:', error.response.data)
      // You might want to redirect to login or refresh token here
    }
    return Promise.reject(error)
  }
)

export default api
