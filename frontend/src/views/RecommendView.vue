<template>
  <div class="container my-5">
    <!-- 캐릭터 선택 안 했을 때 -->
    <div v-if="!characterStore.selectedCharacter" class="alert alert-warning text-center">
      <h2 class="fw-bold mb-3 pt-3">
        <i class="bi bi-heart-pulse-fill"></i> 함께 할 캐릭터를 데리고 돌아와 주세요.
      </h2>
      <div class="fs-5">
        <router-link to="/characters" class="character-link ms-1 d-inline-flex align-items-center"
          @mouseover="hover = true" @mouseleave="hover = false">
          <i :class="hover ? 'bi bi-person-arms-up me-1' : 'bi bi-person-raised-hand me-1'"></i>
          캐릭터
        </router-link>
        를 선택하여 잠을 깨워 주세요!
      </div>
    </div>

    <!-- 캐릭터 선택 됐을 때 -->
    <div v-else>
      <!-- 제목 + 버튼 -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold mb-0">
          <i class="bi bi-heart-pulse-fill text-primary"></i> {{ characterStore.selectedCharacter.name }}의 추천 영화
        </h2>
        <button v-if="!characterStore.loading" class="fw-semibold btn-scale"
          style="border: none; background: none; font-size: 1.5rem;" @click="getRecommendationAgain">
          <i class="bi bi-hand-index "></i>
          {{ characterStore.recommendation || characterStore.error ? '재추천 받기' : '추천 받기' }}
        </button>
      </div>

      <!-- 캐릭터 정보 -->
      <div class="d-flex align-items-start">
        <img :src="characterStore.selectedCharacter.image" class="rounded-circle border border-3"
          style="width: 200px; height: 200px; object-fit: cover;" alt="character" />
        <div class="ms-3 mt-4">
          <h2 class="fw-bold">{{ characterStore.selectedCharacter.movie }}</h2>
          <h4 class="ms-1 mt-3">{{ characterStore.selectedCharacter.name }}</h4>
        </div>
      </div>

      <!-- 안내 메시지 -->
      <div v-if="!characterStore.recommendation && !characterStore.loading && !characterStore.error"
        class="recommend-message-wrapper text-center text-muted fw-semibold d-flex justify-content-center align-items-center">
        <div class="d-inline-flex align-items-center recommend-message-inner">
          <button class="fw-semibold btn-scale p-0 me-2"
            style="border: none; background: none; font-size: 2rem; line-height: 1;" @click="getRecommendationAgain">
            추천 받기
          </button>
          버튼을 눌러서 {{ characterStore.selectedCharacter.name }}의 추천 영화를 확인해보세요
        </div>
      </div>

      <!-- 로딩 중 -->
      <div v-if="characterStore.loading && !characterStore.error"
        class="text-center text-muted d-flex flex-column align-items-center justify-content-center"
        style="min-height: 300px; font-size: 2rem;">
        <strong>{{ characterStore.selectedCharacter.name }} 에게 물어 보는 중 {{ loadingDots }}<i
            class="bi bi-feather"></i></strong>
      </div>

      <!-- 오류 메시지 -->
      <div v-if="characterStore.error"
        class="text-center text-danger fw-bold d-flex flex-column align-items-center justify-content-center"
        style="min-height: 300px; font-size: 1.8rem;">
        {{ characterStore.selectedCharacter.name }}님이 잠시 자리를 비웠나 봐요 다시 한번 추천을 눌러 주세요.
      </div>

      <!-- 탭 전환 -->
      <div v-if="characterStore.recommendation && !characterStore.error" class="d-flex mb-4 mt-5">
        <div class="fw-bold flex-fill text-center py-2 me-2 hover-scale-tab rounded" :style="activeTab === 'top'
          ? 'background-color: rgb(160, 160, 160); color: #212529;'
          : 'background-color: rgb(255, 255, 255); color: #212529;'" style="cursor: pointer;"
          @click="activeTab = 'top'">
          <i class="bi bi-hand-thumbs-up-fill text-primary"></i> 추천 영화
        </div>
        <div class="fw-bold flex-fill text-center py-2 hover-scale-tab rounded" :style="activeTab === 'bottom'
          ? 'background-color: rgb(160, 160, 160); color: #212529;'
          : 'background-color: rgb(255, 255, 255); color: #212529;'" style="cursor: pointer;"
          @click="activeTab = 'bottom'">
          <i class="bi bi-hand-thumbs-down-fill text-primary"></i> 비추천 영화
        </div>
      </div>



      <!-- 추천 결과 -->
      <div v-if="currentList.length && !characterStore.error">
        <div v-for="movie in currentList" :key="movie.title">
          <div class="d-flex align-items-start py-3 border-bottom mt-4 ms-5 me-5">
            <div class="me-4 text-center">
              <img v-if="movie.poster" :src="movie.poster" alt="poster" class="rounded shadow-sm hover-scale"
                style="width: 210px; height: 300px; object-fit: cover; cursor: pointer;"
                @click="goToDetail(movie.id)" />
              <div class="mt-2">
                <span class="fs-2 d-block" v-html="renderStars(movie.score)"></span>
                <span class="text-muted">{{ movie.score }}/10</span>
              </div>
            </div>
            <div class="flex-grow-1">
              <h2 class="fw-bold mt-3">{{ movie.title }}</h2>
              <p class="mt-3" style="font-size: 20px;">{{ movie.reason }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCharacterStore } from '@/stores/characterStore'

const characterStore = useCharacterStore()
const router = useRouter()
const activeTab = ref('top')
const hover = ref(false)

const loadingDots = ref('')
let dotInterval = null

const currentList = computed(() => {
  if (!characterStore.recommendation) return []
  return activeTab.value === 'top'
    ? characterStore.recommendation.top
    : characterStore.recommendation.bottom
})

function renderStars(score) {
  const full = Math.floor(score / 2)
  const half = score % 2 >= 1 ? 1 : 0
  const empty = 5 - full - half
  return (
    '<i class="bi bi-star-fill me-1"></i>'.repeat(full) +
    '<i class="bi bi-star-half me-1"></i>'.repeat(half) +
    '<i class="bi bi-star me-1"></i>'.repeat(empty)
  )
}

function goToDetail(movieId) {
  if (movieId) {
    router.push(`/movies/${movieId}`)
  }
}

function getRecommendationAgain() {
  characterStore.error = false
  characterStore.getRecommendation().catch(() => {
    characterStore.error = true
  })
}

function startDotAnimation() {
  let count = 1
  dotInterval = setInterval(() => {
    loadingDots.value = '.'.repeat(count)
    count = count >= 4 ? 1 : count + 1
  }, 500)
}

function stopDotAnimation() {
  if (dotInterval) {
    clearInterval(dotInterval)
    dotInterval = null
    loadingDots.value = ''
  }
}

onMounted(() => {
  startDotAnimation()
  if (
    !characterStore.recommendation &&
    characterStore.selectedCharacter &&
    characterStore.candidateMovies.length > 0
  ) {
    characterStore.getRecommendation().catch(() => {
      characterStore.error = true
    })
  }
})

onUnmounted(() => {
  stopDotAnimation()
})
</script>

<style scoped>
.hover-scale {
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.05);
}

.btn-scale {
  transition: transform 0.2s ease;
}

.btn-scale:hover {
  transform: scale(1.08);
}

/* 추천 안내 메시지 wrapper – 위치 조정하려면 이 부분 수정 */
.recommend-message-wrapper {
  min-height: 300px;
  font-size: 2rem;
  font-weight: 600;
  margin-top: 0px;
}

.hover-scale-tab {
  transition: transform 0.2s ease;
}

.hover-scale-tab:hover {
  transform: scale(1.03);
}

.character-link {
  text-decoration: none;

}
.character-link:hover {
  text-decoration: none;
}
</style>