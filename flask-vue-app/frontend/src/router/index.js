import { createRouter, createWebHistory } from 'vue-router'
import HomeInputForm from "@/components/HomeInputForm.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeInputForm',
      component: HomeInputForm,
    },
  ]
})

export default router
