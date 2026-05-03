<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { acceptInviteByToken } from '@/api/friendships'
import type { Friendship } from '@/types/api'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const friendship = ref<Friendship | null>(null)

onMounted(async () => {
  const token = route.params.token as string
  if (!token) {
    error.value = 'Link de invitación inválido'
    loading.value = false
    return
  }

  try {
    const response = await acceptInviteByToken(token)
    friendship.value = response.data
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? 'No se pudo procesar la invitación'
  } finally {
    loading.value = false
  }
})

function goToFriends() {
  router.push('/friends')
}

function goHome() {
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen bg-black text-white flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <BaseCard variant="glass">
        <p v-if="loading" class="text-sm text-white/60 text-center py-6">
          Procesando invitación...
        </p>

        <div v-else-if="error" class="text-center py-2 space-y-4">
          <p class="text-2xl">😕</p>
          <h1 class="text-xl font-semibold">Invitación no aceptada</h1>
          <p class="text-sm text-red-400">{{ error }}</p>
          <BaseButton variant="primary" @click="goHome">Ir al mapa</BaseButton>
        </div>

        <div v-else-if="friendship" class="text-center py-2 space-y-4">
          <p class="text-2xl">🎉</p>
          <h1 class="text-xl font-semibold">¡Ahora sois amigos!</h1>
          <p class="text-sm text-white/70">
            Has aceptado la invitación de
            <span class="font-semibold">{{ friendship.requester.username }}</span>
          </p>
          <div class="flex gap-2 justify-center">
            <BaseButton variant="ghost" @click="goHome">Ir al mapa</BaseButton>
            <BaseButton variant="primary" @click="goToFriends">Ver mis amigos</BaseButton>
          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>
