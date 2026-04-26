<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { setOptions, importLibrary } from '@googlemaps/js-api-loader'
import { useGeolocation } from '@vueuse/core'
import { getNearbyPlaces } from '@/api/maps'
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

  map = new Map(mapRef.value, {
    center: props.center,
    zoom: props.zoom,
    disableDefaultUI: true,
    zoomControl: true,
  })

  loadPlaces(props.center.lat, props.center.lng)  // ← AÑADIR
})


async function loadPlaces(lat: number, lng: number) {
  if (!map) return
  try {
    const response = await getNearbyPlaces({
      latitude: lat,
      longitude: lng,
      radius: 1000,
    })

    markers.forEach(m => m.setMap(null))
    markers = []

    response.data.forEach(place => {
  const marker = new google.maps.Marker({
    position: place.location,
    map,
    title: place.name,
  })
  marker.addListener('click', () => emit('place-click', place))  // ← AÑADIR
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
