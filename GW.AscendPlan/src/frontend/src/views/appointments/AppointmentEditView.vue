<template>
  <div class="appointment-edit">
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
          <h1>编辑预约</h1>
          <p class="page-description">修改预约的详细信息。</p>
        </div>
      </div>
      
      <div class="page-actions">
        <el-button @click="goBack">
          取消
        </el-button>
        <el-button
          type="primary"
          :loading="submitLoading"
          @click="handleSubmit"
        >
          保存修改
        </el-button>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>
    
    <!-- 编辑表单 -->
    <div v-else-if="appointment" class="edit-content">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="edit-form"
      >
        <el-row :gutter="24">
          <!-- 左侧表单 -->
          <el-col :lg="16" :md="24">
            <!-- 基本信息 -->
            <el-card class="form-card" shadow="never">
              <template #header>
                <div class="card-title">
                  <el-icon><Calendar /></el-icon>
                  <span>预约信息</span>
                </div>
              </template>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="预约日期" prop="date">
                    <el-date-picker
                      v-model="form.date"
                      type="date"
                      placeholder="选择预约日期"
                      :disabled-date="disabledDate"
                      style="width: 100%"
                      @change="onDateChange"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="预约时间" prop="time">
                    <el-time-picker
                      v-model="form.time"
                      placeholder="选择预约时间"
                      format="HH:mm"
                      value-format="HH:mm"
                      style="width: 100%"
                      @change="onTimeChange"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="服务类型" prop="service_type">
                    <el-select
                      v-model="form.service_type"
                      placeholder="选择服务类型"
                      style="width: 100%"
                    >
                      <el-option
                        v-for="type in serviceTypes"
                        :key="type.value"
                        :label="type.label"
                        :value="type.value"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="预计时长" prop="duration">
                    <el-input-number
                      v-model="form.duration"
                      :min="15"
                      :max="480"
                      :step="15"
                      placeholder="分钟"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="服务地点" prop="location">
                <el-radio-group v-model="form.location">
                  <el-radio value="office">办公室</el-radio>
                  <el-radio value="online">线上会议</el-radio>
                  <el-radio value="customer_site">客户现场</el-radio>
                </el-radio-group>
              </el-form-item>
              
              <!-- 线上会议链接 -->
              <el-form-item
                label="会议链接"
                prop="meeting_url"
                v-if="form.location === 'online'"
              >
                <el-input
                  v-model="form.meeting_url"
                  placeholder="请输入会议链接"
                  clearable
                >
                  <template #append>
                    <el-button @click="generateMeetingUrl">
                      生成链接
                    </el-button>
                  </template>
                </el-input>
              </el-form-item>
              
              <!-- 客户现场地址 -->
              <el-form-item
                label="详细地址"
                prop="address"
                v-if="form.location === 'customer_site'"
              >
                <el-input
                  v-model="form.address"
                  type="textarea"
                  :rows="2"
                  placeholder="请输入详细地址"
                  clearable
                />
              </el-form-item>
              
              <el-form-item label="备注信息">
                <el-input
                  v-model="form.notes"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入备注信息"
                  clearable
                />
              </el-form-item>
            </el-card>
            
            <!-- 客户信息 -->
            <el-card class="form-card" shadow="never">
              <template #header>
                <div class="card-title">
                  <el-icon><User /></el-icon>
                  <span>客户信息</span>
                </div>
              </template>
              
              <el-form-item label="选择客户" prop="customer_id">
                <el-select
                  v-model="form.customer_id"
                  placeholder="搜索并选择客户"
                  filterable
                  remote
                  reserve-keyword
                  :remote-method="searchCustomers"
                  :loading="customerSearchLoading"
                  style="width: 100%"
                  @change="onCustomerChange"
                >
                  <el-option
                    v-for="customer in customerOptions"
                    :key="customer.id"
                    :label="`${customer.name} (${customer.phone})`"
                    :value="customer.id"
                  >
                    <div class="customer-option">
                      <div class="customer-name">{{ customer.name }}</div>
                      <div class="customer-info">{{ customer.phone }} | {{ customer.email }}</div>
                    </div>
                  </el-option>
                </el-select>
              </el-form-item>
              
              <!-- 客户详情展示 -->
              <div v-if="selectedCustomer" class="customer-details">
                <el-descriptions :column="2" border>
                  <el-descriptions-item label="客户姓名">
                    {{ selectedCustomer.name }}
                  </el-descriptions-item>
                  
                  <el-descriptions-item label="性别">
                    {{ selectedCustomer.gender === 'male' ? '男' : '女' }}
                  </el-descriptions-item>
                  
                  <el-descriptions-item label="手机号">
                    {{ selectedCustomer.phone }}
                  </el-descriptions-item>
                  
                  <el-descriptions-item label="邮箱">
                    {{ selectedCustomer.email }}
                  </el-descriptions-item>
                  
                  <el-descriptions-item label="年龄">
                    {{ selectedCustomer.age }}岁
                  </el-descriptions-item>
                  
                  <el-descriptions-item label="职业">
                    {{ selectedCustomer.occupation || '-' }}
                  </el-descriptions-item>
                </el-descriptions>
              </div>
            </el-card>
            
            <!-- 提醒设置 -->
            <el-card class="form-card" shadow="never">
              <template #header>
                <div class="card-title">
                  <el-icon><Bell /></el-icon>
                  <span>提醒设置</span>
                </div>
              </template>
              
              <el-form-item label="提醒方式">
                <el-checkbox-group v-model="form.reminder_methods">
                  <el-checkbox value="email">邮件提醒</el-checkbox>
                  <el-checkbox value="sms">短信提醒</el-checkbox>
                  <el-checkbox value="phone">电话提醒</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
              
              <el-form-item label="提醒时间">
                <el-checkbox-group v-model="form.reminder_times">
                  <el-checkbox value="1day">提前1天</el-checkbox>
                  <el-checkbox value="2hours">提前2小时</el-checkbox>
                  <el-checkbox value="30minutes">提前30分钟</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-card>
          </el-col>
          
          <!-- 右侧信息 -->
          <el-col :lg="8" :md="24">
            <!-- 可用时间段 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="card-title">
                  <el-icon><Clock /></el-icon>
                  <span>可用时间段</span>
                </div>
              </template>
              
              <div v-if="availableSlots.length > 0" class="time-slots">
                <div
                  v-for="slot in availableSlots"
                  :key="slot.time"
                  class="time-slot"
                  :class="{ active: form.time === slot.time }"
                  @click="selectTimeSlot(slot.time)"
                >
                  {{ slot.time }}
                </div>
              </div>
              
              <el-empty
                v-else-if="form.date"
                description="当天暂无可用时间段"
                :image-size="80"
              />
              
              <div v-else class="no-date-selected">
                <el-text type="info">请先选择日期</el-text>
              </div>
            </el-card>
            
            <!-- 预约状态 -->
            <el-card class="info-card" shadow="never">
              <template #header>
                <div class="card-title">
                  <el-icon><Flag /></el-icon>
                  <span>预约状态</span>
                </div>
              </template>
              
              <el-form-item label="当前状态">
                <el-tag :type="getStatusType(form.status)" size="large">
                  {{ getStatusText(form.status) }}
                </el-tag>
              </el-form-item>
              
              <el-form-item label="修改状态" v-if="canChangeStatus">
                <el-select
                  v-model="form.status"
                  placeholder="选择新状态"
                  style="width: 100%"
                >
                  <el-option
                    v-for="status in availableStatuses"
                    :key="status.value"
                    :label="status.label"
                    :value="status.value"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item label="状态说明" v-if="form.status !== appointment.status">
                <el-input
                  v-model="form.status_note"
                  type="textarea"
                  :rows="2"
                  placeholder="请输入状态变更说明"
                />
              </el-form-item>
            </el-card>
            
            <!-- 操作历史 -->
            <el-card class="info-card" shadow="never" v-if="appointment.history?.length > 0">
              <template #header>
                <div class="card-title">
                  <el-icon><Document /></el-icon>
                  <span>操作历史</span>
                </div>
              </template>
              
              <el-timeline size="small">
                <el-timeline-item
                  v-for="item in appointment.history"
                  :key="item.id"
                  :timestamp="formatDateTime(item.created_at)"
                  placement="top"
                >
                  <div class="history-item">
                    <div class="history-action">{{ item.action }}</div>
                    <div class="history-note" v-if="item.note">{{ item.note }}</div>
                    <div class="history-operator">操作人：{{ item.operator }}</div>
                  </div>
                </el-timeline-item>
              </el-timeline>
            </el-card>
          </el-col>
        </el-row>
      </el-form>
    </div>
    
    <!-- 错误状态 -->
    <div v-else class="error-container">
      <el-empty description="预约不存在或已被删除">
        <el-button type="primary" @click="goBack">
          返回列表
        </el-button>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  Calendar,
  User,
  Bell,
  Clock,
  Flag,
  Document
} from '@element-plus/icons-vue'
import { appointmentsApi } from '@/api/appointments'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(true)
const submitLoading = ref(false)
const customerSearchLoading = ref(false)
const appointment = ref(null)
const customerOptions = ref([])
const selectedCustomer = ref(null)
const availableSlots = ref([])

// 表单引用
const formRef = ref()

// 表单数据
const form = reactive({
  customer_id: '',
  date: '',
  time: '',
  service_type: '',
  duration: 60,
  location: 'office',
  meeting_url: '',
  address: '',
  notes: '',
  status: '',
  status_note: '',
  reminder_methods: ['email'],
  reminder_times: ['1day', '2hours']
})

// 服务类型选项
const serviceTypes = [
  { label: '咨询服务', value: 'consultation' },
  { label: '深度访谈', value: 'interview' },
  { label: '数据分析', value: 'analysis' },
  { label: '报告解读', value: 'report' }
]

// 表单验证规则
const rules = {
  customer_id: [
    { required: true, message: '请选择客户', trigger: 'change' }
  ],
  date: [
    { required: true, message: '请选择预约日期', trigger: 'change' }
  ],
  time: [
    { required: true, message: '请选择预约时间', trigger: 'change' }
  ],
  service_type: [
    { required: true, message: '请选择服务类型', trigger: 'change' }
  ],
  duration: [
    { required: true, message: '请输入预计时长', trigger: 'blur' }
  ],
  location: [
    { required: true, message: '请选择服务地点', trigger: 'change' }
  ],
  meeting_url: [
    {
      validator: (rule, value, callback) => {
        if (form.location === 'online' && !value) {
          callback(new Error('线上会议需要提供会议链接'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  address: [
    {
      validator: (rule, value, callback) => {
        if (form.location === 'customer_site' && !value) {
          callback(new Error('客户现场需要提供详细地址'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 计算属性
const appointmentId = computed(() => route.params.id)

const canChangeStatus = computed(() => {
  return appointment.value && ['pending', 'confirmed'].includes(appointment.value.status)
})

const availableStatuses = computed(() => {
  const statuses = [
    { label: '待确认', value: 'pending' },
    { label: '已确认', value: 'confirmed' },
    { label: '已完成', value: 'completed' },
    { label: '已取消', value: 'cancelled' }
  ]
  
  // 根据当前状态过滤可用状态
  if (appointment.value?.status === 'pending') {
    return statuses.filter(s => ['pending', 'confirmed', 'cancelled'].includes(s.value))
  } else if (appointment.value?.status === 'confirmed') {
    return statuses.filter(s => ['confirmed', 'completed', 'cancelled'].includes(s.value))
  }
  
  return statuses
})

// 监听日期变化
watch(() => form.date, (newDate) => {
  if (newDate) {
    loadAvailableSlots()
  } else {
    availableSlots.value = []
  }
})

// 方法
const loadAppointment = async () => {
  loading.value = true
  try {
    const response = await appointmentsApi.getAppointment(appointmentId.value)
    appointment.value = response.data
    
    // 填充表单数据
    const scheduledTime = dayjs(appointment.value.scheduled_time)
    Object.assign(form, {
      customer_id: appointment.value.customer.id,
      date: scheduledTime.format('YYYY-MM-DD'),
      time: scheduledTime.format('HH:mm'),
      service_type: appointment.value.service_type,
      duration: appointment.value.duration,
      location: appointment.value.location,
      meeting_url: appointment.value.meeting_url || '',
      address: appointment.value.address || '',
      notes: appointment.value.notes || '',
      status: appointment.value.status,
      reminder_methods: appointment.value.reminder_methods || ['email'],
      reminder_times: appointment.value.reminder_times || ['1day', '2hours']
    })
    
    // 设置选中的客户
    selectedCustomer.value = appointment.value.customer
    customerOptions.value = [appointment.value.customer]
    
    // 加载可用时间段
    if (form.date) {
      await loadAvailableSlots()
    }
  } catch (error) {
    ElMessage.error('加载预约详情失败')
    console.error('加载预约失败:', error)
  } finally {
    loading.value = false
  }
}

const loadAvailableSlots = async () => {
  if (!form.date) return
  
  try {
    const response = await appointmentsApi.getAvailableSlots({
      date: form.date,
      duration: form.duration,
      exclude_appointment_id: appointmentId.value
    })
    availableSlots.value = response.data
  } catch (error) {
    console.error('加载可用时间段失败:', error)
    availableSlots.value = []
  }
}

const searchCustomers = async (query) => {
  if (!query) {
    customerOptions.value = selectedCustomer.value ? [selectedCustomer.value] : []
    return
  }
  
  customerSearchLoading.value = true
  try {
    const response = await appointmentsApi.searchCustomers({ search: query })
    customerOptions.value = response.data.results || []
  } catch (error) {
    console.error('搜索客户失败:', error)
    customerOptions.value = []
  } finally {
    customerSearchLoading.value = false
  }
}

const onCustomerChange = async (customerId) => {
  if (!customerId) {
    selectedCustomer.value = null
    return
  }
  
  try {
    const response = await appointmentsApi.getCustomer(customerId)
    selectedCustomer.value = response.data
  } catch (error) {
    console.error('获取客户详情失败:', error)
    selectedCustomer.value = null
  }
}

const onDateChange = () => {
  form.time = '' // 清空时间选择
}

const onTimeChange = () => {
  // 时间变化时的处理
}

const selectTimeSlot = (time) => {
  form.time = time
}

const generateMeetingUrl = () => {
  // 生成会议链接的逻辑
  const meetingId = Math.random().toString(36).substr(2, 9)
  form.meeting_url = `https://meet.example.com/${meetingId}`
  ElMessage.success('会议链接已生成')
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
    
    submitLoading.value = true
    
    const data = {
      customer_id: form.customer_id,
      scheduled_time: `${form.date} ${form.time}`,
      service_type: form.service_type,
      duration: form.duration,
      location: form.location,
      meeting_url: form.meeting_url,
      address: form.address,
      notes: form.notes,
      status: form.status,
      status_note: form.status_note,
      reminder_methods: form.reminder_methods,
      reminder_times: form.reminder_times
    }
    
    await appointmentsApi.updateAppointment(appointmentId.value, data)
    
    ElMessage.success('预约修改成功')
    router.push(`/appointments/${appointmentId.value}`)
  } catch (error) {
    ElMessage.error(error.message || '修改预约失败')
  } finally {
    submitLoading.value = false
  }
}

const goBack = () => {
  router.back()
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

const formatDateTime = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 组件挂载时加载数据
onMounted(() => {
  loadAppointment()
})
</script>

<style lang="scss" scoped>
.appointment-edit {
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

.edit-content {
  .edit-form {
    .form-card {
      margin-bottom: 20px;
      
      .card-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }
    }
    
    .customer-option {
      .customer-name {
        font-weight: 500;
        color: var(--el-text-color-primary);
        margin-bottom: 2px;
      }
      
      .customer-info {
        font-size: 12px;
        color: var(--el-text-color-secondary);
      }
    }
    
    .customer-details {
      margin-top: 16px;
    }
  }
}

.info-card {
  margin-bottom: 20px;
  
  .card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
  
  .time-slots {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
    gap: 8px;
    
    .time-slot {
      padding: 8px 12px;
      text-align: center;
      border: 1px solid var(--el-border-color);
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 14px;
      
      &:hover {
        border-color: var(--el-color-primary);
        background: var(--el-color-primary-light-9);
      }
      
      &.active {
        border-color: var(--el-color-primary);
        background: var(--el-color-primary);
        color: white;
      }
    }
  }
  
  .no-date-selected {
    text-align: center;
    padding: 20px;
    color: var(--el-text-color-secondary);
  }
  
  .history-item {
    .history-action {
      font-weight: 500;
      color: var(--el-text-color-primary);
      margin-bottom: 4px;
    }
    
    .history-note {
      color: var(--el-text-color-regular);
      margin-bottom: 4px;
      font-size: 14px;
    }
    
    .history-operator {
      font-size: 12px;
      color: var(--el-text-color-secondary);
    }
  }
}

// 响应式适配
@include respond-to(md) {
  .appointment-edit {
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
  
  .info-card {
    margin-top: 20px;
  }
  
  .time-slots {
    grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
    
    .time-slot {
      padding: 6px 8px;
      font-size: 12px;
    }
  }
}
</style>