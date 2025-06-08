import { defineStore } from 'pinia'
import { fetchCharacterRecommendation } from '@/apis/gptApi'
import { fetchMovieByTitle } from '@/apis/tmdbApi'
import { characters } from '@/assets/data/characters'

export const useCharacterStore = defineStore('character', {
  state: () => ({
    selectedCharacter: null, // 전체 캐릭터 객체 저장
    candidateMovies: [],
    recommendation: null,
    loading: false,
  }),

  actions: {
    setCharacter(name) {
      const found = characters.find(c => c.name === name)
      if (!found) {
        console.warn(`캐릭터 '${name}'를 찾을 수 없습니다.`)
        this.selectedCharacter = null
      } else {
        this.selectedCharacter = found
      }
      this.recommendation = null
    },

    setMovies(movieList) {
      this.candidateMovies = movieList
    },

    async getRecommendation() {
      if (!this.selectedCharacter) {
        console.error('추천 요청 실패: 선택된 캐릭터가 없습니다')
        return
      }

      this.loading = true
      this.recommendation = null

      try {
        const characterInfo = `${this.selectedCharacter.movie} - ${this.selectedCharacter.name}`
        const res = await fetchCharacterRecommendation(characterInfo)

        const enrichMovies = async (list) => {
          const results = await Promise.all(
            list.map(async (movie) => {
              const extra = await fetchMovieByTitle(movie.title)
              if (!extra || !extra.poster) return null  // 포스터 없으면 제외
              return {
                ...movie,
                poster: extra.poster,
                id: extra.id
              }
            })
          )
          return results.filter(Boolean)  // null 제거
        }

        const top = await enrichMovies(res.data.top)
        const bottom = await enrichMovies(res.data.bottom)

        this.recommendation = { top, bottom }

      } catch (e) {
        console.error('추천 요청 실패:', e)
        this.recommendation = null
      } finally {
        this.loading = false
      }
    }
  }
})
