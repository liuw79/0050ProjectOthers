import { api } from './request'

export const authApi = {
  // 用户登录
  login: (credentials) => {
    return api.post('/auth/login/', credentials)
  },

  // 刷新token
  refreshToken: (refreshToken) => {
    return api.post('/auth/refresh/', { refresh: refreshToken })
  },

  // 获取用户信息
  getUserInfo: () => {
    return api.get('/auth/user/')
  },

  // 更新用户信息
  updateProfile: (profileData) => {
    return api.patch('/auth/user/', profileData)
  },

  // 修改密码
  changePassword: (passwordData) => {
    return api.post('/auth/change-password/', passwordData)
  },

  // 用户注册（如果需要）
  register: (userData) => {
    return api.post('/auth/register/', userData)
  },

  // 忘记密码
  forgotPassword: (email) => {
    return api.post('/auth/forgot-password/', { email })
  },

  // 重置密码
  resetPassword: (token, newPassword) => {
    return api.post('/auth/reset-password/', {
      token,
      new_password: newPassword
    })
  },

  // 验证邮箱
  verifyEmail: (token) => {
    return api.post('/auth/verify-email/', { token })
  },

  // 重新发送验证邮件
  resendVerification: (email) => {
    return api.post('/auth/resend-verification/', { email })
  }
}