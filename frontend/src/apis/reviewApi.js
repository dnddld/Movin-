import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'
const REVIEW_URL = `${API_BASE}/reviews/`

// 공통 인증 헤더 생성
function authHeaders() {
  const token = localStorage.getItem('authToken')
  if (!token) throw new Error('로그인 토큰이 없습니다.')
  return {
    Authorization: `Token ${token}`
  }
}

// 리뷰 작성
export function createReview(movieId, reviewData) {
  return axios.post(`${API_BASE}/movies/${movieId}/articles/`, reviewData, {
    headers: authHeaders(),
    withCredentials: true
  })
}

// 특정 영화의 리뷰 목록 가져오기
export function fetchReviewsByMovie(movieId) {
  return axios.get(`${API_BASE}/movies/${movieId}/articles/`, {
    headers: authHeaders(),
    withCredentials: true
  }).then(res => res.data)
}

// 내 리뷰 목록 가져오기 (마이페이지용)
export function fetchMyReviews() {
  return axios.get(`${REVIEW_URL}my/`, {
    headers: authHeaders()
  }).then(res => res.data)
}

// 리뷰 삭제
export function deleteReviewById(movieId, articleId) {
  const token = localStorage.getItem('authToken')
  return axios.delete(`http://localhost:8000/api/movies/${movieId}/articles/${articleId}/`, {
    headers: {
      Authorization: `Token ${token}`
    },
    withCredentials: true
  })
}


// 리뷰 수정
export async function updateReview(movieId, reviewId, data) {
  const token = localStorage.getItem('authToken')
  return axios.put(`http://localhost:8000/api/movies/${movieId}/articles/${reviewId}/`, data, {
    headers: {
      Authorization: `Token ${token}`
    },
    withCredentials: true
  })
}

// 리뷰 좋아요 토글
export function toggleReviewLike(movieId, articleId) {
  return axios.post(`${API_BASE}/movies/${movieId}/articles/${articleId}/like/`, {}, {
    headers: authHeaders()
  })
}

// 전체 리뷰 목록 (모든 영화 통합)
export function fetchAllReviews(sort = 'latest') {
  return axios.get(`http://localhost:8000/api/movies/articles/?sort=${sort}`, {
    headers: authHeaders(),
    withCredentials: true
  }).then(res => res.data)
}

// 댓글 목록 가져오기
export function fetchComments(movieId, articleId) {
  return axios.get(`http://localhost:8000/api/movies/${movieId}/articles/${articleId}/comments/`, {
    headers: authHeaders(),
    withCredentials: true
  }).then(res => res.data)
}

// 댓글 작성
export async function createComment(movieId, articleId, content) {
  const token = localStorage.getItem('authToken')  // 대체
  return axios.post(
    `http://localhost:8000/api/movies/${movieId}/articles/${articleId}/comments/`,
    { content },
    {
      headers: { Authorization: `Token ${token}` },
      withCredentials: true,
    }
  )
}

// 댓글 삭제
export function deleteComment(movieId, articleId, commentId) {
  return axios.delete(`http://localhost:8000/api/movies/${movieId}/articles/${articleId}/comments/${commentId}/`, {
    headers: authHeaders(),
    withCredentials: true
  })
}
// 댓글 수정
export function updateComment(movieId, articleId, commentId, content) {
  return axios.put(`http://localhost:8000/api/movies/${movieId}/articles/${articleId}/comments/${commentId}/`, 
    { content }, {
    headers: authHeaders(),
    withCredentials: true
  })
}