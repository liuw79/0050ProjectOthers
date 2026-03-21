<template>
  <div class="appointment-detail">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-title">
        <el-button
          :icon="ArrowLeft"
          @click="goBack"
          class="back-button"
        >
          返回
        </el-button>
        <div>
          <h1>预约详情</h1>
          <p class="page-description">查看和管理预约的详细信息。</p>
        </div>
      </div>
      
      <div class="page-actions" v-if="appointment">
        <el-dropdown trigger="click" @command="handleAction">
          <el-button type="primary">
            操作
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item
                command="edit"
                :icon="Edit"
                v-if="canEdit"
              >
                编辑预约
              </el-dropdown-item>
              
              <el-dropdown-item
                command="confirm"
                :icon="Check"
                v-if="appointment.status === 'pending'"
              >
                确认预约
              </el-dropdown-item>
              
              <el-dropdown-item
                command="complete"
                :icon="CircleCheck"
                v-if="appointment.status === 'confirmed'"
              >
                完成预约
              </el-dropdown-item>
              
              <el-dropdown-item
                command="reschedule"
                :icon="Clock"
                v-if="canReschedule"
              >
                重新安排
              </el-dropdown-item>
              
              <el-dropdown-item
                command="cancel"
                :icon="Close"
                v-if="canCancel"
                divided
              >
                取消预约
              </el-dropdown-item>
              
              <el-dropdown-item
                command="delete"
                :icon="Delete"
                v-if="canDelete"
                divided
              >
                删除预约
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        
        <el-button :icon="Printer" @click="printAppointment">
          打印
        </el-button>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>
    
    <!-- 预约信息 -->
    <div v-else-if="appointment" class="appointment-content">
      <el-row :gutter="24">
        <!-- 主要信息 -->
        <el-col :lg="16" :md="24">
          <!-- 基本信息卡片 -->
          <el-card class="info-card" shadow="never">
            <template #header>
              <div class="card-header">
                <div class="card-title">
                  <el-icon><Calendar /></el-icon>
                  <span>预约信息</span>
                </div>
                <el-tag :type="getStatusType(appointment.status)" size="large">
                  {{ getStatusText(appointment.status) }}
                </el-tag>
              </div>
            </template>
            
            <el-descriptions :column="2" border>
              <el-descriptions-item label="预约ID">
                <el-tag type="info">#{{ appointment.id }}</el-tag>
              </el-descriptions-item>
              
              <el-descriptions-item label="预约状态">
                <el-tag :type="getStatusType(appointment.status)">
                  {{ getStatusText(appointment.status) }}
                </el-tag>
              </el-descriptions-item>
              
              <el-descriptions-item label="预约时间">
                <div class="appointment-time">
                  <div class="date">{{ formatDate(appointment.scheduled_time) }}</div>
                  <div class="time">{{ formatTime(appointment.scheduled_time) }}</div>
                </div>
              </el-descriptions-item>
              
              <el-descriptions-item label="服务类型">
                <el-tag :type="getServiceTypeColor(appointment.service_type)">
                  {{ getServiceTypeText(appointment.service_type) }}
                </el-tag>
              </el-descriptions-item>
              
              <el-descriptions-item label="预计时长">
                {{ appointment.duration }}分钟
              </el-descriptions-item>
              
              <el-descriptions-item label="服务地点">
                {{ getLocationText(appointment.location) }}
              </el-descriptions-item>
              
              <el-descriptions-item
                label="会议链接"
                v-if="appointment.location === 'online' && appointment.meeting_url"
                :span="2"
              >
                <el-link :href="appointment.meeting_url" target="_blank" type="primary">
                  {{ appointment.meeting_url }}
                </el-link>
              </el-descriptions-item>
              
              <el-descriptions-item
                label="详细地址"
                v-if="appointment.location === 'customer_site' && appointment.address"
                :span="2"
              >
                {{ appointment.address }}
              </el-descriptions-item>
              
              <el-descriptions-item label="创建时间">
                {{ formatDateTime(appointment.created_at) }}
              </el-descriptions-item>
              
              <el-descriptions-item label="更新时间">
                {{ formatDateTime(appointment.updated_at) }}
              </el-descriptions-item>
              
              <el-descriptions-item label="备注信息" :span="2" v-if="appointment.notes">
                <div class="notes-content">{{ appointment.notes }}</div>
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
          
          <!-- 客户信息卡片 -->
          <el-card class="info-card" shadow="never">
            <template #header>
              <div class="card-header">
                <div class="card-title">
                  <el-icon><User /></el-icon>
                  <span>客户信息</span>
                </div>
                <el-button
                  text
                  type="primary"
                  @click="viewCustomer"
                  :icon="View"
                >
                  查看详情
                </el-button>
              </div>
            </template>
            
            <el-descriptions :column="2" border v-if="appointment.customer">
              <el-descriptions-item label="客户姓名">
                {{ appointment.customer.name }}
              </el-descriptions-item>
              
              <el-descriptions-item label="性别">
                {{ getGenderText(appointment.customer.gender) }}
              </el-descriptions-item>
              
              <el-descriptions-item label="手机号">
                <el-link :href="`tel:${appointment.customer.phone}`" type="primary">
                  {{ appointment.customer.phone }}
                </el-link>
              </el-descriptions-item>
              
              <el-descriptions-item label="邮箱">
                <el-link :href="`mailto:${appointment.customer.email}`" type="primary">
                  {{ appointment.customer.email }}
                </el-link>
              </el-descriptions-item>
              
              <el-descriptions-item label="年龄">
                {{ appointment.customer.age }}岁
              </el-descriptions-item>
              
              <el-descriptions-item label="职业">
                {{ appointment.customer.occupation || '-' }}
              </el-descriptions-item>
              
              <el-descriptions-item label="地址" :span="2">
                {{ appointment.customer.address || '-' }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
          
          <!-- 服务记录卡片 -->
          <el-card class="info-card" shadow="never" v-if="appointment.service_records?.length > 0">
            <template #header>
              <div class="card-header">
                <div class="card-title">
                  <el-icon><Document /></el-icon>
                  <span>服务记录</span>
                </div>
              </div>
            </template>
            
            <el-timeline>
              <el-timeline-item
                v-for="record in appointment.service_records"
                :key="record.id"
                :timestamp="formatDateTime(record.created_at)"
                placement="top"
              >
                <div class="service-record">
                  <div class="record-header">
                    <span class="record-type">{{ record.type }}</span>
                    <span class="record-status">{{ record.status }}</span>
                  </div>
                  <div class="record-content">{{ record.content }}</div>
                  <div class="record-meta">
                    <span>操作人：{{ record.operator }}</span>
                  </div>
                </div>
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </el-col>
        
        <!-- 侧边栏 -->
        <el-col :lg="8" :md="24">
          <!-- 快速操作卡片 -->
          <el-card class="action-card" shadow="never">
            <template #header>
              <div class="card-title">
                <el-icon><Operation /></el-icon>
                <span>快速操作</span>
              </div>
            </template>
            
            <div class="quick-actions">
              <el-button
                type="primary"
                :icon="Phone"
                @click="callCustomer"
                class="action-btn"
                v-if="appointment.customer?.phone"
              >
                拨打电话
              </el-button>
              
              <el-button
                type="success"
                :icon="Message"
                @click="sendMessage"
                class="action-btn"
              >
                发送消息
              </el-button>
              
              <el-button
                type="warning"
                :icon="Bell"
                @click="setReminder"
                class="action-btn"
              >
                设置提醒
              </el-button>
              
              <el-button
                type="info"
                :icon="Share"
                @click="shareAppointment"
                class="action-btn"
              >
                分享预约
              </el-button>
            </div>
          </el-card>
          
          <!-- 相关预约卡片 -->
          <el-card class="related-card" shadow="never" v-if="relatedAppointments.length > 0">
            <template #header>
              <div class="card-title">
                <el-icon><Connection /></el-icon>
                <span>相关预约</span>
              </div>
            </template>
            
            <div class="related-appointments">
              <div
                v-for="related in relatedAppointments"
                :key="related.id"
                class="related-item"
                @click="viewRelatedAppointment(related.id)"
              >
                <div class="related-info">
                  <div class="related-time">{{ formatDate(related.scheduled_time) }}</div>
                  <div class="related-type">{{ getServiceTypeText(related.service_type) }}</div>
                </div>
                <el-tag :type="getStatusType(related.status)" size="small">
                  {{ getStatusText(related.status) }}
                </el-tag>
              </div>
            </div>
          </el-card>
          
          <!-- 统计信息卡片 -->
          <el-card class="stats-card" shadow="never">
            <template #header>
              <div class="card-title">
                <el-icon><DataAnalysis /></el-icon>
                <span>客户统计</span>
              </div>
            </template>
            
            <div class="stats-content" v-if="customerStats">
              <div class="stat-item">
                <div class="stat-label">总预约次数</div>
                <div class="stat-value">{{ customerStats.total_appointments }}</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-label">已完成</div>
                <div class="stat-value">{{ customerStats.completed_appointments }}</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-label">取消次数</div>
                <div class="stat-value">{{ customerStats.cancelled_appointments }}</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-label">客户满意度</div>
                <div class="stat-value">
                  <el-rate
                    v-model="customerStats.satisfaction_rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                  />
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 错误状态 -->
    <div v-else class="error-container">
      <el-empty description="预约不存在或已被删除">
        <el-button type="primary" @click="goBack">
          返回列表
        </el-button>
      </el-empty>
    </div>
    
    <!-- 重新安排对话框 -->
    <el-dialog
      v-model="rescheduleDialogVisible"
      title="重新安排预约"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="rescheduleFormRef"
        :model="rescheduleForm"
        :rules="rescheduleRules"
        label-width="80px"
      >
        <el-form-item label="新日期" prop="date">
          <el-date-picker
            v-model="rescheduleForm.date"
            type="date"
            placeholder="选择新日期"
            :disabled-date="disabledDate"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="新时间" prop="time">
          <el-time-picker
            v-model="rescheduleForm.time"
            placeholder="选择新时间"
            format="HH:mm"
            value-format="HH:mm"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="原因">
          <el-input
            v-model="rescheduleForm.reason"
            type="textarea"
            :rows="3"
            placeholder="请输入重新安排的原因"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="rescheduleDialogVisible = false">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="rescheduleLoading"
            @click="confirmReschedule"
          >
            确认重新安排
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  ArrowDown,
  Edit,
  Check,
  CircleCheck,
  Clock,
  Close,
  Delete,
  Printer,
  Calendar,
  User,
  Document,
  Operation,
  Phone,
  Message,
  Bell,
  Share,
  Connection,
  DataAnalysis,
  View
} from '@element-plus/icons-vue'
import { appointmentsApi } from '@/api/appointments'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(true)
const rescheduleLoading = ref(false)
const rescheduleDialogVisible = ref(false)
const appointment = ref(null)
const relatedAppointments = ref([])
const customerStats = ref(null)

// 表单引用
const rescheduleFormRef = ref()

// 重新安排表单
const rescheduleForm = reactive({
  date: '',
  time: '',
  reason: ''
})

// 表单验证规则
const rescheduleRules = {
  date: [
    { required: true, message: '请选择新日期', trigger: 'change' }
  ],
  time: [
    { required: true, message: '请选择新时间', trigger: 'change' }
  ]
}

// 计算属性
const appointmentId = computed(() => route.params.id)

const canEdit = computed(() => {
  return appointment.value && ['pending', 'confirmed'].includes(appointment.value.status)
})

const canReschedule = computed(() => {
  return appointment.value && ['pending', 'confirmed'].includes(appointment.value.status)
})

const canCancel = computed(() => {
  return appointment.value && ['pending', 'confirmed'].includes(appointment.value.status)
})

const canDelete = computed(() => {
  return appointment.value && ['cancelled', 'completed'].includes(appointment.value.status)
})

// 方法
const loadAppointment = async () => {
  loading.value = true
  try {
    const response = await appointmentsApi.getAppointment(appointmentId.value)
    appointment.value = response.data
    
    // 加载相关数据
    await Promise.all([
      loadRelatedAppointments(),
      loadCustomerStats()
    ])
  } catch (error) {
    ElMessage.error('加载预约详情失败')
    console.error('加载预约失败:', error)
  } finally {
    loading.value = false
  }
}

const loadRelatedAppointments = async () => {
  if (!appointment.value?.customer?.id) return
  
  try {
    const response = await appointmentsApi.getAppointments({
      customer_id: appointment.value.customer.id,
      exclude_id: appointmentId.value,
      page_size: 5
    })
    relatedAppointments.value = response.data.results || []
  } catch (error) {
    console.error('加载相关预约失败:', error)
  }
}

const loadCustomerStats = async () => {
  if (!appointment.value?.customer?.id) return
  
  try {
    const response = await appointmentsApi.getCustomerStats(appointment.value.customer.id)
    customerStats.value = response.data
  } catch (error) {
    console.error('加载客户统计失败:', error)
  }
}

const goBack = () => {
  router.back()
}

const handleAction = async (command) => {
  switch (command) {
    case 'edit':
      editAppointment()
      break
    case 'confirm':
      await confirmAppointment()
      break
    case 'complete':
      await completeAppointment()
      break
    case 'reschedule':
      showRescheduleDialog()
      break
    case 'cancel':
      await cancelAppointment()
      break
    case 'delete':
      await deleteAppointment()
      break
  }
}

const editAppointment = () => {
  router.push(`/appointments/${appointmentId.value}/edit`)
}

const confirmAppointment = async () => {
  try {
    await appointmentsApi.confirmAppointment(appointmentId.value)
    ElMessage.success('预约确认成功')
    await loadAppointment()
  } catch (error) {
    ElMessage.error(error.message || '确认预约失败')
  }
}

const completeAppointment = async () => {
  try {
    await appointmentsApi.completeAppointment(appointmentId.value)
    ElMessage.success('预约完成')
    await loadAppointment()
  } catch (error) {
    ElMessage.error(error.message || '完成预约失败')
  }
}

const showRescheduleDialog = () => {
  Object.assign(rescheduleForm, {
    date: '',
    time: '',
    reason: ''
  })
  rescheduleDialogVisible.value = true
}

const confirmReschedule = async () => {
  if (!rescheduleFormRef.value) return
  
  try {
    const valid = await rescheduleFormRef.value.validate()
    if (!valid) return
    
    rescheduleLoading.value = true
    
    const data = {
      scheduled_time: `${rescheduleForm.date} ${rescheduleForm.time}`,
      reschedule_reason: rescheduleForm.reason
    }
    
    await appointmentsApi.rescheduleAppointment(appointmentId.value, data)
    
    ElMessage.success('预约重新安排成功')
    rescheduleDialogVisible.value = false
    await loadAppointment()
  } catch (error) {
    ElMessage.error(error.message || '重新安排失败')
  } finally {
    rescheduleLoading.value = false
  }
}

const cancelAppointment = async () => {
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
    
    await appointmentsApi.cancelAppointment(appointmentId.value)
    ElMessage.success('预约已取消')
    await loadAppointment()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '取消预约失败')
    }
  }
}

const deleteAppointment = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个预约吗？删除后无法恢复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await appointmentsApi.deleteAppointment(appointmentId.value)
    ElMessage.success('预约已删除')
    router.push('/appointments')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除预约失败')
    }
  }
}

const printAppointment = () => {
  window.print()
}

const viewCustomer = () => {
  if (appointment.value?.customer?.id) {
    router.push(`/customers/${appointment.value.customer.id}`)
  }
}

const viewRelatedAppointment = (id) => {
  router.push(`/appointments/${id}`)
}

const callCustomer = () => {
  if (appointment.value?.customer?.phone) {
    window.open(`tel:${appointment.value.customer.phone}`)
  }
}

const sendMessage = () => {
  // 实现发送消息功能
  ElMessage.info('发送消息功能开发中')
}

const setReminder = () => {
  // 实现设置提醒功能
  ElMessage.info('设置提醒功能开发中')
}

const shareAppointment = () => {
  // 实现分享功能
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    ElMessage.success('预约链接已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7
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

const getServiceTypeColor = (type) => {
  const colorMap = {
    consultation: 'primary',
    interview: 'success',
    analysis: 'warning',
    report: 'info'
  }
  return colorMap[type] || 'info'
}

const getServiceTypeText = (type) => {
  const textMap = {
    consultation: '咨询服务',
    interview: '深度访谈',
    analysis: '数据分析',
    report: '报告解读'
  }
  return textMap[type] || type
}

const getLocationText = (location) => {
  const textMap = {
    office: '办公室',
    online: '线上会议',
    customer_site: '客户现场'
  }
  return textMap[location] || location
}

const getGenderText = (gender) => {
  return gender === 'male' ? '男' : '女'
}

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD')
}

const formatTime = (date) => {
  return dayjs(date).format('HH:mm')
}

const formatDateTime = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 组件挂载时加载数据
onMounted(() => {
  loadAppointment()
})
</script>

<style lang="scss" scoped>
.appointment-detail {
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

.loading-container,
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.appointment-content {
  .info-card {
    margin-bottom: 20px;
    
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
    
    .appointment-time {
      .date {
        font-weight: 500;
        color: var(--el-text-color-primary);
        margin-bottom: 2px;
      }
      
      .time {
        font-size: 12px;
        color: var(--el-text-color-secondary);
      }
    }
    
    .notes-content {
      line-height: 1.6;
      color: var(--el-text-color-regular);
    }
    
    .service-record {
      .record-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        
        .record-type {
          font-weight: 500;
          color: var(--el-text-color-primary);
        }
        
        .record-status {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
      
      .record-content {
        color: var(--el-text-color-regular);
        line-height: 1.6;
        margin-bottom: 8px;
      }
      
      .record-meta {
        font-size: 12px;
        color: var(--el-text-color-secondary);
      }
    }
  }
}

.action-card {
  margin-bottom: 20px;
  
  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
  
  .quick-actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
    
    .action-btn {
      width: 100%;
      justify-content: flex-start;
    }
  }
}

.related-card {
  margin-bottom: 20px;
  
  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
  
  .related-appointments {
    .related-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px;
      border-radius: 6px;
      cursor: pointer;
      transition: background-color 0.2s;
      
      &:hover {
        background: var(--el-fill-color-lighter);
      }
      
      &:not(:last-child) {
        margin-bottom: 8px;
      }
      
      .related-info {
        .related-time {
          font-weight: 500;
          color: var(--el-text-color-primary);
          margin-bottom: 2px;
        }
        
        .related-type {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }
}

.stats-card {
  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
  
  .stats-content {
    .stat-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid var(--el-border-color-lighter);
      
      &:last-child {
        border-bottom: none;
      }
      
      .stat-label {
        color: var(--el-text-color-secondary);
        font-size: 14px;
      }
      
      .stat-value {
        font-weight: 500;
        color: var(--el-text-color-primary);
      }
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 打印样式
@media print {
  .page-header .page-actions,
  .action-card,
  .related-card {
    display: none;
  }
  
  .appointment-detail {
    padding: 0;
  }
  
  .info-card {
    box-shadow: none;
    border: 1px solid #ddd;
  }
}

// 响应式适配
@include respond-to(md) {
  .appointment-detail {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
    
    .page-title {
      flex-direction: column;
      gap: 12px;
      align-items: stretch;
    }
    
    .page-actions {
      justify-content: flex-end;
    }
  }
  
  .action-card,
  .related-card,
  .stats-card {
    margin-top: 20px;
  }
  
  .quick-actions {
    .action-btn {
      justify-content: center;
    }
  }
}
</style>