<script setup lang="ts">
import { ref } from 'vue'
import { Switch } from '@headlessui/vue'
import { useAuthStore } from '@/stores/auth'
import { updateMe } from '@/api/users'
import { formatApiError } from '@/utils/api-errors'
import BaseCard from '@/components/ui/BaseCard.vue'

const authStore = useAuthStore()

const togglingShareLocation = ref(false)
const shareLocationError = ref('')

async function handleToggleShareLocation(value: boolean) {
  togglingShareLocation.value = true
  shareLocationError.value = ''
  try {
    const response = await updateMe({ share_location: value })
    authStore.updateUser(response.data)
    // Recargar para que el WS se reconecte con el nuevo valor
    window.location.reload()
  } catch (e) {
    shareLocationError.value = formatApiError(e, 'No se pudo cambiar el ajuste')
  } finally {
    togglingShareLocation.value = false
  }
}
</script>

<template>
  <BaseCard variant="glass">
    <template #header>
      <h2 class="text-lg font-semibold">Privacidad</h2>
    </template>

    <div class="flex justify-between items-start gap-4">
      <div class="flex-1">
        <p class="text-sm font-medium">Compartir mi ubicación con amigos</p>
        <p class="text-xs text-white/60 mt-1">
          Tus amigos verán tu ubicación en tiempo real cuando estés en la app.
        </p>
      </div>
      <Switch
        :model-value="authStore.user?.share_location ?? false"
        :disabled="togglingShareLocation"
        :class="[
          'relative inline-flex h-6 w-11 items-center rounded-full transition-colors flex-shrink-0 border',
          authStore.user?.share_location
            ? 'bg-emerald-500/90 border-emerald-400/60'
            : 'bg-white/10 border-white/20',
          'disabled:opacity-50 disabled:cursor-not-allowed',
        ]"
        @update:model-value="handleToggleShareLocation"
      >
        <span
          :class="[
            'inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform',
            authStore.user?.share_location ? 'translate-x-6' : 'translate-x-1',
          ]"
        />
      </Switch>
    </div>

    <p v-if="shareLocationError" class="text-sm text-red-400 mt-3">
      {{ shareLocationError }}
    </p>
  </BaseCard>
</template>
