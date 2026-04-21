<template>
  <div class="flex flex-col h-screen">
    <nav class="bg-blue-600 text-white px-6 py-3 flex justify-between items-center">
      <router-link to="/" class="font-bold text-lg">MapApp</router-link>
      <router-link to="/profile" class="hover:underline">Perfil</router-link>
    </nav>

    <div v-if="!connected" class="flex flex-col items-center justify-center flex-1 gap-4">
      <h1 class="text-2xl font-bold">Chat</h1>
      <input
        v-model="receiverIdInput"
        type="number"
        placeholder="ID del usuario con quien chatear"
        class="border border-gray-300 rounded px-3 py-2 w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        @click="handleConnect"
        class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
      >
        Conectar
      </button>
    </div>

    <div v-else class="flex flex-col flex-1 overflow-hidden">
      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-2 bg-gray-50">
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="flex"
          :class="msg.sender_id === currentUserId ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-xs px-4 py-2 rounded-lg text-sm"
            :class="msg.sender_id === currentUserId
              ? 'bg-blue-600 text-white'
              : 'bg-white border border-gray-200'"
          >
            {{ msg.content }}
          </div>
        </div>
      </div>

      <form @submit.prevent="handleSend" class="flex gap-2 p-4 border-t bg-white">
        <input
          v-model="newMessage"
          placeholder="Escribe un mensaje..."
          class="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Enviar
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getConversation } from '@/api/messages'
import type { Message } from '@/types/api'

const authStore = useAuthStore()
const currentUserId = authStore.user?.id

const receiverIdInput = ref('')
const connected = ref(false)
const messages = ref<Message[]>([])
const newMessage = ref('')
const messagesContainer = ref<HTMLElement | null>(null)
let socket: WebSocket | null = null

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const handleConnect = async () => {
  const receiverId = parseInt(receiverIdInput.value)
  if (!receiverId || !currentUserId) return

  const historyResponse = await getConversation(receiverId)
  messages.value = historyResponse.data

  const lo = Math.min(currentUserId, receiverId)
  const hi = Math.max(currentUserId, receiverId)
  const roomId = `${lo}_${hi}`
  const token = localStorage.getItem('token')

  socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}?token=${token}`)

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.error) return
    messages.value.push(data)
    scrollToBottom()
  }

  connected.value = true
  scrollToBottom()
}

const handleSend = () => {
  if (!newMessage.value.trim() || !socket) return
  const receiverId = parseInt(receiverIdInput.value)
  socket.send(JSON.stringify({ receiver_id: receiverId, content: newMessage.value }))
  newMessage.value = ''
}

onUnmounted(() => {
  socket?.close()
})
</script>