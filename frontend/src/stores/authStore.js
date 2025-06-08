import { defineStore } from 'pinia'
import { login, signup } from '@/apis/authApi'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    username: null,
    token: localStorage.getItem('authToken') || null,
    userId: localStorage.getItem('authUserId') || null,
  }),

  actions: {
    // 로그인
    async loginUser(payload) {
      try {
        const res = await login(payload)
        this.token = res.data.key
        this.isLoggedIn = true
        this.username = payload.username
        localStorage.setItem('authToken', this.token)

        // 사용자 정보 요청
        await this.fetchUserInfo()
      } catch (err) {
        throw err
      }
    },

    // 회원가입
    async signupUser(payload) {
      try {
        await signup(payload)
        // 로그인 정보 저장 제거
      } catch (err) {
        throw err
      }
    },

    // 사용자 정보 요청
    async fetchUserInfo() {
      try {
        const userInfo = await axios.get('http://localhost:8000/api/accounts/profile/', {
          headers: { Authorization: `Token ${this.token}` },
          withCredentials: true
        })
        this.userId = userInfo.data.id
        localStorage.setItem('authUserId', this.userId)
      } catch (err) {
        console.error('❌ 사용자 정보 요청 실패:', err)
      }
    },

    // 로그아웃
    logout() {
      this.token = null
      this.isLoggedIn = false
      this.username = null
      this.userId = null
      localStorage.removeItem('authToken')
      localStorage.removeItem('authUserId')
    },

    // 앱 로딩 시 로그인 상태 복원
    async initialize() {
      if (this.token && !this.userId) {
        try {
          await this.fetchUserInfo()
          this.isLoggedIn = true
        } catch {
          this.logout()
        }
      } else if (this.token && this.userId) {
        this.isLoggedIn = true
      }
    }
  }
})
