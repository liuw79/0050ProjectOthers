<template>
  <div class="dashboard">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-title">
        <h1>仪表盘</h1>
        <p class="page-description">欢迎回来，{{ userName }}！这里是您的工作概览。</p>
      </div>
      <div class="page-actions">
        <el-button type="primary" :icon="Plus" @click="quickCreateAppointment">
          快速预约
        </el-button>
        <el-button :icon="Refresh" @click="refreshData" :loading="loading">
          刷新数据
        </el-button>
      </div>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in stats" :key="stat.key">
        <div class="stat-icon" :style="{ backgroundColor: stat.color }">
          <el-icon :size="24">
            <component :is="stat.icon" />
          </el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-change" :class="stat.changeType">
            <el-icon :size="12">
              <component :is="stat.changeType === 'increase' ? TrendCharts : Bottom" />
            </el-icon>
            <span>{{ stat.change }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="dashboard-content">
      <!-- 左侧内容 -->
      <div class="content-left">
        <!-- 今日预约 -->
        <el-card class="today-appointments" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">
                <el-icon><Calendar /></el-icon>
                今日预约
              </span>
              <el-button text type="primary" @click="viewAllAppointments">
                查看全部
              </el-button>
            </div>
          </template>
          
          <div class="appointments-list" v-loading="appointmentsLoading">
            <div 
              v-for="appointment in todayAppointments" 
              :key="appointment.id"
              class="appointment-item"
              @click="viewAppointment(appointment.id)"
            >
              <div class="appointment-time">
                <div class="time">{{ formatTime(appointment.scheduled_time) }}</div>
                <div class="duration">{{ appointment.duration }}分钟</div>
              </div>
              <div class="appointment-info">
                <div class="customer-name">{{ appointment.customer_name }}</div>
                <div class="service-type">{{ appointment.service_type }}</div>
              </div>
              <div class="appointment-status">
                <el-tag 
                  :type="getStatusType(appointment.status)"
                  size="small"
                >
                  {{ getStatusText(appointment.status) }}
                </el-tag>
              </div>
              <div class="appointment-actions">
                <el-button 
                  text 
                  type="primary" 
                  size="small"
                  @click.stop="confirmAppointment(appointment.id)"
                  v-if="appointment.status === 'pending'"
                >
                  确认
                </el-button>
                <el-button 
                  text 
                  type="success" 
                  size="small"
                  @click.stop="completeAppointment(appointment.id)"
                  v-if="appointment.status === 'confirmed'"
                >
                  完成
                </el-button>
              </div>
            </div>
            
            <div v-if="todayAppointments.length === 0" class="empty-state">
              <el-empty description="今日暂无预约" :image-size="80" />
            </div>
          </div>
        </el-card>
        
        <!-- 最近分析 -->
        <el-card class="recent-insights" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">
                <el-icon><DataAnalysis /></el-icon>
                最近分析
              </span>
              <el-button text type="primary" @click="viewAllInsights">
                查看全部
              </el-button>
            </div>
          </template>
          
          <div class="insights-list" v-loading="insightsLoading">
            <div 
              v-for="insight in recentInsights" 
              :key="insight.id"
              class="insight-item"
              @click="viewInsight(insight.id)"
            >
              <div class="insight-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="insight-info">
                <div class="insight-title">{{ insight.title }}</div>
                <div class="insight-meta">
                  <span class="customer">{{ insight.customer_name }}</span>
                  <span class="date">{{ formatDate(insight.created_at) }}</span>
                </div>
              </div>
              <div class="insight-status">
                <el-tag 
                  :type="insight.status === 'completed' ? 'success' : 'warning'"
                  size="small"
                >
                  {{ insight.status === 'completed' ? '已完成' : '进行中' }}
                </el-tag>
              </div>
            </div>
            
            <div v-if="recentInsights.length === 0" class="empty-state">
              <el-empty description="暂无分析记录" :image-size="80" />
            </div>
          </div>
        </el-card>
      </div>
      
      <!-- 右侧内容 -->
      <div class="content-right">
        <!-- 数据趋势图表 -->
        <el-card class="trend-chart" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">
                <el-icon><TrendCharts /></el-icon>
                预约趋势
              </span>
              <el-select v-model="trendPeriod" size="small" style="width: 100px">
                <el-option label="7天" value="7d" />
                <el-option label="30天" value="30d" />
                <el-option label="90天" value="90d" />
              </el-select>
            </div>
          </template>
          
          <div class="chart-container" v-loading="chartLoading">
            <div ref="trendChartRef" class="chart" style="height: 300px;"></div>
          </div>
        </el-card>
        
        <!-- 客户分布 -->
        <el-card class="customer-distribution" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">
                <el-icon><PieChart /></el-icon>
                客户分布
              </span>
            </div>
          </template>
          
          <div class="chart-container" v-loading="chartLoading">
            <div ref="distributionChartRef" class="chart" style="height: 250px;"></div>
          </div>
        </el-card>
        
        <!-- 快速操作 -->
        <el-card class="quick-actions" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">
                <el-icon><Operation /></el-icon>
                快速操作
              </span>
            </div>
          </template>
          
          <div class="actions-grid">
            <div 
              v-for="action in quickActions" 
              :key="action.key"
              class="action-item"
              @click="handleQuickAction(action.key)"
            >
              <div class="action-icon" :style="{ backgroundColor: action.color }">
                <el-icon :size="20">
                  <component :is="action.icon" />
                </el-icon>
              </div>
              <div class="action-label">{{ action.label }}</div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 快速预约对话框 -->
    <el-dialog
      v-model="quickAppointmentVisible"
      title="快速预约"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="quickAppointmentFormRef"
        :model="quickAppointmentForm"
        :rules="quickAppointmentRules"
        label-width="80px"
      >
        <el-form-item label="客户" prop="customerId">
          <el-select
            v-model="quickAppointmentForm.customerId"
            placeholder="选择客户"
            filterable
            remote
            :remote-method="searchCustomers"
            :loading="customerSearchLoading"
            style="width: 100%"
          >
            <el-option
              v-for="customer in customerOptions"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="日期" prop="date">
          <el-date-picker
            v-model="quickAppointmentForm.date"
            type="date"
            placeholder="选择日期"
            :disabled-date="disabledDate"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="时间" prop="time">
          <el-time-picker
            v-model="quickAppointmentForm.time"
            placeholder="选择时间"
            format="HH:mm"
            value-format="HH:mm"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="服务类型" prop="serviceType">
          <el-select v-model="quickAppointmentForm.serviceType" placeholder="选择服务类型" style="width: 100%">
            <el-option label="咨询服务" value="consultation" />
            <el-option label="深度访谈" value="interview" />
            <el-option label="数据分析" value="analysis" />
            <el-option label="报告解读" value="report" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="quickAppointmentForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="quickAppointmentVisible = false">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="quickAppointmentLoading"
            @click="createQuickAppointment"
          >
            创建预约
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Refresh,
  Calendar,
  User,
  Document,
  DataAnalysis,
  TrendCharts,
  PieChart,
  Operation,
  Bottom,
  Files,
  Setting
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { appointmentsApi } from '@/api/appointments'
import { insightsApi } from '@/api/insights'
import * as echarts from 'echarts'
import dayjs from 'dayjs'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const loading = ref(false)
const appointmentsLoading = ref(false)
const insightsLoading = ref(false)
const chartLoading = ref(false)
const quickAppointmentVisible = ref(false)
const quickAppointmentLoading = ref(false)
const customerSearchLoading = ref(false)
const trendPeriod = ref('7d')

// 图表引用
const trendChartRef = ref()
const distributionChartRef = ref()
let trendChart = null
let distributionChart = null

// 表单引用
const quickAppointmentFormRef = ref()

// 数据
const stats = ref([])
const todayAppointments = ref([])
const recentInsights = ref([])
const customerOptions = ref([])

// 计算属性
const userName = computed(() => authStore.user?.first_name || authStore.user?.username || '用户')

// 快速预约表单
const quickAppointmentForm = reactive({
  customerId: '',
  date: '',
  time: '',
  serviceType: '',
  notes: ''
})

// 表单验证规则
const quickAppointmentRules = {
  customerId: [
    { required: true, message: '请选择客户', trigger: 'change' }
  ],
  date: [
    { required: true, message: '请选择日期', trigger: 'change' }
  ],
  time: [
    { required: true, message: '请选择时间', trigger: 'change' }
  ],
  serviceType: [
    { required: true, message: '请选择服务类型', trigger: 'change' }
  ]
}

// 快速操作配置
const quickActions = [
  {
    key: 'create-appointment',
    label: '创建预约',
    icon: 'Calendar',
    color: '#409EFF'
  },
  {
    key: 'add-customer',
    label: '添加客户',
    icon: 'User',
    color: '#67C23A'
  },
  {
    key: 'create-transcript',
    label: '创建文稿',
    icon: 'Document',
    color: '#E6A23C'
  },
  {
    key: 'view-insights',
    label: '查看洞察',
    icon: 'DataAnalysis',
    color: '#F56C6C'
  }
]

// 方法
const refreshData = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadStats(),
      loadTodayAppointments(),
      loadRecentInsights(),
      loadChartData()
    ])
    ElMessage.success('数据刷新成功')
  } catch (error) {
    ElMessage.error('数据刷新失败')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await appointmentsApi.getStats()
    stats.value = [
      {
        key: 'total-appointments',
        label: '总预约数',
        value: response.data.total_appointments || 0,
        change: '+12%',
        changeType: 'increase',
        icon: 'Calendar',
        color: '#409EFF'
      },
      {
        key: 'total-customers',
        label: '客户总数',
        value: response.data.total_customers || 0,
        change: '+8%',
        changeType: 'increase',
        icon: 'User',
        color: '#67C23A'
      },
      {
        key: 'completed-insights',
        label: '完成分析',
        value: response.data.completed_insights || 0,
        change: '+15%',
        changeType: 'increase',
        icon: 'DataAnalysis',
        color: '#E6A23C'
      },
      {
        key: 'pending-appointments',
        label: '待确认预约',
        value: response.data.pending_appointments || 0,
        change: '-5%',
        changeType: 'decrease',
        icon: 'Document',
        color: '#F56C6C'
      }
    ]
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadTodayAppointments = async () => {
  appointmentsLoading.value = true
  try {
    const response = await appointmentsApi.getTodayAppointments()
    todayAppointments.value = response.data.results || []
  } catch (error) {
    console.error('加载今日预约失败:', error)
  } finally {
    appointmentsLoading.value = false
  }
}

const loadRecentInsights = async () => {
  insightsLoading.value = true
  try {
    const response = await insightsApi.getInsights({ limit: 5 })
    recentInsights.value = response.data.results || []
  } catch (error) {
    console.error('加载最近分析失败:', error)
  } finally {
    insightsLoading.value = false
  }
}

const loadChartData = async () => {
  chartLoading.value = true
  try {
    const [trendResponse, distributionResponse] = await Promise.all([
      appointmentsApi.getTrendData({ period: trendPeriod.value }),
      appointmentsApi.getCustomerDistribution()
    ])
    
    await nextTick()
    initTrendChart(trendResponse.data)
    initDistributionChart(distributionResponse.data)
  } catch (error) {
    console.error('加载图表数据失败:', error)
  } finally {
    chartLoading.value = false
  }
}

const initTrendChart = (data) => {
  if (!trendChartRef.value) return
  
  if (trendChart) {
    trendChart.dispose()
  }
  
  trendChart = echarts.init(trendChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['预约数量', '完成数量']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.dates || []
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '预约数量',
        type: 'line',
        data: data.appointments || [],
        smooth: true,
        itemStyle: {
          color: '#409EFF'
        }
      },
      {
        name: '完成数量',
        type: 'line',
        data: data.completed || [],
        smooth: true,
        itemStyle: {
          color: '#67C23A'
        }
      }
    ]
  }
  
  trendChart.setOption(option)
}

const initDistributionChart = (data) => {
  if (!distributionChartRef.value) return
  
  if (distributionChart) {
    distributionChart.dispose()
  }
  
  distributionChart = echarts.init(distributionChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '客户类型',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data.distribution || []
      }
    ]
  }
  
  distributionChart.setOption(option)
}

const quickCreateAppointment = () => {
  quickAppointmentVisible.value = true
  // 重置表单
  Object.assign(quickAppointmentForm, {
    customerId: '',
    date: '',
    time: '',
    serviceType: '',
    notes: ''
  })
}

const createQuickAppointment = async () => {
  if (!quickAppointmentFormRef.value) return
  
  try {
    const valid = await quickAppointmentFormRef.value.validate()
    if (!valid) return
    
    quickAppointmentLoading.value = true
    
    const appointmentData = {
      customer_id: quickAppointmentForm.customerId,
      scheduled_time: `${quickAppointmentForm.date} ${quickAppointmentForm.time}`,
      service_type: quickAppointmentForm.serviceType,
      notes: quickAppointmentForm.notes
    }
    
    await appointmentsApi.createAppointment(appointmentData)
    
    ElMessage.success('预约创建成功')
    quickAppointmentVisible.value = false
    
    // 刷新今日预约数据
    await loadTodayAppointments()
  } catch (error) {
    ElMessage.error(error.message || '创建预约失败')
  } finally {
    quickAppointmentLoading.value = false
  }
}

const searchCustomers = async (query) => {
  if (!query) {
    customerOptions.value = []
    return
  }
  
  customerSearchLoading.value = true
  try {
    const response = await appointmentsApi.searchCustomers({ search: query })
    customerOptions.value = response.data.results || []
  } catch (error) {
    console.error('搜索客户失败:', error)
  } finally {
    customerSearchLoading.value = false
  }
}

const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7
}

const confirmAppointment = async (id) => {
  try {
    await appointmentsApi.confirmAppointment(id)
    ElMessage.success('预约确认成功')
    await loadTodayAppointments()
  } catch (error) {
    ElMessage.error(error.message || '确认预约失败')
  }
}

const completeAppointment = async (id) => {
  try {
    await appointmentsApi.completeAppointment(id)
    ElMessage.success('预约完成')
    await loadTodayAppointments()
  } catch (error) {
    ElMessage.error(error.message || '完成预约失败')
  }
}

const handleQuickAction = (key) => {
  switch (key) {
    case 'create-appointment':
      router.push('/appointments/create')
      break
    case 'add-customer':
      router.push('/customers?action=create')
      break
    case 'create-transcript':
      router.push('/transcripts/create')
      break
    case 'view-insights':
      router.push('/insights')
      break
  }
}

const viewAllAppointments = () => {
  router.push('/appointments')
}

const viewAllInsights = () => {
  router.push('/insights')
}

const viewAppointment = (id) => {
  router.push(`/appointments/${id}`)
}

const viewInsight = (id) => {
  router.push(`/insights/${id}`)
}

const getStatusType = (status) => {
  const statusMap = {
    pending: 'warning',
    confirmed: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '待确认',
    confirmed: '已确认',
    completed: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

const formatTime = (time) => {
  return dayjs(time).format('HH:mm')
}

const formatDate = (date) => {
  return dayjs(date).format('MM-DD')
}

// 监听趋势周期变化
watch(trendPeriod, () => {
  loadChartData()
})

// 组件挂载时初始化
onMounted(async () => {
  await refreshData()
  
  // 监听窗口大小变化，重新调整图表
  window.addEventListener('resize', () => {
    if (trendChart) {
      trendChart.resize()
    }
    if (distributionChart) {
      distributionChart.resize()
    }
  })
})

// 组件卸载时清理图表
onBeforeUnmount(() => {
  if (trendChart) {
    trendChart.dispose()
  }
  if (distributionChart) {
    distributionChart.dispose()
  }
})
</script>

<style lang="scss" scoped>
.dashboard {
  padding: 24px;
  background: var(--el-bg-color-page);
  min-height: calc(100vh - #{$header-height});
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  
  .page-title {
    h1 {
      margin: 0 0 8px 0;
      font-size: 28px;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
    
    .page-description {
      margin: 0;
      color: var(--el-text-color-secondary);
      font-size: 14px;
    }
  }
  
  .page-actions {
    display: flex;
    gap: 12px;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
  
  .stat-card {
    background: var(--el-bg-color);
    border-radius: 8px;
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: var(--el-box-shadow-light);
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: var(--el-box-shadow);
    }
    
    .stat-icon {
      width: 48px;
      height: 48px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
    
    .stat-content {
      flex: 1;
      
      .stat-value {
        font-size: 24px;
        font-weight: 600;
        color: var(--el-text-color-primary);
        margin-bottom: 4px;
      }
      
      .stat-label {
        font-size: 14px;
        color: var(--el-text-color-secondary);
        margin-bottom: 8px;
      }
      
      .stat-change {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 12px;
        
        &.increase {
          color: var(--el-color-success);
        }
        
        &.decrease {
          color: var(--el-color-danger);
        }
      }
    }
  }
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
  
  .content-left {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  
  .content-right {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.today-appointments {
  .appointments-list {
    .appointment-item {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 16px;
      border-radius: 8px;
      margin-bottom: 12px;
      background: var(--el-fill-color-lighter);
      cursor: pointer;
      transition: all 0.3s ease;
      
      &:hover {
        background: var(--el-fill-color-light);
        transform: translateX(4px);
      }
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .appointment-time {
        min-width: 80px;
        text-align: center;
        
        .time {
          font-size: 16px;
          font-weight: 600;
          color: var(--el-text-color-primary);
        }
        
        .duration {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
      
      .appointment-info {
        flex: 1;
        
        .customer-name {
          font-size: 14px;
          font-weight: 500;
          color: var(--el-text-color-primary);
          margin-bottom: 4px;
        }
        
        .service-type {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
      
      .appointment-status {
        margin-right: 8px;
      }
      
      .appointment-actions {
        display: flex;
        gap: 8px;
      }
    }
  }
}

.recent-insights {
  .insights-list {
    .insight-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px;
      border-radius: 6px;
      margin-bottom: 8px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      
      &:hover {
        background: var(--el-fill-color-lighter);
      }
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .insight-icon {
        width: 32px;
        height: 32px;
        border-radius: 6px;
        background: var(--el-fill-color-light);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--el-color-primary);
      }
      
      .insight-info {
        flex: 1;
        
        .insight-title {
          font-size: 14px;
          color: var(--el-text-color-primary);
          margin-bottom: 4px;
          @include text-ellipsis;
        }
        
        .insight-meta {
          display: flex;
          gap: 12px;
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }
}

.chart-container {
  .chart {
    width: 100%;
  }
}

.quick-actions {
  .actions-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    
    .action-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      padding: 20px;
      border-radius: 8px;
      background: var(--el-fill-color-lighter);
      cursor: pointer;
      transition: all 0.3s ease;
      
      &:hover {
        background: var(--el-fill-color-light);
        transform: translateY(-2px);
      }
      
      .action-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
      }
      
      .action-label {
        font-size: 12px;
        color: var(--el-text-color-primary);
        text-align: center;
      }
    }
  }
}

.empty-state {
  padding: 40px 20px;
  text-align: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 响应式适配
@include respond-to(lg) {
  .dashboard-content {
    grid-template-columns: 1fr;
    
    .content-right {
      order: -1;
    }
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@include respond-to(md) {
  .dashboard {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
    
    .page-actions {
      justify-content: flex-end;
    }
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions {
    .actions-grid {
      grid-template-columns: repeat(4, 1fr);
    }
  }
}

@include respond-to(sm) {
  .quick-actions {
    .actions-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
}
</style>