<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { setOptions, importLibrary } from '@googlemaps/js-api-loader'
import { useGeolocation } from '@vueuse/core'
import { getRecommendations } from '@/api/recommendations'
import type { NearbyPlace } from '@/types/api'

interface Props {
  center?: { lat: number; lng: number }
  zoom?: number
}

const props = withDefaults(defineProps<Props>(), {
  center: () => ({ lat: 40.4168, lng: -3.7038 }), // Madrid por defecto
  zoom: 14,
})

const emit = defineEmits<{
  'place-click': [place: NearbyPlace]
}>()

const mapRef = ref<HTMLDivElement | null>(null)
let map: any = null
let PinElementClass: any = null
let userMarker: any = null
let markers: any[] = []
let AdvancedMarker: any = null

const { coords, error: geoError } = useGeolocation()

watch(
  () => ({ lat: coords.value.latitude, lng: coords.value.longitude }),
  (pos) => {
    if (!map) return
    if (geoError.value) return
    if (pos.lat === 0 && pos.lng === 0) return

    map.setCenter(pos)

    // Crear o mover el marker del usuario
    if (!userMarker && AdvancedMarker && PinElementClass) {
      const userPin = new PinElementClass({
        background: '#3b82f6',
        borderColor: '#ffffff',
        glyphColor: '#ffffff',
        scale: 1.1,
      })
      userMarker = new AdvancedMarker({
        position: pos,
        map,
        content: userPin.element,
        title: 'Tu ubicación',
      })
    } else if (userMarker) {
      userMarker.position = pos
    }

    loadPlaces(pos.lat, pos.lng)
  },
)


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
  AdvancedMarker = markerLib.AdvancedMarkerElement

  map = new Map(mapRef.value, {
    mapId: 'DEMO_MAP_ID',
    center: props.center,
    zoom: props.zoom,
    disableDefaultUI: true,
    zoomControl: true,
  })

  loadPlaces(props.center.lat, props.center.lng)
})

async function loadPlaces(lat: number, lng: number) {
  if (!map || !AdvancedMarker) return
  try {
    const response = await getRecommendations({
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

    <button
      type="button"
      class="absolute bottom-6 right-6 w-12 h-12 rounded-full
             bg-black/80 backdrop-blur-md border border-white/20
             text-white flex items-center justify-center
             shadow-card hover:bg-black/90 transition-colors z-10"
      title="Centrar en mi ubicación"
      @click="handleRecenter"
    >
      <span class="text-xl">📍</span>
    </button>
  </div>
</template>

