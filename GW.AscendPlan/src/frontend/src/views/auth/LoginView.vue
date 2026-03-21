<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="login-bg">
      <div class="bg-pattern"></div>
    </div>
    
    <!-- 登录表单 -->
    <div class="login-form-wrapper">
      <div class="login-form-container">
        <!-- Logo和标题 -->
        <div class="login-header">
          <div class="logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="12" fill="#2563EB"/>
              <path d="M24 12L32 20H28V32H20V20H16L24 12Z" fill="white"/>
            </svg>
          </div>
          <h1 class="login-title">AscendPlan</h1>
          <p class="login-subtitle">专家助理系统</p>
        </div>
      
        <!-- 登录表单 -->
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
              class="login-input"
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              class="login-input"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <div class="login-options">
              <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
              <el-link type="primary" :underline="false" @click="showForgotPassword">忘记密码？</el-link>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-button"
              :loading="loading"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        
        <!-- 其他登录方式 -->
        <div class="login-divider">
          <span>或</span>
        </div>
        
        <div class="social-login">
          <el-button class="social-button" size="large">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            微信登录
          </el-button>
        </div>
        
        <!-- 注册链接 -->
        <div class="register-link">
          <span>还没有账户？</span>
          <el-link type="primary" :underline="false" @click="showRegister">立即注册</el-link>
        </div>
      </div>
    </div>
      
    <!-- 页面底部 -->
    <div class="login-footer">
      <p>&copy; 2024 AscendPlan. All rights reserved.</p>
    </div>
    
    <!-- 注册对话框 -->
    <el-dialog
      v-model="registerDialogVisible"
      title="用户注册"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱地址"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
            clearable
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            show-password
            clearable
          />
        </el-form-item>
        
        <el-form-item label="姓名" prop="firstName">
          <el-input
            v-model="registerForm.firstName"
            placeholder="请输入姓名"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="角色" prop="role">
          <el-select
            v-model="registerForm.role"
            placeholder="请选择角色"
            style="width: 100%"
          >
            <el-option label="规划师" value="planner" />
            <el-option label="客户" value="customer" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="registerDialogVisible = false">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="registerLoading"
            @click="handleRegister"
          >
            注册
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 忘记密码对话框 -->
    <el-dialog
      v-model="forgotPasswordDialogVisible"
      title="忘记密码"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="forgotPasswordFormRef"
        :model="forgotPasswordForm"
        :rules="forgotPasswordRules"
        label-width="80px"
      >
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="forgotPasswordForm.email"
            placeholder="请输入注册邮箱"
            clearable
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="forgotPasswordDialogVisible = false">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="forgotPasswordLoading"
            @click="handleForgotPassword"
          >
            发送重置邮件
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, TrendCharts } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'

const router = useRouter()
const authStore = useAuthStore()

// 表单引用
const loginFormRef = ref()
const registerFormRef = ref()
const forgotPasswordFormRef = ref()

// 加载状态
const loading = ref(false)
const registerLoading = ref(false)
const forgotPasswordLoading = ref(false)

// 对话框显示状态
const registerDialogVisible = ref(false)
const forgotPasswordDialogVisible = ref(false)

// 登录表单
const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

// 注册表单
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  firstName: '',
  role: 'customer'
})

// 忘记密码表单
const forgotPasswordForm = reactive({
  email: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名或邮箱', trigger: 'blur' },
    { min: 3, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 128, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ]
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 30, message: '长度在 3 到 30 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 128, message: '密码长度至少 8 个字符', trigger: 'blur' },
    { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, message: '密码必须包含大小写字母和数字', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  firstName: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

const forgotPasswordRules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    await authStore.login({
      username: loginForm.username,
      password: loginForm.password,
      remember: loginForm.remember
    })
    
    ElMessage.success('登录成功')
    
    // 跳转到首页或之前访问的页面
    const redirect = router.currentRoute.value.query.redirect || '/dashboard'
    router.push(redirect)
    
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error(error.message || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

// 显示注册对话框
const showRegister = () => {
  registerDialogVisible.value = true
  // 重置表单
  Object.assign(registerForm, {
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    role: 'customer'
  })
  if (registerFormRef.value) {
    registerFormRef.value.clearValidate()
  }
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    const valid = await registerFormRef.value.validate()
    if (!valid) return
    
    registerLoading.value = true
    
    await authApi.register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password,
      first_name: registerForm.firstName,
      role: registerForm.role
    })
    
    ElMessage.success('注册成功，请查收邮箱验证邮件')
    registerDialogVisible.value = false
    
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error(error.message || '注册失败，请稍后重试')
  } finally {
    registerLoading.value = false
  }
}

// 显示忘记密码对话框
const showForgotPassword = () => {
  forgotPasswordDialogVisible.value = true
  forgotPasswordForm.email = ''
  if (forgotPasswordFormRef.value) {
    forgotPasswordFormRef.value.clearValidate()
  }
}

// 处理忘记密码
const handleForgotPassword = async () => {
  if (!forgotPasswordFormRef.value) return
  
  try {
    const valid = await forgotPasswordFormRef.value.validate()
    if (!valid) return
    
    forgotPasswordLoading.value = true
    
    await authApi.forgotPassword({
      email: forgotPasswordForm.email
    })
    
    ElMessage.success('重置密码邮件已发送，请查收邮箱')
    forgotPasswordDialogVisible.value = false
    
  } catch (error) {
    console.error('发送重置邮件失败:', error)
    ElMessage.error(error.message || '发送失败，请稍后重试')
  } finally {
    forgotPasswordLoading.value = false
  }
}

// 组件挂载时检查是否已登录
onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>

<style lang="scss" scoped>
@import '@/styles/variables.scss';
@import '@/styles/mixins.scss';

.login-container {
  min-height: 100vh;
  position: relative;
  @include flex-center;
  overflow: hidden;
}

// 背景装饰
.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  @include brand-gradient;
  z-index: 1;
  
  .bg-pattern {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
      radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
    animation: float 20s ease-in-out infinite;
  }
}

// 登录表单容器
.login-form-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  padding: $spacing-md;
  
  @include respond-below(tablet) {
    max-width: 100%;
    padding: $spacing-sm;
  }
}

.login-form-container {
  background: $surface-primary;
  @include card-shadow(medium);
  border-radius: $border-radius-lg;
  padding: $spacing-xxl;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  
  @include respond-below(tablet) {
    padding: $spacing-xl;
    border-radius: $border-radius-md;
  }
}

// 头部样式
.login-header {
  text-align: center;
  margin-bottom: $spacing-xxl;
  
  .logo {
    margin-bottom: $spacing-lg;
    
    svg {
      border-radius: $border-radius-md;
      @include card-shadow(light);
    }
  }
  
  .login-title {
    font-family: $font-family-heading;
    font-size: $font-size-2xl;
    font-weight: $font-weight-bold;
    color: $text-primary;
    margin: $spacing-md 0 $spacing-xs;
    line-height: $line-height-tight;
  }
  
  .login-subtitle {
    font-size: $font-size-sm;
    color: $text-secondary;
    margin: 0;
    line-height: $line-height-normal;
  }
}

// 表单样式
.login-form {
  margin-bottom: $spacing-xl;
  
  :deep(.el-form-item) {
    margin-bottom: $spacing-lg;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .login-input {
    :deep(.el-input__wrapper) {
      border-radius: $border-radius-md;
      box-shadow: $box-shadow-light;
      border: 1px solid $border-light;
      transition: $transition-base;
      
      &:hover {
        border-color: $border-primary;
        box-shadow: $box-shadow-base;
      }
      
      &.is-focus {
        border-color: $color-primary;
        box-shadow: 0 0 0 2px rgba($color-primary, 0.1);
      }
    }
  }
  
  .login-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    :deep(.el-checkbox) {
      .el-checkbox__label {
        font-size: $font-size-sm;
        color: $text-secondary;
      }
    }
    
    :deep(.el-link) {
      font-size: $font-size-sm;
    }
  }
  
  .login-button {
    width: 100%;
    @include button-size(large);
    font-weight: $font-weight-semibold;
    
    :deep(.el-button) {
      border-radius: $border-radius-md;
    }
  }
}

// 分割线
.login-divider {
  position: relative;
  text-align: center;
  margin: $spacing-xl 0;
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: $border-light;
  }
  
  span {
    background: $surface-primary;
    padding: 0 $spacing-md;
    font-size: $font-size-sm;
    color: $text-tertiary;
  }
}

// 社交登录
.social-login {
  margin-bottom: $spacing-xl;
  
  .social-button {
    width: 100%;
    @include button-size(large);
    background: $surface-secondary;
    border: 1px solid $border-light;
    color: $text-primary;
    border-radius: $border-radius-md;
    
    &:hover {
      background: $surface-tertiary;
      border-color: $border-primary;
    }
    
    svg {
      margin-right: $spacing-xs;
    }
  }
}

// 注册链接
.register-link {
  text-align: center;
  font-size: $font-size-sm;
  color: $text-secondary;
  
  span {
    margin-right: $spacing-xs;
  }
}

// 页面底部
.login-footer {
  position: absolute;
  bottom: $spacing-lg;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  
  p {
    font-size: $font-size-xs;
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
    text-align: center;
  }
}

// 动画
@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-10px) rotate(180deg);
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 响应式适配
@include respond-below(tablet) {
  .login-form-container {
    margin: $spacing-md;
  }
  
  .login-header {
    .login-title {
      font-size: $font-size-xl;
    }
  }
}

// 深色主题适配
.dark {
  .login-form-container {
    background: rgba(30, 30, 30, 0.95);
    
    .login-title {
      color: var(--el-text-color-primary);
    }
  }
  
  .login-bg {
    .bg-pattern {
      background-image: 
        radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.02) 0%, transparent 50%);
    }
  }
}
</style>