import { ref, watch, onUnmounted, type Ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getConversation } from '@/api/messages'
import type { Message } from '@/types/api'

export function useChat(otherUserId: Ref<number | null>) {
  const messages = ref<Message[]>([])
  const connected = ref(false)
  const error = ref('')

  let ws: WebSocket | null = null
  const authStore = useAuthStore()

  function buildRoomId(myId: number, otherId: number): string {
    const [lo, hi] = [myId, otherId].sort((a, b) => a - b)
    return `${lo}_${hi}`
  }

  function disconnect() {
    if (ws) {
      ws.close()
      ws = null
    }
    connected.value = false
  }

  function connect(otherId: number) {
    if (!authStore.user || !authStore.token) return

    const roomId = buildRoomId(authStore.user.id, otherId)
    const wsUrl = import.meta.env.VITE_API_URL.replace(/^http/, 'ws').replace(/\/$/, '')
    const url = `${wsUrl}/ws/chat/${roomId}?token=${authStore.token}`

    ws = new WebSocket(url)

    ws.onopen = () => {
      connected.value = true
      error.value = ''
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.error) {
        error.value = data.error
        return
      }
      messages.value.push(data as Message)
    }

    ws.onerror = () => {
      error.value = 'Error de conexión'
    }

    ws.onclose = () => {
      connected.value = false
    }
  }

  function send(content: string) {
    if (!otherUserId.value || !ws || ws.readyState !== WebSocket.OPEN) return
    ws.send(
      JSON.stringify({
        receiver_id: otherUserId.value,
        content,
      }),
    )
  }

  // Reaccionar a cambios del otro usuario
  watch(
    otherUserId,
    async (newId, oldId) => {
      if (oldId !== null && oldId !== undefined) {
        disconnect()
        messages.value = []
      }
      if (newId !== null && newId !== undefined) {
        try {
          const response = await getConversation(newId)
          messages.value = response.data
        } catch (err) {
          console.error('Error cargando historial:', err)
        }
        connect(newId)
      }
    },
    { immediate: true },
  )

  onUnmounted(() => {
    disconnect()
  })

  return {
    messages,
    connected,
    error,
    send,
  }
}
