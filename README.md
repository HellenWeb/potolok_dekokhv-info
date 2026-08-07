# 🎨 **POTOLOK_DEKOKHV** — Telegram Mini App

**Умное приложение для компании по натяжным потолкам**

Современное Telegram Mini App для автоматизации замеров, оформления заявок и взаимодействия с клиентами.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-0a6fd0)
![Vue.js](https://img.shields.io/badge/Vue.js-3.4.0-42b883)
![Telegram Mini App](https://img.shields.io/badge/Telegram-Mini%20App-229ED9)

---

## ✨ О проекте

**POTOLOK_DEKOKHV** — это удобное Telegram Mini App, которое помогает компании по установке натяжных потолков автоматизировать процесс работы с клиентами

Приложение объединяет красоту современного интерфейса и мощь автоматизации, позволяя клиентам быстро оставить заявку, а менеджерам — получать структурированные данные в реальном времени.

### 🎯 Основные возможности

- **📋 Удобная форма заявки**  
  Быстрое заполнение данных: удобная запись на замер, консультацию

- **📸 Отзывы**  
  Клиент может сразу прикрепить фотографии помещения для предварительной оценки.

- **📍 Геолокация**  
  Автоматический захват или ручной выбор адреса.

- **🔄 Автоматизация**  
  - Мгновенная отправка данных в CRM и передача их в админ бота для удобного управления заявками

- **🎨 Красивый адаптивный дизайн**  
  Полностью соответствует фирменному стилю компании.

- **📱 Полная интеграция с Telegram**  
  Использование Telegram WebApp API (MainButton, BackButton, theme params, haptic feedback).

---

## 🛠 Технологии

### Backend
- **FastAPI** — высокопроизводительный Python-фреймворк
- **Python 3.11+**
- **Pydantic v2** — валидация данных
- **SQLAlchemy** 
- **Telegram Bot API**

### Frontend
- **Vue 3** (Composition API + Script Setup)
- **TypeScript**
- **Vite** — сборка
- **Pinia** — управление состоянием
- **Vue Router**
- **Telegram WebApp** — нативные возможности

### Деплой
- Docker + Docker Compose
- Nginx
- Uvicorn (ASGI)

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/HellenWeb/potolok_dekokhv-info.git
cd potolok_dekokhv-info
