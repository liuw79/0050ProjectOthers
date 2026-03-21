import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const user = ref(null)
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => {
    return !!token.value && !!user.value
  })

  const userRole = computed(() => {
    return user.value?.is_superuser ? 'admin' : 'user'
  })

  // 方法
  const setToken = (newToken, newRefreshToken) => {
    token.value = newToken
    refreshToken.value = newRefreshToken
    localStorage.setItem('token', newToken)
    localStorage.setItem('refreshToken', newRefreshToken)
  }

  const clearAuth = () => {
    token.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  }

  const login = async (credentials) => {
    try {
      loading.value = true
      const response = await authApi.login(credentials)
      
      if (response.access && response.refresh) {
        setToken(response.access, response.refresh)
        
        // 获取用户信息
        await getUserInfo()
        
        ElMessage.success('登录成功')
        
        // 重定向到目标页面或首页
        const redirect = router.currentRoute.value.query.redirect || '/'
        router.push(redirect)
        
        return true
      } else {
        throw new Error('登录响应格式错误')
      }
    } catch (error) {
      console.error('登录失败:', error)
      ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      // 调用后端登出接口（如果有的话）
      // await authApi.logout()
      
      clearAuth()
      ElMessage.success('已退出登录')
      router.push('/login')
    } catch (error) {
      console.error('登出失败:', error)
      // 即使登出接口失败，也要清除本地状态
      clearAuth()
      router.push('/login')
    }
  }

  const getUserInfo = async () => {
    try {
      const userInfo = await authApi.getUserInfo()
      user.value = userInfo
      return userInfo
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // 如果获取用户信息失败，可能是token过期
      if (error.response?.status === 401) {
        await refreshTokens()
        // 重试获取用户信息
        const userInfo = await authApi.getUserInfo()
        user.value = userInfo
        return userInfo
      }
      throw error
    }
  }

  const refreshTokens = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('没有刷新令牌')
      }
      
      const response = await authApi.refreshToken(refreshToken.value)
      
      if (response.access) {
        setToken(response.access, refreshToken.value)
        return response.access
      } else {
        throw new Error('刷新令牌响应格式错误')
      }
    } catch (error) {
      console.error('刷新令牌失败:', error)
      // 刷新失败，清除认证状态
      clearAuth()
      router.push('/login')
      throw error
    }
  }

  const initAuth = async () => {
    if (token.value) {
      try {
        await getUserInfo()
      } catch (error) {
        console.error('初始化认证状态失败:', error)
        clearAuth()
      }
    }
  }

  const updateProfile = async (profileData) => {
    try {
      loading.value = true
      const updatedUser = await authApi.updateProfile(profileData)
      user.value = { ...user.value, ...updatedUser }
      ElMessage.success('个人信息更新成功')
      return updatedUser
    } catch (error) {
      console.error('更新个人信息失败:', error)
      ElMessage.error(error.response?.data?.detail || '更新失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  const changePassword = async (passwordData) => {
    try {
      loading.value = true
      await authApi.changePassword(passwordData)
      ElMessage.success('密码修改成功，请重新登录')
      await logout()
    } catch (error) {
      console.error('修改密码失败:', error)
      ElMessage.error(error.response?.data?.detail || '密码修改失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    token: readonly(token),
    user: readonly(user),
    loading: readonly(loading),
    
    // 计算属性
    isAuthenticated,
    userRole,
    
    // 方法
    login,
    logout,
    getUserInfo,
    refreshTokens,
    initAuth,
    updateProfile,
    changePassword,
    clearAuth
  }
})