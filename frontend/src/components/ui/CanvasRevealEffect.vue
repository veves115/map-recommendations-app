<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

interface Props {
  animationSpeed?: number
  colors?: number[][]
  opacities?: number[]
  dotSize?: number
  showGradient?: boolean
  reverse?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  animationSpeed: 10,
  colors: () => [[0, 255, 255]],
  opacities: () => [0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.8, 0.8, 0.8, 1],
  dotSize: 3,
  showGradient: true,
  reverse: false,
})

const canvasRef = ref<HTMLCanvasElement | null>(null)


let renderer: THREE.WebGLRenderer | null = null
let animationFrameId: number | null = null


onMounted(() => {
  if (!canvasRef.value) return
  const canvas = canvasRef.value

// Configurar renderer
renderer = new THREE.WebGLRenderer({ canvas, alpha: true })
renderer.setSize(canvas.clientWidth, canvas.clientHeight, false)
renderer.setPixelRatio(window.devicePixelRatio)

const scene = new THREE.Scene()
const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1)

function buildColors(colors: number[][]): THREE.Vector3[] {
  // Paso 1: expandir a 6 colores según cuántos entren
  let expanded: number[][]
  
  if (colors.length === 2) {
    expanded = [colors[0], colors[0], colors[0], colors[1], colors[1], colors[1]]
  } else if (colors.length === 3) {
    expanded = [colors[0], colors[0], colors[1], colors[1], colors[2], colors[2]]
  } else {
    // 1 color (o cualquier otro caso): repetir 6 veces
    expanded = [colors[0], colors[0], colors[0], colors[0], colors[0], colors[0]]
  }

  // Paso 2: convertir cada [R, G, B] a THREE.Vector3 normalizado
  return expanded.map(color =>
    new THREE.Vector3(color[0] / 255, color[1] / 255, color[2] / 255)
  )
}
const colorVectors = buildColors(props.colors)
const uniforms = {
  u_time:       { value: 0 },
  u_resolution: { value: new THREE.Vector2(
    canvas.clientWidth * window.devicePixelRatio,
    canvas.clientHeight * window.devicePixelRatio
  )},
  u_colors:     { value: colorVectors },
  u_opacities:  { value: props.opacities },
  u_total_size: { value: 20 },
  u_dot_size:   { value: props.dotSize },
  u_reverse:    { value: props.reverse ? 1 : 0 },
}
const material = new THREE.ShaderMaterial({
  vertexShader: `precision mediump float;
in vec2 coordinates;
uniform vec2 u_resolution;
out vec2 fragCoord;
void main(){
  gl_Position = vec4(position.x, position.y, 0.0, 1.0);
  fragCoord = (position.xy + vec2(1.0)) * 0.5 * u_resolution;
  fragCoord.y = u_resolution.y - fragCoord.y;
}`,
  fragmentShader: `precision mediump float;
in vec2 fragCoord;

uniform float u_time;
uniform float u_opacities[10];
uniform vec3 u_colors[6];
uniform float u_total_size;
uniform float u_dot_size;
uniform vec2 u_resolution;
uniform int u_reverse;

out vec4 fragColor;

float PHI = 1.61803398874989484820459;
float random(vec2 xy) {                  
  return fract(tan(distance(xy * PHI, xy) * 0.5) * xy.x);
}
float map(float value, float min1, float max1, float min2, float max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

void main(){         
  vec2 st = fragCoord.xy;
st.x -= abs(floor((mod(u_resolution.x, u_total_size) - u_dot_size) * 0.5));
st.y -= abs(floor((mod(u_resolution.y, u_total_size) - u_dot_size) * 0.5));

float opacity = step(0.0, st.x);
opacity *= step(0.0, st.y);

vec2 st2 = vec2(int(st.x / u_total_size), int(st.y / u_total_size));

float frequency = 5.0;
float show_offset = random(st2);
float rand = random(st2 * floor((u_time / frequency) + show_offset + frequency));
opacity *= u_opacities[int(rand * 10.0)];
opacity *= 1.0 - step(u_dot_size / u_total_size, fract(st.x / u_total_size));
opacity *= 1.0 - step(u_dot_size / u_total_size, fract(st.y / u_total_size));

vec3 color = u_colors[int(show_offset * 6.0)];

float animation_speed_factor = 0.5;
vec2 center_grid = u_resolution / 2.0 / u_total_size;
float dist_from_center = distance(center_grid, st2);

float timing_offset_intro = dist_from_center * 0.01 + (random(st2) * 0.15);

float max_grid_dist = distance(center_grid, vec2(0.0, 0.0));
float timing_offset_outro = (max_grid_dist - dist_from_center) * 0.02 + (random(st2 + 42.0) * 0.2);

if (u_reverse == 1) {
  opacity *= 1.0 - step(timing_offset_outro, u_time * animation_speed_factor);
  opacity *= clamp((step(timing_offset_outro + 0.1, u_time * animation_speed_factor)) * 1.25, 1.0, 1.25);
} else {
  opacity *= step(timing_offset_intro, u_time * animation_speed_factor);
  opacity *= clamp((1.0 - step(timing_offset_intro + 0.1, u_time * animation_speed_factor)) * 1.25, 1.0, 1.25);
}

fragColor = vec4(color, opacity);
fragColor.rgb *= fragColor.a;

}
`,
  uniforms,
  glslVersion: THREE.GLSL3,
  blending: THREE.CustomBlending,
  blendSrc: THREE.SrcAlphaFactor,
  blendDst: THREE.OneFactor,
})
const geometry = new THREE.PlaneGeometry(2, 2)
const mesh = new THREE.Mesh(geometry, material)
scene.add(mesh)

const timer = new THREE.Timer()

const animate = () => {
  if (!renderer) return
  timer.update()
  material.uniforms.u_time.value = timer.getElapsed()
  renderer.render(scene, camera)
  animationFrameId = requestAnimationFrame(animate)
}
animate()   
})               

onUnmounted(() => {
  if (animationFrameId !== null) {
  cancelAnimationFrame(animationFrameId)
}
if (renderer) {
  renderer.dispose()
  renderer = null
}

})
</script>

<template>
  <div class="relative h-full w-full">
    <canvas ref="canvasRef" class="absolute inset-0 h-full w-full" />
    <div
  v-if="showGradient"
  class="absolute inset-0 bg-gradient-to-t from-black to-transparent"
/>

  </div>
</template>
