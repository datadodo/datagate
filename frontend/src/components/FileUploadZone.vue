<template>
  <div class="glass-card rounded-xl p-6">
    <div
      ref="dropZone"
      @drop="handleDrop"
      @dragover="handleDragOver"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      @click="triggerFileInput"
      :class="[
        'file-upload-zone cursor-pointer',
        { 'dragover': isDragOver }
      ]"
    >
      <input
        ref="fileInput"
        type="file"
        multiple
        @change="handleFileSelect"
        class="hidden"
      />

      <!-- Upload Icon and Text -->
      <div class="text-center">
        <svg class="mx-auto h-12 w-12 text-primary-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        
        <h3 class="text-lg font-medium text-white mb-2">
          {{ isDragOver ? 'Drop files here' : 'Upload files' }}
        </h3>
        <p class="text-white/70 mb-4">
          Drag and drop files here, or click to select files
        </p>
        
        <!-- File Limit Info -->
        <div class="text-sm text-white/60">
          {{ remainingSlots }} of {{ userFileLimit }} files remaining
        </div>
      </div>
    </div>

    <!-- Upload Progress -->
    <div v-if="Object.keys(uploadProgress).length > 0" class="mt-6 space-y-3">
      <h4 class="text-white font-medium">Uploading files...</h4>
      <div v-for="(progress, fileName) in uploadProgress" :key="fileName" class="space-y-2">
        <div class="flex items-center justify-between text-sm">
          <span class="text-white/70 truncate">{{ fileName }}</span>
          <span class="text-primary-400">{{ progress }}%</span>
        </div>
        <div class="w-full bg-white/10 rounded-full h-2">
          <div
            class="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-300"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mt-4 bg-red-500/20 border border-red-500/30 rounded-lg p-4">
      <p class="text-red-200 text-sm">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useFilesStore } from '@/stores/filesStore'

const filesStore = useFilesStore()

// Refs
const dropZone = ref(null)
const fileInput = ref(null)
const isDragOver = ref(false)

// Computed properties
const uploadProgress = computed(() => filesStore.uploadProgress)
const error = computed(() => filesStore.error)
const userFileLimit = computed(() => filesStore.userFileLimit)
const remainingSlots = computed(() => filesStore.remainingSlots)

// Methods
const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  if (files.length > 0) {
    uploadFiles(files)
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragOver.value = false
  
  const files = Array.from(event.dataTransfer.files)
  if (files.length > 0) {
    uploadFiles(files)
  }
}

const handleDragOver = (event) => {
  event.preventDefault()
}

const handleDragEnter = (event) => {
  event.preventDefault()
  isDragOver.value = true
}

const handleDragLeave = (event) => {
  event.preventDefault()
  // Only set isDragOver to false if we're leaving the drop zone entirely
  if (!dropZone.value?.contains(event.relatedTarget)) {
    isDragOver.value = false
  }
}

const uploadFiles = async (files) => {
  try {
    // Check if adding these files would exceed the limit
    if (files.length > remainingSlots.value) {
      throw new Error(`Cannot upload ${files.length} files. Only ${remainingSlots.value} slots remaining.`)
    }

    // Clear any previous errors
    filesStore.clearError()

    if (files.length === 1) {
      await filesStore.uploadFile(files[0])
    } else {
      await filesStore.uploadBatchFiles(files)
    }
  } catch (error) {
    console.error('Upload error:', error)
  }
}

// Prevent default drag behaviors on the document
const preventDefaults = (e) => {
  e.preventDefault()
  e.stopPropagation()
}

// Lifecycle
onMounted(() => {
  document.addEventListener('dragenter', preventDefaults)
  document.addEventListener('dragover', preventDefaults)
  document.addEventListener('dragleave', preventDefaults)
  document.addEventListener('drop', preventDefaults)
})

onUnmounted(() => {
  document.removeEventListener('dragenter', preventDefaults)
  document.removeEventListener('dragover', preventDefaults)
  document.removeEventListener('dragleave', preventDefaults)
  document.removeEventListener('drop', preventDefaults)
})
</script>
