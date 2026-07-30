<template>
  <div class="min-h-screen bg-[#F6F5F2] text-[#1C1D21] pb-10">
    <!-- decorative wire, echoes the logo's cable motif -->
    <svg class="pointer-events-none absolute right-0 top-24 h-56 w-40 opacity-[0.06]" viewBox="0 0 160 220" fill="none">
      <path d="M140 10 V150 H20" stroke="#1C1D21" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="140" cy="10" r="12" fill="#1C1D21"/>
      <circle cx="20" cy="150" r="12" fill="#1C1D21"/>
    </svg>

    <!-- HERO -->
    <header class="relative px-6 pt-8 pb-6 text-center">
      <!-- live status pill, nods to the glowing dots in the logo -->
      <div class="mx-auto mb-6 inline-flex items-center gap-2 rounded-full border border-[#E3E1DC] bg-white/70 px-3 py-1.5 backdrop-blur-sm">
        <span class="relative flex h-2 w-2">
          <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#FFC93C] opacity-75"></span>
          <span class="relative inline-flex h-2 w-2 rounded-full bg-[#E8A800] shadow-[0_0_6px_2px_rgba(255,201,60,0.7)]"></span>
        </span>
        <span class="font-body text-[11px] font-medium uppercase tracking-wide text-[#6B7078]">Принимаем заявки сегодня</span>
      </div>

      <!-- logo panel -->
      <div class="relative mx-auto mb-5 h-24 w-24">
        <div class="absolute inset-0 rounded-[22px] bg-gradient-to-br from-[#FFC93C]/25 to-transparent blur-xl"></div>
        <div class="relative flex h-24 w-24 items-center justify-center rounded-[22px] border border-[#E3E1DC] bg-white shadow-[0_8px_24px_-6px_rgba(28,29,33,0.18)]">
          <img src="../../public/logo.jpg" alt="Потолок Деко" class="h-14 w-14 object-contain">
        </div>
      </div>

      <h1 class="font-display text-[26px] font-bold leading-tight tracking-tight">
        Потолок Деко
      </h1>
      <p class="mt-1 font-body text-[12px] font-semibold uppercase tracking-[0.14em] text-[#C98A00]">
        Натяжные потолки
      </p>
      <p class="mx-auto mt-3 max-w-[280px] font-body text-[14px] leading-relaxed text-[#6B7078]">
        Современные натяжные потолки. Быстрый монтаж, европейские материалы, гарантия 15 лет.
      </p>
    </header>

    <!-- SERVICES -->
    <section class="px-5">
      <h2 class="mb-3 px-1 font-body text-[13px] font-semibold text-[#9AA0AB]">
        Что вам нужно?
      </h2>

      <div class="flex flex-col gap-2.5">
        <button
          v-for="item in services"
          :key="item.type"
          @click="router.push(`/form?type=${item.type}`)"
          class="group flex items-center gap-4 rounded-2xl border border-[#E3E1DC] bg-white px-4 py-3.5 text-left shadow-[0_1px_2px_rgba(28,29,33,0.04)] transition-all active:scale-[0.98] active:shadow-none"
        >
          <span
            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#1C1D21] text-[#FFC93C] transition-shadow group-active:shadow-[0_0_16px_2px_rgba(255,201,60,0.55)]"
            v-html="item.icon"
          ></span>
          <span class="flex-1 font-body text-[15px] font-medium text-[#1C1D21]">
            {{ item.title }}
          </span>
          <svg class="h-4 w-4 shrink-0 text-[#C7CBD1] transition-transform group-active:translate-x-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m9 18 6-6-6-6"/>
          </svg>
        </button>
      </div>
    </section>

    <!-- SECONDARY LINKS -->
    <section class="mt-7 flex flex-col gap-2.5 px-5">
      <button
        @click="router.push('/reviews')"
        class="rounded-2xl border border-[#1C1D21] bg-[#1C1D21] px-4 py-3.5 text-center font-body text-[14px] font-medium text-white transition-transform active:scale-[0.98]"
      >
        Отзывы клиентов
      </button>
      <button
        @click="router.push('/faq')"
        class="rounded-2xl border border-[#E3E1DC] bg-transparent px-4 py-3.5 text-center font-body text-[14px] font-medium text-[#6B7078] transition-transform active:scale-[0.98]"
      >
        Часто задаваемые вопросы
      </button>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

onMounted(() => {
  // подстраиваемся под Telegram Mini App, если открыто внутри клиента Telegram
  window.Telegram?.WebApp?.ready?.();
  window.Telegram?.WebApp?.expand?.();
});

const services = [
  {
    title: 'Записаться на замер',
    type: 'measurement',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-4.6-4.6a1 1 0 0 1 0-1.4L15.3 2.7a1 1 0 0 1 1.4 0l4.6 4.6a1 1 0 0 1 0 1.4Z"/>
      <path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>
    </svg>`
  },
  {
    title: 'Получить консультацию',
    type: 'consultation',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
    </svg>`
  },
  {
    title: 'Слив воды',
    type: 'drain',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7Z"/>
    </svg>`
  }
]
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

.font-display { font-family: 'Unbounded', sans-serif; }
.font-body { font-family: 'Inter', sans-serif; }
body { font-family: 'Inter', sans-serif; }
</style>