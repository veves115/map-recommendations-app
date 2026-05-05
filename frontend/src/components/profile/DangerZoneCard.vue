<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { deleteMe } from '@/api/users'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'

const router = useRouter()
const authStore = useAuthStore()

const deleteOpen = ref(false)
const deletingAccount = ref(false)

async function handleDeleteAccount() {
  deletingAccount.value = true
  try {
    await deleteMe()
    authStore.logout()
    router.push('/login')
  } catch (err) {
    console.error('Error eliminando cuenta:', err)
    deletingAccount.value = false
  }
}
</script>

<template>
  <BaseCard variant="danger">
    <template #header>
      <h2 class="text-lg font-semibold text-red-400">Zona de peligro</h2>
    </template>

    <p class="text-sm text-white/60 mb-4">
      Eliminar tu cuenta desactivará el acceso inmediatamente y deberás contactar con soporte
      para recuperarla.
    </p>

    <BaseButton variant="danger" @click="deleteOpen = true">
      Eliminar mi cuenta
    </BaseButton>
  </BaseCard>

  <ConfirmDialog
    v-model:open="deleteOpen"
    title="¿Eliminar cuenta?"
    message="Tu cuenta se desactivará. Perderás acceso inmediatamente y necesitarás contactar a soporte para reactivarla."
    confirm-text="Eliminar cuenta"
    variant="danger"
    :loading="deletingAccount"
    @confirm="handleDeleteAccount"
  />
</template>
