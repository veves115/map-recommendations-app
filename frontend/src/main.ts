import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import { MotionPlugin } from '@vueuse/motion'
import { useAuthStore } from './stores/auth'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
await useAuthStore().loadFromStorage()
app.use(router)
app.use(MotionPlugin)
app.mount('#app')
