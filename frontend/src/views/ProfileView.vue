<template>
  <div class="min-h-screen bg-black text-white">
    <UserMenu />

    <div class="max-w-2xl mx-auto px-4 py-12 space-y-8">
      <!-- Header -->
      <div>
        <RouterLink to="/" class="text-sm text-white/60 hover:text-white">
          ← Volver al mapa
        </RouterLink>
        <h1 class="text-3xl font-bold mt-2">Mi perfil</h1>
      </div>

      <!-- User info -->
      <BaseCard variant="glass">
        <template #header>
          <h2 class="text-lg font-semibold">Cuenta</h2>
        </template>

        <div class="space-y-2 text-sm">
          <div>
            <span class="text-white/60">Nombre de usuario: </span>
            <span>{{ authStore.user?.username || '—' }}</span>
          </div>
          <div>
            <span class="text-white/60">Email: </span>
            <span>{{ authStore.user?.email || '—' }}</span>
          </div>
        </div>
      </BaseCard>

      <!-- Preferences -->
      <BaseCard variant="glass">
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-semibold">Mis preferencias</h2>
            <span class="text-xs text-white/50"> {{ preferences.length }} guardadas </span>
          </div>
        </template>

        <p v-if="loading" class="text-sm text-white/60">Cargando...</p>

        <p v-else-if="preferences.length === 0" class="text-sm text-white/60">
          Aún no has añadido preferencias. Cuando añadas alguna, mejorará la calidad de las
          recomendaciones del mapa.
        </p>

        <ul v-else class="flex flex-wrap gap-2">
          <li
            v-for="pref in preferences"
            :key="pref.id"
            class="px-3 py-1.5 rounded-full bg-white/10 border border-white/15 text-sm flex items-center gap-2"
          >
            <span>
              {{ pref.category }}
              <span v-if="pref.subcategory" class="text-white/60"> · {{ pref.subcategory }} </span>
            </span>
            <button
              type="button"
              class="text-white/40 hover:text-red-400 transition-colors text-base leading-none"
              @click="handleDelete(pref.id)"
              aria-label="Eliminar preferencia"
            >
              ×
            </button>
          </li>
        </ul>
      </BaseCard>
      <!-- Add new preference -->
      <BaseCard variant="glass">
        <template #header>
          <h2 class="text-lg font-semibold">Añadir preferencia</h2>
        </template>

        <form @submit.prevent="handleAdd" class="space-y-4">
          <!-- Category dropdown -->
          <Listbox v-model="newCategory">
            <div class="relative">
              <ListboxButton
                class="w-full bg-transparent border border-white/10 rounded-full px-4 py-3 text-white text-left flex justify-between items-center hover:border-white/30 focus:outline-none focus:border-white/30 transition-colors"
              >
                <span>{{ newCategory.label }}</span>
                <span class="text-white/50">▼</span>
              </ListboxButton>
              <ListboxOptions
                class="absolute mt-2 w-full bg-surface-raised backdrop-blur-md border border-white/10 rounded-card shadow-card overflow-hidden z-10 focus:outline-none max-h-60 overflow-y-auto"
              >
                <ListboxOption
                  v-for="cat in PLACE_CATEGORIES"
                  :key="cat.value"
                  :value="cat"
                  v-slot="{ active, selected }"
                >
                  <li
                    :class="[
                      'px-4 py-2 cursor-pointer text-sm',
                      active ? 'bg-white/10' : '',
                      selected ? 'text-white' : 'text-white/80',
                    ]"
                  >
                    {{ cat.label }}
                  </li>
                </ListboxOption>
              </ListboxOptions>
            </div>
          </Listbox>

          <!-- Subcategory -->
          <BaseInput
            v-model="newSubcategory"
            placeholder="Subcategoría (opcional, ej: italiana, moderna)"
          />

          <!-- Error -->
          <p v-if="addError" class="text-sm text-red-400 text-center">
            {{ addError }}
          </p>

          <BaseButton type="submit" variant="primary" block :loading="adding">
            Añadir preferencia
          </BaseButton>
        </form>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { Preference } from '@/types/api'
import BaseCard from '@/components/ui/BaseCard.vue'
import UserMenu from '@/components/layout/UserMenu.vue'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { listPreferences, createPreference, deletePreference } from '@/api/preferences'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const authStore = useAuthStore()
const preferences = ref<Preference[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await listPreferences()
    preferences.value = response.data
  } catch (err) {
    console.error('Error en perfil:', err)
  } finally {
    loading.value = false
  }
})
const PLACE_CATEGORIES = [
  { value: 'restaurant', label: 'Restaurantes' },
  { value: 'cafe', label: 'Cafés' },
  { value: 'bar', label: 'Bares' },
  { value: 'bakery', label: 'Panaderías' },
  { value: 'museum', label: 'Museos' },
  { value: 'park', label: 'Parques' },
  { value: 'shopping_mall', label: 'Centros comerciales' },
  { value: 'gym', label: 'Gimnasios' },
  { value: 'tourist_attraction', label: 'Atracciones turísticas' },
  { value: 'movie_theater', label: 'Cines' },
  { value: 'night_club', label: 'Discotecas' },
  { value: 'book_store', label: 'Librerías' },
]

const newCategory = ref(PLACE_CATEGORIES[0])
const newSubcategory = ref('')
const adding = ref(false)
const addError = ref('')

async function handleAdd() {
  adding.value = true
  addError.value = ''
  try {
    const response = await createPreference({
      category: newCategory.value.value,
      subcategory: newSubcategory.value || null,
    })
    preferences.value.push(response.data)
    newSubcategory.value = ''
  } catch (e: any) {
    addError.value = e?.response?.data?.detail || 'No se pudo añadir la preferencia'
  } finally {
    adding.value = false
  }
}
async function handleDelete(id: number) {
  try {
    await deletePreference(id)
    preferences.value = preferences.value.filter((p) => p.id !== id)
  } catch (err) {
    console.error('Error eliminando preferencia:', err)
  }
}
</script>
