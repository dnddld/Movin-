import axios from '@/apis/axios'
import { useAuthStore } from '@/stores/authStore'

// 내 프로필 조회
export async function fetchMyProfile() {
  const authStore = useAuthStore()
  return axios.get('http://localhost:8000/api/accounts/profile/', {
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
    withCredentials: true,
  })
}


// 프로필 수정 요청
export async function updateMyProfile(userId, form) {
  const authStore = useAuthStore()
  const formData = new FormData()

  formData.append('nickname', form.nickname)

  if (form.profile_img instanceof File) {
    formData.append('profile_img', form.profile_img) // 업로드 이미지
  } else if (typeof form.profile_img === 'string') {
    formData.append('profile_img', form.profile_img) // 문자열 경로
  }

  if (form.password) {
    formData.append('password', form.password)
    formData.append('password2', form.password2)
  }

  return axios.post(`http://localhost:8000/api/accounts/${userId}/update/`, form, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Token ${authStore.token}`,
    },
    withCredentials: true,
  })
}

// 다른 유저 프로필 정보 조회
export async function fetchUserProfile(userId) {
  const res = await axios.get(`/accounts/${userId}/profile/`)
  return res.data
}


// 회원 탈퇴 요청
export async function deleteMyAccount(userId) {
  const authStore = useAuthStore()

  return axios.delete(`http://localhost:8000/api/accounts/${userId}/delete/`, {
    headers: {
      Authorization: `Token ${authStore.token}`
    },
    withCredentials: true
  })
}
