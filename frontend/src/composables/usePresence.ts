import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useGeolocation } from '@vueuse/core'
import { useAuthStore } from '@/stores/auth'

export interface FriendLocation {
  user_id: number
  username: string
  lat: number
  lng: number
  updated_at: string
}

type Status = 'connecting' | 'connected' | 'disconnected' | 'error'

const SEND_INTERVAL_MS = 30_000
const RECONNECT_DELAY_MS = 5_000

export function usePresence() {
  const authStore = useAuthStore()

  const friends = ref<Map<number, FriendLocation>>(new Map())
  const status = ref<Status>('disconnected')
  const isConnected = computed(() => status.value === 'connected')

  const { coords, error: geoError } = useGeolocation()

  let ws: WebSocket | null = null
  let sendInterval: ReturnType<typeof setInterval> | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let unmounted = false

  function buildUrl(): string | null {
    const token = authStore.token
    if (!token) return null
    const apiUrl = import.meta.env.VITE_API_URL ?? ''
    // Convertir http(s):// → ws(s)://
    const wsUrl = apiUrl.replace(/^http/, 'ws').replace(/\/$/, '')
    return `${wsUrl}/ws/presence?token=${encodeURIComponent(token)}`
  }

  function handleMessage(raw: string) {
    let data: any
    try {
      data = JSON.parse(raw)
    } catch {
      return
    }

    if (data.type === 'snapshot') {
      const map = new Map<number, FriendLocation>()
      for (const f of data.friends ?? []) {
        map.set(f.user_id, f)
      }
      friends.value = map
    } else if (data.type === 'update') {
      friends.value.set(data.user_id, {
        user_id: data.user_id,
        username: data.username,
        lat: data.lat,
        lng: data.lng,
        updated_at: data.updated_at,
      })
      // Forzar reactividad (Vue 3 ya la detecta en Map, pero por si acaso)
      friends.value = new Map(friends.value)
    } else if (data.type === 'offline') {
      friends.value.delete(data.user_id)
      friends.value = new Map(friends.value)
    }
  }

  function startSending() {
    if (sendInterval) return
    sendInterval = setInterval(() => {
      if (!ws || ws.readyState !== WebSocket.OPEN) return
      if (!authStore.user?.share_location) return
      if (geoError.value) return
      const lat = coords.value.latitude
      const lng = coords.value.longitude
      if (lat === 0 && lng === 0) return
      ws.send(JSON.stringify({ type: 'location', lat, lng }))
    }, SEND_INTERVAL_MS)
  }

  function stopSending() {
    if (sendInterval) {
      clearInterval(sendInterval)
      sendInterval = null
    }
  }

  function connect() {
    const url = buildUrl()
    if (!url) {
      status.value = 'error'
      return
    }

    status.value = 'connecting'
    ws = new WebSocket(url)

    ws.onopen = () => {
      status.value = 'connected'
      startSending()
    }

    ws.onmessage = (event) => {
      handleMessage(event.data)
    }

    ws.onerror = () => {
      status.value = 'error'
    }

    ws.onclose = () => {
      stopSending()
      status.value = 'disconnected'
      friends.value = new Map()
      if (!unmounted) {
        reconnectTimer = setTimeout(connect, RECONNECT_DELAY_MS)
      }
    }
  }

  function disconnect() {
    unmounted = true
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    stopSending()
    if (ws) {
      ws.close()
      ws = null
    }
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    friends,
    status,
    isConnected,
  }
}
