import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // 백엔드 주소
  withCredentials: true
})

// 로그인 후 저장된 토큰을 자동으로 Authorization 헤더에 포함
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default api
