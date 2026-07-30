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
        <h1 class="font-display text-[19px] font-bold leading-tight">Заявка</h1>
        <p class="font-body text-[12px] text-[#9AA0AB]">{{ titles[type] || 'Оставить заявку' }}</p>
      </div>
    </header>

    <!-- SUCCESS STATE -->
    <div v-if="success" class="flex flex-col items-center px-6 pt-10 text-center">
      <div class="relative mb-6 h-20 w-20">
        <div class="absolute inset-0 rounded-full bg-[#FFC93C]/25 blur-xl"></div>
        <div class="relative flex h-20 w-20 items-center justify-center rounded-full bg-[#1C1D21] shadow-[0_0_24px_2px_rgba(255,201,60,0.45)]">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#FFC93C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 6 9 17l-5-5"/>
          </svg>
        </div>
      </div>
      <h2 class="font-display text-[20px] font-bold leading-tight">Заявка отправлена</h2>
      <p class="mt-2 max-w-[260px] font-body text-[14px] leading-relaxed text-[#6B7078]">
        Мы свяжемся с вами в ближайшее время, чтобы подтвердить детали
      </p>
      <button
        @click="router.push('/')"
        class="mt-7 w-full max-w-[280px] rounded-2xl bg-[#1C1D21] px-4 py-3.5 font-body text-[14px] font-medium text-white transition-transform active:scale-[0.98]"
      >
        На главную
      </button>
    </div>

    <!-- FORM STATE -->
    <template v-else>
      <!-- type badge, echoes the service card icon -->
      <section class="mx-5 mb-5 flex items-center gap-3 rounded-2xl border border-[#E3E1DC] bg-white px-4 py-3.5">
        <span
          class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#1C1D21] text-[#FFC93C]"
          v-html="icons[type] || icons.consultation"
        ></span>
        <div>
          <p class="font-body text-[14.5px] font-semibold leading-tight">{{ titles[type] || 'Оставить заявку' }}</p>
          <p class="font-body text-[12px] text-[#9AA0AB]">Заполните форму — мы перезвоним</p>
        </div>
      </section>

      <form @submit.prevent="submit" class="flex flex-col gap-4 px-5">
        <label class="flex flex-col gap-1.5">
          <span class="px-1 font-body text-[12px] font-medium text-[#9AA0AB]">Ваше имя</span>
          <input
            v-model="form.name"
            class="rounded-2xl border border-[#E3E1DC] bg-white px-4 py-3.5 font-body text-[15px] text-[#1C1D21] outline-none transition-colors placeholder:text-[#C7CBD1] focus:border-[#FFC93C]"
            placeholder="Иван Иванов"
            required
          />
        </label>

        <label class="flex flex-col gap-1.5">
          <span class="px-1 font-body text-[12px] font-medium text-[#9AA0AB]">Телефон</span>
          <input
            v-model="form.phone"
            type="tel"
            class="rounded-2xl border border-[#E3E1DC] bg-white px-4 py-3.5 font-body text-[15px] text-[#1C1D21] outline-none transition-colors placeholder:text-[#C7CBD1] focus:border-[#FFC93C]"
            placeholder="+7 (___) ___-__-__"
            required
          />
        </label>

        <label class="flex flex-col gap-1.5">
          <span class="px-1 font-body text-[12px] font-medium text-[#9AA0AB]">Адрес</span>
          <input
            v-model="form.address"
            class="rounded-2xl border border-[#E3E1DC] bg-white px-4 py-3.5 font-body text-[15px] text-[#1C1D21] outline-none transition-colors placeholder:text-[#C7CBD1] focus:border-[#FFC93C]"
            placeholder="Город, улица, дом, квартира"
            required
          />
        </label>

        <label class="flex flex-col gap-1.5">
          <span class="px-1 font-body text-[12px] font-medium text-[#9AA0AB]">Желаемая дата</span>
          <input
            v-model="form.arrival_time"
            type="date"
            class="rounded-2xl border border-[#E3E1DC] bg-white px-4 py-3.5 font-body text-[15px] text-[#1C1D21] outline-none transition-colors focus:border-[#FFC93C]"
            required
          />
        </label>

        <p v-if="errorMsg" class="rounded-xl bg-[#FDECEC] px-4 py-3 font-body text-[13px] text-[#C0392B]">
          {{ errorMsg }}
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="mt-1 flex items-center justify-center gap-2 rounded-2xl bg-[#1C1D21] px-4 py-3.5 font-body text-[14.5px] font-medium text-white transition-transform active:scale-[0.98] disabled:opacity-60"
        >
          <svg
            v-if="loading"
            class="h-4 w-4 animate-spin text-[#FFC93C]"
            viewBox="0 0 24 24" fill="none"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-90" fill="currentColor" d="M4 12a8 8 0 0 1 8-8V0C5.4 0 0 5.4 0 12h4Z"/>
          </svg>
          {{ loading ? 'Отправка...' : 'Отправить заявку' }}
        </button>

        <p class="px-1 text-center font-body text-[11.5px] text-[#9AA0AB]">
          Нажимая «Отправить заявку», вы соглашаетесь на обработку персональных данных
        </p>
      </form>
    </template>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import { ref, computed } from 'vue'

const route = useRoute()
const router = useRouter()
const api = window.APP_CONFIG.API_URL
const tg = window.Telegram.WebApp

tg.ready();

const type = computed(() => route.query.type || 'consultation')

const titles = {
    measurement: 'Запись на замер',
    consultation: 'Получить консультацию',
    drain: 'Заявка на слив воды'
}

const icons = {
  measurement: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-4.6-4.6a1 1 0 0 1 0-1.4L15.3 2.7a1 1 0 0 1 1.4 0l4.6 4.6a1 1 0 0 1 0 1.4Z"/>
    <path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>
  </svg>`,
  consultation: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
  </svg>`,
  drain: `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7Z"/>
  </svg>`
}

const form = ref({
    tg_id: tg.initDataUnsafe.user?.id,
    name: '',
    phone: '',
    address: '',
    arrival_time: ''
})

const loading = ref(false)
const success = ref(false)
const errorMsg = ref('')

async function submit() {
    loading.value = true
    errorMsg.value = ''
    try {
        const res = await fetch(`${api}/api/v1/add`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ ...form.value, work_type: titles[type.value] })
        })

        if (!res.ok)
        {
            let errMessage = 'Ошибка отправки. Попробуйте позже'

            try {
                const errorData = await res.json()
                errMessage = errorData.detail || errorData.message || errMessage

            } catch {

            }

            throw new Error(errMessage)
        }

        success.value = true
    } catch (e)
    {
        console.error(e)
        errorMsg.value = e.message
    } finally {
        loading.value = false
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

.font-display { font-family: 'Unbounded', sans-serif; }
.font-body { font-family: 'Inter', sans-serif; }
</style>