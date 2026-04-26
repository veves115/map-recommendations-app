<script setup lang="ts">
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

const userInitial = () => {
  const name = authStore.user?.username || authStore.user?.email || '?'
  return name.charAt(0).toUpperCase()
}
</script>

<template>
  <Menu as="div" class="absolute top-4 right-4 z-20">
    <MenuButton
      class="w-11 h-11 rounded-full bg-white/10 backdrop-blur-md border border-white/20
             text-white font-semibold flex items-center justify-center
             hover:bg-white/15 transition-colors shadow-card"
    >
      {{ userInitial() }}
    </MenuButton>

    <transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <MenuItems
        class="absolute right-0 mt-2 w-48 origin-top-right
               bg-surface-raised backdrop-blur-md border border-white/10
               rounded-card shadow-card overflow-hidden focus:outline-none"
      >
        <MenuItem v-slot="{ active }">
          <RouterLink
            to="/profile"
            :class="[
              'block px-4 py-3 text-sm text-white',
              active ? 'bg-white/10' : '',
            ]"
          >
            Mi perfil
          </RouterLink>
        </MenuItem>
        <MenuItem v-slot="{ active }">
          <RouterLink
            to="/chat"
            :class="[
              'block px-4 py-3 text-sm text-white',
              active ? 'bg-white/10' : '',
            ]"
          >
            Chat
          </RouterLink>
        </MenuItem>
        <MenuItem v-slot="{ active }">
          <button
            type="button"
            :class="[
              'block w-full text-left px-4 py-3 text-sm text-red-400',
              active ? 'bg-white/10' : '',
            ]"
            @click="handleLogout"
          >
            Cerrar sesión
          </button>
        </MenuItem>
      </MenuItems>
    </transition>
  </Menu>
</template>
