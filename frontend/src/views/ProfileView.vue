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
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-semibold">Cuenta</h2>
            <button
              v-if="!isEditing"
              type="button"
              class="text-sm text-white/60 hover:text-white transition-colors"
              @click="startEdit"
            >
              Editar
            </button>
          </div>
        </template>

        <!-- Modo view -->
        <div v-if="!isEditing" class="space-y-2 text-sm">
          <div>
            <span class="text-white/60">Nombre de usuario: </span>
            <span>{{ authStore.user?.username || '—' }}</span>
          </div>
          <div>
            <span class="text-white/60">Email: </span>
            <span>{{ authStore.user?.email || '—' }}</span>
          </div>
          <p v-if="saveSuccess" class="text-sm text-green-400 mt-2">✓ Guardado correctamente</p>
        </div>

        <!-- Modo edit -->
        <form v-else @submit.prevent="saveEdit" class="space-y-4">
          <BaseInput v-model="editForm.username" label="Nombre de usuario" id="edit-username" />
          <BaseInput v-model="editForm.email" type="email" label="Email" id="edit-email" />

          <p v-if="saveError" class="text-sm text-red-400">
            {{ saveError }}
          </p>

          <div class="flex gap-2 justify-end">
            <BaseButton type="button" variant="ghost" :disabled="saving" @click="cancelEdit">
              Cancelar
            </BaseButton>
            <BaseButton type="submit" variant="primary" :loading="saving"> Guardar </BaseButton>
          </div>
        </form>
      </BaseCard>
      <BaseCard variant="glass">
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-semibold">Seguridad</h2>
            <button
              v-if="!isChangingPassword"
              type="button"
              class="text-sm text-white/60 hover:text-white transition-colors"
              @click="startPasswordChange"
            >
              Cambiar contraseña
            </button>
          </div>
        </template>

        <!-- Modo view -->
        <div v-if="!isChangingPassword" class="text-sm text-white/60">
          <p>Tu contraseña está protegida. Cámbiala periódicamente.</p>
          <p v-if="passwordSuccess" class="text-green-400 mt-2">✓ Contraseña actualizada</p>
        </div>

        <!-- Modo edit -->
        <form v-else @submit.prevent="savePasswordChange" class="space-y-4">
          <BaseInput
            v-model="passwordForm.current"
            type="password"
            label="Contraseña actual"
            id="current-password"
            toggle-password
          />
          <BaseInput
            v-model="passwordForm.new"
            type="password"
            label="Nueva contraseña"
            id="new-password"
            toggle-password
          />
          <BaseInput
            v-model="passwordForm.confirm"
            type="password"
            label="Confirmar nueva contraseña"
            id="confirm-password"
            toggle-password
          />

          <p v-if="passwordError" class="text-sm text-red-400">
            {{ passwordError }}
          </p>

          <div class="flex gap-2 justify-end">
            <BaseButton
              type="button"
              variant="ghost"
              :disabled="changingPassword"
              @click="cancelPasswordChange"
            >
              Cancelar
            </BaseButton>
            <BaseButton type="submit" variant="primary" :loading="changingPassword">
              Guardar
            </BaseButton>
          </div>
        </form>
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
              @click="askDelete(pref.id)"
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
      <!-- Zona de peligro -->
  <BaseCard variant="danger">
    <template #header>
      <h2 class="text-lg font-semibold text-red-400">Zona de peligro</h2>
    </template>

    <p class="text-sm text-white/60 mb-4">
      Eliminar tu cuenta desactivará el acceso inmediatamente y deberás contactar con soporte para
      recuperarla.
    </p>

    <BaseButton variant="danger" @click="deleteOpen = true"> Eliminar mi cuenta </BaseButton>
  </BaseCard>
    </div>
  </div>
  <ConfirmDialog
    v-model:open="confirmOpen"
    title="¿Eliminar preferencia?"
    message="Esta acción no se puede deshacer."
    confirm-text="Eliminar"
    variant="danger"
    :loading="deleting"
    @confirm="handleDelete"
  />
  <ConfirmDialog
    v-model:open="deleteOpen"
    title="¿Eliminar cuenta?"
    message="Tu cuenta se desactivará. Perderás acceso inmediatamente y necesitarás contactar a soporte para reactivarla."
    confirm-text="Eliminar cuenta"
    variant="danger"
    :loading="deletingAccount"
    @confirm="handleDeleteAccount"
  />
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
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import { updateMe } from '@/api/users'
import { changePassword } from '@/api/auth'
import { useRouter } from 'vue-router'
import { deleteMe } from '@/api/users'

const router = useRouter()

const deleteOpen = ref(false)
const deletingAccount = ref(false)

const isChangingPassword = ref(false)
const passwordForm = ref({
  current: '',
  new: '',
  confirm: '',
})
const changingPassword = ref(false)
const passwordError = ref('')
const passwordSuccess = ref(false)

const isEditing = ref(false)
const editForm = ref({ username: '', email: '' })
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)
const authStore = useAuthStore()
const preferences = ref<Preference[]>([])
const loading = ref(true)
const confirmOpen = ref(false)
const prefIdToDelete = ref<number | null>(null)
const deleting = ref(false)

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

const newCategory = ref(PLACE_CATEGORIES[0]!)
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

function askDelete(id: number) {
  prefIdToDelete.value = id
  confirmOpen.value = true
}

function startEdit() {
  editForm.value = {
    username: authStore.user?.username ?? '',
    email: authStore.user?.email ?? '',
  }
  saveError.value = ''
  saveSuccess.value = false
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
  saveError.value = ''
}
const typeMessages: Record<string, string> = {
  string_pattern_mismatch: 'Solo se permiten letras, números, guiones bajos y guiones medios.',
  string_too_short: 'Demasiado corto.',
  string_too_long: 'Demasiado largo.',
  value_error: 'Valor no válido.',
  missing: 'Campo obligatorio.',
}

function formatApiError(e: any, fallback: string): string {
  const detail = e?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((err) => typeMessages[err.type] ?? err.msg).join(', ')
  }
  return fallback
}

async function saveEdit() {
  if (!authStore.user) return

  // Construir payload solo con campos que cambiaron
  const payload: { username?: string; email?: string } = {}
  if (editForm.value.username !== authStore.user.username) {
    payload.username = editForm.value.username
  }
  if (editForm.value.email !== authStore.user.email) {
    payload.email = editForm.value.email
  }

  // Si no hay cambios, simplemente cerrar
  if (Object.keys(payload).length === 0) {
    isEditing.value = false
    return
  }

  saving.value = true
  saveError.value = ''
  try {
    const response = await updateMe(payload)
    authStore.updateUser(response.data)
    isEditing.value = false
    saveSuccess.value = true
    setTimeout(() => {
      saveSuccess.value = false
    }, 3000)
  } catch (e: any) {
    saveError.value = formatApiError(e, 'No se pudo actualizar')
  } finally {
    saving.value = false
  }
}
function startPasswordChange() {
  passwordForm.value = { current: '', new: '', confirm: '' }
  passwordError.value = ''
  passwordSuccess.value = false
  isChangingPassword.value = true
}

function cancelPasswordChange() {
  isChangingPassword.value = false
  passwordError.value = ''
}

async function savePasswordChange() {
  passwordError.value = ''

  // Validación frontend: confirmación coincide
  if (passwordForm.value.new !== passwordForm.value.confirm) {
    passwordError.value = 'La nueva contraseña y su confirmación no coinciden'
    return
  }

  // Validación frontend: longitud mínima (espejo del backend)
  if (passwordForm.value.new.length < 8) {
    passwordError.value = 'La nueva contraseña debe tener al menos 8 caracteres'
    return
  }

  changingPassword.value = true
  try {
    await changePassword(passwordForm.value.current, passwordForm.value.new)
    isChangingPassword.value = false
    passwordSuccess.value = true
    setTimeout(() => {
      passwordSuccess.value = false
    }, 3000)
  } catch (e: any) {
    passwordError.value = formatApiError(e, 'No se pudo cambiar la contraseña')
  } finally {
    changingPassword.value = false
  }
}

async function handleDeleteAccount() {
  deletingAccount.value = true
  try {
    await deleteMe()
    authStore.logout()
    router.push('/login')
  } catch (err) {
    console.error('Error eliminando cuenta:', err)
    deletingAccount.value = false
  }
}
</script>
