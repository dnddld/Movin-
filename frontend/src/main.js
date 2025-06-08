import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './assets/global.css'
import { useAuthStore } from '@/stores/authStore'


const app = createApp(App)

app.use(createPinia())
app.use(router)


useAuthStore().initialize()

app.mount('#app')

axios.defaults.baseURL = 'http://localhost:8000'  // Django 서버 주소
axios.defaults.withCredentials = true             // 세션 기반 인증 시 필요