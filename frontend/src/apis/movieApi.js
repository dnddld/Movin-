import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const API_URL = 'http://localhost:8000/api/movies'

export async function toggleLike(movieId) {
  
  const authStore = useAuthStore()
  // console.log(authStore.token) // null이면 로그인 안 된 상태
  return axios.post(`http://localhost:8000/api/movies/${movieId}/like/`, {}, {
    headers: {
      Authorization: `Token ${authStore.token}`
    },
    withCredentials: true
  })
}

export async function toggleBookmark(movieId) {
  const authStore = useAuthStore()

  return axios.post(`http://localhost:8000/api/movies/${movieId}/bookmark/`, {}, {
    headers: {
      Authorization: `Token ${authStore.token}`
    },
    withCredentials: true
  })
}

export async function fetchLocalMovies() {
  const res = await axios.get(`${API_URL}/simple/`)
  return res.data
}

export const fetchMovieDetail = (movieId) => {
  return axios.get(`${API_URL}/${movieId}/`).then(res => res.data)
}