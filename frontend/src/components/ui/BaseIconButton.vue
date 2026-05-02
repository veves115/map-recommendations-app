<script setup lang="ts">
import { computed } from 'vue'

type Variant = 'ghost' | 'subtle' | 'danger'
type Size = 'sm' | 'md' | 'lg'

interface Props {
  variant?: Variant
  size?: Size
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'ghost',
  size: 'md',
  disabled: false,
  type: 'button',
})

const variantClasses: Record<Variant, string> = {
  ghost: 'text-white/60 hover:text-white hover:bg-white/10',
  subtle: 'text-white/80 bg-white/5 hover:text-white hover:bg-white/15',
  danger: 'text-white/40 hover:text-red-400 hover:bg-red-500/10',
}

const sizeClasses: Record<Size, string> = {
  sm: 'w-7 h-7 text-sm',
  md: 'w-9 h-9 text-base',
  lg: 'w-11 h-11 text-lg',
}

const buttonClasses = computed(() => [
  'inline-flex items-center justify-center rounded-full',
  'transition-colors leading-none',
  'focus:outline-none focus:ring-2 focus:ring-white/30',
  'disabled:opacity-50 disabled:cursor-not-allowed',
  variantClasses[props.variant],
  sizeClasses[props.size],
])
</script>

<template>
  <button :type="type" :disabled="disabled" :class="buttonClasses">
    <slot />
  </button>
</template>
