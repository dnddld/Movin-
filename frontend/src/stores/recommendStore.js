import { defineStore } from 'pinia'

export const useRecommendStore = defineStore('recommend', {
  state: () => ({
    selectedCharacter: null,
    recommendedMovies: []
  }),
  actions: {
    setCharacter(character) {
      this.selectedCharacter = character
    },
    setRecommendations(movies) {
      this.recommendedMovies = movies
    }
  }
})
