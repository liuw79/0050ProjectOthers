<template>
  <div class="customer-detail" v-loading="loading">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-title">
        <el-button
          :icon="ArrowLeft"
          @click="$router.back()"
          class="back-button"
        >
          返回
        </el-button>
        
        <div class="title-content">
          <h1>客户详情</h1>
          <p class="page-description">查看和管理客户的详细信息。</p>
        </div>
      </div>
      
      <div class="page-actions">
        <el-button
          type="success"
          :icon="Plus"
          @click="createAppointment"
        >
          创建预约
        </el-button>
        
        <el-button
          type="primary"
          :icon="Edit"
          @click="editCustomer"
        >
          编辑客户
        </el-button>
        
        <el-dropdown trigger="click" @command="handleAction">
          <el-button :icon="More">
            更多操作
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="message" :icon="Message">
                发送消息
              </el-dropdown-item>
              <el-dropdown-item command="export" :icon="Download">
                导出信息
              </el-dropdown-item>
              <el-dropdown-item command="print" :icon="Printer">
                打印信息
              </el-dropdown-item>
              <el-dropdown-item command="delete" :icon="Delete" divided>
                删除客户
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    
    <div class="customer-content" v-if="customer">
      <el-row :gutter="24">
        <!-- 左侧：客户基本信息 -->
        <el-col :xl="8" :lg="10" :md="24" :sm="24">
          <!-- 客户信息卡片 -->
          <el-card class="customer-info-card" shadow="never">
            <template #header>
              <div class="card-header">
                <span>基本信息</span>
                <el-button
                  type="primary"
                  size="small"
                  :icon="Edit"
                  @click="editCustomer"
                >
                  编辑
                </el-button>
              </div>
            </template>
            
            <div class="customer-profile">
              <div class="avatar-section">
                <el-avatar
                  :size="80"
                  :src="customer.avatar"
                  class="customer-avatar"
                >
                  {{ customer.name.charAt(0) }}
                </el-avatar>
                
                <div class="profile-info">
                  <h2 class="customer-name">{{ customer.name }}</h2>
                  <div class="customer-tags">
                    <el-tag
                      :type="customer.gender === 'male' ? 'primary' : 'danger'"
                      size="small"
                    >
                      {{ customer.gender === 'male' ? '男' : '女' }}
                    </el-tag>
                    <el-tag type="info" size="small">
                      {{ customer.age }}岁
                    </el-tag>
                  </div>
                </div>
              </div>
              
              <div class="contact-info">
                <div class="info-item">
                  <label>手机号：</label>
                  <div class="info-value">
                    <el-link :href="`tel:${customer.phone}`" type="primary">
                      {{ customer.phone }}
                    </el-link>
                    <el-button
                      size="small"
                      :icon="CopyDocument"
                      @click="copyToClipboard(customer.phone)"
                    />
                  </div>
                </div>
                
                <div class="info-item">
                  <label>邮箱：</label>
                  <div class="info-value">
                    <el-link :href="`mailto:${customer.email}`" type="primary">
                      {{ customer.email }}
                    </el-link>
                    <el-button
                      size="small"
                      :icon="CopyDocument"
                      @click="copyToClipboard(customer.email)"
                    />
                  </div>
                </div>
                
                <div class="info-item" v-if="customer.occupation">
                  <label>职业：</label>
                  <span class="info-value">{{ customer.occupation }}</span>
                </div>
                
                <div class="info-item" v-if="customer.company">
                  <label>公司：</label>
                  <span class="info-value">{{ customer.company }}</span>
                </div>
                
                <div class="info-item" v-if="customer.address">
                  <label>地址：</label>
                  <span class="info-value">{{ customer.address }}</span>
                </div>
                
                <div class="info-item" v-if="customer.notes">
                  <label>备注：</label>
                  <span class="info-value">{{ customer.notes }}</span>
                </div>
                
                <div class="info-item">
                  <label>注册时间：</label>
                  <span class="info-value">{{ formatDateTime(customer.created_at) }}</span>
                </div>
                
                <div class="info-item">
                  <label>最后更新：</label>
                  <span class="info-value">{{ formatDateTime(customer.updated_at) }}</span>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 统计信息卡片 -->
          <el-card class="stats-card" shadow="never">
            <template #header>
              <span>统计信息</span>
            </template>
            
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ customerStats.total_appointments || 0 }}</div>
                <div class="stat-label">总预约次数</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-value">{{ customerStats.completed_appointments || 0 }}</div>
                <div class="stat-label">已完成预约</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-value">{{ customerStats.cancelled_appointments || 0 }}</div>
                <div class="stat-label">取消预约</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-value">{{ customerStats.total_insights || 0 }}</div>
                <div class="stat-label">分析报告</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <!-- 右侧：预约历史和其他信息 -->
        <el-col :xl="16" :lg="14" :md="24" :sm="24">
          <el-tabs v-model="activeTab" class="detail-tabs">
            <!-- 预约历史 -->
            <el-tab-pane label="预约历史" name="appointments">
              <div class="appointments-section">
                <div class="section-header">
                  <h3>预约历史</h3>
                  <el-button
                    type="primary"
                    size="small"
                    :icon="Plus"
                    @click="createAppointment"
                  >
                    新建预约
                  </el-button>
                </div>
                
                <div class="appointments-filter">
                  <el-select
                    v-model="appointmentFilter.status"
                    placeholder="筛选状态"
                    clearable
                    style="width: 120px"
                    @change="loadAppointments"
                  >
                    <el-option label="待确认" value="pending" />
                    <el-option label="已确认" value="confirmed" />
                    <el-option label="已完成" value="completed" />
                    <el-option label="已取消" value="cancelled" />
                  </el-select>
                  
                  <el-date-picker
                    v-model="appointmentFilter.date_range"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                    style="width: 240px"
                    @change="loadAppointments"
                  />
                </div>
                
                <div class="appointments-list" v-loading="appointmentsLoading">
                  <div
                    v-for="appointment in appointments"
                    :key="appointment.id"
                    class="appointment-item"
                  >
                    <div class="appointment-header">
                      <div class="appointment-title">
                        <h4>{{ appointment.service_type }}</h4>
                        <el-tag
                          :type="getStatusType(appointment.status)"
                          size="small"
                        >
                          {{ getStatusText(appointment.status) }}
                        </el-tag>
                      </div>
                      
                      <div class="appointment-actions">
                        <el-button
                          type="primary"
                          size="small"
                          :icon="View"
                          @click="viewAppointment(appointment.id)"
                        >
                          查看
                        </el-button>
                        
                        <el-dropdown
                          trigger="click"
                          @command="(cmd) => handleAppointmentAction(cmd, appointment)"
                        >
                          <el-button size="small" :icon="More" />
                          <template #dropdown>
                            <el-dropdown-menu>
                              <el-dropdown-item
                                v-if="appointment.status === 'pending'"
                                command="confirm"
                                :icon="Check"
                              >
                                确认预约
                              </el-dropdown-item>
                              <el-dropdown-item
                                v-if="appointment.status === 'confirmed'"
                                command="complete"
                                :icon="Check"
                              >
                                完成预约
                              </el-dropdown-item>
                              <el-dropdown-item
                                v-if="['pending', 'confirmed'].includes(appointment.status)"
                                command="reschedule"
                                :icon="Calendar"
                              >
                                重新安排
                              </el-dropdown-item>
                              <el-dropdown-item
                                v-if="['pending', 'confirmed'].includes(appointment.status)"
                                command="cancel"
                                :icon="Close"
                              >
                                取消预约
                              </el-dropdown-item>
                              <el-dropdown-item command="edit" :icon="Edit">
                                编辑预约
                              </el-dropdown-item>
                            </el-dropdown-menu>
                          </template>
                        </el-dropdown>
                      </div>
                    </div>
                    
                    <div class="appointment-details">
                      <div class="detail-row">
                        <el-icon><Clock /></el-icon>
                        <span>{{ formatDateTime(appointment.appointment_date) }}</span>
                      </div>
                      
                      <div class="detail-row" v-if="appointment.duration">
                        <el-icon><Timer /></el-icon>
                        <span>{{ appointment.duration }} 分钟</span>
                      </div>
                      
                      <div class="detail-row" v-if="appointment.location">
                        <el-icon><Location /></el-icon>
                        <span>{{ appointment.location }}</span>
                      </div>
                      
                      <div class="detail-row" v-if="appointment.notes">
                        <el-icon><Document /></el-icon>
                        <span>{{ appointment.notes }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <el-empty
                    v-if="appointments.length === 0 && !appointmentsLoading"
                    description="暂无预约记录"
                  />
                </div>
                
                <div class="appointments-pagination" v-if="appointmentPagination.total > 0">
                  <el-pagination
                    v-model:current-page="appointmentPagination.page"
                    v-model:page-size="appointmentPagination.page_size"
                    :total="appointmentPagination.total"
                    :page-sizes="[10, 20, 50]"
                    layout="total, sizes, prev, pager, next"
                    @size-change="handleAppointmentSizeChange"
                    @current-change="handleAppointmentCurrentChange"
                  />
                </div>
              </div>
            </el-tab-pane>
            
            <!-- 分析报告 -->
            <el-tab-pane label="分析报告" name="insights">
              <div class="insights-section">
                <div class="section-header">
                  <h3>分析报告</h3>
                  <el-button
                    type="primary"
                    size="small"
                    :icon="Plus"
                    @click="createInsight"
                  >
                    新建分析
                  </el-button>
                </div>
                
                <div class="insights-list" v-loading="insightsLoading">
                  <div
                    v-for="insight in insights"
                    :key="insight.id"
                    class="insight-item"
                  >
                    <div class="insight-header">
                      <div class="insight-title">
                        <h4>{{ insight.title }}</h4>
                        <el-tag
                          :type="insight.status === 'completed' ? 'success' : 'warning'"
                          size="small"
                        >
                          {{ insight.status === 'completed' ? '已完成' : '进行中' }}
                        </el-tag>
                      </div>
                      
                      <div class="insight-actions">
                        <el-button
                          type="primary"
                          size="small"
                          :icon="View"
                          @click="viewInsight(insight.id)"
                        >
                          查看
                        </el-button>
                      </div>
                    </div>
                    
                    <div class="insight-details">
                      <div class="detail-row">
                        <el-icon><Calendar /></el-icon>
                        <span>{{ formatDate(insight.created_at) }}</span>
                      </div>
                      
                      <div class="detail-row" v-if="insight.summary">
                        <el-icon><Document /></el-icon>
                        <span>{{ insight.summary }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <el-empty
                    v-if="insights.length === 0 && !insightsLoading"
                    description="暂无分析报告"
                  />
                </div>
              </div>
            </el-tab-pane>
            
            <!-- 操作日志 -->
            <el-tab-pane label="操作日志" name="logs">
              <div class="logs-section">
                <div class="section-header">
                  <h3>操作日志</h3>
                </div>
                
                <div class="logs-list" v-loading="logsLoading">
                  <el-timeline>
                    <el-timeline-item
                      v-for="log in logs"
                      :key="log.id"
                      :timestamp="formatDateTime(log.created_at)"
                      placement="top"
                    >
                      <div class="log-content">
                        <div class="log-action">{{ log.action }}</div>
                        <div class="log-details" v-if="log.details">
                          {{ log.details }}
                        </div>
                        <div class="log-user">
                          操作人：{{ log.user_name }}
                        </div>
                      </div>
                    </el-timeline-item>
                  </el-timeline>
                  
                  <el-empty
                    v-if="logs.length === 0 && !logsLoading"
                    description="暂无操作日志"
                  />
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  Plus,
  Edit,
  More,
  ArrowDown,
  Message,
  Download,
  Printer,
  Delete,
  CopyDocument,
  View,
  Check,
  Close,
  Calendar,
  Clock,
  Timer,
  Location,
  Document
} from '@element-plus/icons-vue'
import { appointmentsApi } from '@/api/appointments'
import { insightsApi } from '@/api/insights'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(false)
const customer = ref(null)
const customerStats = ref({})
const activeTab = ref('appointments')

// 预约相关
const appointments = ref([])
const appointmentsLoading = ref(false)
const appointmentFilter = reactive({
  status: '',
  date_range: []
})
const appointmentPagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

// 分析报告相关
const insights = ref([])
const insightsLoading = ref(false)

// 操作日志相关
const logs = ref([])
const logsLoading = ref(false)

// 方法
const loadCustomer = async () => {
  loading.value = true
  try {
    const customerId = route.params.id
    const response = await appointmentsApi.getCustomer(customerId)
    customer.value = response.data
    
    // 加载统计信息
    await loadCustomerStats()
  } catch (error) {
    ElMessage.error('加载客户信息失败')
    console.error('加载客户失败:', error)
  } finally {
    loading.value = false
  }
}

const loadCustomerStats = async () => {
  try {
    const customerId = route.params.id
    const response = await appointmentsApi.getCustomerStats(customerId)
    customerStats.value = response.data
  } catch (error) {
    console.error('加载客户统计失败:', error)
  }
}

const loadAppointments = async () => {
  appointmentsLoading.value = true
  try {
    const customerId = route.params.id
    const params = {
      customer_id: customerId,
      page: appointmentPagination.page,
      page_size: appointmentPagination.page_size,
      ...appointmentFilter
    }
    
    // 处理日期范围
    if (appointmentFilter.date_range && appointmentFilter.date_range.length === 2) {
      params.date_start = appointmentFilter.date_range[0]
      params.date_end = appointmentFilter.date_range[1]
    }
    delete params.date_range
    
    const response = await appointmentsApi.getAppointments(params)
    appointments.value = response.data.results || []
    appointmentPagination.total = response.data.count || 0
  } catch (error) {
    ElMessage.error('加载预约历史失败')
    console.error('加载预约失败:', error)
  } finally {
    appointmentsLoading.value = false
  }
}

const loadInsights = async () => {
  insightsLoading.value = true
  try {
    const customerId = route.params.id
    const response = await insightsApi.getInsights({
      customer_id: customerId,
      page_size: 20
    })
    insights.value = response.data.results || []
  } catch (error) {
    ElMessage.error('加载分析报告失败')
    console.error('加载分析报告失败:', error)
  } finally {
    insightsLoading.value = false
  }
}

const loadLogs = async () => {
  logsLoading.value = true
  try {
    const customerId = route.params.id
    const response = await appointmentsApi.getCustomerLogs(customerId)
    logs.value = response.data.results || []
  } catch (error) {
    ElMessage.error('加载操作日志失败')
    console.error('加载操作日志失败:', error)
  } finally {
    logsLoading.value = false
  }
}

const handleAction = async (command) => {
  switch (command) {
    case 'message':
      sendMessage()
      break
    case 'export':
      await exportCustomer()
      break
    case 'print':
      printCustomer()
      break
    case 'delete':
      await deleteCustomer()
      break
  }
}

const handleAppointmentAction = async (command, appointment) => {
  switch (command) {
    case 'confirm':
      await confirmAppointment(appointment.id)
      break
    case 'complete':
      await completeAppointment(appointment.id)
      break
    case 'reschedule':
      rescheduleAppointment(appointment.id)
      break
    case 'cancel':
      await cancelAppointment(appointment.id)
      break
    case 'edit':
      editAppointment(appointment.id)
      break
  }
}

const handleAppointmentSizeChange = (size) => {
  appointmentPagination.page_size = size
  appointmentPagination.page = 1
  loadAppointments()
}

const handleAppointmentCurrentChange = (page) => {
  appointmentPagination.page = page
  loadAppointments()
}

const editCustomer = () => {
  router.push(`/customers/${route.params.id}/edit`)
}

const createAppointment = () => {
  router.push(`/appointments/create?customer_id=${route.params.id}`)
}

const viewAppointment = (id) => {
  router.push(`/appointments/${id}`)
}

const editAppointment = (id) => {
  router.push(`/appointments/${id}/edit`)
}

const rescheduleAppointment = (id) => {
  router.push(`/appointments/${id}/reschedule`)
}

const createInsight = () => {
  router.push(`/insights/create?customer_id=${route.params.id}`)
}

const viewInsight = (id) => {
  router.push(`/insights/${id}`)
}

const confirmAppointment = async (id) => {
  try {
    await appointmentsApi.confirmAppointment(id)
    ElMessage.success('预约确认成功')
    await loadAppointments()
    await loadCustomerStats()
  } catch (error) {
    ElMessage.error(error.message || '确认预约失败')
  }
}

const completeAppointment = async (id) => {
  try {
    await appointmentsApi.completeAppointment(id)
    ElMessage.success('预约完成成功')
    await loadAppointments()
    await loadCustomerStats()
  } catch (error) {
    ElMessage.error(error.message || '完成预约失败')
  }
}

const cancelAppointment = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确定要取消这个预约吗？',
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await appointmentsApi.cancelAppointment(id)
    ElMessage.success('预约取消成功')
    await loadAppointments()
    await loadCustomerStats()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '取消预约失败')
    }
  }
}

const sendMessage = () => {
  ElMessage.info('发送消息功能开发中')
}

const exportCustomer = async () => {
  try {
    const response = await appointmentsApi.exportCustomers({
      ids: [route.params.id]
    })
    
    // 下载文件
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `customer_${route.params.id}_${dayjs().format('YYYY-MM-DD')}.xlsx`
    link.click()
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
    console.error('导出客户失败:', error)
  }
}

const printCustomer = () => {
  window.print()
}

const deleteCustomer = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个客户吗？删除后无法恢复，相关的预约记录也会被删除。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await appointmentsApi.deleteCustomer(route.params.id)
    ElMessage.success('删除成功')
    router.push('/customers')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('复制成功')
  } catch (error) {
    ElMessage.error('复制失败')
  }
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

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD')
}

const formatDateTime = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 监听标签页切换
const handleTabChange = (tabName) => {
  switch (tabName) {
    case 'appointments':
      if (appointments.value.length === 0) {
        loadAppointments()
      }
      break
    case 'insights':
      if (insights.value.length === 0) {
        loadInsights()
      }
      break
    case 'logs':
      if (logs.value.length === 0) {
        loadLogs()
      }
      break
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadCustomer()
  loadAppointments()
})
</script>

<style lang="scss" scoped>
.customer-detail {
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
    display: flex;
    align-items: flex-start;
    gap: 16px;
    
    .back-button {
      margin-top: 4px;
    }
    
    .title-content {
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
  }
  
  .page-actions {
    display: flex;
    gap: 12px;
  }
}

.customer-content {
  .customer-info-card {
    margin-bottom: 20px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
    
    .customer-profile {
      .avatar-section {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 24px;
        padding-bottom: 20px;
        border-bottom: 1px solid var(--el-border-color-lighter);
        
        .profile-info {
          flex: 1;
          
          .customer-name {
            margin: 0 0 8px 0;
            font-size: 20px;
            font-weight: 600;
            color: var(--el-text-color-primary);
          }
          
          .customer-tags {
            display: flex;
            gap: 8px;
          }
        }
      }
      
      .contact-info {
        .info-item {
          display: flex;
          align-items: center;
          margin-bottom: 16px;
          
          &:last-child {
            margin-bottom: 0;
          }
          
          label {
            width: 80px;
            font-weight: 500;
            color: var(--el-text-color-secondary);
            flex-shrink: 0;
          }
          
          .info-value {
            flex: 1;
            color: var(--el-text-color-primary);
            display: flex;
            align-items: center;
            gap: 8px;
            
            .el-button {
              padding: 4px;
            }
          }
        }
      }
    }
  }
  
  .stats-card {
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      
      .stat-item {
        text-align: center;
        padding: 16px;
        background: var(--el-bg-color);
        border-radius: var(--el-border-radius-base);
        border: 1px solid var(--el-border-color-lighter);
        
        .stat-value {
          font-size: 24px;
          font-weight: 600;
          color: var(--el-color-primary);
          margin-bottom: 4px;
        }
        
        .stat-label {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }
  
  .detail-tabs {
    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      
      h3 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }
    }
    
    .appointments-section {
      .appointments-filter {
        display: flex;
        gap: 16px;
        margin-bottom: 20px;
      }
      
      .appointments-list {
        .appointment-item {
          padding: 16px;
          margin-bottom: 16px;
          background: var(--el-bg-color);
          border: 1px solid var(--el-border-color-lighter);
          border-radius: var(--el-border-radius-base);
          
          &:last-child {
            margin-bottom: 0;
          }
          
          .appointment-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
            
            .appointment-title {
              display: flex;
              align-items: center;
              gap: 12px;
              
              h4 {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
                color: var(--el-text-color-primary);
              }
            }
            
            .appointment-actions {
              display: flex;
              gap: 8px;
            }
          }
          
          .appointment-details {
            .detail-row {
              display: flex;
              align-items: center;
              gap: 8px;
              margin-bottom: 8px;
              font-size: 14px;
              color: var(--el-text-color-regular);
              
              &:last-child {
                margin-bottom: 0;
              }
              
              .el-icon {
                color: var(--el-text-color-secondary);
                font-size: 16px;
              }
            }
          }
        }
      }
      
      .appointments-pagination {
        display: flex;
        justify-content: center;
        margin-top: 20px;
      }
    }
    
    .insights-section {
      .insights-list {
        .insight-item {
          padding: 16px;
          margin-bottom: 16px;
          background: var(--el-bg-color);
          border: 1px solid var(--el-border-color-lighter);
          border-radius: var(--el-border-radius-base);
          
          &:last-child {
            margin-bottom: 0;
          }
          
          .insight-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
            
            .insight-title {
              display: flex;
              align-items: center;
              gap: 12px;
              
              h4 {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
                color: var(--el-text-color-primary);
              }
            }
          }
          
          .insight-details {
            .detail-row {
              display: flex;
              align-items: center;
              gap: 8px;
              margin-bottom: 8px;
              font-size: 14px;
              color: var(--el-text-color-regular);
              
              &:last-child {
                margin-bottom: 0;
              }
              
              .el-icon {
                color: var(--el-text-color-secondary);
                font-size: 16px;
              }
            }
          }
        }
      }
    }
    
    .logs-section {
      .logs-list {
        .log-content {
          .log-action {
            font-weight: 600;
            color: var(--el-text-color-primary);
            margin-bottom: 4px;
          }
          
          .log-details {
            color: var(--el-text-color-regular);
            margin-bottom: 4px;
          }
          
          .log-user {
            font-size: 12px;
            color: var(--el-text-color-secondary);
          }
        }
      }
    }
  }
}

// 响应式适配
@include respond-to(lg) {
  .customer-detail {
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
    grid-template-columns: repeat(4, 1fr) !important;
  }
}

@include respond-to(md) {
  .page-header {
    .page-title {
      flex-direction: column;
      gap: 8px;
      
      .back-button {
        align-self: flex-start;
        margin-top: 0;
      }
    }
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  
  .appointments-filter {
    flex-direction: column !important;
    
    .el-select,
    .el-date-picker {
      width: 100% !important;
    }
  }
  
  .appointment-header,
  .insight-header {
    flex-direction: column !important;
    gap: 12px !important;
    align-items: stretch !important;
    
    .appointment-actions,
    .insight-actions {
      justify-content: flex-end;
    }
  }
}

// 打印样式
@media print {
  .customer-detail {
    padding: 0;
    
    .page-actions,
    .appointment-actions,
    .insight-actions {
      display: none;
    }
    
    .detail-tabs {
      .el-tabs__header {
        display: none;
      }
      
      .el-tab-pane {
        display: block !important;
      }
    }
  }
}
</style>