<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import createGlobe from 'cobe'

interface Props {
  speed?: number
}

const props = withDefaults(defineProps<Props>(), {
  speed: 0.003,
})

const canvasRef = ref<HTMLCanvasElement | null>(null)

let globe: ReturnType<typeof createGlobe> | null = null
let animationId: number
let phi = 0

const pointerInteracting = { x: 0, y: 0, active: false }
const dragOffset = { phi: 0, theta: 0 }
const phiOffset = { value: 0 }
const thetaOffset = { value: 0 }
let isPaused = false

function onPointerDown(e: PointerEvent) {
  pointerInteracting.x = e.clientX
  pointerInteracting.y = e.clientY
  pointerInteracting.active = true
  isPaused = true
  if (canvasRef.value) canvasRef.value.style.cursor = 'grabbing'
}

function onPointerUp() {
  if (pointerInteracting.active) {
    phiOffset.value += dragOffset.phi
    thetaOffset.value += dragOffset.theta
    dragOffset.phi = 0
    dragOffset.theta = 0
  }
  pointerInteracting.active = false
  isPaused = false
  if (canvasRef.value) canvasRef.value.style.cursor = 'grab'
}

function onPointerMove(e: PointerEvent) {
  if (!pointerInteracting.active) return
  dragOffset.phi = (e.clientX - pointerInteracting.x) / 300
  dragOffset.theta = (e.clientY - pointerInteracting.y) / 1000
}

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return

  function init() {
    const width = canvas!.offsetWidth
    if (width === 0 || globe) return

    globe = createGlobe(canvas!, {
      devicePixelRatio: Math.min(window.devicePixelRatio || 1, 2),
      width,
      height: width,
      phi: 0,
      theta: 0.2,
      dark: 1,
      diffuse: 1.5,
      mapSamples: 16000,
      mapBrightness: 10,
      baseColor: [0.5, 0.5, 0.5],
      markerColor: [0.2, 0.8, 0.9],
      glowColor: [0.05, 0.05, 0.05],
      markers: [
        { location: [51.51, -0.13], size: 0.025 },
        { location: [40.71, -74.01], size: 0.025 },
        { location: [35.68, 139.65], size: 0.025 },
        { location: [-33.87, 151.21], size: 0.025 },
        { location: [48.85, 2.35], size: 0.025 },
        { location: [40.41, -3.7], size: 0.025 },
      ],
      opacity: 0.7,
    })

    function animate() {
      if (!isPaused) phi += props.speed
      globe!.update({
        phi: phi + phiOffset.value + dragOffset.phi,
        theta: 0.2 + thetaOffset.value + dragOffset.theta,
      })
      animationId = requestAnimationFrame(animate)
    }

    animate()
    setTimeout(() => {
      if (canvas) canvas.style.opacity = '1'
    })
  }

  if (canvas.offsetWidth > 0) {
    init()
  } else {
    const ro = new ResizeObserver((entries) => {
      if ((entries[0]?.contentRect.width ?? 0) > 0) {
        ro.disconnect()
        init()
      }
    })
    ro.observe(canvas)
  }

  window.addEventListener('pointermove', onPointerMove, { passive: true })
  window.addEventListener('pointerup', onPointerUp, { passive: true })
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  if (globe) globe.destroy()
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', onPointerUp)
})
</script>

<template>
  <div class="relative aspect-square select-none w-full">
    <canvas
      ref="canvasRef"
      style="width: 100%; height: 100%; cursor: grab; opacity: 0; transition: opacity 1.2s ease; border-radius: 50%; touch-action: none;"
      @pointerdown="onPointerDown"
    />
  </div>
</template>
