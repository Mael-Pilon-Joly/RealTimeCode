import { createMemoryHistory, createRouter } from 'vue-router'

import HomeView from './HomeVue.vue'
import SignUpView from './SignupView'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: SignUpView },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router;