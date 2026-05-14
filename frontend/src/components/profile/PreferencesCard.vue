<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import type { Preference } from '@/types/api'
import { listPreferences, createPreference, deletePreference } from '@/api/preferences'
import { formatApiError } from '@/utils/api-errors'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseIconButton from '@/components/ui/BaseIconButton.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import { PLACE_CATEGORIES } from '@/utils/placeCategories'




const preferences = ref<Preference[]>([])
const loading = ref(true)

const newCategory = ref(PLACE_CATEGORIES[0]!)
const newSubcategory = ref('')
const adding = ref(false)
const addError = ref('')

const confirmOpen = ref(false)
const prefIdToDelete = ref<number | null>(null)
const deleting = ref(false)

onMounted(async () => {
  try {
    const response = await listPreferences()
    preferences.value = response.data
  } catch (err) {
    console.error('Error cargando preferencias:', err)
  } finally {
    loading.value = false
  }
})

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
  } catch (e) {
    addError.value = formatApiError(e, 'No se pudo añadir la preferencia')
  } finally {
    adding.value = false
  }
}

function askDelete(id: number) {
  prefIdToDelete.value = id
  confirmOpen.value = true
}

async function handleDelete() {
  if (prefIdToDelete.value === null) return
  deleting.value = true
  try {
    await deletePreference(prefIdToDelete.value)
    preferences.value = preferences.value.filter((p) => p.id !== prefIdToDelete.value)
    confirmOpen.value = false
    prefIdToDelete.value = null
  } catch (err) {
    console.error('Error eliminando preferencia:', err)
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <!-- Mis preferencias -->
  <BaseCard variant="glass">
    <template #header>
      <div class="flex justify-between items-center">
        <h2 class="text-lg font-semibold">Mis preferencias</h2>
        <span class="text-xs text-white/50">{{ preferences.length }} guardadas</span>
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
          <span v-if="pref.subcategory" class="text-white/60"> · {{ pref.subcategory }}</span>
        </span>
        <BaseIconButton
          variant="danger"
          size="sm"
          aria-label="Eliminar preferencia"
          @click="askDelete(pref.id)"
        >
          ×
        </BaseIconButton>
      </li>
    </ul>
  </BaseCard>

  <!-- Añadir preferencia -->
  <BaseCard variant="glass">
    <template #header>
      <h2 class="text-lg font-semibold">Añadir preferencia</h2>
    </template>

    <form @submit.prevent="handleAdd" class="space-y-4">
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

      <BaseInput
        v-model="newSubcategory"
        placeholder="Subcategoría (opcional, ej: italiana, moderna)"
      />

      <p v-if="addError" class="text-sm text-red-400 text-center">{{ addError }}</p>

      <BaseButton type="submit" variant="primary" block :loading="adding">
        Añadir preferencia
      </BaseButton>
    </form>
  </BaseCard>

  <ConfirmDialog
    v-model:open="confirmOpen"
    title="¿Eliminar preferencia?"
    message="Esta acción no se puede deshacer."
    confirm-text="Eliminar"
    variant="danger"
    :loading="deleting"
    @confirm="handleDelete"
  />
</template>
