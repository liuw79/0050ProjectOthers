import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 配置NProgress
NProgress.configure({ showSpinner: false })

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false
    }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Dashboard.vue'),
        meta: {
          title: '工作台',
          icon: 'House'
        }
      },
      {
        path: '/appointments',
        name: 'Appointments',
        component: () => import('@/views/appointments/AppointmentList.vue'),
        meta: {
          title: '预约管理',
          icon: 'Calendar'
        }
      },
      {
        path: '/appointments/create',
        name: 'CreateAppointment',
        component: () => import('@/views/appointments/CreateAppointment.vue'),
        meta: {
          title: '创建预约',
          icon: 'Plus'
        }
      },
      {
        path: '/appointments/:id',
        name: 'AppointmentDetail',
        component: () => import('@/views/appointments/AppointmentDetail.vue'),
        meta: {
          title: '预约详情'
        }
      },
      {
        path: '/customers',
        name: 'Customers',
        component: () => import('@/views/customers/CustomerList.vue'),
        meta: {
          title: '客户管理',
          icon: 'User'
        }
      },
      {
        path: '/customers/:id',
        name: 'CustomerDetail',
        component: () => import('@/views/customers/CustomerDetail.vue'),
        meta: {
          title: '客户详情'
        }
      },
      {
        path: '/transcripts',
        name: 'Transcripts',
        component: () => import('@/views/insights/TranscriptList.vue'),
        meta: {
          title: '访谈文稿',
          icon: 'Document'
        }
      },
      {
        path: '/transcripts/create',
        name: 'CreateTranscript',
        component: () => import('@/views/insights/CreateTranscript.vue'),
        meta: {
          title: '创建文稿'
        }
      },
      {
        path: '/transcripts/:id',
        name: 'TranscriptDetail',
        component: () => import('@/views/insights/TranscriptDetail.vue'),
        meta: {
          title: '文稿详情'
        }
      },
      {
        path: '/analysis',
        name: 'Analysis',
        component: () => import('@/views/insights/AnalysisList.vue'),
        meta: {
          title: '洞察分析',
          icon: 'TrendCharts'
        }
      },
      {
        path: '/analysis/:id',
        name: 'AnalysisDetail',
        component: () => import('@/views/insights/AnalysisDetail.vue'),
        meta: {
          title: '分析详情'
        }
      },
      {
        path: '/customer-insights',
        name: 'CustomerInsights',
        component: () => import('@/views/insights/CustomerInsights.vue'),
        meta: {
          title: '客户洞察',
          icon: 'DataAnalysis'
        }
      },
      {
        path: '/templates',
        name: 'Templates',
        component: () => import('@/views/insights/TemplateList.vue'),
        meta: {
          title: '分析模板',
          icon: 'Files'
        }
      },
      {
        path: '/settings',
        name: 'Settings',
        component: () => import('@/views/settings/Settings.vue'),
        meta: {
          title: '系统设置',
          icon: 'Setting'
        }
      }
    ]
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: {
      title: '页面不存在'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  NProgress.start()
  
  const authStore = useAuthStore()
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - AscendPlan`
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth !== false) {
    if (!authStore.isAuthenticated) {
      // 尝试从本地存储恢复认证状态
      await authStore.initAuth()
      
      if (!authStore.isAuthenticated) {
        next({ name: 'Login', query: { redirect: to.fullPath } })
        return
      }
    }
  } else {
    // 如果已登录且访问登录页，重定向到首页
    if (authStore.isAuthenticated && to.name === 'Login') {
      next({ name: 'Dashboard' })
      return
    }
  }
  
  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router