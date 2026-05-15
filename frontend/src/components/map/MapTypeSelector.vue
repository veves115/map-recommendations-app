<script setup lang="ts">
import { ref } from 'vue'
import { Layers } from 'lucide-vue-next'

type MapType = 'auto' | 'roadmap' | 'hybrid'

const props = defineProps<{ modelValue: MapType }>()
const emit = defineEmits<{ 'update:modelValue': [value: MapType] }>()

const open = ref(false)

const options: { value: MapType; label: string; description: string }[] = [
  { value: 'auto', label: 'Auto', description: 'Cambia según el zoom' },
  { value: 'roadmap', label: 'Mapa', description: 'Calles y edificios' },
  { value: 'hybrid', label: 'Satélite', description: 'Vista aérea' },
]

function select(value: MapType) {
  emit('update:modelValue', value)
  open.value = false
}
</script>

<template>
  <!-- Botón -->
  <button
    type="button"
    :class="[
      'w-12 h-12 rounded-full bg-black/80 backdrop-blur-md border border-white/20 text-white flex items-center justify-center shadow-card hover:bg-black/90 transition-colors z-10',
      open ? 'bg-white/20' : '',
    ]"
    @click="open = !open"
  >
    <Layers :size="20" />
  </button>

  <!-- Overlay -->
  <Transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="open" class="fixed inset-0 z-20" @click="open = false" />
  </Transition>

  <!-- Card -->
  <Transition
    enter-active-class="transition duration-250 ease-out"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100 translate-y-0"
    leave-to-class="opacity-0 translate-y-4"
  >
    <div
      v-if="open"
      class="fixed bottom-24 left-1/2 -translate-x-1/2 z-30 bg-black/90 backdrop-blur-md border border-white/15 rounded-2xl p-4 shadow-card w-80"
    >
      <p class="text-xs text-white/40 mb-3 text-center uppercase tracking-widest">Tipo de mapa</p>
      <div class="flex gap-3">
        <button
          v-for="opt in options"
          :key="opt.value"
          type="button"
          class="flex-1 flex flex-col items-center gap-2 group"
          @click="select(opt.value)"
        >
          <!-- Preview -->
          <!-- Preview -->
          <div
            :class="[
              'w-full aspect-square rounded-xl overflow-hidden border-2 transition-colors',
              modelValue === opt.value
                ? 'border-white'
                : 'border-white/10 group-hover:border-white/40',
            ]"
          >
            <!-- Auto -->
            <div v-if="opt.value === 'auto'" class="relative w-full h-full">
              <img
                src="https://tile.openstreetmap.org/14/8186/6125.png"
                class="absolute inset-0 w-full h-full object-cover"
                alt=""
              />
              <img
                src="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/14/6125/8186"
                class="absolute inset-0 w-full h-full object-cover animate-auto-fade"
                alt=""
              />
            </div>
            <!-- Mapa -->
            <img
              v-else-if="opt.value === 'roadmap'"
              src="https://tile.openstreetmap.org/14/8186/6125.png"
              class="w-full h-full object-cover"
              alt=""
            />
            <!-- Satélite -->
            <img
              v-else
              src="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/14/6125/8186"
              class="w-full h-full object-cover"
              alt=""
            />
          </div>

          <!-- Label -->
          <span
            :class="[
              'text-xs font-medium',
              modelValue === opt.value ? 'text-white' : 'text-white/50',
            ]"
          >
            {{ opt.label }}
          </span>
          <span class="text-[10px] text-white/30 text-center leading-tight">{{
            opt.description
          }}</span>
        </button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
@keyframes auto-fade {
  0%,
  45% {
    opacity: 0;
  }
  50%,
  95% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
.animate-auto-fade {
  animation: auto-fade 4s ease-in-out infinite;
}
</style>
