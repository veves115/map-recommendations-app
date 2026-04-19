<template>
  <div class="flex flex-col h-screen">
    <nav class="bg-blue-600 text-white px-6 py-3 flex justify-between items-center">
      <span class="font-bold text-lg">MapApp</span>
      <div class="flex gap-4">
        <router-link to="/profile" class="hover:underline">Perfil</router-link>
        <router-link to="/chat" class="hover:underline">Chat</router-link>
      </div>
    </nav>
    <div ref="mapContainer" class="flex-1"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'

const mapContainer = ref<HTMLElement | null>(null)

onMounted(async () => {
  const loader = new Loader({
    apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
    version: 'weekly',
  })

  const { Map } = await loader.importLibrary('maps')
  const { Marker } = await loader.importLibrary('marker') as google.maps.MarkerLibrary

  navigator.geolocation.getCurrentPosition(async (position) => {
    const center = {
      lat: position.coords.latitude,
      lng: position.coords.longitude,
    }

    const map = new Map(mapContainer.value!, { center, zoom: 15 })
    new Marker({ position: center, map })
  })
})
</script>
