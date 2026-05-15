<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { setOptions, importLibrary } from '@googlemaps/js-api-loader'
import { useGeolocation } from '@vueuse/core'
import { getRecommendations } from '@/api/recommendations'
import type { NearbyPlace } from '@/types/api'
import { getNearbyPlaces } from '@/api/maps'
import { usePresence } from '@/composables/usePresence'
import { useWeather } from '@/composables/useWeather'
import WeatherIcon from '@/components/ui/WeatherIcon.vue'
import { MapPin, RefreshCw } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import MapTypeSelector from '@/components/map/MapTypeSelector.vue'

const authStore = useAuthStore()
const { weather, fetchWeather } = useWeather()
const refreshing = ref(false)

async function refreshWeather() {
  if (refreshing.value) return
  refreshing.value = true
  const lat = coords.value.latitude
  const lng = coords.value.longitude
  if (lat && lng) await fetchWeather(lat, lng)
  refreshing.value = false
}

interface Props {
  center?: { lat: number; lng: number }
  zoom?: number
  placeType?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  center: () => ({ lat: 40.4168, lng: -3.7038 }),
  zoom: 14,
  placeType: null,
})

import type { FriendLocation } from '@/composables/usePresence'

const emit = defineEmits<{
  'place-click': [place: NearbyPlace]
  'friend-click': [friend: FriendLocation]
}>()

const mapRef = ref<HTMLDivElement | null>(null)
let map: any = null
let PinElementClass: any = null
let userMarker: any = null
let markers: any[] = []
let AdvancedMarker: any = null
const { friends } = usePresence()
const friendMarkers: Map<number, any> = new Map()

type MapType = 'auto' | 'roadmap' | 'hybrid'
const mapType = ref<MapType>('auto')

function applyMapType(type: MapType, currentZoom?: number) {
  if (!map) return
  if (type === 'roadmap') {
    map.setMapTypeId('roadmap')
  } else if (type === 'hybrid') {
    map.setMapTypeId('hybrid')
  } else {
    const zoom = currentZoom ?? map.getZoom() ?? 14
    map.setMapTypeId(zoom < 14 ? 'hybrid' : 'roadmap')
  }
}

const { coords, error: geoError } = useGeolocation()

let hasInitialCenter = false

watch(
  () => ({ lat: coords.value.latitude, lng: coords.value.longitude }),
  (pos) => {
    if (!map) return
    if (geoError.value) return
    if (pos.lat === 0 && pos.lng === 0) return

    if (!hasInitialCenter) {
      map.setCenter(pos)
      hasInitialCenter = true
      loadPlaces(pos.lat, pos.lng)
      fetchWeather(pos.lat, pos.lng)
    }

    if (!userMarker && AdvancedMarker) {
      const el = document.createElement('div')
el.style.cssText = 'display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:#3b82f6;border:2px solid white;color:white;font-size:14px;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,0.3)'
el.textContent = (authStore.user?.username ?? authStore.user?.email ?? '?').charAt(0).toUpperCase()
      userMarker = new AdvancedMarker({
        position: pos,
        map,
        content: el,
        title: 'Tu ubicación',
      })
    } else if (userMarker) {
      userMarker.position = pos
    }
  },
)

watch(
  () => props.placeType,
  () => {
    if (!map) return
    const center = map.getCenter()
    if (!center) return
    loadPlaces(center.lat(), center.lng())
  },
)
function hasMovedSignificantly(
  a: { lat: number; lng: number },
  b: { lat: number; lng: number },
): boolean {
  return Math.abs(a.lat - b.lat) > 0.0001 || Math.abs(a.lng - b.lng) > 0.0001
}

watch(
  friends,
  (currentFriends) => {
    if (!map || !AdvancedMarker || !PinElementClass) return

    // Añadir o actualizar markers de amigos presentes
    currentFriends.forEach((f, userId) => {
      const existing = friendMarkers.get(userId)
      if (existing) {
        if (hasMovedSignificantly(existing.position, { lat: f.lat, lng: f.lng })) {
          existing.position = { lat: f.lat, lng: f.lng }
        }
      } else {
        const el = document.createElement('div')
el.style.cssText = 'display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:#10b981;border:2px solid white;color:white;font-size:14px;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,0.3)'
el.textContent = (f.username ?? '?').charAt(0).toUpperCase()

        const marker = new AdvancedMarker({
          position: { lat: f.lat, lng: f.lng },
          map,
          content: el,
          title: f.username,
          gmpClickable: true,
        })

        marker.addListener('gmp-click', () => {
          const current = friends.value.get(userId)
          if (current) emit('friend-click', current)
        })

        friendMarkers.set(userId, marker)
      }
    })

    // Quitar markers de amigos que ya no están
    friendMarkers.forEach((marker, userId) => {
      if (!currentFriends.has(userId)) {
        marker.map = null
        friendMarkers.delete(userId)
      }
    })
  },
  { deep: true },
)

watch(mapType, (type) => {
  applyMapType(type)
})


onMounted(async () => {
  if (!mapRef.value) return

  setOptions({
    key: import.meta.env.VITE_GOOGLE_MAPS_KEY,
    v: 'weekly',
  })

  const { Map } = await importLibrary('maps')
  const markerLib = (await importLibrary('marker')) as any
  AdvancedMarker = markerLib.AdvancedMarkerElement
  PinElementClass = markerLib.PinElement

  map = new Map(mapRef.value, {
    mapId: 'DEMO_MAP_ID',
    center: props.center,
    zoom: props.zoom,
    disableDefaultUI: true,
    zoomControl: false,
  })

  map.addListener('zoom_changed', () => {
    if (mapType.value === 'auto') {
      applyMapType('auto')
    }
  })
  applyMapType(mapType.value, props.zoom)

  

  loadPlaces(props.center.lat, props.center.lng)
})

async function loadPlaces(lat: number, lng: number) {
  if (!map || !AdvancedMarker) return
  try {
    const response = props.placeType
      ? await getNearbyPlaces({
          latitude: lat,
          longitude: lng,
          radius: 1500,
          place_type: props.placeType,
        })
      : await getRecommendations({
          latitude: lat,
          longitude: lng,
          radius: 1500,
          limit: 20,
        })

    markers.forEach((m) => {
      m.map = null
    })
    markers = []

    response.data.forEach((place) => {
      const marker = new AdvancedMarker({
        position: place.location,
        map,
        title: place.name,
        gmpClickable: true,
      })
      marker.addListener('gmp-click', () => emit('place-click', place))
      markers.push(marker)
    })
  } catch (err) {
    console.error('Error cargando lugares cercanos:', err)
  }
}
function handleRecenter() {
  if (!map) return
  if (geoError.value) return
  const lat = coords.value.latitude
  const lng = coords.value.longitude
  if (lat === 0 && lng === 0) return
  map.setCenter({ lat, lng })
  map.setZoom(15)
}
</script>

<template>
  <div class="relative w-full h-full">
    <div ref="mapRef" class="w-full h-full" />

    <!-- Widget del tiempo -->
    <div
      v-if="weather"
      class="absolute top-20 right-4 z-10 bg-black/70 backdrop-blur-md border border-white/20 rounded-2xl px-3 py-2 text-white shadow-card flex items-center gap-3"
    >
      <WeatherIcon :condition="weather.condition" :size="32" />
      <div class="flex flex-col leading-tight">
        <div class="text-2xl font-extralight">
          {{ weather.temp }}<span class="text-base">°</span>
        </div>
        <div class="flex items-center gap-1 text-xs text-white/60">
          <MapPin :size="10" />
          <span>{{ weather.city }}</span>
        </div>
        <div class="text-xs text-white/40 capitalize">{{ weather.description }}</div>
      </div>
      <button
        type="button"
        class="text-white/40 hover:text-white transition-colors p-0.5 rounded-full ml-1"
        :class="{ 'animate-spin': refreshing }"
        @click="refreshWeather"
      >
        <RefreshCw :size="13" />
      </button>
    </div>

    <button
      type="button"
      class="absolute bottom-6 right-6 w-12 h-12 rounded-full bg-black/80 backdrop-blur-md border border-white/20 text-white flex items-center justify-center shadow-card hover:bg-black/90 transition-colors z-10"
      title="Centrar en mi ubicación"
      @click="handleRecenter"
    >
      <span class="text-xl">📍</span>
    </button>
    <!-- Selector de tipo de mapa -->
    <div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-10">
  <MapTypeSelector v-model="mapType" />
</div>

  </div>
</template>
