<template>
  <div class="relative min-h-screen bg-black overflow-hidden">
    <div class="absolute inset-0">
      <CanvasRevealEffect :animation-speed="3" :colors="[[255, 255, 255]]" :dot-size="6" />
    </div>

    <div class="relative z-10 min-h-screen flex items-center justify-center px-4">
      <div class="w-full max-w-sm space-y-6">
        <div class="text-center space-y-1">
          <h1 class="text-4xl font-bold text-white">Crear cuenta</h1>
          <p class="text-white/60">Empieza a descubrir lugares</p>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <BaseInput v-model="email" type="email" placeholder="info@gmail.com" />
          <BaseInput v-model="username" type="text" placeholder="Nombre de usuario" />
          <BaseInput v-model="password" type="password" placeholder="Contraseña" />
          <BaseButton variant="primary" type="submit" block> Registrarse </BaseButton>
          <p class="text-center text-sm text-white/60">
            ¿Ya tienes cuenta?
            <router-link to="/login" class="text-white hover:underline">
              Inicia sesión
            </router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register, getMe } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'
import CanvasRevealEffect from '@/components/ui/CanvasRevealEffect.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const email = ref('')
const password = ref('')
const username = ref('')
const router = useRouter()
const authStore = useAuthStore()
const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  loading.value = true
  try {
    const response = await register(email.value, username.value, password.value)
    const token = response.data.access_token
    const meResponse = await getMe()
    authStore.login(token, meResponse.data)
    router.push('/')
  } catch (e: any) {
    console.error('Error al registrarse:', e)
    error.value = e?.response?.data?.detail || 'No se pudo crear la cuenta. Inténtalo de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>
