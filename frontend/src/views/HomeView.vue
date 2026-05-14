<template>
  <div class="w-screen h-screen relative">
    <MapContainer
      :place-type="activeFilter"
      @place-click="handlePlaceClick"
      @friend-click="handleFriendClick"
    />
    <div class="absolute top-4 left-4 right-20 z-10 flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
      <button
        v-for="filter in PLACE_FILTERS"
        :key="filter.value ?? 'all'"
        type="button"
        :class="[
          'px-4 py-2 rounded-full text-sm whitespace-nowrap transition-colors flex-shrink-0',
          activeFilter === filter.value
            ? 'bg-white text-black'
            : 'bg-black/80 text-white border border-white/20 hover:bg-black/90 backdrop-blur-md',
        ]"
        @click="activeFilter = filter.value"
      >
        {{ filter.label }}
      </button>
    </div>
    <UserMenu />
    <!-- Animación emoji saliente -->
    <div
      v-if="flyingEmoji"
      class="pointer-events-none fixed z-50 text-5xl animate-fly-out"
      :style="flyingEmoji.style"
    >
      {{ flyingEmoji.emoji }}
    </div>
    <!-- Animación emoji entrante -->
    <div
      v-if="incomingEmoji"
      class="pointer-events-none fixed z-50 text-5xl animate-fly-in"
      :style="incomingEmoji.style"
    >
      {{ incomingEmoji.emoji }}
    </div>
  </div>

  <!-- Card flotante de detalles -->
  <div
    v-if="placeDetails"
    class="absolute bottom-6 left-1/2 -translate-x-1/2 w-[90%] max-w-md z-10"
  >
    <BaseCard variant="solid" class="max-h-[70vh] overflow-y-auto">
      <template #header>
        <div class="flex justify-between items-start gap-4">
          <div>
            <h2 class="text-xl font-bold">{{ placeDetails.name }}</h2>
            <p class="text-sm text-white/70 mt-0.5 flex flex-wrap items-center gap-x-2">
              <span v-if="placeDetails.rating"> ⭐ {{ placeDetails.rating }} </span>
              <span v-if="placeDetails.user_ratings_total" class="text-white/50">
                · {{ placeDetails.user_ratings_total }} reseñas
              </span>
              <span v-if="placeDetails.price_level !== null" class="text-white/50">
                · {{ '€'.repeat(placeDetails.price_level + 1) }}
              </span>
            </p>
          </div>
          <BaseIconButton
            variant="ghost"
            size="sm"
            aria-label="Cerrar"
            class="flex-shrink-0"
            @click="placeDetails = null"
          >
            ✕
          </BaseIconButton>
        </div>
      </template>

      <p class="text-sm text-white/80">
        {{ placeDetails.formatted_address }}
      </p>

      <p v-if="placeDetails.phone" class="text-sm text-white/60 mt-2">
        📞 {{ placeDetails.phone }}
      </p>

      <a
        v-if="placeDetails.website"
        :href="placeDetails.website"
        target="_blank"
        rel="noopener"
        class="text-sm text-white/60 mt-2 underline block hover:text-white transition-colors"
      >
        🔗 {{ shortDomain(placeDetails.website) }}
      </a>
      <a
        :href="`https://www.google.com/maps/dir/?api=1&destination=${placeDetails.location.lat},${placeDetails.location.lng}`"
        target="_blank"
        rel="noopener"
        class="mt-3 flex items-center gap-2 text-sm font-medium text-white bg-white/10 hover:bg-white/20 transition-colors rounded-lg px-3 py-2"
      >
        <Navigation :size="16" />
        Cómo llegar
      </a>

      <details v-if="placeDetails.opening_hours" class="mt-3 text-sm">
        <summary class="text-white/70 cursor-pointer hover:text-white">Horarios</summary>
        <ul class="mt-2 space-y-0.5 text-white/80 pl-2">
          <li v-for="line in placeDetails.opening_hours" :key="line">
            {{ line }}
          </li>
        </ul>
      </details>

      <div v-if="placeDetails.reviews.length > 0" class="mt-4">
        <h3 class="text-sm font-medium mb-2 text-white/70">Reseñas destacadas</h3>
        <ul class="space-y-3">
          <li
            v-for="review in placeDetails.reviews.slice(0, 3)"
            :key="review.time"
            class="text-sm border-t border-white/10 pt-3 first:border-t-0 first:pt-0"
          >
            <div class="flex justify-between items-center mb-1">
              <span class="font-medium">{{ review.author }}</span>
              <span class="text-white/50 text-xs">⭐ {{ review.rating }}</span>
            </div>
            <p class="text-white/70 line-clamp-3">{{ review.text }}</p>
          </li>
        </ul>
      </div>
    </BaseCard>
  </div>
  <!-- Card flotante de amigo -->
  <div
    v-if="selectedFriend"
    class="absolute bottom-6 left-1/2 -translate-x-1/2 w-[90%] max-w-md z-10"
  >
    <BaseCard variant="solid">
      <template #header>
        <div class="flex justify-between items-start gap-4">
          <div>
            <h2 class="text-xl font-bold">{{ selectedFriend.username }}</h2>
            <p class="text-sm text-white/60 mt-0.5">
              {{ relativeTime(selectedFriend.updated_at) }}
            </p>
          </div>
          <BaseIconButton
            variant="ghost"
            size="sm"
            aria-label="Cerrar"
            class="flex-shrink-0"
            @click="selectedFriend = null"
          >
            ✕
          </BaseIconButton>
        </div>
      </template>

      <p class="text-sm text-white/60">Tu amigo está compartiendo su ubicación en tiempo real.</p>
      <div class="flex gap-3 mt-3">
        <button
          v-for="emoji in ['🔥', '❤️', '👋', '😂', '👍']"
          :key="emoji"
          type="button"
          class="text-2xl hover:scale-125 transition-transform"
          @click="sendEmojiToFriend(emoji)"
        >
          {{ emoji }}
        </button>
      </div>
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
import BaseIconButton from '@/components/ui/BaseIconButton.vue'
import type { FriendLocation } from '@/composables/usePresence'
import { relativeTime } from '@/utils/time'
import { useUserSocket } from '@/composables/useUserSocket'
import { Navigation } from 'lucide-vue-next'
import { PLACE_CATEGORIES } from '@/utils/placeCategories'


const PLACE_FILTERS = [{ value: null, label: 'Todo' }, ...PLACE_CATEGORIES]
const placeDetails = ref<PlaceDetails | null>(null)
const selectedFriend = ref<FriendLocation | null>(null)
const { sendEmoji, onEmoji } = useUserSocket()
const flyingEmoji = ref<{ emoji: string; style: string } | null>(null)

function triggerFlyOut(emoji: string) {
  const cx = window.innerWidth / 2
  const cy = window.innerHeight / 2
  flyingEmoji.value = {
    emoji,
    style: `left: ${cx}px; top: ${cy}px; --tx: ${cx}px; --ty: ${-cy}px;`,
  }
  setTimeout(() => {
    flyingEmoji.value = null
  }, 800)
}

const incomingEmoji = ref<{ emoji: string; style: string } | null>(null)

function triggerFlyIn(emoji: string) {
  const cx = window.innerWidth / 2
  const cy = window.innerHeight / 2
  incomingEmoji.value = {
    emoji,
    style: `left: ${cx}px; top: ${cy}px; --tx: ${cx}px; --ty: ${-cy}px;`,
  }
  setTimeout(() => {
    incomingEmoji.value = null
  }, 800)
}

onEmoji((_senderId, emoji) => {
  triggerFlyIn(emoji)
})

function sendEmojiToFriend(emoji: string) {
  if (!selectedFriend.value) return
  sendEmoji(selectedFriend.value.user_id, emoji)
  triggerFlyOut(emoji)
}

function handleFriendClick(friend: FriendLocation) {
  selectedFriend.value = friend
  placeDetails.value = null
}


const activeFilter = ref<string | null>(null)

const handlePlaceClick = async (place: NearbyPlace) => {
  try {
    const response = await getPlaceDetails(place.place_id)
    placeDetails.value = response.data
    selectedFriend.value = null // cerrar card de amigo si estaba abierta
  } catch (err) {
    console.error('Error cargando detalles:', err)
  }
}
function shortDomain(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, '')
  } catch {
    return url
  }
}
</script>
