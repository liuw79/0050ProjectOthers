import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 状态
  const isDark = ref(false)
  const sidebarCollapsed = ref(false)
  const primaryColor = ref('#409EFF')
  
  // 计算属性
  const theme = computed(() => isDark.value ? 'dark' : 'light')
  
  // 方法
  const toggleTheme = () => {
    isDark.value = !isDark.value
    applyTheme()
    saveThemeToStorage()
  }
  
  const setTheme = (theme) => {
    isDark.value = theme === 'dark'
    applyTheme()
    saveThemeToStorage()
  }
  
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
    saveSidebarToStorage()
  }
  
  const setSidebarCollapsed = (collapsed) => {
    sidebarCollapsed.value = collapsed
    saveSidebarToStorage()
  }
  
  const setPrimaryColor = (color) => {
    primaryColor.value = color
    applyPrimaryColor()
    saveThemeToStorage()
  }
  
  const applyTheme = () => {
    const html = document.documentElement
    if (isDark.value) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
  }
  
  const applyPrimaryColor = () => {
    const html = document.documentElement
    html.style.setProperty('--el-color-primary', primaryColor.value)
    
    // 生成主色调的各种变体
    const colors = generateColorVariants(primaryColor.value)
    Object.entries(colors).forEach(([key, value]) => {
      html.style.setProperty(key, value)
    })
  }
  
  const generateColorVariants = (color) => {
    // 这里可以实现颜色变体生成逻辑
    // 简化版本，实际项目中可以使用更复杂的颜色计算
    return {
      '--el-color-primary-light-3': lightenColor(color, 0.3),
      '--el-color-primary-light-5': lightenColor(color, 0.5),
      '--el-color-primary-light-7': lightenColor(color, 0.7),
      '--el-color-primary-light-8': lightenColor(color, 0.8),
      '--el-color-primary-light-9': lightenColor(color, 0.9),
      '--el-color-primary-dark-2': darkenColor(color, 0.2)
    }
  }
  
  const lightenColor = (color, amount) => {
    // 简化的颜色变亮函数
    const num = parseInt(color.replace('#', ''), 16)
    const amt = Math.round(2.55 * amount * 100)
    const R = (num >> 16) + amt
    const G = (num >> 8 & 0x00FF) + amt
    const B = (num & 0x0000FF) + amt
    return '#' + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
      (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
      (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1)
  }
  
  const darkenColor = (color, amount) => {
    // 简化的颜色变暗函数
    const num = parseInt(color.replace('#', ''), 16)
    const amt = Math.round(2.55 * amount * 100)
    const R = (num >> 16) - amt
    const G = (num >> 8 & 0x00FF) - amt
    const B = (num & 0x0000FF) - amt
    return '#' + (0x1000000 + (R > 255 ? 255 : R < 0 ? 0 : R) * 0x10000 +
      (G > 255 ? 255 : G < 0 ? 0 : G) * 0x100 +
      (B > 255 ? 255 : B < 0 ? 0 : B)).toString(16).slice(1)
  }
  
  const saveThemeToStorage = () => {
    const themeConfig = {
      isDark: isDark.value,
      primaryColor: primaryColor.value
    }
    localStorage.setItem('theme-config', JSON.stringify(themeConfig))
  }
  
  const saveSidebarToStorage = () => {
    localStorage.setItem('sidebar-collapsed', JSON.stringify(sidebarCollapsed.value))
  }
  
  const loadThemeFromStorage = () => {
    try {
      const saved = localStorage.getItem('theme-config')
      if (saved) {
        const config = JSON.parse(saved)
        isDark.value = config.isDark || false
        primaryColor.value = config.primaryColor || '#409EFF'
      }
    } catch (error) {
      console.error('加载主题配置失败:', error)
    }
  }
  
  const loadSidebarFromStorage = () => {
    try {
      const saved = localStorage.getItem('sidebar-collapsed')
      if (saved) {
        sidebarCollapsed.value = JSON.parse(saved)
      }
    } catch (error) {
      console.error('加载侧边栏配置失败:', error)
    }
  }
  
  const initTheme = () => {
    loadThemeFromStorage()
    loadSidebarFromStorage()
    applyTheme()
    applyPrimaryColor()
  }
  
  const resetTheme = () => {
    isDark.value = false
    primaryColor.value = '#409EFF'
    sidebarCollapsed.value = false
    applyTheme()
    applyPrimaryColor()
    saveThemeToStorage()
    saveSidebarToStorage()
  }
  
  return {
    // 状态
    isDark: readonly(isDark),
    sidebarCollapsed: readonly(sidebarCollapsed),
    primaryColor: readonly(primaryColor),
    
    // 计算属性
    theme,
    
    // 方法
    toggleTheme,
    setTheme,
    toggleSidebar,
    setSidebarCollapsed,
    setPrimaryColor,
    initTheme,
    resetTheme
  }
})