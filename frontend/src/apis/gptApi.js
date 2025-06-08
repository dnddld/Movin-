import axios from 'axios'

export async function fetchCharacterRecommendation(characterInfo) {
  return axios.post('http://localhost:8000/recommend/character/', {
    character_info: characterInfo
  })
}




