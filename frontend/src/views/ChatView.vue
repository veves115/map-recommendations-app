<template>
  <div class="h-screen bg-black text-white flex flex-col overflow-hidden">
    <UserMenu />

    <!-- Header -->
    <div class="max-w-2xl w-full mx-auto px-4 pt-12 pb-4">
      <RouterLink to="/" class="text-sm text-white/60 hover:text-white">
        ← Volver al mapa
      </RouterLink>
      <h1 class="text-3xl font-bold mt-2">
        {{ selectedUser ? selectedUser.username : 'Chat' }}
      </h1>
    </div>

    <!-- Content -->
    <div class="max-w-2xl w-full mx-auto px-4 pb-8 flex-1 flex flex-col min-h-0">
      <!-- User list -->
      <BaseCard v-if="!selectedUser" variant="glass">
        <template #header>
          <h2 class="text-lg font-semibold">Usuarios</h2>
        </template>

        <p v-if="loadingUsers" class="text-sm text-white/60">Cargando...</p>

        <p
          v-else-if="otherUsers.length === 0"
          class="text-sm text-white/60"
        >
          No hay otros usuarios todavía.
        </p>

        <ul v-else class="divide-y divide-white/10">
          <li v-for="user in otherUsers" :key="user.id">
            <button
              type="button"
              class="w-full text-left py-3 px-2 -mx-2 rounded-lg
                     hover:bg-white/5 transition-colors
                     flex items-center gap-3"
              @click="selectedUser = user"
            >
              <div class="w-9 h-9 rounded-full bg-white/10 border border-white/15
                          flex items-center justify-center font-semibold">
                {{ user.username.charAt(0).toUpperCase() }}
              </div>
              <div>
                <p class="font-medium">{{ user.username }}</p>
                <p class="text-xs text-white/50">{{ user.email }}</p>
              </div>
            </button>
          </li>
        </ul>
      </BaseCard>

      <!-- Chat conversation -->
      <div v-else class="flex-1 flex flex-col gap-3 min-h-0">
        <button
          type="button"
          class="text-sm text-white/60 hover:text-white text-left"
          @click="selectedUser = null"
        >
          ← Atrás
        </button>

        <BaseCard variant="glass" padding="none" class="flex-1 flex flex-col min-h-0">
          <!-- Messages -->
          <div
            ref="messagesEl"
            class="flex-1 overflow-y-auto p-5 space-y-2 min-h-0"
          >
            <p
              v-if="messages.length === 0"
              class="text-sm text-white/50 text-center mt-8"
            >
              Aún no hay mensajes. Escribe el primero.
            </p>
            <div
              v-for="msg in messages"
              :key="msg.id"
              :class="['flex', isOwn(msg) ? 'justify-end' : 'justify-start']"
            >
              <div
                :class="[
                  'max-w-[75%] px-4 py-2 rounded-2xl text-sm',
                  isOwn(msg)
                    ? 'bg-white text-black'
                    : 'bg-white/10 text-white border border-white/15',
                ]"
              >
                {{ msg.content }}
              </div>
            </div>
          </div>

          <!-- Input -->
          <form
            @submit.prevent="handleSend"
            class="p-3 border-t border-white/10 flex gap-2"
          >
            <input
              v-model="draft"
              type="text"
              placeholder="Escribe un mensaje..."
              class="flex-1 bg-white/5 border border-white/10 rounded-full
                     px-4 py-2 text-white placeholder:text-white/40
                     focus:outline-none focus:border-white/30"
            />
            <BaseButton
              type="submit"
              variant="primary"
              :disabled="!draft.trim() || !connected"
            >
              Enviar
            </BaseButton>
          </form>

          <p v-if="error" class="text-xs text-red-400 px-3 pb-3">{{ error }}</p>
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { listUsers } from '@/api/users'
import { useChat } from '@/composables/useChat'
import type { User, Message } from '@/types/api'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import UserMenu from '@/components/layout/UserMenu.vue'

const authStore = useAuthStore()
const users = ref<User[]>([])
const loadingUsers = ref(true)
const selectedUser = ref<User | null>(null)
const draft = ref('')
const messagesEl = ref<HTMLDivElement | null>(null)

const otherUsers = computed(() =>
  users.value.filter(u => u.id !== authStore.user?.id),
)

const otherUserId = computed(() => selectedUser.value?.id ?? null)
const { messages, connected, error, send } = useChat(otherUserId)

function isOwn(msg: Message): boolean {
  return msg.sender_id === authStore.user?.id
}

function handleSend() {
  const content = draft.value.trim()
  if (!content) return
  send(content)
  draft.value = ''
}

// Auto-scroll al fondo cuando llegan mensajes
watch(messages, async () => {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}, { deep: true })

onMounted(async () => {
  try {
    const response = await listUsers()
    users.value = response.data
  } catch (err) {
    console.error('Error cargando usuarios:', err)
  } finally {
    loadingUsers.value = false
  }
})
</script>
