<template>
  <div class="relative min-h-screen bg-black overflow-hidden">
    <!-- Fondo de puntos -->
    <div class="absolute inset-0">
      <CanvasRevealEffect :animation-speed="3" :colors="[[255, 255, 255]]" :dot-size="6" />
    </div>

    <!-- Formulario actual, encima del fondo -->
    <div class="relative z-10 min-h-screen flex items-center justify-center px-4">
      <div class="w-full max-w-sm space-y-6">
        <!-- Título -->
        <div class="text-center space-y-1">
          <h1 class="text-4xl font-bold text-white">Iniciar sesión</h1>
          <p class="text-white/60">Bienvenido de vuelta</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <BaseInput v-model="email" type="email" placeholder="info@gmail.com" />
          <BaseInput v-model="password" type="password" placeholder="Contraseña" />

          <p v-if="error" class="text-center text-sm text-red-400">
            {{ error }}
          </p>

          <BaseButton variant="primary" type="submit" block :loading="loading">
            Iniciar sesión
          </BaseButton>
          <p class="text-center text-sm text-white/60">
            ¿No tienes cuenta?
            <router-link to="/register" class="text-white hover:underline">
              Regístrate
            </router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'
import { getMe } from '@/api/auth'
import CanvasRevealEffect from '@/components/ui/CanvasRevealEffect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const email = ref('')
const password = ref('')
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    const response = await login(email.value, password.value)
    const token = response.data.access_token
    localStorage.setItem('token', token) // ← AÑADIR esta línea
    const meResponse = await getMe()
    authStore.login(token, meResponse.data)

    const redirect =
      typeof route.query.redirect === 'string' && route.query.redirect.startsWith('/')
        ? route.query.redirect
        : '/'
    router.push(redirect)
  } catch (e: any) {
    console.error('Error al iniciar sesión:', e)
    error.value = e?.response?.data?.detail || 'Credenciales incorrectas. Inténtalo de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>
