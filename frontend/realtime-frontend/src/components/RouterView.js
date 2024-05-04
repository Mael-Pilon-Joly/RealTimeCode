import { createMemoryHistory, createRouter } from 'vue-router'

import LoginView from './LoginVue.vue'
import HomeView from './HomeVue.vue'
import SignUpView from './SignupView'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView},
  { path: '/signup', component: SignUpView },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router;