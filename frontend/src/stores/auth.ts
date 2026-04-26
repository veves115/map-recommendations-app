import type { User } from '@/types/api'
import { defineStore } from 'pinia'
import { getMe } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
  }),
  getters: {
    isAuthenticated: (state) => state.token !== null,
  },
  actions: {
    login(token: string, user: User) {
      this.token = token
      this.user = user
      localStorage.setItem('token', token)
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },
    async loadFromStorage() {
      const token = localStorage.getItem('token')
      if (!token) return

      this.token = token

      try {
        const response = await getMe()
        this.user = response.data
      } catch (err) {
        // Token expirado o inválido → cerrar sesión
        this.logout()
      }
    },
  },
})
