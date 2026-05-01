<script setup lang="ts">
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  DialogDescription,
  TransitionRoot,
  TransitionChild,
} from '@headlessui/vue'
import BaseCard from './BaseCard.vue'
import BaseButton from './BaseButton.vue'

type Variant = 'primary' | 'danger'

interface Props {
  open: boolean
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  variant?: Variant
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  title: '¿Estás seguro?',
  message: '',
  confirmText: 'Confirmar',
  cancelText: 'Cancelar',
  variant: 'primary',
  loading: false,
})

const emit = defineEmits<{
  'update:open': [value: boolean]
  confirm: []
  cancel: []
}>()

function close() {
  emit('update:open', false)
  emit('cancel')
}
</script>

<template>
  <TransitionRoot :show="open" as="template">
    <Dialog as="div" class="relative z-50" @close="close">
      <!-- Overlay -->
      <TransitionChild
        as="template"
        enter="duration-200 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-150 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" />
      </TransitionChild>

      <!-- Panel centrado -->
      <div class="fixed inset-0 flex items-center justify-center p-4">
        <TransitionChild
          as="template"
          enter="duration-200 ease-out"
          enter-from="opacity-0 scale-95"
          enter-to="opacity-100 scale-100"
          leave="duration-150 ease-in"
          leave-from="opacity-100 scale-100"
          leave-to="opacity-0 scale-95"
        >
          <DialogPanel class="w-full max-w-md">
            <BaseCard variant="solid">
              <DialogTitle class="text-lg font-semibold">
                {{ title }}
              </DialogTitle>

              <DialogDescription v-if="message" class="mt-2 text-sm text-white/70">
                {{ message }}
              </DialogDescription>

              <div class="flex justify-end gap-2 mt-6">
                <BaseButton variant="ghost" @click="close">
                  {{ cancelText }}
                </BaseButton>
                <BaseButton :variant="variant" :loading="loading" @click="emit('confirm')">
                  {{ confirmText }}
                </BaseButton>
              </div>
            </BaseCard>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
