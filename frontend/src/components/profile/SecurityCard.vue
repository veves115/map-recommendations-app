<script setup lang="ts">
import { ref } from 'vue'
import { changePassword } from '@/api/auth'
import { formatApiError } from '@/utils/api-errors'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const isChangingPassword = ref(false)
const passwordForm = ref({
  current: '',
  new: '',
  confirm: '',
})
const changingPassword = ref(false)
const passwordError = ref('')
const passwordSuccess = ref(false)

function startPasswordChange() {
  passwordForm.value = { current: '', new: '', confirm: '' }
  passwordError.value = ''
  passwordSuccess.value = false
  isChangingPassword.value = true
}

function cancelPasswordChange() {
  isChangingPassword.value = false
  passwordError.value = ''
}

async function savePasswordChange() {
  passwordError.value = ''

  if (passwordForm.value.new !== passwordForm.value.confirm) {
    passwordError.value = 'La nueva contraseña y su confirmación no coinciden'
    return
  }

  if (passwordForm.value.new.length < 8) {
    passwordError.value = 'La nueva contraseña debe tener al menos 8 caracteres'
    return
  }

  changingPassword.value = true
  try {
    await changePassword(passwordForm.value.current, passwordForm.value.new)
    isChangingPassword.value = false
    passwordSuccess.value = true
    setTimeout(() => {
      passwordSuccess.value = false
    }, 3000)
  } catch (e) {
    passwordError.value = formatApiError(e, 'No se pudo cambiar la contraseña')
  } finally {
    changingPassword.value = false
  }
}
</script>

<template>
  <BaseCard variant="glass">
    <template #header>
      <div class="flex justify-between items-center">
        <h2 class="text-lg font-semibold">Seguridad</h2>
        <button
          v-if="!isChangingPassword"
          type="button"
          class="text-sm text-white/60 hover:text-white transition-colors"
          @click="startPasswordChange"
        >
          Cambiar contraseña
        </button>
      </div>
    </template>

    <!-- Modo view -->
    <div v-if="!isChangingPassword" class="text-sm text-white/60">
      <p>Tu contraseña está protegida. Cámbiala periódicamente.</p>
      <p v-if="passwordSuccess" class="text-green-400 mt-2">✓ Contraseña actualizada</p>
    </div>

    <!-- Modo edit -->
    <form v-else @submit.prevent="savePasswordChange" class="space-y-4">
      <BaseInput
        v-model="passwordForm.current"
        type="password"
        label="Contraseña actual"
        id="current-password"
        toggle-password
      />
      <BaseInput
        v-model="passwordForm.new"
        type="password"
        label="Nueva contraseña"
        id="new-password"
        toggle-password
      />
      <BaseInput
        v-model="passwordForm.confirm"
        type="password"
        label="Confirmar nueva contraseña"
        id="confirm-password"
        toggle-password
      />

      <p v-if="passwordError" class="text-sm text-red-400">{{ passwordError }}</p>

      <div class="flex gap-2 justify-end">
        <BaseButton
          type="button"
          variant="ghost"
          :disabled="changingPassword"
          @click="cancelPasswordChange"
        >
          Cancelar
        </BaseButton>
        <BaseButton type="submit" variant="primary" :loading="changingPassword">
          Guardar
        </BaseButton>
      </div>
    </form>
  </BaseCard>
</template>
