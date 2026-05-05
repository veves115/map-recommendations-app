<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { updateMe } from '@/api/users'
import { formatApiError } from '@/utils/api-errors'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const authStore = useAuthStore()

const isEditing = ref(false)
const editForm = ref({ username: '', email: '' })
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)

function startEdit() {
  editForm.value = {
    username: authStore.user?.username ?? '',
    email: authStore.user?.email ?? '',
  }
  saveError.value = ''
  saveSuccess.value = false
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
  saveError.value = ''
}

async function saveEdit() {
  if (!authStore.user) return

  const payload: { username?: string; email?: string } = {}
  if (editForm.value.username !== authStore.user.username) {
    payload.username = editForm.value.username
  }
  if (editForm.value.email !== authStore.user.email) {
    payload.email = editForm.value.email
  }

  if (Object.keys(payload).length === 0) {
    isEditing.value = false
    return
  }

  saving.value = true
  saveError.value = ''
  try {
    const response = await updateMe(payload)
    authStore.updateUser(response.data)
    isEditing.value = false
    saveSuccess.value = true
    setTimeout(() => {
      saveSuccess.value = false
    }, 3000)
  } catch (e) {
    saveError.value = formatApiError(e, 'No se pudo actualizar')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <BaseCard variant="glass">
    <template #header>
      <div class="flex justify-between items-center">
        <h2 class="text-lg font-semibold">Cuenta</h2>
        <button
          v-if="!isEditing"
          type="button"
          class="text-sm text-white/60 hover:text-white transition-colors"
          @click="startEdit"
        >
          Editar
        </button>
      </div>
    </template>

    <!-- Modo view -->
    <div v-if="!isEditing" class="space-y-2 text-sm">
      <div>
        <span class="text-white/60">Nombre de usuario: </span>
        <span class="font-medium">{{ authStore.user?.username || '—' }}</span>
      </div>
      <div>
        <span class="text-white/60">Email: </span>
        <span class="font-medium">{{ authStore.user?.email || '—' }}</span>
      </div>
      <p v-if="saveSuccess" class="text-sm text-green-400 mt-2">✓ Guardado correctamente</p>
    </div>

    <!-- Modo edit -->
    <form v-else @submit.prevent="saveEdit" class="space-y-4">
      <BaseInput
        v-model="editForm.username"
        label="Nombre de usuario"
        id="edit-username"
      />
      <BaseInput
        v-model="editForm.email"
        type="email"
        label="Email"
        id="edit-email"
      />

      <p v-if="saveError" class="text-sm text-red-400">{{ saveError }}</p>

      <div class="flex gap-2 justify-end">
        <BaseButton type="button" variant="ghost" :disabled="saving" @click="cancelEdit">
          Cancelar
        </BaseButton>
        <BaseButton type="submit" variant="primary" :loading="saving">
          Guardar
        </BaseButton>
      </div>
    </form>
  </BaseCard>
</template>
