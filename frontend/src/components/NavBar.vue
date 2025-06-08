<template>
  <nav class="navbar navbar-expand-lg fixed-top navbar-dark bg-dark px-3">
    <div class="container">
      <router-link class="navbar-brand logo-link" to="/">
        <img src="/img/logo/movin.png" alt="movin" class="logo-img default" />
        <img src="/img/logo/movie-in.png" alt="moviein" class="logo-img hover" />
      </router-link>

      <button class="navbar-toggler" type="button" @click="toggleNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent" ref="navbar">
        <!-- 좌측 메뉴 -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/">홈</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/movies">영화</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/recommend">추천</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/reviews">코멘트</router-link>
          </li>
        </ul>

        <!-- 우측 메뉴 -->
        <ul class="navbar-nav">
          <template v-if="authStore.isLoggedIn">
            <li class="nav-item">
              <router-link class="nav-link d-flex align-items-center" to="/characters"
                @mouseover="hoverCharacter = true" @mouseleave="hoverCharacter = false">
                <i :class="hoverCharacter ? 'bi bi-person-arms-up me-1' : 'bi bi-person-raised-hand me-1'"></i>
                캐릭터 선택
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/mypage">마이페이지</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">로그아웃</a>
            </li>
          </template>
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">로그인</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/signup">회원가입</router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter, useRoute } from 'vue-router'
import * as bootstrap from 'bootstrap'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const navbar = ref(null)
const hoverCharacter = ref(false)

function logout() {
  authStore.logout()
  router.push('/')
}

const toggleNavbar = () => {
  if (!navbar.value) return
  const collapse = bootstrap.Collapse.getOrCreateInstance(navbar.value)
  collapse.toggle()
}

onMounted(() => {
  watch(
    () => route.path,
    () => {
      if (!navbar.value) return
      const bsCollapse = bootstrap.Collapse.getInstance(navbar.value)
      bsCollapse?.hide()
    }
  )
})

</script>

<style scoped>
.logo-link {
  position: relative;
  display: inline-block;
  width: 110px;
  height: 40px;
}

.logo-img {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  transition: opacity 0.3s ease;
}

.logo-img.default {
  opacity: 1;
}

.logo-img.hover {
  opacity: 0;
}

.logo-link:hover .logo-img.default {
  opacity: 0;
}

.logo-link:hover .logo-img.hover {
  opacity: 1;
}

.navbar-nav .nav-link {
  transition: transform 0.2s ease;
}

.navbar-nav .nav-link:hover {
  transform: scale(1.08);
}

.navbar {
  padding-top: 0.4rem;
  padding-bottom: 0.4rem;
}
</style>