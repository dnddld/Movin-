<template>
  <footer class="bg-dark text-white pt-3 pb-3 mt-5">
    <div class="container">
      <!-- 로고 -->
      <div class="text-center mb-1 ms-2">
        <a class="logo-link d-inline-block" @click="navigateWithScrollTop('/')">
          <img src="/img/logo/movin.png" alt="movin" class="logo-img default" />
          <img src="/img/logo/movie-in.png" alt="moviein" class="logo-img hover" />
        </a>
      </div>

      <!-- 네비게이션 링크 (가로 정렬) -->
      <div class="d-flex flex-wrap justify-content-center gap-4 mb-2">
        <a class="text-secondary text-decoration-none" @click.prevent="navigateWithScrollTop('/')"
          style="cursor: pointer;">홈</a>
        <a class="text-secondary text-decoration-none" @click.prevent="navigateWithScrollTop('/movies')"
          style="cursor: pointer;">영화</a>
        <a class="text-secondary text-decoration-none" @click.prevent="navigateWithScrollTop('/recommend')"
          style="cursor: pointer;">추천</a>
        <a class="text-secondary text-decoration-none" @click.prevent="navigateWithScrollTop('/reviews')"
          style="cursor: pointer;">코멘트</a>
        <a class="text-secondary text-decoration-none" @click.prevent="navigateWithScrollTop('/characters')"
          style="cursor: pointer;">캐릭터 선택</a>
      </div>
           <!-- 저작권 문구 -->
      <div class="text-center mt-2 small text-secondary">
        &copy; 2025 MOVIN. All rights reserved.
      </div>
      <div class="d-flex flex-wrap justify-content-center gap-4 mt-2">
        <i class="bi bi-twitter-x text-secondary"></i>
        <i class="bi bi-instagram text-secondary"></i>
        <i class="bi bi-youtube text-secondary"></i>
      </div>
 
    </div>
  </footer>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function navigateWithScrollTop(path) {
  router.push(path).then(() => {
    window.scrollTo({ top: 0, behavior: 'auto' })
  })
}
</script>

<style scoped>
.logo-link {
  position: relative;
  width: 120px;
  height: 45px;
  cursor: pointer;
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
</style>