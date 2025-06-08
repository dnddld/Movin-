<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100" >
    <div class="card shadow-sm p-4 bg-dark" style="width: 100%; max-width: 400px;">
      <!-- ✅ 로고 이미지 (호버 변경) -->
      <div class="text-center mb-1">
        <img :src="logoSrc" alt="로고" style="height: 100px; cursor: pointer;" @mouseover="logoSrc = hoverLogo"
          @mouseleave="logoSrc = defaultLogo" />
      </div>

      <p class="mb-0 text-center text-white">
        로그인 후 <span class="text-primary">캐릭터</span>를 선택하고
      </p>
      <p class="mb-3 text-center text-white">추천 영화를 받아 보세요!</p>

      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label for="username" class="form-label text-white">이메일</label>
          <input v-model="username" type="text" id="username" class="form-control bg-light" placeholder="이메일을 입력하세요."
            required />
        </div>

        <div class="mb-4">
          <label for="password" class="form-label text-white">비밀번호</label>
          <input v-model="password" type="password" id="password" class="form-control bg-light"
            placeholder="비밀번호를 입력하세요." required />
        </div>

        <button class="btn btn-primary w-100">로그인</button>
      </form>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')

const authStore = useAuthStore()
const router = useRouter()

// ✅ 로고 상태 관리
const defaultLogo = '/img/logo/movin.png'
const hoverLogo = '/img/logo/movie-in.png'
const logoSrc = ref(defaultLogo)

async function loginUser() {
  console.log('✅ 로그인 버튼 클릭됨')
  try {
    await authStore.loginUser({ username: username.value, password: password.value })
    alert('로그인에 성공했습니다!')
    router.push('/')
  } catch {
    alert('로그인에 실패했습니다. 다시 확인해 주세요.')
  }
}

</script>


<style scoped>
  .min-vh-100 {
    min-height: 70vh !important;
}
</style>