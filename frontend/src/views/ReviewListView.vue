<template>
  <div class="container py-5">
    <div>
      <h2 class="fw-bold mb-2"><i class="bi bi-chat-left-heart text-primary"></i> 전체 코멘트</h2>
      <div class="d-flex justify-content-end">
        <select v-model="selectedSort" @change="sortReviews"
          class="form-select border border-dark text-dark rounded-0 mb-4" style="width: 100px; min-width: 120px">
          <option value="latest">최신 순</option>
          <option value="likes">좋아요 순</option>
        </select>
      </div>
    </div>




    <div v-if="reviews.length === 0" class="text-muted">작성된 리뷰가 없습니다.</div>

    <!-- 리뷰 카드 목록 -->
    <div v-else class="row row-cols-1 g-4">
      <div class="col" v-for="review in paginatedReviews" :key="review.id">
        <div class="card p-3">
          <div class="d-flex gap-3">
            <!-- 포스터 + 별점 + 평점 -->
            <div class="d-flex flex-column align-items-center" style="width: 100px;">
              <img :src="getPosterUrl(review.movie?.poster_path)" class="rounded"
                style="width: 100px; height: 150px; object-fit: cover; object-position: left center; cursor: pointer;"
                alt="poster" @click.stop="goToMovieDetail(review.movie.id)" />
              <div class="mt-2 text-center">
                <i v-for="n in 5" :key="n" class="bi me-1" :class="getStarClass(review.rate, n)"></i>
                <div>{{ review.rate }} / 10</div>
              </div>
            </div>

            <div class="flex-grow-1 d-flex flex-column justify-content-between">
              <div>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="mb-0 fw-bold">{{ review.movie?.title }}</h5>
                  <div class="d-flex align-items-center">
                    <i class="bi bi-hand-thumbs-up me-1"></i> {{ review.like_user_count }} 개
                  </div>
                </div>

                <div class="d-flex align-items-center gap-2 mb-2">
                  <img :src="getProfileImage(review.user.profile_img)" class="rounded-circle" width="40" height="40"
                    alt="user" @click.stop="goToUserProfile(review.user.id)" style="cursor: pointer; border: 2px solid #ccc;" />
                  <span @click.stop="goToUserProfile(review.user.id)" style="cursor: pointer;">
                    {{ review.user.nickname || review.user.username }}
                  </span>
                </div>

                <div class="border rounded bg-light p-2 mb-2 small"
                  style="height: 120px; overflow-y: auto; white-space: pre-wrap;">
                  {{ review.content }}
                </div>
              </div>

              <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted me-3">작성일 : {{ review.created_at.slice(0, 10) }}</small>
                <button class="btn p-0" @click="openModal(review)">
                  <i class="bi bi-plus-lg"></i> 대 댓글 {{ review.comments.length }}개
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <nav v-if="totalReviewPages > 1" aria-label="Page navigation example" class="mt-5 d-flex justify-content-center">
      <ul class="pagination">
        <li :class="['page-item', { disabled: currentReviewPage === 1 }]" @click="goToReviewPage(1)">
          <button class="page-link" tabindex="-1">
            <i class="bi bi-chevron-double-left"></i>
          </button>
        </li>
        <li :class="['page-item', { disabled: currentReviewPage === 1 }]"
          @click="goToReviewPage(currentReviewPage - 1)">
          <button class="page-link" tabindex="-1">
            <i class="bi bi-chevron-left"></i>
          </button>
        </li>
        <li v-for="page in totalReviewPages" :key="page" :class="['page-item', { active: currentReviewPage === page }]"
          @click="goToReviewPage(page)">
          <button class="page-link">{{ page }}</button>
        </li>
        <li :class="['page-item', { disabled: currentReviewPage === totalReviewPages }]"
          @click="goToReviewPage(currentReviewPage + 1)">
          <button class="page-link">
            <i class="bi bi-chevron-right"></i>
          </button>
        </li>
        <li :class="['page-item', { disabled: currentReviewPage === totalReviewPages }]"
          @click="goToReviewPage(totalReviewPages)">
          <button class="page-link">
            <i class="bi bi-chevron-double-right"></i>
          </button>
        </li>
      </ul>
    </nav>
  </div>

  <!-- 리뷰 상세 모달 -->
  <teleport to="body">
    <div class="modal fade" id="reviewModal" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body" v-if="selectedReview">
            <div class="container-fluid mb-3">
              <div class="row align-items-start">
                <div class="col">
                  <div class="d-flex align-items-center mb-2">
                    <img :src="getProfileImage(selectedReview.user.profile_img)" class="rounded-circle me-2"
                      width="50" height="50" style="border: 2px solid #ccc;" />
                    <strong @click.stop="goToUserProfile(selectedReview.user.id)" style="cursor: pointer;">
                      {{ selectedReview.user.nickname || selectedReview.user.username }}
                    </strong>
                  </div>
                  <div class="border rounded p-2 bg-light small text-break"
                    style="height: 200px; overflow-y: auto; white-space: pre-wrap;">
                    {{ selectedReview.content }}
                  </div>
                </div>
                <div class="col-auto text-end">
                  <div class="mt-4 mb-2">
                    <img :src="getPosterUrl(selectedReview.movie?.poster_path)" class="rounded"
                      style="height: 220px; width: auto; object-fit: cover; cursor: pointer;"
                      @click.stop="goToMovieDetail(selectedReview.movie.id)" />
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
            <div v-if="paginatedComments.length === 0" class="text-muted mb-2">아직 댓글이 없습니다.</div>
            <ul class="list-group mb-3">
              <li v-for="comment in paginatedComments" :key="comment.id"
                class="list-group-item border-0 border-bottom px-1 py-2">
                <div class="d-flex justify-content-between align-items-start flex-wrap">
                  <div class="d-flex flex-column" style="min-width: 120px;">
                    <strong class="mb-1" @click="goToUserProfile(comment.user.id)" style="cursor: pointer;">
                      {{ comment.user.nickname || comment.user.username }}
                    </strong>
                    <div class="text-break">{{ comment.content }}</div>
                  </div>
                  <button v-if="comment.user.id === Number(authStore.userId)"
                    class="bg-transparent border-0 text-dark d-flex align-items-center gap-1 ms-auto mt-1"
                    @click="removeComment(selectedReview.movie.id, selectedReview.id, comment.id)">
                    <i class="bi bi-trash"></i> 삭제
                  </button>
                </div>
              </li>
            </ul>
            <div class="d-flex justify-content-center mb-3" v-if="totalPages > 1">
              <button class="btn btn-sm btn-outline-secondary me-2" :disabled="currentPage === 1"
                @click="currentPage--">
                이전
              </button>
              <button class="btn btn-sm btn-outline-secondary" :disabled="currentPage === totalPages"
                @click="currentPage++">
                다음
              </button>
            </div>
            <div class="input-group">
              <input v-model="newComment" class="form-control rounded-pill" placeholder="내용을 입력해 주세요" />
              <button class="btn text-dark border-0 d-flex align-items-center gap-1" @click="submitModalComment">
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
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as bootstrap from 'bootstrap'

import {
  fetchAllReviews,
  fetchComments,
  createComment,
  deleteComment
} from '@/apis/reviewApi'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const router = useRouter()
const reviewsPerPage = 5
const currentReviewPage = ref(1)
const selectedSort = ref('latest') // 최신순 기본

const reviews = ref([])
const selectedReview = ref(null)
const comments = ref([])
const newComment = ref('')
const currentPage = ref(1)
const commentsPerPage = 5

const totalReviewPages = computed(() => {
  return Math.ceil(reviews.value.length / reviewsPerPage)
})

const paginatedReviews = computed(() => {
  const start = (currentReviewPage.value - 1) * reviewsPerPage
  return reviews.value.slice(start, start + reviewsPerPage)
})

function goToReviewPage(page) {
  if (page < 1 || page > totalReviewPages.value) return
  currentReviewPage.value = page
}

// 별점 표시용 클래스 계산
const getStarClass = (rate, n) => {
  const score = rate / 2
  if (score >= n) return 'bi-star-fill text-dark'
  if (score >= n - 0.5) return 'bi-star-half text-dark'
  return 'bi-star text-dark'
}

// TMDB 포스터 URL
const getPosterUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : '/img/placeholder.png'
}

// 리뷰 정렬 적용 (프론트 정렬)
const sortReviews = () => {
  if (selectedSort.value === 'latest') {
    reviews.value.sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
  } else if (selectedSort.value === 'likes') {
    reviews.value.sort((a, b) => b.like_user_count - a.like_user_count)
  }
}

// 리뷰 불러오기
const fetchReviews = async () => {
  try {
    const data = await fetchAllReviews() // 백엔드 정렬 옵션 미지원 시 빈 인자로 호출
    for (const review of data) {
      review.comments = await fetchComments(review.movie.id, review.id)
    }
    reviews.value = data
    sortReviews()
  } catch (err) {
    console.error('리뷰 불러오기 실패:', err)
  }
}

// 정렬 변경 시 리뷰 재정렬 및 1페이지 초기화
watch(selectedSort, () => {
  currentReviewPage.value = 1
  sortReviews()
})

onMounted(fetchReviews)

// 모달 열기
const openModal = async (review) => {
  selectedReview.value = review
  comments.value = await fetchComments(review.movie.id, review.id)
  newComment.value = ''
  currentPage.value = 1

  const modal = new bootstrap.Modal(document.getElementById('reviewModal'))
  modal.show()
}

// 모달 댓글 작성
const submitModalComment = async () => {
  if (!newComment.value.trim()) return
  try {
    await createComment(selectedReview.value.movie.id, selectedReview.value.id, newComment.value.trim())
    comments.value = await fetchComments(selectedReview.value.movie.id, selectedReview.value.id)
    newComment.value = ''
    currentPage.value = 1
  } catch {
    alert('댓글 작성 실패')
  }
}

// 댓글 삭제
const removeComment = async (movieId, reviewId, commentId) => {
  try {
    await deleteComment(movieId, reviewId, commentId)
    const updated = await fetchComments(movieId, reviewId)
    if (selectedReview.value?.id === reviewId) {
      comments.value = updated
    }
    const review = reviews.value.find((r) => r.id === reviewId)
    if (review) review.comments = updated
  } catch {
    alert('댓글 삭제 실패')
  }
}

// 댓글 페이지네이션
const totalPages = computed(() => {
  return Math.ceil(comments.value.length / commentsPerPage)
})

const paginatedComments = computed(() => {
  const start = (currentPage.value - 1) * commentsPerPage
  return comments.value.slice(start, start + commentsPerPage)
})

// 유저 프로필 페이지 이동
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

// 영화 상세 페이지 이동
const goToMovieDetail = (movieId) => {
  // 모달 닫기
  const modalEl = document.getElementById('reviewModal')
  const modal = bootstrap.Modal.getInstance(modalEl)
  if (modal) modal.hide()
  router.push({ name: 'movie-detail', params: { id: movieId } })
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
.card {
  cursor: default;
}

.card-text {
  max-height: 3.6em;
  overflow: hidden;
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

/* 선택된 페이지: 부트스트랩 기본 파란색 강조 */
.pagination .page-item.active .page-link {
  color: #0d6efd !important;
  font-weight: 700;
  text-decoration: underline;
}
</style>