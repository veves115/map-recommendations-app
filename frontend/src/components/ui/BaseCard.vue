<script setup lang="ts">
import { computed } from 'vue'

type Variant = 'flat' | 'elevated' | 'glass' | 'solid' | 'danger'
type Padding = 'none' | 'sm' | 'md' | 'lg'

interface Props {
  variant?: Variant
  padding?: Padding
  interactive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'glass',
  padding: 'md',
  interactive: false,
})

const variantClasses: Record<Variant, string> = {
  flat: 'bg-white/[0.03] border border-white/10',
  elevated: 'bg-white/[0.08] border border-white/15 shadow-card',
  glass: 'bg-white/5 backdrop-blur-md border border-white/10',
  solid: 'bg-black/80 backdrop-blur-md border border-white/10 shadow-card',
  danger: 'bg-zinc-950 border border-red-500/30',
}

const paddingClasses: Record<Padding, string> = {
  none: '',
  sm: 'p-3',
  md: 'p-5',
  lg: 'p-7',
}

const cardClasses = computed(() => [
  'rounded-card text-white',
  variantClasses[props.variant],
  paddingClasses[props.padding],
  props.interactive && 'cursor-pointer transition-colors hover:bg-white/10',
])
</script>

<template>
  <div :class="cardClasses">
    <header v-if="$slots.header" class="mb-4">
      <slot name="header" />
    </header>

    <slot />

    <footer v-if="$slots.footer" class="mt-4">
      <slot name="footer" />
    </footer>
  </div>
</template>
