<template>
  <div class="app">
    <router-view />
  </div>
</template>
<script>
import { onMounted } from 'vue'

onMounted(() => {
  if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp
    tg.ready();
    tg.expand();
    tg.disableVerticalSwipes()
  }
})

export default {
  name: "App"
}
</script>
<style>

.app {
  min-height: 100vh;
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
  box-sizing: border-box;
}

</style>