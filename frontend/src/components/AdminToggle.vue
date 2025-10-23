<template>
  <div class="flex items-center space-x-3">
    <span class="text-white/70 text-sm">Admin View</span>
    <button
      @click="toggleAdminView"
      :class="[
        'admin-toggle',
        isAdminView ? 'enabled' : 'disabled'
      ]"
    >
      <span
        :class="[
          'admin-toggle-thumb',
          isAdminView ? 'enabled' : 'disabled'
        ]"
      ></span>
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isAdminView = ref(false)

const toggleAdminView = () => {
  isAdminView.value = !isAdminView.value
  
  if (isAdminView.value) {
    router.push('/admin')
  } else {
    router.push('/')
  }
}

// Watch for route changes to update toggle state
watch(() => router.currentRoute.value.path, (newPath) => {
  isAdminView.value = newPath === '/admin'
}, { immediate: true })
</script>
