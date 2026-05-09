import { onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

type EmojiHandler = (senderId: number, emoji: string) => void

let ws: WebSocket | null = null
let emojiHandlers: EmojiHandler[] = []

function connect() {
  const authStore = useAuthStore()
  if (!authStore.user || !authStore.token) return
  if (ws && ws.readyState === WebSocket.OPEN) return

  const wsUrl = import.meta.env.VITE_API_URL.replace(/^http/, 'ws').replace(/\/$/, '')
  const url = `${wsUrl}/ws/user/${authStore.user.id}?token=${authStore.token}`

  ws = new WebSocket(url)

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'emoji') {
      emojiHandlers.forEach(h => h(data.sender_id, data.emoji))
    }
  }

  ws.onclose = () => {
    ws = null
  }
}

function sendEmoji(receiverId: number, emoji: string) {
  if (!ws || ws.readyState !== WebSocket.OPEN) return
  ws.send(JSON.stringify({ type: 'emoji', receiver_id: receiverId, emoji }))
}

export function useUserSocket() {
  function onEmoji(handler: EmojiHandler) {
    emojiHandlers.push(handler)
    onUnmounted(() => {
      emojiHandlers = emojiHandlers.filter(h => h !== handler)
    })
  }

  return { connect, sendEmoji, onEmoji }
}
