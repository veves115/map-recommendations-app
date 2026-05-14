<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{ texts: string[] }>()

const morphTime = 1.5
const cooldownTime = 0.5

const text1Ref = ref<HTMLSpanElement | null>(null)
const text2Ref = ref<HTMLSpanElement | null>(null)

let textIndex = 0
let morph = 0
let cooldown = cooldownTime
let lastTime = new Date()
let animationId: number

function setStyles(fraction: number) {
  const el1 = text1Ref.value
  const el2 = text2Ref.value
  if (!el1 || !el2) return

  el2.style.filter = `blur(${Math.min(8 / fraction - 8, 100)}px)`
  el2.style.opacity = `${Math.pow(fraction, 0.4) * 100}%`

  const inv = 1 - fraction
  el1.style.filter = `blur(${Math.min(8 / inv - 8, 100)}px)`
  el1.style.opacity = `${Math.pow(inv, 0.4) * 100}%`

  el1.textContent = props.texts[textIndex % props.texts.length] ?? ''
  el2.textContent = props.texts[(textIndex + 1) % props.texts.length] ?? ''
}

function doMorph() {
  morph -= cooldown
  cooldown = 0
  let fraction = morph / morphTime
  if (fraction > 1) {
    cooldown = cooldownTime
    fraction = 1
  }
  setStyles(fraction)
  if (fraction === 1) textIndex++
}

function doCooldown() {
  morph = 0
  const el1 = text1Ref.value
  const el2 = text2Ref.value
  if (!el1 || !el2) return
  el2.style.filter = 'none'
  el2.style.opacity = '100%'
  el1.style.filter = 'none'
  el1.style.opacity = '0%'
}

function animate() {
  animationId = requestAnimationFrame(animate)
  const now = new Date()
  const dt = (now.getTime() - lastTime.getTime()) / 1000
  lastTime = now
  cooldown -= dt
  if (cooldown <= 0) doMorph()
  else doCooldown()
}

onMounted(() => animate())
onUnmounted(() => cancelAnimationFrame(animationId))
</script>

<template>
  <div
    class="relative mx-auto h-16 w-full text-center font-bold text-5xl leading-none [filter:url(#threshold)_blur(0.6px)]"
  >
    <span ref="text1Ref" class="absolute inset-x-0 top-0 text-white" />
    <span ref="text2Ref" class="absolute inset-x-0 top-0 text-white" />
    <svg class="hidden">
      <defs>
        <filter id="threshold">
          <feColorMatrix
            in="SourceGraphic"
            type="matrix"
            values="1 0 0 0 0
                    0 1 0 0 0
                    0 0 1 0 0
                    0 0 0 255 -140"
          />
        </filter>
      </defs>
    </svg>
  </div>
</template>
