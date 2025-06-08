<template>
  <div class="container my-5">
    <!-- 예고편 영상 -->
    <div class="ratio ratio-16x9 mb-4" v-if="trailerKey">
      <iframe :src="`https://www.youtube.com/embed/${trailerKey}`" frameborder="0" allowfullscreen></iframe>
    </div>

    <!-- 영화 정보 -->
    <div v-if="movie">
      <div class="row mb-4">
        <div class="col-md-3">
          <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" class="img-fluid rounded shadow" />
        </div>
        <div class="col-md-9">
          <h2 class="fw-bold">{{ movie.title }}</h2>
          <div class="d-flex align-items-center gap-3 mb-3">
            <span class="text-muted">개봉 일자 : {{ movie.release_date }}</span>
            <span>
              <i class="bi bi-star-fill text-dark"></i> {{ movie.vote_average.toFixed(1) }}
            </span>
            <div class="d-flex gap-2 ms-2">
              <button class="bg-transparent border-0 p-0" @click="authStore.isLoggedIn ? handleLike() : goLogin()"
                aria-label="좋아요">
                <i :class="['bi fs-4', liked ? 'bi-heart-fill text-danger' : 'bi-heart text-danger']"></i>
              </button>
              <button class="bg-transparent border-0 p-0" @click="authStore.isLoggedIn ? handleBookmark() : goLogin()"
                aria-label="북마크">
                <i :class="['bi fs-4', bookmarked ? 'bi-bookmark-fill text-primary' : 'bi-bookmark text-primary']"></i>
              </button>
            </div>
          </div>
          <p>{{ movie.overview }}</p>
        </div>
      </div>
    </div>

    <!-- 리뷰 목록 -->
    <div class="mt-5">
      <h4 class="mb-3">코멘트 <i class="bi bi-chat-left"></i></h4>

      <div v-for="review in reviews" :key="review.id" class="card mb-3" @click="handleCardClick(review)">
        <div class="card-body" style="cursor: pointer;">
          <!-- 닉네임 & 별점 & 좋아요 -->
          <div class="d-flex justify-content-between align-items-center mb-2">
            <div class="d-flex align-items-center gap-2">
              <img :src="getProfileImage(review.user.profile_img)" alt="profile" class="rounded-circle"
                style="width: 50px; height: 50px; object-fit: cover; border: 2px solid #ccc;" />
              <strong>{{ review.user.nickname || review.user.email }}</strong>
            </div>
            <div class="d-flex align-items-center gap-3 text-muted">
              <span><i class="bi bi-star-fill"></i> {{ review.rate }}</span>
              <button class="btn btn-sm p-0 d-flex align-items-center gap-1 text-muted border-0 bg-transparent"
                @click.stop="handleReviewLike(review)">
                <i class="bi bi-hand-thumbs-up"></i>
                <!-- <span v-if="review.like_user_count > 0" class="ms-1">{{ review.like_user_count }}</span> -->
                <span>{{ review.like_user_count }}</span>
              </button>
              
            </div>
          </div>

          <!-- 수정 모드 -->
          <div v-if="editingReviewId === review.id">
            <div class="star-rating mb-2" @mouseleave="resetEditedHover">
              <template v-for="starIndex in 5" :key="starIndex">
                <div class="fa-container" @mousemove="onEditedHover($event, starIndex)"
                  @click="onEditedClick($event, starIndex)">
                  <i :class="getEditedStarClass(starIndex)"></i>
                </div>
              </template>
            </div>
            <textarea v-model="editedContent" class="form-control mb-2" rows="3"></textarea>
            <div class="d-flex gap-2 justify-content-end">
              <button class="bg-transparent border-0 text-muted d-flex align-items-center gap-1"
                style="font-size: 0.85rem" @click.stop="submitEdit(review.id)">
                <i class="bi bi-check2-square"></i> 저장
              </button>
              <span class="divider"></span>
              <button class="bg-transparent border-0 text-muted d-flex align-items-center gap-1"
                style="font-size: 0.85rem" @click.stop="cancelEdit">
                <i class="bi bi-x"></i> 취소
              </button>
            </div>
          </div>

          <!-- 본문 -->
          <p class="mb-2" v-else>{{ review.content }}</p>

          <!-- 작성일자 + 수정/삭제 -->
          <div v-if="editingReviewId !== review.id" class="d-flex justify-content-between align-items-center">
            <small class="text-muted">{{ review.created_at.slice(0, 10) }}</small>
            <div v-if="review.user.id === Number(authStore.userId)" class="d-flex gap-2">
              <button class="bg-transparent border-0 text-muted d-flex align-items-center gap-1"
                style="font-size: 0.85rem" @click.stop="deleteReview(review.id)">
                <i class="bi bi-trash"></i> 삭제
              </button>
              <span class="divider"></span>
              <button class="bg-transparent border-0 text-muted d-flex align-items-center gap-1"
                style="font-size: 0.85rem" @click.stop="startEditing(review)">
                <i class="bi bi-pencil-fill"></i> 수정
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- 리뷰 작성 -->
    <div class="mt-5">
      <h4 class="mb-3">코멘트 작성 <i class="bi bi-chat-left-dots"></i></h4>
      <div v-if="authStore.isLoggedIn">
        <form @submit.prevent="submitReview">
          <div class="mb-3">
            <div class="star-rating" @mouseleave="resetHover">
              <template v-for="starIndex in 5" :key="starIndex">
                <div class="fa-container" @mousemove="onHover($event, starIndex)" @click="onClick($event, starIndex)">
                  <i :class="getStarClass(starIndex)"></i>
                </div>
              </template>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">내용</label>
            <textarea v-model="newReview.content" rows="3" class="form-control"
              placeholder="이 작품에 대한 생각을 자유롭게 표현해 주세요"></textarea>
          </div>
          <div class="text-end">
            <button class="btn btn-sm border-0" :class="{
              'text-dark fw-semibold': newReview.rating && newReview.content,
              'text-secondary fw-normal': !newReview.rating || !newReview.content
            }" :disabled="!newReview.rating || !newReview.content">
              <i class="bi bi-check2-square"></i> 저장
            </button>
          </div>
        </form>
      </div>
      <div v-else class="alert alert-warning">
        리뷰를 작성하려면 <router-link to="/login" class="alert-link">로그인</router-link>해 주세요.
      </div>
    </div>
  </div>

  <!-- 리뷰 상세 모달 -->
  <teleport to="body">
    <div class="modal fade" id="reviewModal" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body" v-if="selectedReview">

            <!-- 상단 레이아웃 -->
            <div class="container-fluid mb-3">
              <div class="row align-items-start">
                <!-- 좌측: 프로필 + 닉네임 + 리뷰 내용 -->
                <div class="col">
                  <div class="d-flex align-items-center mb-2">
                    <img :src="getProfileImage(selectedReview.user.profile_img)" class="rounded-circle me-2" width="50"
                      height="50" />
                    <strong @click="goToUserProfile(selectedReview.user.id)" style="cursor: pointer;">{{
                      selectedReview.user.nickname ||
                      selectedReview.user.username }}</strong>
                  </div>

                  <!-- 본문 박스 -->
                  <div class="border rounded p-2 bg-light small text-break"
                    style="height: 200px; overflow-y: auto; white-space: pre-wrap;">
                    {{ selectedReview.content }}
                  </div>

                </div>

                <!-- 우측: 작성일 + 좋아요 + 포스터 -->
                <div class="col-auto text-end">
                  <!-- 영화 포스터 -->
                  <div class="mt-4 mb-2"><img
                      :src="'https://image.tmdb.org/t/p/w500' + selectedReview.movie.poster_path" class="rounded"
                      style="height: 220px; width: auto; object-fit: cover;" /></div>
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
                  <!-- 좌측: 닉네임 위, 댓글 아래 -->
                  <div class="d-flex flex-column" style="min-width: 120px;">
                    <strong class="mb-1" @click="goToUserProfile(comment.user.id)" style="cursor: pointer;">{{
                      comment.user.nickname ||
                      comment.user.username }}</strong>
                    <div class="text-break">{{ comment.content }}</div>
                  </div>

                  <!-- 삭제 버튼 우측 고정 -->
                  <button v-if="comment.user.id === Number(authStore.userId)"
                    class="bg-transparent border-0 text-dark d-flex align-items-center gap-1 ms-auto mt-1"
                    @click="removeComment(comment.id)">
                    <i class="bi bi-trash"></i> 삭제
                  </button>
                </div>
              </li>
            </ul>

            <!-- 댓글 작성 -->
            <div class="input-group">
              <input v-model="newComment" class="form-control rounded-pill" placeholder="내용을 입력해 주세요" />
              <button class="btn text-dark border-0 d-flex align-items-center gap-1" @click="submitComment">
                <i class="bi bi-chat"></i> 작성
              </button>
            </div>
          </div>

          <!-- 닫기 버튼 -->
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
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/authStore"
import { fetchMovieVideos } from "@/apis/tmdbApi"
import { searchTrailerOnYouTube } from "@/apis/youtubeApi"
import { toggleLike, toggleBookmark, fetchMovieDetail } from "@/apis/movieApi"
import { createReview, fetchReviewsByMovie, toggleReviewLike, updateReview, deleteReviewById, fetchComments, createComment, deleteComment } from '@/apis/reviewApi'
import * as bootstrap from 'bootstrap'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const liked = ref(false)
const bookmarked = ref(false)
const movie = ref(null)
const trailerKey = ref("")
const reviews = ref([])

const goLogin = () => {
  router.push('/login')
}

const newReview = ref({ rating: 0, content: "" })
const hoverRating = ref(0)

const editingReviewId = ref(null)
const editedRating = ref(0)
const editedContent = ref("")
const editedHoverRating = ref(0)

const comments = ref([])
const newComment = ref('')

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

function startEditing(review) {
  editingReviewId.value = review.id
  editedRating.value = review.rating
  editedContent.value = review.content
}

function cancelEdit() {
  editingReviewId.value = null
  editedRating.value = 0
  editedContent.value = ""
  editedHoverRating.value = 0
}

async function submitEdit(id) {
  try {
    const payload = {
      title: `${authStore.username}님의 수정된 리뷰`,
      content: editedContent.value,
      rate: editedRating.value,
    }

    await updateReview(movie.value.id, id, payload)
    await loadReviews()  // 저장 후 목록 갱신

    cancelEdit()
  } catch (err) {
    console.error('리뷰 수정 실패:', err)
    alert('리뷰 수정에 실패했습니다.')
  }
}

async function deleteReview(articleId) {
  if (!confirm("정말 삭제하시겠습니까?")) return

  try {
    await deleteReviewById(movie.value.id, articleId)
    await loadReviews()  // 백엔드에서 다시 가져오기
  } catch (err) {
    console.error("삭제 실패:", err)
    alert("삭제에 실패했습니다.")
  }
}



async function submitReview() {
  if (!newReview.value.rating || !newReview.value.content) return

  try {
    const payload = {
      title: `${authStore.username}님의 리뷰`,  // or 빈 문자열
      content: newReview.value.content,
      rate: newReview.value.rating
    }

    const res = await createReview(movie.value.id, payload)
    // reviews.value.unshift(res.data)

    // await createReview(movie.value.id, payload)
    await loadReviews()


    newReview.value.rating = 0
    newReview.value.content = ""
    hoverRating.value = 0

  } catch (err) {
    console.error("리뷰 작성 실패:", err)
    alert("리뷰 작성에 실패했습니다.")
  }
}

async function loadReviews() {
  reviews.value = await fetchReviewsByMovie(movie.value.id)
}

onMounted(async () => {
  const movieId = route.params.id
  movie.value = await fetchMovieDetail(movieId)

  if (authStore.isLoggedIn && movie.value) {
    const userId = Number(authStore.userId)
    liked.value = movie.value.like_users?.some(user => user.id === userId)
    bookmarked.value = movie.value.bookmark_users?.some(user => user.id === userId)
  }

  const videos = await fetchMovieVideos(movieId)
  const trailer = videos.find((v) => v.site === "YouTube" && v.type === "Trailer")
  if (trailer) {
    trailerKey.value = trailer.key
  } else {
    const fallbackKey = await searchTrailerOnYouTube(`${movie.value.title} official trailer`)
    if (fallbackKey) trailerKey.value = fallbackKey
  }
  await loadReviews()
  // reviews.value = await fetchReviewsByMovie(movieId)
})

async function handleLike() {
  try {
    await toggleLike(movie.value.id)
    liked.value = !liked.value
  } catch (err) {
    alert("좋아요 요청 실패")
  }
}

async function handleBookmark() {
  try {
    await toggleBookmark(movie.value.id)
    bookmarked.value = !bookmarked.value
  } catch (err) {
    alert("북마크 요청 실패")
  }
}

function getStarClass(starIndex) {
  const rating = hoverRating.value || newReview.value.rating
  const score = starIndex * 2
  if (rating >= score) return "fa-solid fa-star text-secondary"
  if (rating === score - 1) return "fa-solid fa-star-half-stroke text-secondary"
  return "fa-regular fa-star text-secondary"
}

function onHover(event, starIndex) {
  const { offsetX, currentTarget } = event
  const width = currentTarget.offsetWidth
  hoverRating.value = offsetX < width / 2 ? starIndex * 2 - 1 : starIndex * 2
}

function onClick(event, starIndex) {
  const { offsetX, currentTarget } = event
  const width = currentTarget.offsetWidth
  newReview.value.rating = offsetX < width / 2 ? starIndex * 2 - 1 : starIndex * 2
}

function resetHover() {
  hoverRating.value = 0
}

function getEditedStarClass(starIndex) {
  const rating = editedHoverRating.value || editedRating.value
  const score = starIndex * 2
  if (rating >= score) return "fa-solid fa-star text-secondary"
  if (rating === score - 1) return "fa-solid fa-star-half-stroke text-secondary"
  return "fa-regular fa-star text-secondary"
}

function onEditedHover(event, starIndex) {
  const { offsetX, currentTarget } = event
  const width = currentTarget.offsetWidth
  editedHoverRating.value = offsetX < width / 2 ? starIndex * 2 - 1 : starIndex * 2
}

function onEditedClick(event, starIndex) {
  const { offsetX, currentTarget } = event
  const width = currentTarget.offsetWidth
  editedRating.value = offsetX < width / 2 ? starIndex * 2 - 1 : starIndex * 2
}

function resetEditedHover() {
  editedHoverRating.value = 0
}

async function handleReviewLike(review) {
  try {
    await toggleReviewLike(movie.value.id, review.id)
    await loadReviews()
  } catch (err) {
    alert("리뷰 좋아요 실패")
  }
}

const selectedReview = ref(null)

const openReviewModal = (review) => {
  selectedReview.value = review
  const modal = new bootstrap.Modal(document.getElementById('reviewModal'))
  modal.show()
  loadComments()
}

function handleCardClick(review) {
  if (editingReviewId.value === review.id) return
  openReviewModal(review)
}


// 댓글 관련 API 호출 함수들
async function loadComments() {
  try {
    const res = await fetchComments(movie.value.id, selectedReview.value.id)
    comments.value = res
  } catch (err) {
    console.error('댓글 로딩 실패', err)
  }
}

async function submitComment() {
  if (!newComment.value.trim()) return
  try {
    await createComment(movie.value.id, selectedReview.value.id, newComment.value.trim())
    newComment.value = ''
    await loadComments()
  } catch (err) {
    alert('댓글 작성 실패')
  }
}

async function removeComment(commentId) {
  try {
    await deleteComment(movie.value.id, selectedReview.value.id, commentId)
    await loadComments()
  } catch (err) {
    alert('댓글 삭제 실패')
  }
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
.star-rating {
  display: flex;
  gap: 6px;
  cursor: pointer;
}

.fa-container {
  width: 2rem;
  text-align: center;
}

.fa-container i {
  font-size: 2rem;
  transition: color 0.2s;
}

.divider {
  width: 1px;
  background-color: #ddd;
  margin: 0 4px;
}
</style>