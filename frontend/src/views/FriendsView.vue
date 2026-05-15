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
import { createInvite, deleteInvite } from '@/api/friendships'
import BaseIconButton from '@/components/ui/BaseIconButton.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import { removeFriend } from '@/api/friendships'
import GlobePulse from '@/components/ui/GlobePulse.vue'


const creatingInvite = ref(false)
const copiedKey = ref<string | null>(null) // 'code-1', 'link-1', etc.
const friends = ref<Friend[]>([])
const invites = ref<Invite[]>([])
const loading = ref(true)
const codeInput = ref('')
const lookupResult = ref<InvitePreview | null>(null)
const lookupError = ref('')
const lookingUp = ref(false)
const accepting = ref(false)
const joinSuccess = ref(false)
const removeOpen = ref(false)
const friendToRemove = ref<Friend | null>(null)
const removing = ref(false)

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

async function handleCreateInvite() {
  creatingInvite.value = true
  try {
    await createInvite()
    const res = await listInvites()
    invites.value = res.data
  } catch (err) {
    console.error('Error creando invitación:', err)
  } finally {
    creatingInvite.value = false
  }
}

async function handleDeleteInvite(id: number) {
  try {
    await deleteInvite(id)
    invites.value = invites.value.filter((i) => i.id !== id)
  } catch (err) {
    console.error('Error revocando invitación:', err)
  }
}

async function copyToClipboard(text: string, key: string) {
  try {
    await navigator.clipboard.writeText(text)
    copiedKey.value = key
    setTimeout(() => {
      if (copiedKey.value === key) copiedKey.value = null
    }, 2000)
  } catch (err) {
    console.error('No se pudo copiar:', err)
  }
}

function inviteLink(token: string): string {
  return `${window.location.origin}/invite/${token}`
}

function daysUntil(iso: string): number {
  const ms = new Date(iso).getTime() - Date.now()
  return Math.max(0, Math.ceil(ms / (1000 * 60 * 60 * 24)))
}
function askRemove(friend: Friend) {
  friendToRemove.value = friend
  removeOpen.value = true
}

async function handleRemoveFriend() {
  if (!friendToRemove.value) return

  removing.value = true
  try {
    await removeFriend(friendToRemove.value.user.id)
    friends.value = friends.value.filter(
      (f) => f.friendship_id !== friendToRemove.value!.friendship_id,
    )
    removeOpen.value = false
    friendToRemove.value = null
  } catch (err) {
    console.error('Error eliminando amigo:', err)
  } finally {
    removing.value = false
  }
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}
</script>

<template>
  <div class="relative min-h-screen bg-black text-white overflow-hidden">
    <div class="pointer-events-none absolute inset-0 flex items-center justify-center opacity-20">
      <div class="w-[600px] max-w-full">
        <GlobePulse />
      </div>
    </div>

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
              <BaseButton type="submit" variant="primary" :loading="lookingUp">Buscar</BaseButton>
            </div>
          </form>

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

        <!-- Card: Invitar amigos -->
        <BaseCard variant="glass">
          <template #header>
            <div class="flex justify-between items-center">
              <h2 class="text-lg font-semibold">Invitar amigos</h2>
              <BaseButton
                type="button"
                variant="primary"
                size="sm"
                :loading="creatingInvite"
                @click="handleCreateInvite"
              >
                + Crear
              </BaseButton>
            </div>
          </template>

          <p v-if="invites.length === 0" class="text-sm text-white/60">
            No tienes invitaciones activas. Crea una para invitar a alguien.
          </p>

          <ul v-else class="space-y-3">
            <li
              v-for="invite in invites"
              :key="invite.id"
              class="border border-white/10 rounded-card p-3 space-y-2"
            >
              <div class="flex justify-between items-start gap-2">
                <div>
                  <p class="font-mono text-base">{{ invite.code }}</p>
                  <p class="text-xs text-white/50 mt-0.5">
                    {{
                      daysUntil(invite.expires_at) === 0
                        ? 'Caduca hoy'
                        : `Caduca en ${daysUntil(invite.expires_at)} días`
                    }}
                  </p>
                </div>
                <BaseIconButton
                  variant="danger"
                  size="sm"
                  aria-label="Revocar invitación"
                  @click="handleDeleteInvite(invite.id)"
                >
                  ×
                </BaseIconButton>
              </div>

              <div class="flex gap-2">
                <BaseButton
                  type="button"
                  variant="ghost"
                  size="sm"
                  @click="copyToClipboard(invite.code, `code-${invite.id}`)"
                >
                  {{ copiedKey === `code-${invite.id}` ? '✓ Copiado' : 'Copiar código' }}
                </BaseButton>
                <BaseButton
                  type="button"
                  variant="ghost"
                  size="sm"
                  @click="copyToClipboard(inviteLink(invite.token), `link-${invite.id}`)"
                >
                  {{ copiedKey === `link-${invite.id}` ? '✓ Copiado' : 'Copiar link' }}
                </BaseButton>
              </div>
            </li>
          </ul>
        </BaseCard>

        <!-- Card: Mis amigos -->
        <BaseCard variant="glass">
          <template #header>
            <h2 class="text-lg font-semibold">Mis amigos ({{ friends.length }})</h2>
          </template>

          <p v-if="friends.length === 0" class="text-sm text-white/60">
            Aún no tienes amigos. Comparte una invitación para empezar.
          </p>

          <ul v-else class="space-y-2">
            <li
              v-for="f in friends"
              :key="f.friendship_id"
              class="flex justify-between items-center border border-white/10 rounded-card p-3"
            >
              <div>
                <p class="font-medium text-sm">{{ f.user.username }}</p>
                <p class="text-xs text-white/50 mt-0.5">
                  Amigos desde {{ formatDate(f.friends_since) }}
                </p>
              </div>
              <BaseIconButton
                variant="danger"
                size="sm"
                aria-label="Eliminar amigo"
                @click="askRemove(f)"
              >
                ×
              </BaseIconButton>
            </li>
          </ul>
        </BaseCard>
      </template>
      <ConfirmDialog
        v-model:open="removeOpen"
        title="¿Eliminar amistad?"
        :message="friendToRemove ? `Dejarás de ser amigo de ${friendToRemove.user.username}.` : ''"
        confirm-text="Eliminar"
        variant="danger"
        :loading="removing"
        @confirm="handleRemoveFriend"
      />
    </div>
  </div>
</template>
