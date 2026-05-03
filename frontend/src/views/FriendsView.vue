<script setup lang="ts">
import { ref, onMounted } from 'vue'
import UserMenu from '@/components/layout/UserMenu.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { listFriends, listInvites } from '@/api/friendships'
import type { Friend, Invite } from '@/types/api'
import { acceptInviteByCode, lookupInviteByCode } from '@/api/friendships'
import type { InvitePreview } from '@/types/api'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const friends = ref<Friend[]>([])
const invites = ref<Invite[]>([])
const loading = ref(true)
const codeInput = ref('')
const lookupResult = ref<InvitePreview | null>(null)
const lookupError = ref('')
const lookingUp = ref(false)
const accepting = ref(false)
const joinSuccess = ref(false)

onMounted(async () => {
  try {
    const [friendsRes, invitesRes] = await Promise.all([listFriends(), listInvites()])
    friends.value = friendsRes.data
    invites.value = invitesRes.data
  } catch (err) {
    console.error('Error cargando datos de amigos:', err)
  } finally {
    loading.value = false
  }
})
async function handleLookup() {
  lookupError.value = ''
  lookupResult.value = null

  const code = codeInput.value.trim().toUpperCase()
  if (code.length !== 6) {
    lookupError.value = 'El código debe tener 6 caracteres'
    return
  }

  lookingUp.value = true
  try {
    const response = await lookupInviteByCode(code)
    lookupResult.value = response.data
    if (!response.data.is_valid) {
      lookupError.value = 'Esta invitación ya no es válida (usada o caducada)'
    }
  } catch (e: any) {
    lookupError.value = e?.response?.data?.detail ?? 'Código no encontrado'
  } finally {
    lookingUp.value = false
  }
}

function cancelLookup() {
  lookupResult.value = null
  lookupError.value = ''
  codeInput.value = ''
}

async function handleAcceptCode() {
  if (!lookupResult.value) return

  accepting.value = true
  try {
    await acceptInviteByCode(lookupResult.value.code)
    const res = await listFriends()
    friends.value = res.data
    cancelLookup()
    joinSuccess.value = true
    setTimeout(() => {
      joinSuccess.value = false
    }, 3000)
  } catch (e: any) {
    lookupError.value = e?.response?.data?.detail ?? 'No se pudo aceptar la invitación'
  } finally {
    accepting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-black text-white">
    <UserMenu />

    <div class="max-w-2xl mx-auto px-4 py-12 space-y-8">
      <!-- Header -->
      <div>
        <RouterLink to="/" class="text-sm text-white/60 hover:text-white">
          ← Volver al mapa
        </RouterLink>
        <h1 class="text-3xl font-bold mt-2">Mis amigos</h1>
      </div>

      <p v-if="loading" class="text-sm text-white/60">Cargando...</p>

      <template v-else>
        <!-- Card: Unirse con código -->
        <BaseCard variant="glass">
          <template #header>
            <h2 class="text-lg font-semibold">Unirse con un código</h2>
          </template>

          <!-- Estado: sin lookup hecho aún -->
          <form v-if="!lookupResult" @submit.prevent="handleLookup" class="space-y-3">
            <BaseInput
              v-model="codeInput"
              id="invite-code"
              label="Código de invitación"
              placeholder="Ej: K3F8XY"
            />
            <p v-if="lookupError" class="text-sm text-red-400">
              {{ lookupError }}
            </p>
            <p v-if="joinSuccess" class="text-sm text-green-400">✓ Invitación aceptada</p>
            <div class="flex justify-end">
              <BaseButton type="submit" variant="primary" :loading="lookingUp"> Buscar </BaseButton>
            </div>
          </form>

          <!-- Estado: lookup OK, mostrando preview -->
          <div v-else class="space-y-4">
            <div class="text-sm">
              <p>
                Te invita
                <span class="font-semibold">{{ lookupResult.inviter.username }}</span>
              </p>
              <p class="text-white/60 mt-1">
                Código: <span class="font-mono">{{ lookupResult.code }}</span>
              </p>
            </div>

            <p v-if="lookupError" class="text-sm text-red-400">
              {{ lookupError }}
            </p>

            <div class="flex gap-2 justify-end">
              <BaseButton type="button" variant="ghost" :disabled="accepting" @click="cancelLookup">
                Cancelar
              </BaseButton>
              <BaseButton
                type="button"
                variant="primary"
                :loading="accepting"
                :disabled="!lookupResult.is_valid"
                @click="handleAcceptCode"
              >
                Aceptar invitación
              </BaseButton>
            </div>
          </div>
        </BaseCard>

        <!-- Card: Mis invitaciones -->
        <BaseCard variant="glass">
          <template #header>
            <h2 class="text-lg font-semibold">Invitar amigos</h2>
          </template>
          <p class="text-sm text-white/60">{{ invites.length }} invitaciones activas</p>
        </BaseCard>

        <!-- Card: Mis amigos -->
        <BaseCard variant="glass">
          <template #header>
            <h2 class="text-lg font-semibold">Mis amigos ({{ friends.length }})</h2>
          </template>
          <p v-if="friends.length === 0" class="text-sm text-white/60">
            Aún no tienes amigos. Comparte una invitación para empezar.
          </p>
          <ul v-else class="space-y-1 text-sm">
            <li v-for="f in friends" :key="f.friendship_id">
              {{ f.user.username }}
            </li>
          </ul>
        </BaseCard>
      </template>
    </div>
  </div>
</template>
