<template>
  <div class="min-h-screen bg-[#F6F5F2] pb-10 text-[#1C1D21]">
    <!-- HEADER -->
    <header class="flex items-center gap-3 px-5 pb-4 pt-6">
      <button
        @click="router.back()"
        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-[#E3E1DC] bg-white active:scale-95"
        aria-label="Назад"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m15 18-6-6 6-6"/>
        </svg>
      </button>
      <div>
        <h1 class="font-display text-[19px] font-bold leading-tight">Частые вопросы</h1>
        <p class="font-body text-[12px] text-[#9AA0AB]">{{ faqs.length }} вопросов о натяжных потолках</p>
      </div>
    </header>

    <!-- FAQ LIST -->
    <section class="flex flex-col gap-2.5 px-5">
      <article
        v-for="(item, index) in faqs"
        :key="item.id"
        class="overflow-hidden rounded-2xl border border-[#E3E1DC] bg-white"
      >
        <button
          @click="toggle(index)"
          class="flex w-full items-center gap-3 px-4 py-3.5 text-left"
        >
          <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#1C1D21] text-[#FFC93C]">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9.1 9a3 3 0 0 1 5.82 1c0 2-3 3-3 3"/>
              <path d="M12 17h.01"/>
            </svg>
          </span>
          <span class="flex-1 font-body text-[14.5px] font-medium leading-snug">
            {{ item.question }}
          </span>
          <svg
            width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round"
            class="shrink-0 text-[#C7CBD1] transition-transform duration-200"
            :class="{ 'rotate-180': openIndex === index }"
          >
            <path d="m6 9 6 6 6-6"/>
          </svg>
        </button>

        <div
          class="grid transition-all duration-200 ease-out"
          :style="{ gridTemplateRows: openIndex === index ? '1fr' : '0fr' }"
        >
          <div class="overflow-hidden">
            <p class="border-t border-[#EEEDE9] px-4 py-3.5 pl-[52px] font-body text-[13.5px] leading-relaxed text-[#6B7078]">
              {{ item.answer }}
            </p>
          </div>
        </div>
      </article>
    </section>

    <!-- CONTACT CTA -->
    <section class="mx-5 mt-6 rounded-2xl border border-[#E3E1DC] bg-white px-4 py-4 text-center">
      <p class="font-body text-[13.5px] text-[#6B7078]">Не нашли ответ на свой вопрос?</p>
      <button
        @click="router.push('/form?type=consultation')"
        class="mt-3 w-full rounded-xl bg-[#1C1D21] px-4 py-3 font-body text-[14px] font-medium text-white transition-transform active:scale-[0.98]"
      >
        Получить консультацию
      </button>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const openIndex = ref(0);


const toggle = (index) => {
  openIndex.value = openIndex.value === index ? -1 : index;
};

// пример данных — замените на реальные вопросы/ответы
const faqs = [
  {
    id: 1,
    question: 'Сколько времени занимает установка натяжного потолка?',
    answer: 'В среднем монтаж одной комнаты занимает от 3 до 5 часов. Точные сроки зависят от площади, формы потолка и количества источников света.'
  },
  {
    id: 2,
    question: 'Нужно ли освобождать комнату от мебели?',
    answer: 'Крупную мебель лучше сдвинуть к центру комнаты и накрыть плёнкой — мы привозим её с собой. Полностью выносить мебель не обязательно.'
  },
  {
    id: 3,
    question: 'Остаётся ли запах после монтажа?',
    answer: 'Лёгкий запах возможен в первые сутки при использовании глянцевого ПВХ-полотна, он выветривается сам. Тканевые потолки запаха не имеют.'
  },
  {
    id: 4,
    question: 'Что делать, если соседи сверху затопили?',
    answer: 'Позвоните нам — мы приезжаем в день обращения, аккуратно сливаем воду через клапан и возвращаем потолку исходный вид без замены полотна.'
  },
  {
    id: 5,
    question: 'Какая гарантия на потолок?',
    answer: 'Мы даём гарантию 15 лет на полотно и монтажные работы. Гарантийный талон выдаётся сразу после установки.'
  }
];
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

.font-display { font-family: 'Unbounded', sans-serif; }
.font-body { font-family: 'Inter', sans-serif; }
</style>