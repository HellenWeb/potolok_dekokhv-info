import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css';
import { initTelegramWebApp } from './lib/telegram';

const app = createApp(App)

initTelegramWebApp();

app.use(router)

app.mount('#app')
