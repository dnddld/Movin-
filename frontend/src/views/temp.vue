<template>
  <div class="container my-5">
    <h1 class="h3 mb-4 fw-bold">🎬 추천 영화</h1>

    <!-- 캐릭터 선택 안 했을 때 -->
    <div v-if="!characterStore.selectedCharacter" class="alert alert-warning">
      캐릭터가 선택되지 않았습니다. <router-link to="/characters">캐릭터 선택 페이지</router-link>로 이동하세요.
    </div>

    <!-- 캐릭터 선택된 경우 -->
    <div v-else>
      <!-- 캐릭터 정보 -->
      <div class="d-flex align-items-center mb-4">
        <img
          :src="characterStore.selectedCharacter.image"
          :alt="characterStore.selectedCharacter.name"
          class="rounded-circle me-3"
          style="width: 60px; height: 60px; object-fit: cover;"
        />
        <h5 class="mb-0">{{ characterStore.selectedCharacter.movie }} - {{ characterStore.selectedCharacter.name }}</h5>
      </div>

      <button
        class="btn btn-primary mb-4"
        @click="characterStore.getRecommendation"
        :disabled="characterStore.loading"
      >
        추천 받기
      </button>

      <div v-if="characterStore.loading" class="text-muted">GPT에게 추천 요청 중...</div>

      <!-- 추천 결과 -->
      <div v-if="characterStore.recommendation" class="mt-4">
        <!-- 👍 Top 10 -->
        <h4 class="fw-semibold mb-3">👍 Top 10 추천 영화</h4>
        <div class="row g-4 mb-5">
          <div
            class="col-6 col-md-4 col-lg-3"
            v-for="movie in characterStore.recommendation.top"
            :key="movie.title"
          >
            <div
              class="card h-100 shadow-sm"
              style="cursor: pointer"
              @click="goToDetail(movie.id)"
            >
              <img
                v-if="movie.poster"
                :src="movie.poster"
                :alt="movie.title"
                class="card-img-top"
                style="height: 250px; object-fit: cover;"
              />
              <div class="card-body">
                <h6 class="card-title">{{ movie.title }} ({{ movie.score }}/10)</h6>
                <p class="card-text small text-muted">{{ movie.reason }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 👎 Bottom 5 -->
        <h4 class="fw-semibold mb-3">👎 Bottom 5 비추천 영화</h4>
        <div class="row g-4">
          <div
            class="col-6 col-md-4 col-lg-3"
            v-for="movie in characterStore.recommendation.bottom"
            :key="movie.title"
          >
            <div
              class="card h-100 border-light shadow-sm"
              style="cursor: pointer"
              @click="goToDetail(movie.id)"
            >
              <img
                v-if="movie.poster"
                :src="movie.poster"
                :alt="movie.title"
                class="card-img-top"
                style="height: 250px; object-fit: cover;"
              />
              <div class="card-body">
                <h6 class="card-title">{{ movie.title }} ({{ movie.score }}/10)</h6>
                <p class="card-text small text-muted">{{ movie.reason }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCharacterStore } from '@/stores/characterStore'

const characterStore = useCharacterStore()
const router = useRouter()

function goToDetail(movieId) {
  if (movieId) {
    router.push(`/movies/${movieId}`)
  }
}

onMounted(() => {
  if (
    !characterStore.recommendation &&
    characterStore.selectedCharacter &&
    characterStore.candidateMovies.length > 0
  ) {
    characterStore.getRecommendation()
  }
})
</script>
