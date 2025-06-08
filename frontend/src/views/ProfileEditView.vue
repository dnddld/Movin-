<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-sm p-4 bg-dark" style="width: 100%; max-width: 500px;">
      <!-- 로고 (호버 시 이미지 변경) -->
      <div class="text-center mb-2">
        <img
          :src="logoSrc"
          alt="로고"
          style="height: 100px; cursor: pointer;"
          @mouseover="logoSrc = hoverLogo"
          @mouseleave="logoSrc = defaultLogo"
        />
      </div>

      <h3 class="mb-4 text-center text-white">
        <span class="text-primary">회원</span>정보수정
      </h3>

      <form @submit.prevent="submitUpdate">
        <!-- 닉네임 -->
        <div class="mb-3">
          <label class="form-label text-white">닉네임</label>
          <input
            v-model="form.nickname"
            class="form-control bg-light"
            placeholder="새로운 닉네임을 입력하세요."
            required
          />
        </div>

        <hr class="border-light" />

        <!-- 이미지 업로드 -->
        <div class="mb-3">
          <label class="form-label text-white">새로운 프로필 이미지</label>
          <input type="file" class="form-control" @change="handleFileUpload" />
        </div>

        <hr class="border-light" />

        <!-- 비밀번호 -->
        <div class="mb-3">
          <label class="form-label text-white">새 비밀번호</label>
          <input
            v-model="form.password"
            type="password"
            class="form-control bg-light"
            placeholder="비밀번호를 수정하려면 입력하세요."
          />
        </div>

        <!-- 비밀번호 확인 -->
        <div class="mb-4">
          <label class="form-label text-white">비밀번호 확인</label>
          <input
            v-model="form.password2"
            type="password"
            class="form-control bg-light"
            placeholder="비밀번호를 다시 입력하세요."
          />
        </div>

        <button class="btn btn-primary w-100">수정 완료</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { updateMyProfile } from '@/apis/userApi'

const router = useRouter()
const authStore = useAuthStore()

// 프로필 이미지 목록
const profileImages = [
  '/img/profile1.png',
  '/img/profile2.png',
  '/img/profile3.png',
  '/img/profile4.png',
  '/img/profile5.png'
]

const selectedImage = ref('')
const uploadedFile = ref(null)

const form = ref({
  nickname: '',
  password: '',
  password2: '',
  profile_img: ''
})

// 로고 호버 이미지 전환
const defaultLogo = '/img/logo/movin.png'
const hoverLogo = '/img/logo/movie-in.png'
const logoSrc = ref(defaultLogo)

function selectImage(img) {
  selectedImage.value = img
  uploadedFile.value = null
  form.value.profile_img = img
}

function handleFileUpload(event) {
  uploadedFile.value = event.target.files[0]
  selectedImage.value = ''
  form.value.profile_img = uploadedFile.value
}

async function submitUpdate() {
  try {
    const formData = new FormData()
    formData.append('nickname', form.value.nickname)
    if (form.value.password) formData.append('password', form.value.password)
    if (form.value.password2) formData.append('password2', form.value.password2)

    // 업로드 파일만 formData에 추가, 기본 이미지 문자열은 제외
    if (form.value.profile_img instanceof File) {
      formData.append('profile_img', form.value.profile_img)
    }

    console.log('전송 데이터:', [...formData.entries()])

    const res = await updateMyProfile(authStore.userId, formData)
    console.log('서버 응답:', res)
    
    alert('프로필이 수정되었습니다.')
    router.push('/mypage')
  } catch (err) {
    alert('수정 실패')
    console.error(err)
  }
}
</script>

<style scoped>
.min-vh-100 {
  min-height: 85vh !important;
}

</style>