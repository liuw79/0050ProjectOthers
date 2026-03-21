import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    
    // 添加认证token
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    
    // 添加请求时间戳（防止缓存）
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 直接返回数据部分
    return response.data
  },
  async (error) => {
    const authStore = useAuthStore()
    const { response } = error
    
    if (response) {
      switch (response.status) {
        case 401:
          // 未授权，尝试刷新token
          if (authStore.refreshToken && !error.config._retry) {
            error.config._retry = true
            try {
              await authStore.refreshTokens()
              // 重新发送原请求
              error.config.headers.Authorization = `Bearer ${authStore.token}`
              return request(error.config)
            } catch (refreshError) {
              console.error('刷新token失败:', refreshError)
              authStore.clearAuth()
              router.push('/login')
              ElMessage.error('登录已过期，请重新登录')
            }
          } else {
            authStore.clearAuth()
            router.push('/login')
            ElMessage.error('登录已过期，请重新登录')
          }
          break
          
        case 403:
          ElMessage.error('没有权限访问该资源')
          break
          
        case 404:
          ElMessage.error('请求的资源不存在')
          break
          
        case 422:
          // 表单验证错误
          const errors = response.data?.errors || response.data?.detail
          if (errors) {
            if (typeof errors === 'string') {
              ElMessage.error(errors)
            } else if (typeof errors === 'object') {
              // 显示第一个错误信息
              const firstError = Object.values(errors)[0]
              ElMessage.error(Array.isArray(firstError) ? firstError[0] : firstError)
            }
          } else {
            ElMessage.error('请求参数错误')
          }
          break
          
        case 429:
          ElMessage.error('请求过于频繁，请稍后再试')
          break
          
        case 500:
          ElMessage.error('服务器内部错误，请稍后再试')
          break
          
        case 502:
        case 503:
        case 504:
          ElMessage.error('服务暂时不可用，请稍后再试')
          break
          
        default:
          const message = response.data?.detail || response.data?.message || '请求失败'
          ElMessage.error(message)
      }
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请检查网络连接')
    } else if (error.message === 'Network Error') {
      ElMessage.error('网络连接失败，请检查网络设置')
    } else {
      ElMessage.error('请求失败，请稍后再试')
    }
    
    return Promise.reject(error)
  }
)

// 封装常用请求方法
export const api = {
  get: (url, params = {}, config = {}) => {
    return request.get(url, { params, ...config })
  },
  
  post: (url, data = {}, config = {}) => {
    return request.post(url, data, config)
  },
  
  put: (url, data = {}, config = {}) => {
    return request.put(url, data, config)
  },
  
  patch: (url, data = {}, config = {}) => {
    return request.patch(url, data, config)
  },
  
  delete: (url, config = {}) => {
    return request.delete(url, config)
  },
  
  upload: (url, formData, config = {}) => {
    return request.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      ...config
    })
  },
  
  download: async (url, filename, config = {}) => {
    try {
      const response = await request.get(url, {
        responseType: 'blob',
        ...config
      })
      
      // 创建下载链接
      const blob = new Blob([response])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
      
      return response
    } catch (error) {
      console.error('下载失败:', error)
      throw error
    }
  }
}

// 请求状态管理
export const createRequestState = () => {
  const loading = ref(false)
  const error = ref(null)
  
  const execute = async (requestFn) => {
    try {
      loading.value = true
      error.value = null
      const result = await requestFn()
      return result
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }
  
  return {
    loading: readonly(loading),
    error: readonly(error),
    execute
  }
}

export default request