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
  const markerLib = await importLibrary('marker') as any
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

    markers.forEach(m => { m.map = null })
    markers = []

    response.data.forEach(place => {
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
</script>

<template>
  <div ref="mapRef" class="w-full h-full" />
</template>
