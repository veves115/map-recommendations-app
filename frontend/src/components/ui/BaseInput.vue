<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  id?: string
  type?: string
  placeholder?: string
  label?: string
  error?: string
  disabled?: boolean
  togglePassword?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  id: '',
  type: 'text',
  placeholder: '',
  label: '',
  error: '',
  disabled: false,
  togglePassword: false,
})

const model = defineModel<string>()
const showPassword = ref(false)

const effectiveType = computed(() => {
  if (props.type === 'password' && showPassword.value) return 'text'
  return props.type
})
</script>

<template>
  <div class="w-full">
    <!-- label opcional arriba -->
    <label v-if="label" :for="id || undefined" class="block text-sm text-white/70 mb-2">
      {{ label }}
    </label>

    <!-- wrapper relative para posicionar prefix/suffix -->
    <div class="relative">
      <div
        v-if="$slots.suffix || (togglePassword && type === 'password')"
        class="absolute right-2 top-1/2 -translate-y-1/2 z-10 flex items-center gap-1"
      >
        <slot name="suffix" />
        <button
          v-if="togglePassword && type === 'password'"
          type="button"
          class="px-2 py-1 text-white/60 hover:text-white transition-colors text-sm"
          :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
          @click="showPassword = !showPassword"
        >
          {{ showPassword ? '👁‍🗨' : '👁' }}
        </button>
      </div>

      <input
        v-model="model"
        :id="id || undefined"
        :type="effectiveType"
        :placeholder="placeholder"
        :disabled="disabled"
        class="w-full backdrop-blur-[1px] text-white border border-white/10 rounded-full py-3 px-4 bg-transparent placeholder:text-white/40 focus:outline-none focus:border-white/30 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      />

      <div v-if="$slots.suffix" class="absolute right-2 top-1/2 -translate-y-1/2 z-10">
        <slot name="suffix" />
      </div>
    </div>

    <!-- error opcional abajo -->
    <p v-if="error" class="mt-2 text-sm text-red-400 text-center">
      {{ error }}
    </p>
  </div>
</template>
