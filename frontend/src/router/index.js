import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import MovieListView from "@/views/MovieListView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import RecommendView from "@/views/RecommendView.vue";
import CharacterSelectView from "@/views/CharacterSelectView.vue";
import LoginView from "@/views/LoginView.vue";
import SignupView from "@/views/SignupView.vue";
import MypageView from "@/views/MypageView.vue";
import ProfileEditView from "@/views/ProfileEditView.vue";
import ProfileView from "@/views/ProfileView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/movies", name: "movie-list", component: MovieListView },
  { path: "/movies/:id", name: "movie-detail", component: MovieDetailView },
  { path: "/recommend", name: "recommend", component: RecommendView },
  { path: "/characters", name: "character-select", component: CharacterSelectView },
  { path: "/login", name: "login", component: LoginView },
  { path: "/signup", name: "signup", component: SignupView },
  { path: "/mypage", name: "mypage", component: MypageView },
  { path: "/mypage/edit", name: "profile-edit", component: ProfileEditView },
  { path: "/reviews", name: "ReviewList", component: () => import("@/views/ReviewListView.vue") },
  { path: "/users/:userId", name: "user-profile", component: ProfileView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 로그인 여부 확인 함수 (토큰 이름은 실제 프로젝트에 맞게 수정)
function isAuthenticated() {
  return !!localStorage.getItem('authToken');
}

// 네비게이션 가드: 추천/리뷰목록은 로그인 필요
router.beforeEach((to, from, next) => {
  const authRequiredRoutes = ['recommend', 'ReviewList'];
  if (authRequiredRoutes.includes(to.name) && !isAuthenticated()) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;