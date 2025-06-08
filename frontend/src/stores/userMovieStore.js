import { defineStore } from 'pinia'

export const useUserMovieStore = defineStore('userMovie', {
  state: () => ({
    liked: [],
    bookmarked: []
  }),
  actions: {
    toggleLike(movie) {
      const idx = this.liked.findIndex((m) => m.id === movie.id)
      if (idx !== -1) {
        this.liked.splice(idx, 1)
      } else {
        this.liked.push(movie)
      }
    },
    toggleBookmark(movie) {
      const idx = this.bookmarked.findIndex((m) => m.id === movie.id)
      if (idx !== -1) {
        this.bookmarked.splice(idx, 1)
      } else {
        this.bookmarked.push(movie)
      }
    },
    isLiked(id) {
      return this.liked.some((m) => m.id === id)
    },
    isBookmarked(id) {
      return this.bookmarked.some((m) => m.id === id)
    }
  }
})
