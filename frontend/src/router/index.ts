import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
  },
  { 
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
  },
  { 
    meta: { requiresAuth: true },
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
  },
  {
    meta: { requiresAuth: true },
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
  },
  {
    meta: { requiresAuth: true },
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/ChatView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const token = localStorage.getItem('token')

  if (requiresAuth && !token) {
    return '/login'
  }
})

export default router