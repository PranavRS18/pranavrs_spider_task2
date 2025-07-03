<script setup>
import { ref, watch, nextTick } from "vue";
import AskQuestion from "@/components/AskQuestion.vue";

const answer = ref("");
const currentAnswer = ref("");
const index = ref(0);
const isTyping = ref(false);
function giveAnswer(getQuestion, getAnswer) {
  answer.value = getAnswer;
  currentAnswer.value += `\n\n<div style="display: inline-block; background-color: #414141; padding: 0.5rem 2rem; border-radius: 0.4rem; font-size: 1.2rem; font-weight: bold; margin: 1rem 1rem 0 auto;">${getQuestion.value || getQuestion}</div>\n`
  index.value = 0;
  isTyping.value = true;
  const typingInterval = setInterval(() => {
    if (index.value >= answer.value.length) {
      clearInterval(typingInterval);
      isTyping.value = false
    } else {
      currentAnswer.value += answer.value[index.value];
      index.value++;
    }
  }, 15)
}

const answerBox = ref(null);
watch(currentAnswer, () => {
  nextTick(() => {
    answerBox.value.scrollTo({
      top: answerBox.value.scrollHeight,
      behavior: "smooth",
    })
  });
});

</script>

<template>
  <div class = "window">
    <h1>AskMyPaper</h1>
    <h2 v-if = "!answer.length">Because your PDF won't answer itself</h2>
    <div class = "box output" :class = "{'query-mode' : answer.length}">
      <p v-html = "currentAnswer" ref = "answerBox"></p>
    </div>
    <div class = "box input">
      <AskQuestion @answer = "giveAnswer" :isTyping = "isTyping" />
    </div>
  </div>
</template>

<style scoped>

.window {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: rgb(var(--font-color));
}

.box {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 60%;
  height: auto;
  background-color: var(--fg-color);
  border-radius: 1rem;
}

.input {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.output {
  height: 0;
  font-size: 1.2rem;
  transition: height 1s;
}

.query-mode {
  height: 65%;
}

.output p {
  display: flex;
  flex-direction: column;
  margin: 1rem;
  width: 98%;
  text-wrap: wrap;
  white-space: pre-wrap;
  overflow: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.output p::-webkit-scrollbar {
  display: none;
}

h1, h2, h3 {
  margin: 0;
  width: 100%;
  text-align: center;
}

h1 {
  font-size: 3rem;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 3rem;
}

h3 {
  font-size: 2rem;
}

</style>
