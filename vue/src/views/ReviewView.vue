<template>
  <div class="min-h-screen bg-[#F6F5F2] pb-10 text-[#1C1D21]">
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
        <h1 class="font-display text-[19px] font-bold leading-tight">Отзывы клиентов</h1>
        <p class="font-body text-[12px] text-[#9AA0AB]">
          {{ loading ? 'Загрузка…' : `${reviews.length} отзывов · средний рейтинг ${averageRating}` }}
        </p>
      </div>
    </header>
    <section class="mx-5 mb-5 flex items-center gap-4 rounded-2xl border border-[#E3E1DC] bg-white px-4 py-4">
      <div class="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-[#1C1D21]">
        <span class="font-display text-[18px] font-bold text-[#FFC93C]">{{ averageRating }}</span>
      </div>
      <div class="flex-1">
        <div class="flex gap-0.5">
          <svg
            v-for="n in 5"
            :key="n"
            width="14"
            height="14"
            viewBox="0 0 24 24"
            :fill="n <= Math.round(Number(averageRating)) ? '#FFC93C' : 'none'"
            stroke="#FFC93C"
            stroke-width="1.5"
          >
            <path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.9-6.2-3.3-6.2 3.3 1.2-6.9-5-4.9 6.9-1L12 2Z"/>
          </svg>
        </div>
        <p class="mt-1 font-body text-[12px] text-[#6B7078]">На основе отзывов наших клиентов</p>
      </div>
    </section>
    <div v-if="loading" class="px-5 py-10 text-center font-body text-[14px] text-[#9AA0AB]">
      Загрузка отзывов…
    </div>
    <div v-else-if="error" class="mx-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 font-body text-[13px] text-red-700">
      Не удалось загрузить отзывы: {{ error }}
    </div>
    <section v-else class="flex flex-col gap-3 px-5">
      <article
        v-for="review in reviews"
        :key="review.id"
        class="rounded-2xl border border-[#E3E1DC] bg-white p-4"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="flex items-center gap-3">
            <div
              class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full font-display text-[13px] font-semibold text-white"
              :style="{ background: review.color }"
            >
              {{ review.initials }}
            </div>
            <div>
              <p class="font-body text-[14px] mb-1 font-semibold leading-tight">{{ review.name }}</p>
              <p class="font-body text-[10px] text-[#9AA0AB]">{{ review.date }}</p>
              <p class="mt-3 font-body text-[13.5px] leading-relaxed text-[#3D3F44]">
                {{ review.title }}
              </p>    
            </div>
          </div>
          <div class="flex shrink-0 gap-0.5">
            <svg
              v-for="n in 5"
              :key="n"
              width="12"
              height="12"
              viewBox="0 0 24 24"
              :fill="n <= review.rating ? '#FFC93C' : 'none'"
              stroke="#FFC93C"
              stroke-width="1.5"
            >
              <path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.9-6.2-3.3-6.2 3.3 1.2-6.9-5-4.9 6.9-1L12 2Z"/>
            </svg>
          </div>
        </div>
    </article>
      <p v-if="reviews.length === 0" class="py-8 text-center font-body text-[13px] text-[#9AA0AB]">
        Отзывов пока нет
      </p>
    </section>

    <section class="mx-5 mt-6 rounded-2xl border border-[#E3E1DC] bg-white p-4">
      <h2 class="font-display text-[15px] font-bold mb-4">Оставить свой отзыв</h2>

      <form @submit.prevent="submitReview" class="flex flex-col gap-3">
        <div>
          <label class="font-body text-[12px] text-[#6B7078] mb-1 block">Ваше имя</label>
          <input
            v-model="form.name"
            type="text"
            required
            placeholder="Иван И."
            class="w-full rounded-xl border border-[#E3E1DC] bg-[#F6F5F2] px-3 py-2.5 font-body text-[14px] outline-none focus:border-[#1C1D21] transition"
          />
        </div>

        <div>
          <label class="font-body text-[12px] text-[#6B7078] mb-1 block">Напишите насколько вам понравились наши услуги :)</label>
          <input
            v-model="form.title"
            type="text"
            required
            placeholder="Самый прекрасный отзыв"
            class="w-full rounded-xl border border-[#E3E1DC] bg-[#F6F5F2] px-3 py-2.5 font-body text-[14px] outline-none focus:border-[#1C1D21] transition"
          />
        </div>

        <div>
          <label class="font-body text-[12px] text-[#6B7078] mb-1.5 block">Оценка</label>
          <div class="flex gap-1.5">
            <button
              v-for="n in 5"
              :key="n"
              type="button"
              @click="form.stars = n"
              class="transition active:scale-90"
            >
              <svg
                width="28"
                height="28"
                viewBox="0 0 24 24"
                :fill="n <= form.stars ? '#FFC93C' : 'none'"
                stroke="#FFC93C"
                stroke-width="1.5"
              >
                <path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.9-6.2-3.3-6.2 3.3 1.2-6.9-5-4.9 6.9-1L12 2Z"/>
              </svg>
            </button>
          </div>
        </div>

        <p v-if="formError" class="font-body text-[12px] text-red-600">{{ formError }}</p>
        <p v-if="formSuccess" class="font-body text-[12px] text-green-600">{{ formSuccess }}</p>

        <button
          type="submit"
          :disabled="submitting || form.stars === 0"
          class="mt-1 w-full rounded-xl bg-[#1C1D21] py-3 font-body text-[14px] font-semibold text-white active:scale-[0.98] transition disabled:opacity-50 disabled:active:scale-100"
        >
          {{ submitting ? 'Отправка…' : 'Отправить отзыв' }}
        </button>
      </form>
    </section>

    <p class="mt-5 px-5 text-center font-body text-[12px] text-[#9AA0AB]">
      Данные загружены с API
    </p>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { apiRequest } from '@/lib/api';
import { initTelegramWebApp } from '@/lib/telegram';

const router = useRouter();
initTelegramWebApp();

const reviews = ref([]);
const loading = ref(true);
const error = ref(null);

const form = ref({
  name: '',
  title: '',
  stars: 0,
});
const submitting = ref(false);
const formError = ref(null);
const formSuccess = ref(null);

const colors = ['#C98A00', '#1C1D21', '#9AA0AB', '#4A6FA5', '#6B8E23', '#8B4513'];

function getInitials(name = '') {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .toUpperCase()
    .slice(0, 2) || '?';
}

function normalizeReview(item, index) {
  return {
    id: item.id ?? index,
    name: item.name || 'Без имени',
    title: item.title || '',
    rating: Number(item.stars) || 0,
    date: item.created_at
      ? new Date(item.created_at).toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'long',
          year: 'numeric',
        })
      : 'Дата не указана',
    initials: getInitials(item.name),
    color: colors[index % colors.length],
  };
}

async function fetchReviews() {
  loading.value = true;
  error.value = null;

  try {
    const data = await apiRequest('/reviews', { method: 'GET' });
    reviews.value = (Array.isArray(data) ? data : []).map(normalizeReview);
  } catch (e) {
    console.error('Ошибка загрузки отзывов:', e);
    error.value = e.message || 'Неизвестная ошибка';
    reviews.value = [];
  } finally {
    loading.value = false;
  }
}

async function submitReview() {
  formError.value = null;
  formSuccess.value = null;

  if (!form.value.name.trim() || !form.value.title.trim() || form.value.stars === 0) {
    formError.value = 'Заполните все поля и выберите оценку';
    return;
  }

  submitting.value = true;

  try {
    await apiRequest('/reviews', {
      method: 'POST',
      body: JSON.stringify({
        name: form.value.name.trim(),
        title: form.value.title.trim(),
        stars: form.value.stars,
      }),
    });

    formSuccess.value = 'Отзыв успешно отправлен!';
    form.value = { name: '', title: '', stars: 0 };

    // Обновляем список
    await fetchReviews();
  } catch (e) {
    console.error('Ошибка отправки отзыва:', e);
    formError.value = e.message || 'Не удалось отправить отзыв';
  } finally {
    submitting.value = false;
  }
}

const averageRating = computed(() => {
  if (reviews.value.length === 0) return '0.0';
  const sum = reviews.value.reduce((acc, r) => acc + (r.rating || 0), 0);
  return (sum / reviews.value.length).toFixed(1);
});

onMounted(() => {
  fetchReviews();
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');
.font-display { font-family: 'Unbounded', sans-serif; }
.font-body { font-family: 'Inter', sans-serif; }
</style>
