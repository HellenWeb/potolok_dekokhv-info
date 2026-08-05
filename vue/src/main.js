import { createApp, onMounted } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css';

const app = createApp(App)

onMounted(() => {
    const tg = window.Telegram?.WebApp;

    if (!tg) return;

    tg.ready();
    tg.expand();

    if (tg.requestFullscreen) {
        tg.requestFullscreen();
    }

    tg.setHeaderColor('#111111');
    tg.setBackgroundColor('#111111');

})

if (window.Telegram?.WebApp)
{
    window.Telegram.WebApp.ready();
    window.Telegram.WebApp.expand();
}

app.use(router)

app.mount('#app')
