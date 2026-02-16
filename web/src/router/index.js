import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/Home.vue') },
  { path: '/new', name: 'NewProject', component: () => import('../views/NewProject.vue') },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
