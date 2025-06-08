<template>
  <!-- 캐릭터 캐러셀: 전체 너비 -->
  <div class="fullwidth-wrapper pt-0 pb-1 mt-fix-navbar">
    <div class="position-relative carousel-wrapper character-carousel-wrapper mb-0">
      <button class="carousel-nav left white-nav" @click="scrollCarousel('character', -1)"><i
          class="bi bi-caret-left"></i></button>
      <div ref="characterCarousel" class="d-flex overflow-hidden carousel-container character-carousel"
        @mousedown="startDrag($event, 'character')" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
        <div v-for="(char, index) in characters" :key="char.id"
          class="flex-shrink-0 character-item text-center blue-filter"
          :class="{ 'no-clip': index === characters.length - 1 }" :style="{ zIndex: characters.length - index }"
          @click="handleClick($event, () => selectCharacterAndGo(char.name))">
          <img :src="char.image" class="rounded character_poster hover-reveal" draggable="false" />
          <div class="character-label">
            <h5>{{ char.movie }}</h5>
            <h6>{{ char.name }}</h6>
          </div>
        </div>
      </div>
      <button class="carousel-nav right white-nav" @click="scrollCarousel('character', 1)"><i
          class="bi bi-caret-right"></i></button>
    </div>
    <h6 class="mini-banner-text"><i class="bi bi-arrow-up-short"></i> 캐릭터를 선택해 캐릭터가 좋아하는 영화를 추천 받아보세요.</h6>
    <h1 class="main-banner-text">
      <i :class="[randomPhrase.icon, 'text-primary', 'me-3']"></i>
      <span v-html="highlightedText"></span>
    </h1>
  </div>

  <div class="py-5">
    <div class="container">
      <!-- 최신 인기 영화 -->
      <h3 class="fw-bold" style="margin-bottom: -1rem; margin-top: 3rem;"><i class="bi bi-fire"></i> 최신 인기 영화</h3>
      <div class="position-relative carousel-wrapper mb-5">
        <button class="carousel-nav left" @click="scrollCarousel('popular', -1)"><i
            class="bi bi-chevron-compact-left mb-5"></i></button>
        <div ref="popularCarousel" class="d-flex popular-carousel overflow-hidden carousel-container"
          @mousedown="startDrag($event, 'popular')" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
          <div v-for="(movie, idx) in popularMovies.slice(0, 20)" :key="movie.id"
            class="flex-shrink-0 movie-item square-movie position-relative"
            @click="handleClick($event, () => goToDetail(movie.id))">
            <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="poster square" draggable="false" />
            <div class="overlay-rank-number">{{ idx + 1 }}</div>
            <div class="movie-hover-info text-center p-2">
              <h6 class="mb-0 fw-bold">{{ movie.title }}</h6>
              <small><i class="bi bi-star-fill"></i> {{ movie.vote_average.toFixed(1) }}</small>
            </div>
          </div>
        </div>
        <button class="carousel-nav right" @click="scrollCarousel('popular', 1)"><i
            class="bi bi-chevron-compact-right mb-5"></i></button>
      </div>

      <!-- 최신 예고편 -->
      <h3 class="fw-bold mb-4"><i class="bi bi-youtube"></i> 최신 예고편</h3>
      <div class="row g-4 mb-5">
        <div v-for="video in upcomingTrailers" :key="video.movieId" class="col-12 col-md-6">
          <div class="ratio ratio-16x9">
            <iframe :src="`https://www.youtube.com/embed/${video.youtubeKey}`" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>
      </div>

      <!-- 지금 상영 중인 영화 -->
      <h3 class="fw-bold" style="margin-bottom: -1rem;"><i class="bi bi-calendar2-check-fill"></i> 지금 상영 중인 영화</h3>
      <div class="position-relative carousel-wrapper mb-3">
        <button class="carousel-nav left" @click="scrollCarousel('nowPlaying', -1)"><i
            class="bi bi-chevron-compact-left mb-5"></i></button>
        <div ref="nowPlayingCarousel" class="d-flex gap-3 overflow-hidden carousel-container nowPlaying-carousel"
          @mousedown="startDrag($event, 'nowPlaying')" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
          <div v-for="movie in nowPlayingMovies.slice(0, 20)" :key="movie.id" class="flex-shrink-0 movie-item"
            @click="handleClick($event, () => goToDetail(movie.id))">
            <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="poster" draggable="false" />
            <div class="movie-hover-info text-center p-2">
              <h6 class="mb-0 fw-bold">{{ movie.title }}</h6>
              <small><i class="bi bi-star-fill"></i> {{ movie.vote_average.toFixed(1) }}</small>
            </div>
          </div>
        </div>
        <button class="carousel-nav right" @click="scrollCarousel('nowPlaying', 1)"><i
            class="bi bi-chevron-compact-right mb-5"></i></button>
      </div>

      <!-- 개봉 예정 영화 -->
      <h3 class="fw-bold" style="margin-bottom: -1rem;"><i class="bi bi-calendar2-week"></i> 개봉 예정 영화</h3>
      <div class="position-relative carousel-wrapper mb-3">
        <button class="carousel-nav left" @click="scrollCarousel('upcoming', -1)"><i
            class="bi bi-chevron-compact-left mb-5"></i></button>
        <div ref="upcomingCarousel" class="d-flex overflow-hidden carousel-container upcoming-carousel"
          @mousedown="startDrag($event, 'upcoming')" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
          <div v-for="movie in upcomingMovies.slice(0, 20)" :key="movie.id" class="flex-shrink-0 movie-item"
            @click="handleClick($event, () => goToDetail(movie.id))">
            <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="poster" draggable="false" />
            <div class="movie-hover-info text-center p-2">
              <h6 class="mb-0 fw-bold">{{ movie.title }}</h6>
              <small><i class="bi bi-star-fill"></i> {{ movie.vote_average.toFixed(1) }}</small>
            </div>
          </div>
        </div>
        <button class="carousel-nav right" @click="scrollCarousel('upcoming', 1)"><i
            class="bi bi-chevron-compact-right mb-5"></i></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { characters } from '@/assets/data/characters'
import { useCharacterStore } from '@/stores/characterStore'
import {
  fetchPopularMovies,
  fetchUpcomingMovies,
  fetchMovieVideos,
  fetchNowPlayingMovies
} from '@/apis/tmdbApi'

const phrases = [
  {
    text: "내가 선택한 주인공과 함께 영화 속' 세계를 탐험해보세요.",
    icon: 'bi bi-person-walking'
  },
  {
    text: "당신만의 친구와 함께 영화 속' 여정을 떠나보세요.",
    icon: 'bi bi-person-raised-hand'
  },
  {
    text: "마음에 드는 인물과 함께 스크린 안' 으로 모험을 떠나보세요.",
    icon: 'bi bi-person-arms-up'
  }
]


const randomPhrase = ref({ text: '', icon: '' })  // 표시할 문장
const highlightedText = ref('')

const router = useRouter()
const characterStore = useCharacterStore()

const popularMovies = ref([])
const upcomingMovies = ref([])
const upcomingTrailers = ref([])
const nowPlayingMovies = ref([])

const characterCarousel = ref(null)
const popularCarousel = ref(null)
const upcomingCarousel = ref(null)
const nowPlayingCarousel = ref(null)

const isMounted = ref(false)
const isDragging = ref(false)
const startX = ref(0)
const scrollLeft = ref(0)
const preventClick = ref(false)
let activeCarousel = null

function scrollCarousel(type, direction) {
  const map = {
    character: characterCarousel,
    popular: popularCarousel,
    upcoming: upcomingCarousel,
    nowPlaying: nowPlayingCarousel
  }
  const el = map[type]?.value
  if (!el) {
    console.warn(`❗[scrollCarousel] ${type} 캐러셀 마운트 안됨`)
    return
  }
  el.scrollBy({ left: direction * 160, behavior: 'smooth' })
}

function startDrag(e, type) {
  const map = {
    character: characterCarousel,
    popular: popularCarousel,
    upcoming: upcomingCarousel,
    nowPlaying: nowPlayingCarousel
  }
  activeCarousel = map[type]?.value
  isDragging.value = true
  preventClick.value = false
  startX.value = e.pageX - activeCarousel.offsetLeft
  scrollLeft.value = activeCarousel.scrollLeft
}

function onDrag(e) {
  if (!isDragging.value || !activeCarousel) return
  const x = e.pageX - activeCarousel.offsetLeft
  const walk = (x - startX.value) * 1.5
  if (Math.abs(walk) > 5) preventClick.value = true
  activeCarousel.scrollLeft = scrollLeft.value - walk
}

function stopDrag() {
  isDragging.value = false
  activeCarousel = null
}

function handleClick(e, callback) {
  if (preventClick.value) {
    e.preventDefault()
    e.stopPropagation()
  } else {
    callback()
  }
}

function goToDetail(id) {
  router.push(`/movies/${id}`)
}

function selectCharacterAndGo(name) {
  characterStore.setCharacter(name)
  router.push('/recommend')
}

onMounted(async () => {
  isMounted.value = true
  popularMovies.value = await fetchPopularMovies()
  const upcoming = await fetchUpcomingMovies()
  upcomingMovies.value = upcoming
  nowPlayingMovies.value = await fetchNowPlayingMovies()

  const index = Math.floor(Math.random() * phrases.length)
  randomPhrase.value = phrases[index]
  highlightedText.value = randomPhrase.value.text.replace(
    /'/g,
    `<span class="text-primary">'</span>`
  )
  const trailers = []
  for (const movie of upcoming) {
    const videos = await fetchMovieVideos(movie.id)
    const trailer = videos.find(v => v.site === 'YouTube' && v.type === 'Trailer')
    if (trailer) {
      trailers.push({
        movieId: movie.id,
        title: movie.title,
        youtubeKey: trailer.key
      })
    }
    if (trailers.length >= 4) break
  }
  upcomingTrailers.value = trailers
})
</script>

<style scoped>
.character-carousel-wrapper {
  height: 450px;
  padding-top: 40px;
  padding-bottom: 40px;
}


/* 버튼을 캐러셀 안쪽 중간에 흰색으로 띄우기 */
.carousel-nav.white-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  color: white;
  width: 40px;
  height: 40px;
  font-size: 2rem;
  z-index: 999;
}

.carousel-nav.left.white-nav {
  left: 20px;
}

.carousel-nav.right.white-nav {
  right: 20px;
}

.carousel-nav {
  background: none;
  border: none;
  font-size: 2rem;
  font-weight: bold;
  color: #000;
  width: 40px;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 5;
  pointer-events: auto;
  cursor: pointer;
}


.carousel-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  padding: 40px 0;
}

.carousel-container {
  scroll-snap-type: x mandatory;
  overflow-x: auto;
  flex-grow: 1;
  cursor: grab;
  user-select: none;

}

.carousel-container:active {
  cursor: grabbing;
}



.poster {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin-top: 25px;
  margin-bottom: 90px;
  position: relative;
  z-index: 1;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.character_poster {
  position: relative;
  width: 240px !important;
  height: 360px !important;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.3s ease, filter 0.3s ease, clip-path 0.3s ease, box-shadow 0.3s ease;

  /* 대각선 잘림 (왼쪽 위에서 오른쪽 아래로) */
  clip-path: polygon(0% 0%,
      /* 왼쪽 위 꼭짓점을 오른쪽으로 30px 이동 → 오른쪽 위가 잘려나가도록 만듦 */

      100% 0%,
      /* 오른쪽 위 꼭짓점 (화면 가장 오른쪽 위) */

      calc(100% - 30px) 100%,
      /* 오른쪽 아래 꼭짓점 */

      0% 100%
      /* 왼쪽 아래 꼭짓점 */
    );

  margin-top: 35px;
  margin-bottom: 35px;
  display: block;
  /* ✅ 인라인 간격 제거 */
}

.poster.square {
  border-radius: 0;
}

/* .character-item:hover .poster, */
.movie-item:hover .poster {
  transform: scale(1.05);
  /* ✔️ 호버 시 확대 */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.7);
}

.character-item {
  position: relative;
  margin-left: -40px;
  flex: 0 0 auto;
  /* ❗왼쪽으로 겹쳐지게 */
  transition: transform 0.3s ease, z-index 0.3s ease;

}

.character-item:hover {
  z-index: 2;
  /* 겹칠 때 위로 올라오게 */
  /* transform: scale(1.08) translate(10px, -10px); */
  /* 호버 확대 */
  filter: none;


}

/*  캐릭터 이미지에 파란 톤 필터 적용 및 부드러운 전환 효과 설정 */
.blue-filter img {
  /* 더 쨍한 파란 느낌의 필터 */
  filter: none;
  /* 애니메이션: 필터, 확대, 그림자 효과가 부드럽게 전환됨 */
  transition: transform 0.3s ease, filter 0.3s ease, box-shadow 0.3s ease;
}

/*  마우스를 올렸을 때 원래 이미지 색상으로 복원 및 확대 효과 */
.blue-filter:hover img {
  /* 필터 제거로 원래 색상 노출 */
  filter: grayscale(0.3) brightness(0.8) sepia(3) hue-rotate(165deg) saturate(3);


  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
}



/* ✅ 숫자 포스터 위 겹치기용 */
.overlay-rank-number {
  position: absolute;
  bottom: 0;
  right: -18px;
  /* ✅ 포스터 오른쪽 밖으로 살짝 이동 */
  font-size: 7rem;
  font-weight: 900;
  color: white;
  font-family: 'Tahoma', sans-serif;
  /* 깔끔한 숫자 폰트 */

  -webkit-text-stroke: 3px rgb(55, 133, 236);
  /* 테두리 */
  text-shadow: 1px 4px 7px rgba(0, 0, 0, 0.5);
  /* 그림자 */

  transform: translateY(-18%);
  /* ✅ 아래로 살짝 내려주기 */
  z-index: 2;
  pointer-events: none;
}

/*  캐릭터 캐러셀 왼쪽 여백 */
.character-carousel {
  padding-left: 40px;
  gap: 0px;
  /* 아이템 사이 여백 제거 */

}

/*  인기 영화 캐러셀 왼쪽 여백 */
.popular-carousel {
  padding-left: 20px;
  gap: 56px;

}

/*  개봉 예정 영화 캐러셀 왼쪽 여백 */
.upcoming-carousel {
  padding-left: 16px;
  gap: 18px;

}

/*  상영 중인 영화 캐러셀 왼쪽 여백 */
.nowPlaying-carousel {
  padding-left: 16px;
  gap: 18px;
}

/* 마지막 캐릭터에는 clip-path 제거 */
.character-item.no-clip .character_poster {
  clip-path: none !important;
}

.mt-fix-navbar {
  margin-top: -38px;
}

.character-label {
  position: absolute;
  bottom: 40px;
  right: 14px;
  color: white;
  text-align: right;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
  text-shadow: 2px 2px 2px rgba(0, 0, 0, 1);
  /* 가독성 보조 */
  z-index: 999;
  /* ✅ 이미지보다 위에 위치하도록 */

}

.character-item:hover .character-label {
  opacity: 1;
}

.main-banner-text {
  text-align: center;
  color: rgb(0, 0, 0);
  font-weight: 900;
  font-size: 2.7rem;
  margin-bottom: 1rem;
  margin-top: 1rem;
}

.mini-banner-text {
  text-align: center;
  color: rgb(88, 88, 88);

  margin-bottom: 3rem;
  margin-top: -2rem;
}

.movie-hover-info {
  position: absolute;
  bottom: 0px;
  left: 0;
  right: 0;
  padding: 8px 4px;
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 2;
  text-shadow: 1px 1px 3px rgba(112, 112, 112, 0.685);

}

.movie-item {
  position: relative;
  /* ✅ 반드시 있어야 포스터 위에 표시됨 */
  border-radius: 12px;

}

.movie-item:hover .movie-hover-info {
  opacity: 1;
}
</style>