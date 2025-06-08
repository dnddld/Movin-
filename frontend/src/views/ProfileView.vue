<template>

  <div class="container my-5" v-if="profile">
    <h1 class="mb-5 fw-bold"><i class="bi bi-house-heart-fill text-primary"></i> {{ profile.nickname }}<span
        class="text-primary"> '</span>S HOME</h1>
    <!-- 프로필 헤더 -->
    <div class="d-flex justify-content-between align-items-start mb-4">
      <div class="d-flex align-items-center gap-3">
        <img :src="getProfileImage(profile.profile_img)" alt="profile" class="rounded-circle shadow"
          style="width: 150px; height: 150px; object-fit: cover;" />
        <div>
          <h4 class="mb-1 fw-bold">{{ profile.nickname }}</h4>
          <p class="text-muted mb-1">{{ profile.username }}</p>
          <!-- <p class="text-muted small">팔로워 {{ profile.follower_count }} · 팔로잉 {{ profile.following_count }}</p> -->
        </div>
      </div>
    </div>

    <!-- 좋아요한 영화 캐러셀 -->
    <div class="mt-5 mb-5 section-min-height">
      <h4 class="fw-bold mb-3">
        <i class="bi bi-heart-fill text-primary"></i>
        {{ profile.nickname }}<span class="text-primary">'</span> 님이 좋아요한 영화
      </h4>

      <template v-if="profile.like_movies.length">
        <div class="position-relative carousel-wrapper">
          <button class="carousel-nav left" @click="scrollCarousel('like', -1)">
            <i class="bi bi-chevron-compact-left"></i>
          </button>
          <div ref="likeCarousel" class="gap-3 d-flex overflow-hidden carousel-container"
            @mousedown="startDrag($event, 'like')" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
            <div v-for="movie in profile.like_movies" :key="movie.id" class="flex-shrink-0 movie-item"
              @click.prevent="handleClick">
              <router-link :to="`/movies/${movie.id}`" @click.prevent="preventClick ? null : goToMovie(movie.id)"
                @dragstart.prevent>
                <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="poster rounded shadow-sm"
                  draggable="false" />
              </router-link>
            </div>
          </div>
          <button class="carousel-nav right" @click="scrollCarousel('like', 1)">
            <i class="bi bi-chevron-compact-right"></i>
          </button>
        </div>
      </template>

      <template v-else>
        <div class="empty-message">좋아요한 영화가 없습니다.</div>
      </template>
    </div>


    <!-- 북마크한 영화 캐러셀 -->
    <div class="mb-5 section-min-height">
      <h4 class="fw-bold mb-3">
        <i class="bi bi-bookmark text-primary"></i>
        {{ profile.nickname }}<span class="text-primary">'</span> 님이 북마크한 영화
      </h4>

      <template v-if="profile.bookmark_movies.length">
        <div class="position-relative carousel-wrapper">
          <button class="carousel-nav left" @click="scrollCarousel('bookmark', -1)">
            <i class="bi bi-chevron-compact-left"></i>
          </button>
          <div ref="bookmarkCarousel" class="d-flex gap-3 overflow-hidden carousel-container"
            @mousedown="startDrag($event, 'bookmark')" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
            <div v-for="movie in profile.bookmark_movies" :key="movie.id" class="flex-shrink-0 movie-item"
              @click.prevent="handleClick">
              <router-link :to="`/movies/${movie.id}`" @click.prevent="preventClick ? null : goToMovie(movie.id)"
                @dragstart.prevent>
                <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="poster rounded shadow-sm"
                  draggable="false" />
              </router-link>
            </div>
          </div>
          <button class="carousel-nav right" @click="scrollCarousel('bookmark', 1)">
            <i class="bi bi-chevron-compact-right"></i>
          </button>
        </div>
      </template>

      <template v-else>
        <div class="empty-message">북마크한 영화가 없습니다.</div>
      </template>
    </div>


    <!-- 작성한 리뷰 (마이페이지 동일하게) -->
    <div class="mt-4 section-min-height">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-3 fw-bold"><i class="bi bi-pencil  text-primary"></i> {{ profile.nickname }}<span
            class="text-primary">'</span> 님이 작성한 리뷰</h4>
        <button class="btn btn-sm border-0 bg-transparent text-dark d-flex align-items-center gap-1 hover-dark"
          @click="showAllReviews = !showAllReviews">
          <template v-if="!showAllReviews">
            <i class="bi bi-list"></i> 목록
          </template>
          <template v-else>접기</template>
        </button>
      </div>

      <template v-if="visibleReviews.length">
        <div v-for="review in visibleReviews" :key="review.id" class="card mb-3">
          <div class="card-body d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center">
              <img :src="getPosterUrl(review.movie?.poster_path)" alt="poster" class="me-3 rounded"
                style="width: 66px; height: 99px; object-fit: cover; pointer-events: none;" />
              <div>
                <h6 class="mb-1 fw-bold">{{ review.movie.title }}</h6>
                <p class="mb-1 text-muted">
                  <i class="bi bi-star-fill text-dark"></i> {{ review.rate }}/10
                </p>
              </div>
            </div>
            <button class="btn btn-sm bg-transparent border-0 text-dark position-absolute" style="top: 8px; right: 8px;"
              @click="openModal(review)">
              <i class="bi bi-plus-lg"></i> 더 보기
            </button>
          </div>
        </div>
      </template>

      <template v-else>
        <div class="empty-message">작성한 리뷰가 없습니다.</div>
      </template>
    </div>

    <!-- 리뷰 상세 모달 (마이페이지 동일하게 좌우 구조) -->
    <teleport to="body">
      <div class="modal fade" id="reviewModal" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-body" v-if="selectedReview && selectedReview.user && selectedReview.movie">
              <div class="container-fluid mb-3">
                <div class="row align-items-start">
                  <div class="col">
                    <div class="d-flex align-items-center mb-2">
                      <img :src="getProfileImage(profile.profile_img)" class="rounded-circle me-2"
                        width="50" height="50" />
                      <strong>{{ selectedReview.user.nickname || selectedReview.user.username }}</strong>
                    </div>
                    <div class="border rounded p-2 bg-light small text-break"
                      style="height: 200px; overflow-y: auto; white-space: pre-wrap;">
                      {{ selectedReview.content }}
                    </div>
                  </div>
                  <div class="col-auto text-end">
                    <div class="mt-4 mb-2">
                      <img :src="'https://image.tmdb.org/t/p/w500' + selectedReview.movie.poster_path" class="rounded"
                        style="height: 220px; width: auto; object-fit: cover; cursor: pointer;"
                        @click="goToMovie(selectedReview.movie.id)" />
                    </div>
                    <div class="text-muted">
                      <small class="me-3">{{ formatDate(selectedReview.created_at) }}</small>
                      <small class="me-3">
                        <i class="bi bi-hand-thumbs-up"></i> {{ selectedReview.like_user_count }}
                      </small>
                    </div>
                  </div>
                </div>
              </div>
              <hr />
              <h6>댓글</h6>
              <div v-for="comment in comments" :key="comment.id" class="mb-2">
                <strong @click="goToUserProfile(comment.user.id)" style="cursor: pointer;">
                  {{ comment.user.nickname }}
                </strong>
                <span class="ms-2">{{ comment.content }}</span>
              </div>
              <div class="input-group mt-3">
                <input type="text" class="form-control" v-model="newComment" placeholder="댓글 입력" />
                <button class="btn btn-outline-primary" @click="submitComment">등록</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchUserProfile } from '@/apis/userApi'
import { fetchComments, createComment } from '@/apis/reviewApi'
import * as bootstrap from 'bootstrap'

const route = useRoute()
const router = useRouter()

const profile = ref(null)
const selectedReview = ref(null)
const comments = ref([])
const newComment = ref('')
const showAllReviews = ref(false)

const likeCarousel = ref(null)
const bookmarkCarousel = ref(null)
const isDragging = ref(false)
const startX = ref(0)
const scrollLeft = ref(0)
const preventClick = ref(false)
let activeCarousel = null

const getCarouselRef = (type) => type === 'like' ? likeCarousel : bookmarkCarousel

const startDrag = (e, type) => {
  activeCarousel = getCarouselRef(type).value
  isDragging.value = true
  preventClick.value = false
  startX.value = e.pageX - activeCarousel.offsetLeft
  scrollLeft.value = activeCarousel.scrollLeft
}

const onDrag = (e) => {
  if (!isDragging.value || !activeCarousel) return
  const x = e.pageX - activeCarousel.offsetLeft
  const walk = (x - startX.value) * 1.5
  if (Math.abs(walk) > 5) preventClick.value = true
  activeCarousel.scrollLeft = scrollLeft.value - walk
}

const stopDrag = () => {
  isDragging.value = false
  activeCarousel = null
}

const handleClick = (e) => {
  if (preventClick.value) {
    e.preventDefault()
    e.stopPropagation()
  }
}

const scrollCarousel = (type, direction) => {
  const el = getCarouselRef(type).value
  if (el) el.scrollBy({ left: direction * 130, behavior: 'smooth' })
}

const goToMovie = (id) => router.push(`/movies/${id}`)

const fetchProfile = async () => {
  const userId = route.params.userId
  profile.value = await fetchUserProfile(userId)
}
onMounted(fetchProfile)
watch(() => route.params.userId, fetchProfile)

const openModal = async (review) => {
  selectedReview.value = review
  comments.value = await fetchComments(review.movie.id, review.id)
  newComment.value = ''
  const modal = new bootstrap.Modal(document.getElementById('reviewModal'))
  modal.show()
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  await createComment(selectedReview.value.movie.id, selectedReview.value.id, newComment.value)
  comments.value = await fetchComments(selectedReview.value.movie.id, selectedReview.value.id)
  newComment.value = ''
}

const goToUserProfile = (id) => {
  const modalEl = document.getElementById('reviewModal')
  const modal = bootstrap.Modal.getInstance(modalEl)
  if (modal) modal.hide()
  document.querySelectorAll('.modal-backdrop').forEach(el => el.remove())
  document.body.classList.remove('modal-open')
  document.body.style = ''
  router.push(`/users/${id}`)
}

const formatDate = (datetime) => datetime ? new Date(datetime).toLocaleDateString() : ''

const visibleReviews = computed(() => {
  if (!profile.value?.articles) return []
  return showAllReviews.value ? profile.value.articles : profile.value.articles.slice(0, 3)
})

const getPosterUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : '/img/placeholder.png'
}

// 업로드 이미지 vs 기본 이미지 구분 처리
const getProfileImage = (path) => {
  if (!path) return '/img/profile1.png'

  // 기본 이미지 파일일 경우
  if (path.startsWith('/media/img/profile') && path.endsWith('.png')) {
    const filename = path.split('/').pop()
    return `/img/${filename}`   // 👉 public/img/ 에 있는 파일로 매핑
  }
  // 업로드된 사용자 이미지일 경우
  return import.meta.env.VITE_API_URL + path
}
</script>

<style scoped>
.poster {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.movie-item {
  width: 160px;
  scroll-snap-align: start;
}

.carousel-wrapper {
  display: flex;
  align-items: center;
  position: relative;
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

.carousel-nav {
  background: none;
  border: none;
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  width: 40px;
  height: 100%;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-nav.left {
  margin-right: 8px;
}

.carousel-nav.right {
  margin-left: 8px;
}

.section-min-height {
  min-height: 280px;
}

.empty-message {
  height: 100%;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #6c757d;
  font-size: 0.95rem;
}
</style>