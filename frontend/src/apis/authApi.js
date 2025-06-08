import axios from 'axios'

export function login(data) {
  console.log('🚀 login API 호출됨')
  return axios.post('http://localhost:8000/api/dj-rest-auth/login/', data, {
    withCredentials: true
  })
}

export function signup(data) {
  return axios.post('http://localhost:8000/api/dj-rest-auth/registration/', data, {
    withCredentials: true
  })
}
