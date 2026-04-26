<template>
  <div class="w-screen h-screen relative">
    <MapContainer @place-click="handlePlaceClick" />
    <UserMenu />
  </div>

  <!-- Card flotante de detalles (queda igual) -->
  ...


    <!-- Card flotante de detalles -->
    <div
      v-if="placeDetails"
      class="absolute bottom-6 left-1/2 -translate-x-1/2 w-[90%] max-w-md z-10"
    >
      <BaseCard variant="glass">
        <template #header>
          <div class="flex justify-between items-start gap-4">
            <div>
              <h2 class="text-xl font-bold">{{ placeDetails.name }}</h2>
              <p v-if="placeDetails.rating" class="text-sm text-white/70">
                ⭐ {{ placeDetails.rating }} · {{ placeDetails.user_ratings_total }} reseñas
              </p>
            </div>
            <button
              type="button"
              class="text-white/60 hover:text-white text-xl leading-none"
              @click="placeDetails = null"
            >
              ✕
            </button>
          </div>
        </template>

        <p class="text-sm text-white/80">
          {{ placeDetails.formatted_address }}
        </p>

        <p
          v-if="placeDetails.phone"
          class="text-sm text-white/60 mt-2"
        >
          📞 {{ placeDetails.phone }}
        </p>
      </BaseCard>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MapContainer from '@/components/map/MapContainer.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { getPlaceDetails } from '@/api/maps'
import type { NearbyPlace, PlaceDetails } from '@/types/api'
import UserMenu from '@/components/layout/UserMenu.vue'


const placeDetails = ref<PlaceDetails | null>(null)

const handlePlaceClick = async (place: NearbyPlace) => {
  try {
    const response = await getPlaceDetails(place.place_id)
    placeDetails.value = response.data
  } catch (err) {
    console.error('Error cargando detalles:', err)
  }
}
</script>
