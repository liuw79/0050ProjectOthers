<template>
  <div class="main-layout" :class="{ 'is-collapsed': isCollapsed }">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'is-collapsed': isCollapsed }">
      <div class="sidebar-header">
        <div class="logo" v-show="!isCollapsed">
          <el-icon class="logo-icon">
            <TrendCharts />
          </el-icon>
          <span class="logo-text">AscendPlan</span>
        </div>
        <div class="logo-mini" v-show="isCollapsed">
          <el-icon class="logo-icon">
            <TrendCharts />
          </el-icon>
        </div>
      </div>
      
      <div class="sidebar-menu">
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapsed"
          :unique-opened="true"
          router
          background-color="var(--el-bg-color)"
          text-color="var(--el-text-color-primary)"
          active-text-color="var(--el-color-primary)"
        >
          <!-- 仪表盘 -->
          <el-menu-item index="/dashboard">
            <el-icon><Odometer /></el-icon>
            <template #title>仪表盘</template>
          </el-menu-item>
          
          <!-- 预约管理 -->
          <el-sub-menu index="appointments">
            <template #title>
              <el-icon><Calendar /></el-icon>
              <span>预约管理</span>
            </template>
            <el-menu-item index="/appointments">预约列表</el-menu-item>
            <el-menu-item index="/appointments/create">创建预约</el-menu-item>
          </el-sub-menu>
          
          <!-- 客户管理 -->
          <el-sub-menu index="customers">
            <template #title>
              <el-icon><User /></el-icon>
              <span>客户管理</span>
            </template>
            <el-menu-item index="/customers">客户列表</el-menu-item>
          </el-sub-menu>
          
          <!-- 访谈文稿 -->
          <el-sub-menu index="transcripts">
            <template #title>
              <el-icon><Document /></el-icon>
              <span>访谈文稿</span>
            </template>
            <el-menu-item index="/transcripts">文稿列表</el-menu-item>
            <el-menu-item index="/transcripts/create">创建文稿</el-menu-item>
          </el-sub-menu>
          
          <!-- 洞察分析 -->
          <el-sub-menu index="insights">
            <template #title>
              <el-icon><DataAnalysis /></el-icon>
              <span>洞察分析</span>
            </template>
            <el-menu-item index="/insights">分析列表</el-menu-item>
            <el-menu-item index="/customer-insights">客户洞察</el-menu-item>
          </el-sub-menu>
          
          <!-- 分析模板 -->
          <el-menu-item index="/analysis-templates">
            <el-icon><Files /></el-icon>
            <template #title>分析模板</template>
          </el-menu-item>
          
          <!-- 系统设置 -->
          <el-menu-item index="/settings" v-if="userRole === 'admin'">
            <el-icon><Setting /></el-icon>
            <template #title>系统设置</template>
          </el-menu-item>
        </el-menu>
      </div>
    </aside>
    
    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 顶部导航 -->
      <header class="header-nav">
        <div class="header-left">
          <el-button
            class="collapse-btn"
            :icon="isCollapsed ? Expand : Fold"
            @click="toggleSidebar"
            text
          />
          
          <!-- 面包屑导航 -->
          <el-breadcrumb class="breadcrumb" separator="/">
            <el-breadcrumb-item
              v-for="item in breadcrumbs"
              :key="item.path"
              :to="item.path"
            >
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <!-- 主题切换 -->
          <el-tooltip content="切换主题" placement="bottom">
            <el-button
              :icon="isDark ? Sunny : Moon"
              @click="toggleTheme"
              text
              circle
            />
          </el-tooltip>
          
          <!-- 全屏切换 -->
          <el-tooltip content="全屏" placement="bottom">
            <el-button
              :icon="FullScreen"
              @click="toggleFullscreen"
              text
              circle
            />
          </el-tooltip>
          
          <!-- 通知 -->
          <el-dropdown trigger="click">
            <el-badge :value="unreadCount" :hidden="unreadCount === 0">
              <el-button :icon="Bell" text circle />
            </el-badge>
            <template #dropdown>
              <el-dropdown-menu>
                <div class="notification-header">
                  <span>通知消息</span>
                  <el-button text size="small" @click="markAllAsRead">
                    全部已读
                  </el-button>
                </div>
                <el-scrollbar max-height="300px">
                  <div class="notification-list">
                    <div
                      v-for="notification in notifications"
                      :key="notification.id"
                      class="notification-item"
                      :class="{ 'is-unread': !notification.read }"
                      @click="markAsRead(notification.id)"
                    >
                      <div class="notification-content">
                        <div class="notification-title">{{ notification.title }}</div>
                        <div class="notification-time">{{ formatTime(notification.created_at) }}</div>
                      </div>
                    </div>
                    <div v-if="notifications.length === 0" class="no-notifications">
                      暂无通知
                    </div>
                  </div>
                </el-scrollbar>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <!-- 用户菜单 -->
          <el-dropdown trigger="click">
            <div class="user-info">
              <el-avatar :size="32" :src="userAvatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="username" v-show="!isCollapsed">{{ userName }}</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="showProfile">
                  <el-icon><User /></el-icon>
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item @click="showSettings">
                  <el-icon><Setting /></el-icon>
                  账户设置
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>
      
      <!-- 页面内容 -->
      <main class="page-content">
        <router-view v-slot="{ Component, route }">
          <transition name="fade" mode="out-in">
            <keep-alive :include="cachedViews">
              <component :is="Component" :key="route.path" />
            </keep-alive>
          </transition>
        </router-view>
      </main>
    </div>
    
    <!-- 个人资料对话框 -->
    <el-dialog
      v-model="profileDialogVisible"
      title="个人资料"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="profileFormRef"
        :model="profileForm"
        :rules="profileRules"
        label-width="80px"
      >
        <el-form-item label="头像">
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :http-request="uploadAvatar"
          >
            <el-avatar :size="80" :src="profileForm.avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="用户名" prop="username">
          <el-input v-model="profileForm.username" disabled />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="profileForm.email" disabled />
        </el-form-item>
        
        <el-form-item label="姓名" prop="firstName">
          <el-input v-model="profileForm.firstName" />
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="profileForm.phone" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="profileDialogVisible = false">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="profileLoading"
            @click="updateProfile"
          >
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 账户设置对话框 -->
    <el-dialog
      v-model="settingsDialogVisible"
      title="账户设置"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-tabs v-model="activeSettingsTab">
        <el-tab-pane label="修改密码" name="password">
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px"
          >
            <el-form-item label="当前密码" prop="currentPassword">
              <el-input
                v-model="passwordForm.currentPassword"
                type="password"
                show-password
              />
            </el-form-item>
            
            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                show-password
              />
            </el-form-item>
            
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                show-password
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="通知设置" name="notifications">
          <el-form label-width="120px">
            <el-form-item label="邮件通知">
              <el-switch v-model="notificationSettings.email" />
            </el-form-item>
            
            <el-form-item label="系统通知">
              <el-switch v-model="notificationSettings.system" />
            </el-form-item>
            
            <el-form-item label="预约提醒">
              <el-switch v-model="notificationSettings.appointment" />
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="settingsDialogVisible = false">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="settingsLoading"
            @click="saveSettings"
          >
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  TrendCharts,
  Odometer,
  Calendar,
  User,
  Document,
  DataAnalysis,
  Files,
  Setting,
  Expand,
  Fold,
  Sunny,
  Moon,
  FullScreen,
  Bell,
  ArrowDown,
  SwitchButton
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

// 响应式数据
const profileDialogVisible = ref(false)
const settingsDialogVisible = ref(false)
const profileLoading = ref(false)
const settingsLoading = ref(false)
const activeSettingsTab = ref('password')
const notifications = ref([])
const unreadCount = ref(0)
const cachedViews = ref(['Dashboard'])

// 表单引用
const profileFormRef = ref()
const passwordFormRef = ref()

// 计算属性
const isCollapsed = computed(() => themeStore.sidebarCollapsed)
const isDark = computed(() => themeStore.isDark)
const userName = computed(() => authStore.user?.first_name || authStore.user?.username || '用户')
const userRole = computed(() => authStore.user?.role || 'customer')
const userAvatar = computed(() => authStore.user?.avatar || '')

// 当前激活的菜单
const activeMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/appointments')) return '/appointments'
  if (path.startsWith('/customers')) return '/customers'
  if (path.startsWith('/transcripts')) return '/transcripts'
  if (path.startsWith('/insights') || path.startsWith('/customer-insights')) return '/insights'
  return path
})

// 面包屑导航
const breadcrumbs = computed(() => {
  const matched = route.matched.filter(item => item.meta && item.meta.title)
  const breadcrumbList = []
  
  matched.forEach(item => {
    breadcrumbList.push({
      title: item.meta.title,
      path: item.path
    })
  })
  
  return breadcrumbList
})

// 个人资料表单
const profileForm = reactive({
  username: '',
  email: '',
  firstName: '',
  phone: '',
  avatar: ''
})

// 密码修改表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 通知设置
const notificationSettings = reactive({
  email: true,
  system: true,
  appointment: true
})

// 表单验证规则
const profileRules = {
  firstName: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少 8 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 方法
const toggleSidebar = () => {
  themeStore.toggleSidebar()
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

const showProfile = () => {
  // 填充当前用户信息
  Object.assign(profileForm, {
    username: authStore.user?.username || '',
    email: authStore.user?.email || '',
    firstName: authStore.user?.first_name || '',
    phone: authStore.user?.phone || '',
    avatar: authStore.user?.avatar || ''
  })
  profileDialogVisible.value = true
}

const showSettings = () => {
  settingsDialogVisible.value = true
  activeSettingsTab.value = 'password'
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch (error) {
    // 用户取消
  }
}

const updateProfile = async () => {
  if (!profileFormRef.value) return
  
  try {
    const valid = await profileFormRef.value.validate()
    if (!valid) return
    
    profileLoading.value = true
    
    await authStore.updateProfile({
      first_name: profileForm.firstName,
      phone: profileForm.phone
    })
    
    ElMessage.success('个人资料更新成功')
    profileDialogVisible.value = false
  } catch (error) {
    ElMessage.error(error.message || '更新失败')
  } finally {
    profileLoading.value = false
  }
}

const saveSettings = async () => {
  if (activeSettingsTab.value === 'password') {
    await changePassword()
  } else {
    await updateNotificationSettings()
  }
}

const changePassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    const valid = await passwordFormRef.value.validate()
    if (!valid) return
    
    settingsLoading.value = true
    
    await authStore.changePassword({
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    })
    
    ElMessage.success('密码修改成功')
    settingsDialogVisible.value = false
    
    // 重置表单
    Object.assign(passwordForm, {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
  } catch (error) {
    ElMessage.error(error.message || '密码修改失败')
  } finally {
    settingsLoading.value = false
  }
}

const updateNotificationSettings = async () => {
  try {
    settingsLoading.value = true
    
    // 这里应该调用API更新通知设置
    // await api.updateNotificationSettings(notificationSettings)
    
    ElMessage.success('设置保存成功')
    settingsDialogVisible.value = false
  } catch (error) {
    ElMessage.error(error.message || '保存失败')
  } finally {
    settingsLoading.value = false
  }
}

const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isJPG) {
    ElMessage.error('头像只能是 JPG/PNG 格式!')
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
  }
  return isJPG && isLt2M
}

const uploadAvatar = async (options) => {
  try {
    // 这里应该调用API上传头像
    // const response = await api.uploadAvatar(options.file)
    // profileForm.avatar = response.data.url
    ElMessage.success('头像上传成功')
  } catch (error) {
    ElMessage.error('头像上传失败')
  }
}

const markAsRead = (id) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification && !notification.read) {
    notification.read = true
    unreadCount.value--
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true
  })
  unreadCount.value = 0
}

const formatTime = (time) => {
  return dayjs(time).format('MM-DD HH:mm')
}

// 监听路由变化，更新面包屑
watch(
  () => route.path,
  () => {
    // 可以在这里添加页面缓存逻辑
  }
)

// 组件挂载时初始化
onMounted(() => {
  // 加载通知数据
  loadNotifications()
})

const loadNotifications = async () => {
  try {
    // 这里应该调用API获取通知
    // const response = await api.getNotifications()
    // notifications.value = response.data.results
    // unreadCount.value = notifications.value.filter(n => !n.read).length
  } catch (error) {
    console.error('加载通知失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.main-layout {
  display: flex;
  height: 100vh;
  background-color: var(--el-bg-color-page);
}

.sidebar {
  width: $sidebar-width;
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color-lighter);
  transition: width 0.3s ease;
  flex-shrink: 0;
  
  &.is-collapsed {
    width: $sidebar-collapsed-width;
  }
  
  .sidebar-header {
    height: $header-height;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid var(--el-border-color-lighter);
    
    .logo {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .logo-icon {
        font-size: 24px;
        color: var(--el-color-primary);
      }
      
      .logo-text {
        font-size: 18px;
        font-weight: 700;
        color: var(--el-text-color-primary);
      }
    }
    
    .logo-mini {
      .logo-icon {
        font-size: 24px;
        color: var(--el-color-primary);
      }
    }
  }
  
  .sidebar-menu {
    height: calc(100vh - #{$header-height});
    overflow-y: auto;
    
    .el-menu {
      border: none;
      height: 100%;
    }
  }
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header-nav {
  height: $header-height;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-lighter);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  flex-shrink: 0;
  
  .header-left {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .collapse-btn {
      font-size: 18px;
    }
    
    .breadcrumb {
      font-size: 14px;
    }
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 6px;
      transition: background-color 0.3s ease;
      
      &:hover {
        background: var(--el-fill-color-light);
      }
      
      .username {
        font-size: 14px;
        color: var(--el-text-color-primary);
      }
      
      .dropdown-icon {
        font-size: 12px;
        color: var(--el-text-color-secondary);
      }
    }
  }
}

.page-content {
  flex: 1;
  overflow: auto;
  background: var(--el-bg-color-page);
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--el-border-color-lighter);
  font-weight: 600;
}

.notification-list {
  .notification-item {
    padding: 12px 16px;
    border-bottom: 1px solid var(--el-border-color-lighter);
    cursor: pointer;
    transition: background-color 0.3s ease;
    
    &:hover {
      background: var(--el-fill-color-light);
    }
    
    &.is-unread {
      background: rgba(var(--el-color-primary-rgb), 0.05);
      
      &::before {
        content: '';
        position: absolute;
        left: 8px;
        top: 50%;
        transform: translateY(-50%);
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--el-color-primary);
      }
    }
    
    .notification-content {
      .notification-title {
        font-size: 14px;
        color: var(--el-text-color-primary);
        margin-bottom: 4px;
      }
      
      .notification-time {
        font-size: 12px;
        color: var(--el-text-color-secondary);
      }
    }
  }
  
  .no-notifications {
    padding: 40px 16px;
    text-align: center;
    color: var(--el-text-color-secondary);
    font-size: 14px;
  }
}

.avatar-uploader {
  .el-avatar {
    border: 2px dashed var(--el-border-color);
    cursor: pointer;
    transition: border-color 0.3s ease;
    
    &:hover {
      border-color: var(--el-color-primary);
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 页面过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 响应式适配
@include respond-to(md) {
  .main-layout {
    &.is-collapsed {
      .sidebar {
        transform: translateX(-100%);
        position: fixed;
        z-index: 1000;
        height: 100vh;
      }
    }
  }
  
  .header-nav {
    .header-left {
      .breadcrumb {
        display: none;
      }
    }
    
    .header-right {
      .user-info {
        .username {
          display: none;
        }
      }
    }
  }
}
</style>