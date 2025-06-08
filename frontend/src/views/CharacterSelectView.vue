<template>
  <div class="container my-5">
    <h2 class="mb-4 fw-bold text-dark">
      <i :class="[randomPhrase.icon, 'text-primary', 'me-2']"></i>
      <span v-html="highlightedText"></span>
    </h2>


    <div class="row row-cols-2 row-cols-sm-3 row-cols-md-6 row-cols-xl-9 g-4 mt-1">
      <div
        v-for="character in characters"
        :key="character.name"
        class="col"
      >
        <div
          class="card border-0 shadow-sm text-center p-0"
          :class="{
            'border border-primary shadow': characterStore.selectedCharacter?.name === character.name,
            'hover-shadow': characterStore.selectedCharacter?.name !== character.name
          }"
          style="cursor: pointer; height: 270px; overflow: visible;"
          @click="selectCharacterAndGo(character)"
        >
          <img
            :src="character.image"
            :alt="character.name"
            class="rounded"
            style="width: 100%; height: 100%; object-fit: cover; border-radius: 6px;"
          />
        </div>
        <div class="text-center mt-2">
          <div class=" fw-semibold text-dark">{{ character.movie }}</div>
          <div class=" small">{{ character.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { characters } from '@/assets/data/characters'
import { useCharacterStore } from '@/stores/characterStore'

const characterStore = useCharacterStore()
const router = useRouter()

const phrases = [
  {
    text: "내가 선택한 주인공과 함께 영화 속' 세계를 탐험해보세요.",
    icon: 'bi bi-person-walking'
  },
  {
    text: "당신만의 친구와 함께 영화 속' 여정을 떠나보세요.",
    icon: 'bi bi-person-raised-hand'
  },
  {
    text: "마음에 드는 인물과 함께 스크린 안' 으로 모험을 떠나보세요.",
    icon: 'bi bi-person-arms-up'
  }
]

const randomPhrase = ref({ text: '', icon: '' })
const highlightedText = ref('')

onMounted(() => {
  const index = Math.floor(Math.random() * phrases.length)
  randomPhrase.value = phrases[index]
  highlightedText.value = randomPhrase.value.text.replace(
    /'/g,
    `<span class="text-primary">'</span>`
  )
})

function selectCharacterAndGo(character) {
  characterStore.setCharacter(character.name)
  router.push('/recommend')
}
</script>

<style scoped>
.hover-shadow {
  transition: all 0.2s ease-in-out;
}

.hover-shadow:hover {
  transform: scale(1.03) translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}


.border-primary {
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
</style>