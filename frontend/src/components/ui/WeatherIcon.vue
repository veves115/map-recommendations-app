<script setup lang="ts">
import type { WeatherCondition } from '@/composables/useWeather'

defineProps<{ condition: WeatherCondition; size?: number }>()
</script>

<template>
  <!-- SUN -->
  <svg v-if="condition === 'clear'" :width="size ?? 40" :height="size ?? 40" viewBox="0 0 48 48" fill="none">
    <g style="transform-origin: 24px 24px" class="animate-spin-slow">
      <line v-for="deg in [0,45,90,135,180,225,270,315]" :key="deg"
        x1="24" y1="6" x2="24" y2="10" stroke="#FBBF24" stroke-width="2" stroke-linecap="round"
        :style="`transform-origin: 24px 24px; rotate: ${deg}deg`" />
    </g>
    <circle cx="24" cy="24" r="8" fill="#FBBF24" opacity="0.2" class="animate-pulse" />
    <circle cx="24" cy="24" r="8" stroke="#FBBF24" stroke-width="2" />
  </svg>

  <!-- CLOUDS -->
  <svg v-else-if="condition === 'clouds'" :width="size ?? 40" :height="size ?? 40" viewBox="0 0 48 48" fill="none">
    <g class="animate-sway">
      <path d="M36 30H14a8 8 0 01-.5-16A10 10 0 0134 16a7 7 0 012 14z" fill="#94A3B8" opacity="0.15" />
      <path d="M36 30H14a8 8 0 01-.5-16A10 10 0 0134 16a7 7 0 012 14z" stroke="#94A3B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
    </g>
  </svg>

  <!-- RAIN -->
  <svg v-else-if="condition === 'rain' || condition === 'drizzle'" :width="size ?? 40" :height="size ?? 40" viewBox="0 0 48 48" fill="none">
    <path d="M36 22H14a7 7 0 01-.5-14A9 9 0 0134 10a6 6 0 012 12z" fill="#60A5FA" opacity="0.1" />
    <path d="M36 22H14a7 7 0 01-.5-14A9 9 0 0134 10a6 6 0 012 12z" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" />
    <line v-for="(drop, i) in [{x:16,d:0},{x:22,d:0.3},{x:28,d:0.6},{x:34,d:0.15}]" :key="i"
      :x1="drop.x" y1="26" :x2="drop.x" y2="30" stroke="#60A5FA" stroke-width="2" stroke-linecap="round"
      class="animate-raindrop" :style="`animation-delay: ${drop.d}s`" />
  </svg>

  <!-- THUNDERSTORM -->
  <svg v-else-if="condition === 'thunderstorm'" :width="size ?? 40" :height="size ?? 40" viewBox="0 0 48 48" fill="none">
    <path d="M36 20H14a7 7 0 01-.5-14A9 9 0 0134 8a6 6 0 012 12z" fill="#F59E0B" opacity="0.08" />
    <path d="M36 20H14a7 7 0 01-.5-14A9 9 0 0134 8a6 6 0 012 12z" stroke="#94A3B8" stroke-width="2" stroke-linecap="round" />
    <path d="M26 20l-3 8h6l-3 10" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
      class="animate-lightning" />
  </svg>

  <!-- SNOW -->
  <svg v-else-if="condition === 'snow'" :width="size ?? 40" :height="size ?? 40" viewBox="0 0 48 48" fill="none">
    <path d="M36 22H14a7 7 0 01-.5-14A9 9 0 0134 10a6 6 0 012 12z" fill="#CBD5E1" opacity="0.15" />
    <path d="M36 22H14a7 7 0 01-.5-14A9 9 0 0134 10a6 6 0 012 12z" stroke="#CBD5E1" stroke-width="2" stroke-linecap="round" />
    <circle v-for="(f, i) in [{x:16,d:0},{x:22,d:0.5},{x:28,d:0.2},{x:34,d:0.7},{x:19,d:1.0},{x:31,d:0.4}]" :key="i"
      :cx="f.x" cy="26" r="1.5" fill="#CBD5E1"
      class="animate-snowflake" :style="`animation-delay: ${f.d}s`" />
  </svg>

  <!-- MIST -->
  <svg v-else-if="condition === 'mist'" :width="size ?? 40" :height="size ?? 40" viewBox="0 0 48 48" fill="none">
    <line v-for="(l, i) in [{y:16,w:28,d:0},{y:22,w:32,d:0.5},{y:28,w:24,d:1.0},{y:34,w:30,d:1.5}]" :key="i"
      :x1="24 - l.w/2" :y1="l.y" :x2="24 + l.w/2" :y2="l.y"
      stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round"
      class="animate-fog" :style="`animation-delay: ${l.d}s`" />
  </svg>
</template>
