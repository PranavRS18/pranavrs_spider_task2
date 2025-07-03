<script setup>
import { ref, defineEmits, defineProps } from "vue";
import axios from "axios";

import { checkIfCommands, isValidScholarlyUrl } from "../commands.js";

const emit = defineEmits(['answer']);
const props = defineProps({
  isTyping: {
    type: Boolean,
    required: true,
  }
})
const isAnalysis = ref(false);
const isDisabled = ref(false);

const question = ref("");

function askQuestion() {
  if (isDisabled.value) return;
  isDisabled.value = true;

  const cleanedQuestion = question.value.trim();
  if (!props.isTyping) {
    const fromCommands = checkIfCommands(cleanedQuestion);
    if (fromCommands) {
      emit('answer', cleanedQuestion, fromCommands);
      isDisabled.value = false;
      question.value = "";
    }
    else if (!isAnalysis.value && isValidScholarlyUrl(cleanedQuestion)) {
      emit("answer", cleanedQuestion, "Analyzing your research paper. Please hold on a moment...");
      question.value = "";
      isAnalysis.value = true;
      setTimeout(() => {
        axios.post(`${import.meta.env.VITE_API_SERVER}/api/v1/analysis`, {
          "question": cleanedQuestion,
        }).then((response) => {
          if (response?.data?.success) emit("answer", `Analysis complete for (${cleanedQuestion})`, `Ready to answer your questions!`);
          else  emit("answer", cleanedQuestion, "Either this paper has already been analyzed or the provided link isn't a valid PDF. Please ensure you're using a direct scholarly PDF link from a supported domain.");
          isAnalysis.value = false;
          question.value = "";
          isDisabled.value = false;
        }).catch((error) => {
          console.log(error);
          emit("answer", cleanedQuestion, "I am facing a temporary issue on my end. Please try again shortly.\n");
          isAnalysis.value = false;
          isDisabled.value = false;
        })
      }, 2000);
    } else {
      axios.post(`${import.meta.env.VITE_API_SERVER}/api/v1/ask`, {
        "question": cleanedQuestion,
      }).then((response) => {
        emit("answer", cleanedQuestion, response?.data?.answer);
        question.value = "";
        isDisabled.value = false;
      }).catch((error) => {
        console.log(error);
        emit("answer", cleanedQuestion, "I am facing a temporary issue on my end. Please try again shortly.\n");
        isDisabled.value = false;
      })
    }
  }
}
</script>

<template>
  <div class = "ask-question">
    <div class = "search-bar">
      <input class = "question" v-model = "question" type = "text" @keydown.enter = "askQuestion" placeholder = "Ask a question or provide a valid paper URL from supported domains. Type ‘domains’ to see the list." spellcheck = "false" :disabled = "isDisabled"/>
      <button class = "normal" @click = "askQuestion" :disabled = "isDisabled || !question.length">ASK</button>
    </div>
  </div>
</template>

<style scoped>

.ask-question {
  width: 100%;
  height: 100%;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;
}

.search-bar {
  display: flex;
  flex-direction: row;
  padding: 1rem;
  align-items: center;
  width: 100%;
  height: auto;
  border-radius: 1rem;
}

.search-bar .question {
  width: 95%;
  height: 3.5rem;
  font-size: 1.2rem;
  font-family: "Spectral", serif;
  border: none;
  background-color: var(--fg-color);
  color: rgb(var(--font-color));
}

.search-bar .question:focus {
  outline: none;
}

.search-bar .question::placeholder {
  color: rgba(var(--font-color), 0.6);
}

.search-bar .question:disabled {
  caret-color: transparent;
}

button.normal {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  font-size: 1rem;
  margin: 0 0.5rem;
  font-family: 'Poppins', sans-serif;
  background-color: white;
  box-shadow: 0.01rem 0.01rem 0.2rem 0.1rem rgba(255, 255, 255, 0.1);
  border: none;
  transition: background-color 0.3s;
}

button.normal:not(:disabled):hover {
  background-color: var(--accent-color);
  color: rgb(var(--font-color));
  cursor: pointer;
}

button:focus {
  outline: none;
}

</style>