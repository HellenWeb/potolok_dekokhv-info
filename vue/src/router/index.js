import { createWebHistory, createRouter } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "Home", component: () => import('@/views/HomeView.vue') },
    { path: "/faq", name: "FAQ", component: () => import('@/views/FAQView.vue') },
    { path: "/form", name: "Form", component: () => import('@/views/FormView.vue') },
    { path: "/reviews", name: "Review", component: () => import('@/views/ReviewView.vue') }
  ]
})

export default router