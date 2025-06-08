<template>
  <div class="container my-5" v-if="profile">
    <h1 class="mb-5 fw-bold"><i class="bi bi-house-heart text-primary"></i> MY<span class="text-primary"> '</span>HOME
    </h1>

    <!-- 프로필 헤더 -->
    <div class="d-flex justify-content-between align-items-start mb-4">
      <div class="d-flex align-items-center gap-3">
        <!-- getProfileImage 함수로 경로 처리 -->
        <img :src="getProfileImage(profile.profile_img)" alt="profile" class="rounded-circle shadow"
          style="width: 150px; height: 150px; object-fit: cover;" />
        <div>
          <h4 class="mb-1 fw-bold">{{ profile.nickname }}</h4>
          <p class="text-muted mb-1">{{ profile.username }}</p>
        </div>
      </div>
      <div>
        <router-link to="/mypage/edit" class="btn p-0 border-0">
          <i class="bi bi-gear-fill fs-4 text-secondary hover-dark"></i>
        </router-link>
      </div>
    </div>

    <!-- 좋아요한 영화 -->
    <div class="mt-5 mb-5 section-min-height">
      <h4 class="mb-3 fw-bold"><i class="bi bi-heart-fill text-primary "></i> 좋아요한 영화</h4>
      <template v-if="profile.like_movies.length">
        <div class="position-relative carousel-wrapper">
          <button class="carousel-nav left" @click="scrollCarousel('like', -1)"><i
              class="bi bi-chevron-compact-left"></i></button>
          <div ref="likeCarousel" class="d-flex gap-3 overflow-hidden carousel-container"
            @mousedown="startDrag($event, 'like')" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
            <div v-for="movie in profile.like_movies" :key="movie.id" class="flex-shrink-0 movie-item"
              @click.prevent="handleClick">
              <router-link :to="`/movies/${movie.id}`" @click.prevent="preventClick ? null : navigate(movie.id)"
                @dragstart.prevent>
                <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="img-fluid rounded poster"
                  draggable="false" />
              </router-link>
            </div>
          </div>
          <button class="carousel-nav right" @click="scrollCarousel('like', 1)"><i
              class="bi bi-chevron-compact-right"></i></button>
        </div>
      </template>
      <template v-else>
        <div class="empty-message">좋아요한 영화가 없습니다.</div>
      </template>
    </div>

    <!-- 북마크한 영화 -->
    <div class="mb-5 section-min-height">
      <h4 class="mb-3 fw-bold"><i class="bi bi-bookmark-fill text-primary "></i> 북마크한 영화</h4>
      <template v-if="profile.bookmark_movies.length">
        <div class="position-relative carousel-wrapper">
          <button class="carousel-nav left" @click="scrollCarousel('bookmark', -1)"><i
              class="bi bi-chevron-compact-left"></i></button>
          <div ref="bookmarkCarousel" class="d-flex gap-3 overflow-hidden carousel-container"
            @mousedown="startDrag($event, 'bookmark')" @mousemove="onDrag" @mouseup="stopDrag" @mouseleave="stopDrag">
            <div v-for="movie in profile.bookmark_movies" :key="movie.id" class="flex-shrink-0 movie-item"
              @click.prevent="handleClick">
              <router-link :to="`/movies/${movie.id}`" @click.prevent="preventClick ? null : navigate(movie.id)"
                @dragstart.prevent>
                <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="img-fluid rounded poster"
                  draggable="false" />
              </router-link>
            </div>
          </div>
          <button class="carousel-nav right" @click="scrollCarousel('bookmark', 1)"><i
              class="bi bi-chevron-compact-right"></i></button>
        </div>
      </template>
      <template v-else>
        <div class="empty-message">북마크한 영화가 없습니다.</div>
      </template>
    </div>

    <!-- 작성한 리뷰 -->
    <div class="mt-4 section-min-height">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-3 fw-bold"><i class="bi bi-pencil-fill text-primary"></i> 작성한 리뷰</h4>
        <button class="btn btn-sm border-0 bg-transparent text-dark d-flex align-items-center gap-1 hover-dark"
          @click="showAllReviews = !showAllReviews">
          <template v-if="!showAllReviews">
            <i class="bi bi-list"></i> 목록
          </template>
          <template v-else>
            접기
          </template>
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

    <!-- 리뷰 모달 -->
    <teleport to="body">
      <div class="modal fade" id="reviewModal" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-body" v-if="selectedReview && selectedReview.user && selectedReview.movie">
              <div class="container-fluid mb-3">
                <div class="row align-items-start">
                  <div class="col">
                    <div class="d-flex align-items-center mb-2">
                      <img :src="getProfileImage(selectedReview.user.profile_img)" class="rounded-circle me-2"
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
                        @click="closeModalAndNavigate" />
                    </div>
                    <div class="text-muted">
                      <small class="me-3">{{ selectedReview.created_at.slice(0, 10) }}</small>
                      <small class="me-3">
                        <i class="bi bi-hand-thumbs-up"></i> {{ selectedReview.like_user_count }}
                      </small>
                    </div>
                  </div>
                </div>
              </div>
              <hr />
              <h6>댓글</h6>
              <div v-if="comments.length === 0" class="text-muted mb-2">아직 댓글이 없습니다.</div>
              <ul class="list-group mb-3">
                <li v-for="comment in comments" :key="comment.id"
                  class="list-group-item border-0 border-bottom px-1 py-2">
                  <div class="d-flex justify-content-between align-items-start flex-wrap">
                    <div class="d-flex flex-column" style="min-width: 120px;">
                      <strong class="mb-1" @click="goToUserProfile(comment.user.id)" style="cursor: pointer;"k>{{ comment.user.nickname ||
                        comment.user.username }}</strong>
                      <div class="text-break">{{ comment.content }}</div>
                    </div>
                    <button v-if="comment.user.id === Number(authStore.userId)"
                      class="bg-transparent border-0 text-dark d-flex align-items-center gap-1 ms-auto mt-1"
                      @click="removeComment(comment.id)">
                      <i class="bi bi-trash"></i> 삭제
                    </button>
                  </div>
                </li>
              </ul>
              <div class="input-group">
                <input v-model="newComment" class="form-control rounded-pill" placeholder="내용을 입력해 주세요" />
                <button class="btn text-dark border-0 d-flex align-items-center gap-1" @click="submitComment">
                  <i class="bi bi-chat"></i> 작성
                </button>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="bg-transparent border-0 text-dark d-flex align-items-center gap-1"
                data-bs-dismiss="modal">
                <i class="bi bi-x-circle"></i> 닫기
              </button>
            </div>
          </div>
        </div>
      </div>
    </teleport>


    <!-- 회원 탈퇴 버튼 -->
    <br>
    <div class="d-flex justify-content-end mt-5">
      <button @click="deleteAccount" class="btn btn-sm btn-danger">회원 탈퇴</button>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import { fetchMyProfile, deleteMyAccount } from '@/apis/userApi'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { createReview, fetchReviewsByMovie, toggleReviewLike, updateReview, deleteReviewById, fetchComments, createComment, deleteComment } from '@/apis/reviewApi'
import * as bootstrap from 'bootstrap'

const profile = ref(null)
const showAllReviews = ref(false)
const authStore = useAuthStore()
const router = useRouter()

const selectedReview = ref(null)
const comments = ref([])
const newComment = ref('')

const likeCarousel = ref(null)
const bookmarkCarousel = ref(null)
const isDragging = ref(false)
const startX = ref(0)
const scrollLeft = ref(0)
const preventClick = ref(false)
let activeCarousel = null

function scrollCarousel(type, direction) {
  const el = type === 'like' ? likeCarousel.value : bookmarkCarousel.value
  if (el) el.scrollBy({ left: direction * 130, behavior: 'smooth' })
}

function startDrag(e, type) {
  activeCarousel = type === 'like' ? likeCarousel.value : bookmarkCarousel.value
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

function handleClick(e) {
  if (preventClick.value) {
    e.preventDefault()
    e.stopPropagation()
  }
}

function navigate(id) {
  router.push(`/movies/${id}`)
}

function openModal(review) {
  console.log('모달 열기 리뷰', review)  // ✅ 콘솔 확인용
  selectedReview.value = review
  const modal = new bootstrap.Modal(document.getElementById('reviewModal'))
  modal.show()
  loadComments()
}

onMounted(async () => {
  try {
    const res = await fetchMyProfile()
    profile.value = res.data

  } catch (err) {
    alert('마이페이지 정보를 불러오는 데 실패했습니다.')
    console.error(err)
  }
})

function deleteAccount() {
  if (!confirm('정말로 탈퇴하시겠습니까?')) return
  deleteMyAccount(authStore.userId)
    .then(() => {
      authStore.logout()
      alert('회원 탈퇴 완료 !')
      router.push('/')
    })
    .catch(err => {
      alert('회원 탈퇴 실패 !')
      console.error(err)
    })
}

const getPosterUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : '/img/placeholder.png'
}

const visibleReviews = computed(() => {
  if (!profile.value?.articles) return []
  return showAllReviews.value
    ? profile.value.articles
    : profile.value.articles.slice(0, 3)
})

// 댓글 관련 API 호출 함수들
async function loadComments() {
  try {
    const res = await fetchComments(selectedReview.value.movie.id, selectedReview.value.id)
    comments.value = res
  } catch (err) {
    console.error('댓글 로딩 실패', err)
  }
}

async function submitComment() {
  if (!newComment.value.trim()) return
  try {
    await createComment(selectedReview.value.movie.id, selectedReview.value.id, newComment.value.trim())
    newComment.value = ''
    await loadComments()
  } catch (err) {
    alert('댓글 작성 실패')
  }
}

async function removeComment(commentId) {
  try {
    await deleteComment(selectedReview.value.movie.id, selectedReview.value.id, commentId)
    await loadComments()
  } catch (err) {
    alert('댓글 삭제 실패')
  }
}
function closeModalAndNavigate() {
  const modalEl = document.getElementById('reviewModal')
  const modal = bootstrap.Modal.getInstance(modalEl)
  if (modal) modal.hide()
  router.push(`/movies/${selectedReview.value.movie.id}`)
}

const goToUserProfile = (id) => {
  // 모달 닫기
  const modalEl = document.getElementById('reviewModal')
  const modal = bootstrap.Modal.getInstance(modalEl)
  if (modal) modal.hide()

  // backdrop 및 상태 제거
  document.querySelectorAll('.modal-backdrop').forEach(el => el.remove())
  document.body.classList.remove('modal-open')
  document.body.style = ''

  // 페이지 이동
  router.push(`/users/${id}`)
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
.card-body {
  padding: 1rem;
}

.movie-item {
  width: 160px;
  scroll-snap-align: start;
}

.poster {
  width: 100%;
  height: 250px;
  object-fit: cover;
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
  color: black;
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

.hover-dark:hover {
  color: black !important;
}

.section-min-height {
  min-height: 280px;
  position: relative;
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