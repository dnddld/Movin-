<template>
  <div class="container my-5">
    <h2 class="mb-4 fw-bold"><i class="bi bi-film text-primary"> </i> 영화</h2>

    <!-- 카테고리 탭 + 장르 필터 -->
    <div class="mb-4 d-flex align-items-center justify-content-between">
      <div class="d-flex flex-grow-1 gap-3">
        <button v-for="tab in tabs" :key="tab.value" @click="selectTab(tab.value)" :class="[
          'btn fw-bold text-dark w-100 fs-6 rounded-0 py-1 category-tab',
          tab.value === selectedTab ? 'bg-secondary-subtle' : 'bg-white',
        ]" style="border: none">
          {{ tab.label }}
        </button>
      </div>

      <select v-model="selectedGenre" @change="fetchMovies"
        class="form-select ms-4 me-3 border border-dark text-dark rounded-0" style="width: 170px; min-width: 130px">
        <option value="">전체</option>
        <option v-for="genre in genres" :key="genre.id" :value="genre.id">
          {{ genre.name }}
        </option>
      </select>
    </div>

    <!-- 영화 카드 그리드 -->
    <div class="row g-4">
      <div v-for="movie in pagedMovies" :key="movie.id" class="col-6 col-sm-4 col-md-3 col-lg-3 col-xl-2">
        <router-link :to="`/movies/${movie.id}`" class="text-decoration-none text-dark">
          <div class="movie-card position-relative rounded overflow-hidden w-100"
            style="aspect-ratio: 2 / 3; background-size: cover; background-position: center;" :style="{
              backgroundImage: movie.poster_path
                ? `url(https://image.tmdb.org/t/p/w500${movie.poster_path})`
                : 'url(/img/default-poster.jpg)',
            }">

            <!-- D-day 표시 (upcoming 전용) -->
            <!-- 개봉예정 표시 -->
            <!-- D-day 표시 -->
            <div v-if="selectedTab === 'upcoming'"
              class="position-absolute top-0 end-0 m-1 px-1 text-white rounded small fw-semibold"
              style="background-color: rgba(0, 0, 0, 0.75); padding: 1px 4px;">
              {{ getDday(movie.release_date) }}
            </div>

            <!-- 평점 표시 (개봉 예정 탭 제외) -->
            <div v-if="selectedTab !== 'upcoming'"
              class="position-absolute top-0 end-0 m-1 px-1 text-white rounded small fw-semibold"
              style="background-color: rgba(0, 0, 0, 0.75); padding: 1px 4px;">
              <i class="bi bi-star-fill text-white"></i>
              {{ movie.vote_average.toFixed(1) }}
            </div>



            <div class="movie-info text-white text-center p-2">
              <h6 class="mb-1 fw-bold" :style="{ fontSize: movie.title.length > 20 ? '0.8rem' : '1rem' }">
                {{ movie.title }}
              </h6>
              <small>{{ movie.release_date }}</small>
            </div>
          </div>
        </router-link>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <nav class="mt-5 d-flex justify-content-center" v-if="totalPages > 1">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: currentPage === 1 }" @click="goToPage(1)">
          <a class="page-link" href="#"><i class="bi bi-chevron-double-left"></i></a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === 1 }" @click="goToPage(currentPage - 1)">
          <a class="page-link" href="#"><i class="bi bi-chevron-left"></i></a>
        </li>

        <li v-if="startPage > 1" class="page-item disabled">
          <a class="page-link" href="#">...</a>
        </li>

        <li v-for="page in pageRange" :key="page" class="page-item" :class="{ active: currentPage === page }"
          @click="goToPage(page)">
          <a class="page-link" href="#">{{ page }}</a>
        </li>

        <li v-if="endPage < totalPages" class="page-item disabled">
          <a class="page-link" href="#">...</a>
        </li>

        <li class="page-item" :class="{ disabled: currentPage === totalPages }" @click="goToPage(currentPage + 1)">
          <a class="page-link" href="#"><i class="bi bi-chevron-right"></i></a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }" @click="goToPage(totalPages)">
          <a class="page-link" href="#"><i class="bi bi-chevron-double-right"></i></a>
        </li>
      </ul>
    </nav>

  </div>
</template>

<script setup>
import {
  fetchPopularMovies,
  fetchTopRatedMovies,
  fetchNowPlayingMovies,
  fetchUpcomingMovies,
  fetchGenres,
} from "@/apis/tmdbApi";
import { fetchLocalMovies } from '@/apis/movieApi';
import { ref, computed, onMounted, onBeforeUnmount } from "vue";

const tabs = [
  { label: "전체", value: "all" },
  { label: "최고 평점", value: "top" },
  { label: "인기", value: "popular" },
  { label: "상영 중", value: "now" },
  { label: "개봉 예정", value: "upcoming" },
];

const selectedTab = ref("popular");
const selectedGenre = ref("");
const movies = ref([]);
const genres = ref([]);
const currentPage = ref(1);
const pagedMovies = ref([]);
const moviesPerPage = ref(36);
const screenWidth = ref(window.innerWidth);

function getMoviesPerPage() {
  if (screenWidth.value >= 1200) return 6 * 6;
  if (screenWidth.value >= 992) return 4 * 6;
  if (screenWidth.value >= 768) return 4 * 6;
  if (screenWidth.value >= 576) return 3 * 6;
  return 2 * 6;
}

function handleResize() {
  screenWidth.value = window.innerWidth;
  moviesPerPage.value = getMoviesPerPage();
  currentPage.value = 1;
  updatePagedMovies();
}

onMounted(async () => {
  window.addEventListener("resize", handleResize);
  handleResize();
  genres.value = await fetchGenres();
  await selectTab(selectedTab.value);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
});

function updatePagedMovies() {
  const start = (currentPage.value - 1) * moviesPerPage.value;
  const end = start + moviesPerPage.value;
  pagedMovies.value = movies.value.slice(start, end);
}

const totalPages = computed(() => {
  return Math.ceil(movies.value.length / moviesPerPage.value);
});

const maxVisiblePages = 5;

const pageRange = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  const half = Math.floor(maxVisiblePages / 2);
  let start = Math.max(1, current - half);
  let end = start + maxVisiblePages - 1;

  if (end > total) {
    end = total;
    start = Math.max(1, end - maxVisiblePages + 1);
  }

  const range = [];
  for (let i = start; i <= end; i++) {
    range.push(i);
  }
  return range;
});

const startPage = computed(() => pageRange.value[0] || 1);
const endPage = computed(() => pageRange.value[pageRange.value.length - 1] || 1);

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  updatePagedMovies();
}

async function fetchMovies() {
  let baseMovies = [];
  if (selectedTab.value === 'all') {
    const localData = await fetchLocalMovies()
    baseMovies = localData.map(movie => ({
      ...movie,
      poster_path: movie.poster_path?.startsWith('http')
        ? movie.poster_path
        : `https://image.tmdb.org/t/p/w500${movie.poster_path}`,
    }))
  } else if (selectedTab.value === "popular") {
    baseMovies = await fetchPopularMovies();
  } else if (selectedTab.value === "top") {
    baseMovies = await fetchTopRatedMovies();  // ✅ 추가
  } else if (selectedTab.value === "now") {
    baseMovies = await fetchNowPlayingMovies();
  } else if (selectedTab.value === "upcoming") {
    baseMovies = await fetchUpcomingMovies();
  } else {
    baseMovies = await fetchPopularMovies();  // fallback
  }

  if (selectedGenre.value) {
    baseMovies = baseMovies.filter((movie) =>
      movie.genre_ids?.includes(Number(selectedGenre.value))
    );
  }

  movies.value = baseMovies;
  currentPage.value = 1;
  updatePagedMovies();
}


async function selectTab(tab) {
  selectedTab.value = tab;
  await fetchMovies();
}

function getDday(releaseDateStr) {
  const today = new Date()
  const releaseDate = new Date(releaseDateStr)
  const diffTime = releaseDate.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < -365) {
    return '재개봉'  // ✅ 과거 1년 이상이면 재개봉 처리
  }
  return `D${diffDays >= 0 ? '-' + diffDays : diffDays}`  // ✅ 음수일 때는 그대로 D-표시 유지
}
</script>

<style scoped>
.movie-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.movie-card:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.movie-info {
  position: absolute;
  bottom: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.6);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.movie-card:hover .movie-info {
  opacity: 1;
}

.pagination .page-link {
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  color: black;
  cursor: pointer;
  user-select: none;
  padding: 0.375rem 0.75rem;
  transition: color 0.2s ease;
}

.pagination .page-item.disabled .page-link {
  opacity: 0.5;
  pointer-events: none;
}

/* 선택된 페이지: 파란색 강조 */
.pagination .page-item.active .page-link {
  color: #0d6efd !important; /* bootstrap primary blue */
  font-weight: 700;
  text-decoration: underline;
}


.category-tab {
  transition: transform 0.2s ease;
}

.category-tab:hover {
  transform: scale(1.07);
}
</style>