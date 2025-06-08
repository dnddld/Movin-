<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="card shadow-sm p-4 bg-dark" style="width: 100%; max-width: 400px;">
      <!-- 로고 -->
      <div class="text-center mb-2">
        <img
          :src="logoSrc"
          @mouseover="logoSrc = hoverLogo"
          @mouseleave="logoSrc = defaultLogo"
          alt="로고"
          style="height: 100px; cursor: pointer;"
        />
      </div>

      <!-- 안내 문구 -->
      <h3 class="mb-4 text-center text-white"><span class="text-primary">회원</span>가입</h3>

      <form @submit.prevent="signup">
        <p class="text-white">기본 <span class="text-primary">프로필</span> 이미지</p>
        <!-- 프로필 선택 -->
        <div class="ms-3 mb-3" style="margin-top: -30px;">
          <label class="form-label text-white fw-semibold"></label>
          <div class="d-flex flex-wrap gap-3">
            <img
              v-for="img in profileImages"
              :key="img"
              :src="img"
              class="rounded-circle border"
              :class="{ 'border-3 border-primary': selectedImage === img }"
              @click="selectedImage = img"
              style="width: 60px; height: 60px; object-fit: cover; cursor: pointer;"
            />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label text-white">이메일</label>
          <input
            v-model="username"
            class="form-control bg-light"
            placeholder="아이디로 사용 할 이메일을 입력하세요."
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label text-white">비밀번호</label>
          <input
            v-model="password"
            type="password"
            class="form-control bg-light"
            placeholder="비밀번호를 입력하세요."
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label text-white">비밀번호 확인</label>
          <input
            v-model="password2"
            type="password"
            class="form-control bg-light"
            placeholder="비밀번호를 다시 입력하세요."
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label text-white">닉네임</label>
          <input
            v-model="nickname"
            class="form-control bg-light"
            placeholder="닉네임을 입력하세요."
            required
          />
        </div>

        <div class="mb-4">
          <label class="form-label text-white">생년월일</label>
          <input
            v-model="birth"
            type="date"
            class="form-control bg-light"
            required
          />
        </div>

        <button class="btn btn-primary w-100">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const profileImages = [
  '/img/profile1.png',
  '/img/profile2.png',
  '/img/profile3.png',
  '/img/profile4.png',
  '/img/profile5.png'
]

const selectedImage = ref(profileImages[0])
const username = ref('')
const password = ref('')
const password2 = ref('')
const nickname = ref('')
const birth = ref('')

// 로고 호버 이미지 처리
const defaultLogo = '/img/logo/movin.png'
const hoverLogo = '/img/logo/movie-in.png'
const logoSrc = ref(defaultLogo)

async function signup() {
  if (password.value !== password2.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    await authStore.signupUser({
      username: username.value,
      password1: password.value,
      password2: password2.value,
      nickname: nickname.value,
      birth: birth.value,
      profile_img: selectedImage.value
    })
    alert('회원가입에 성공 했습니다! 로그인 페이지로 이동합니다.')
    router.push('/login')
  } catch {
    alert('회원가입 실패에 실패 했습니다! 잠시 후 다시 시도 해주세요..')
  }
}
</script>
<style scoped>
  .min-vh-100 {
    min-height: 85vh !important;
}
</style>