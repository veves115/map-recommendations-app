<template>
  <div class="relative min-h-screen bg-black overflow-hidden">
    <div class="absolute inset-0">
      <CanvasRevealEffect :animation-speed="3" :colors="[[255, 255, 255]]" :dot-size="6" />
    </div>

    <div class="relative z-10 min-h-screen flex items-center justify-center px-4">
      <div class="w-full max-w-sm space-y-6">
        <div class="text-center space-y-1">
          <h1 class="text-4xl font-bold text-white">Nueva contraseña</h1>
          <p class="text-white/60">Elige una contraseña segura</p>
        </div>

        <form v-if="!done" @submit.prevent="handleSubmit" class="space-y-4">
          <BaseInput v-model="password" type="password" placeholder="Nueva contraseña (mín. 8 caracteres)" :togglePassword="true" />
          <BaseInput v-model="confirm" type="password" placeholder="Confirmar contraseña" :togglePassword="true" />

          <p v-if="error" class="text-center text-sm text-red-400">{{ error }}</p>

          <BaseButton variant="primary" type="submit" block :loading="loading">
            Restablecer contraseña
          </BaseButton>
        </form>

        <div v-else class="text-center space-y-4">
          <p class="text-white/80">¡Contraseña actualizada correctamente!</p>
          <router-link to="/login" class="text-white hover:underline text-sm">
            Iniciar sesión
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/api/client'
import CanvasRevealEffect from '@/components/ui/CanvasRevealEffect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const route = useRoute()
const token = route.query.token as string

const password = ref('')
const confirm = ref('')
const error = ref('')
const loading = ref(false)
const done = ref(false)

async function handleSubmit() {
  error.value = ''
  if (password.value !== confirm.value) {
    error.value = 'Las contraseñas no coinciden'
    return
  }
  loading.value = true
  try {
    await apiClient.post('api/v1/auth/reset-password', {
      token,
      new_password: password.value,
    })
    done.value = true
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Token inválido o expirado'
  } finally {
    loading.value = false
  }
}
</script>
