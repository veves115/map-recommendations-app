<template>
  <div class="flex flex-col h-screen">
    <nav class="bg-blue-600 text-white px-6 py-3 flex justify-between items-center">
      <router-link to="/" class="font-bold text-lg">MapApp</router-link>
      <div class="flex gap-4">
        <router-link to="/chat" class="hover:underline">Chat</router-link>
      </div>
    </nav>

    <div class="p-6 max-w-xl mx-auto w-full">
      <h1 class="text-2xl font-bold mb-6">Mis preferencias</h1>

      <form @submit.prevent="handleAdd" class="flex gap-2 mb-6">
        <input
          v-model="newCategory"
          placeholder="Categoría (ej: restaurantes)"
          required
          class="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          v-model="newSubcategory"
          placeholder="Subcategoría (opcional)"
          class="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Añadir
        </button>
      </form>

      <ul class="space-y-2">
        <li
          v-for="pref in preferences"
          :key="pref.id"
          class="flex justify-between items-center bg-white border border-gray-200 rounded px-4 py-3 shadow-sm"
        >
          <span>
            <span class="font-medium">{{ pref.category }}</span>
            <span v-if="pref.subcategory" class="text-gray-500"> · {{ pref.subcategory }}</span>
          </span>
          <button
            @click="handleDelete(pref.id)"
            class="text-red-500 hover:text-red-700 text-sm"
          >
            Eliminar
          </button>
        </li>
      </ul>

      <p v-if="preferences.length === 0" class="text-gray-400 text-center mt-8">
        No tienes preferencias aún.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getPreferences, createPreference, deletePreference } from '@/api/preferences'
import type { Preference } from '@/types/api'

const preferences = ref<Preference[]>([])
const newCategory = ref('')
const newSubcategory = ref('')

onMounted(async () => {
  const response = await getPreferences()
  preferences.value = response.data
})

const handleAdd = async () => {
  await createPreference(newCategory.value, newSubcategory.value || undefined)
  newCategory.value = ''
  newSubcategory.value = ''
  const response = await getPreferences()
  preferences.value = response.data
}

const handleDelete = async (id: number) => {
  await deletePreference(id)
  preferences.value = preferences.value.filter(p => p.id !== id)
}
</script>