<template>
  <div class="relative min-h-screen bg-black overflow-hidden">
    <div class="absolute inset-0">
      <CanvasRevealEffect :animation-speed="3" :colors="[[255, 255, 255]]" :dot-size="6" />
    </div>

    <div class="relative z-10 min-h-screen flex items-center justify-center px-4">
      <div class="w-full max-w-sm space-y-6">
        <div class="text-center space-y-1">
          <h1 class="text-4xl font-bold text-white">Recuperar contraseña</h1>
          <p class="text-white/60">Te enviaremos un enlace a tu email</p>
        </div>

        <form v-if="!sent" @submit.prevent="handleSubmit" class="space-y-4">
          <BaseInput v-model="email" type="email" placeholder="Tu correo electrónico" />

          <p v-if="error" class="text-center text-sm text-red-400">{{ error }}</p>

          <BaseButton variant="primary" type="submit" block :loading="loading">
            Enviar enlace
          </BaseButton>

          <p class="text-center text-sm text-white/60">
            <router-link to="/login" class="text-white hover:underline">
              Volver al inicio de sesión
            </router-link>
          </p>
        </form>

        <div v-else class="text-center space-y-4">
          <p class="text-white/80">
            Si existe una cuenta con ese email, recibirás un enlace para restablecer tu contraseña.
          </p>
          <router-link to="/login" class="text-white hover:underline text-sm">
            Volver al inicio de sesión
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import apiClient from '@/api/client'
import CanvasRevealEffect from '@/components/ui/CanvasRevealEffect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const email = ref('')
const error = ref('')
const loading = ref(false)
const sent = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    await apiClient.post('api/v1/auth/forgot-password', { email: email.value })
    sent.value = true
  } catch {
    error.value = 'No se pudo enviar el email. Inténtalo de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>
