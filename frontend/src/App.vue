<script setup lang="ts">
import { watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUserSocket } from '@/composables/useUserSocket'

const authStore = useAuthStore()
const { connect } = useUserSocket()

watch(
  () => authStore.user,
  (user) => {
    if (user) connect()
  },
  { immediate: true },
)

</script>

<template>
  <RouterView />
</template>

<style scoped></style>
