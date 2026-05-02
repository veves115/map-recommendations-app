<script setup lang="ts">
import { computed } from 'vue'

type Variant = 'primary' | 'ghost' | 'glass' | 'danger'
type Size = 'sm' | 'md' | 'lg'

interface Props {
  variant?: Variant
  size?: Size
  block?: boolean
  loading?: boolean
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  block: false,
  loading: false,
  disabled: false,
  type: 'button',
})
const variantClasses: Record<Variant, string> = {
  primary: 'bg-white text-black hover:bg-white/90 focus:ring-black/30',
  ghost: 'bg-transparent text-white border border-white/10 hover:border-white/30 hover:bg-white/5 focus:ring-white/30',
  glass: 'bg-white/5 text-white border border-white/10 backdrop-blur-sm hover:bg-white/10 focus:ring-white/30',
  danger: 'bg-red-500/90 text-white hover:bg-red-500 focus:ring-red-500/40',

}


const sizeClasses: Record<Size, string> = {
  sm: 'text-xs px-3 py-1.5',
  md: 'text-sm px-4 py-2',
  lg: 'text-base px-6 py-3',
}

const buttonClasses = computed(() => [
  // Base (siempre aplicado)
  'inline-flex items-center justify-center font-medium transition-colors rounded-full',
  'focus:outline-none focus:ring-2',
  'disabled:opacity-50 disabled:cursor-not-allowed',
  // Dinámico
  variantClasses[props.variant],
  sizeClasses[props.size],
  props.block ? 'w-full' : '',
])

</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
  >
    <svg
      v-if="loading"
      class="animate-spin mr-2 h-4 w-4"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12" cy="12" r="10"
        stroke="currentColor" stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
    <slot />
  </button>
</template>

