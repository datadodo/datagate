<template>
  <div id="app" class="min-h-screen">
    <RouterView />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()

onMounted(() => {
  // Initialize auth state
  authStore.initializeAuth()
})
</script>
