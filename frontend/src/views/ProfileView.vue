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
      <AccountCard />
      <!-- Privacy -->
      <PrivacyCard />
      <!-- Security -->
      <SecurityCard />

      <!-- Preferences -->
      <PreferencesCard /> 
      <!-- Zona de peligro -->
      <DangerZoneCard />
    </div>
  </div>

</template>

<script setup lang="ts">
import UserMenu from '@/components/layout/UserMenu.vue'
import AccountCard from '@/components/profile/AccountCard.vue'
import PrivacyCard from '@/components/profile/PrivacyCard.vue'
import SecurityCard from '@/components/profile/SecurityCard.vue'
import PreferencesCard from '@/components/profile/PreferencesCard.vue'
import DangerZoneCard from '@/components/profile/DangerZoneCard.vue'
</script>

