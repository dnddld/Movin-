import axios from 'axios'

const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3'

const youtube = axios.create({
  baseURL: YOUTUBE_API_URL,
  params: {
    key: YOUTUBE_API_KEY,
    maxResults: 1,
    type: 'video',
    part: 'snippet'
  }
})

export async function searchTrailerOnYouTube(query) {
  try {
    const response = await youtube.get('/search', {
      params: {
        q: query
      }
    })
    const item = response.data.items[0]
    return item ? item.id.videoId : null
  } catch (err) {
    console.error('유튜브 검색 오류:', err)
    return null
  }
}
