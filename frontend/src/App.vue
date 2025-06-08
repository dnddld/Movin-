<template>
  <div id="app" class="app-wrapper">
    <!-- 흐림 배경 이미지 -->
    <div v-if="characterStore.selectedCharacter" class="background-blur"
      :style="{ backgroundImage: `url(${backgroundImageUrl})` }"></div>

    <!-- 실제 콘텐츠 -->
    <div class="content-wrapper min-vh-100">
      <NavBar />
      <main class="flex-grow-1">
        <router-view />
      </main>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import { useCharacterStore } from '@/stores/characterStore'
import Footer from '@/components/Footer.vue'
import { computed } from 'vue'

const characterStore = useCharacterStore()

// 선택된 캐릭터 이름으로 배경 이미지 경로 생성
const backgroundImageUrl = computed(() => {
  const char = characterStore.selectedCharacter
  if (!char) return ''
  const filename = char.name.toLowerCase().replace(/\s+/g, '_') + '.jpg'
  return `/img/characters_bg/${filename}`
})
</script>

<style scoped>
/* 전체 앱 래퍼 */
.app-wrapper {
  position: relative;
  z-index: 0;
  /* background-blur 아래로 내려감 방지 */
  min-height: 100vh;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 캐릭터 배경 이미지 흐림 효과 */
.background-blur {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-size: cover;
  background-position: center;
  filter: grayscale(1) brightness(0.5) blur(2px);
  opacity: 0.12;
  z-index: -1;
  /*  모든 콘텐츠보다 뒤 */
  pointer-events: none;
  /*  클릭 영향 없음 */
}

/* 콘텐츠 wrapper */
.content-wrapper {
  position: relative;
  padding-top: 40px;
  /* NavBar 높이 확보 */
  /* z-index 없음! modal보다 위로 가지 않도록 */
}
</style>