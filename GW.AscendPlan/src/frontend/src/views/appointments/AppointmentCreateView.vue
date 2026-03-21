<template>
  <div class="appointment-create">
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
          <h1>创建预约</h1>
          <p class="page-description">为客户创建新的预约，填写完整信息以确保服务质量。</p>
        </div>
      </div>
    </div>
    
    <el-row :gutter="24">
      <!-- 主表单区域 -->
      <el-col :lg="16" :md="24">
        <el-card class="form-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span class="card-title">预约信息</span>
              <el-steps :active="currentStep" simple>
                <el-step title="客户信息" />
                <el-step title="预约详情" />
                <el-step title="确认提交" />
              </el-steps>
            </div>
          </template>
          
          <el-form
            ref="appointmentFormRef"
            :model="appointmentForm"
            :rules="appointmentRules"
            label-width="100px"
            class="appointment-form"
          >
            <!-- 步骤1: 客户信息 -->
            <div v-show="currentStep === 0" class="form-step">
              <div class="step-title">
                <el-icon><User /></el-icon>
                <span>客户信息</span>
              </div>
              
              <el-form-item label="选择客户" prop="customer_id">
                <div class="customer-selector">
                  <el-select
                    v-model="appointmentForm.customer_id"
                    placeholder="搜索并选择客户"
                    filterable
                    remote
                    reserve-keyword
                    :remote-method="searchCustomers"
                    :loading="customerLoading"
                    style="width: 100%"
                    @change="handleCustomerChange"
                  >
                    <el-option
                      v-for="customer in customers"
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
                  <el-button
                    type="primary"
                    :icon="Plus"
                    @click="showCreateCustomerDialog"
                    class="create-customer-btn"
                  >
                    新建客户
                  </el-button>
                </div>
              </el-form-item>
              
              <!-- 选中客户信息展示 -->
              <div v-if="selectedCustomer" class="selected-customer">
                <el-descriptions title="客户详情" :column="2" border>
                  <el-descriptions-item label="姓名">{{ selectedCustomer.name }}</el-descriptions-item>
                  <el-descriptions-item label="性别">{{ getGenderText(selectedCustomer.gender) }}</el-descriptions-item>
                  <el-descriptions-item label="手机号">{{ selectedCustomer.phone }}</el-descriptions-item>
                  <el-descriptions-item label="邮箱">{{ selectedCustomer.email }}</el-descriptions-item>
                  <el-descriptions-item label="年龄">{{ selectedCustomer.age }}岁</el-descriptions-item>
                  <el-descriptions-item label="职业">{{ selectedCustomer.occupation || '-' }}</el-descriptions-item>
                  <el-descriptions-item label="地址" :span="2">{{ selectedCustomer.address || '-' }}</el-descriptions-item>
                </el-descriptions>
              </div>
            </div>
            
            <!-- 步骤2: 预约详情 -->
            <div v-show="currentStep === 1" class="form-step">
              <div class="step-title">
                <el-icon><Calendar /></el-icon>
                <span>预约详情</span>
              </div>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="预约日期" prop="date">
                    <el-date-picker
                      v-model="appointmentForm.date"
                      type="date"
                      placeholder="选择预约日期"
                      :disabled-date="disabledDate"
                      style="width: 100%"
                      @change="handleDateChange"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="预约时间" prop="time">
                    <el-select
                      v-model="appointmentForm.time"
                      placeholder="选择预约时间"
                      style="width: 100%"
                      :loading="timeSlotLoading"
                    >
                      <el-option
                        v-for="slot in availableTimeSlots"
                        :key="slot.value"
                        :label="slot.label"
                        :value="slot.value"
                        :disabled="slot.disabled"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="服务类型" prop="service_type">
                    <el-select
                      v-model="appointmentForm.service_type"
                      placeholder="选择服务类型"
                      style="width: 100%"
                      @change="handleServiceTypeChange"
                    >
                      <el-option label="咨询服务" value="consultation" />
                      <el-option label="深度访谈" value="interview" />
                      <el-option label="数据分析" value="analysis" />
                      <el-option label="报告解读" value="report" />
                    </el-select>
                  </el-form-item>
                </el-col>
                
                <el-col :span="12">
                  <el-form-item label="预计时长" prop="duration">
                    <el-input-number
                      v-model="appointmentForm.duration"
                      :min="30"
                      :max="240"
                      :step="30"
                      placeholder="分钟"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
              
              <el-form-item label="服务地点" prop="location">
                <el-radio-group v-model="appointmentForm.location">
                  <el-radio label="office">办公室</el-radio>
                  <el-radio label="online">线上会议</el-radio>
                  <el-radio label="customer_site">客户现场</el-radio>
                </el-radio-group>
              </el-form-item>
              
              <el-form-item label="会议链接" prop="meeting_url" v-if="appointmentForm.location === 'online'">
                <el-input
                  v-model="appointmentForm.meeting_url"
                  placeholder="请输入会议链接（如腾讯会议、钉钉等）"
                />
              </el-form-item>
              
              <el-form-item label="详细地址" prop="address" v-if="appointmentForm.location === 'customer_site'">
                <el-input
                  v-model="appointmentForm.address"
                  type="textarea"
                  :rows="2"
                  placeholder="请输入详细地址"
                />
              </el-form-item>
              
              <el-form-item label="备注信息">
                <el-input
                  v-model="appointmentForm.notes"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入备注信息，如特殊需求、准备材料等"
                  maxlength="500"
                  show-word-limit
                />
              </el-form-item>
              
              <el-form-item label="提醒设置">
                <el-checkbox-group v-model="appointmentForm.reminders">
                  <el-checkbox label="email">邮件提醒</el-checkbox>
                  <el-checkbox label="sms">短信提醒</el-checkbox>
                  <el-checkbox label="system">系统通知</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </div>
            
            <!-- 步骤3: 确认提交 -->
            <div v-show="currentStep === 2" class="form-step">
              <div class="step-title">
                <el-icon><CircleCheck /></el-icon>
                <span>确认信息</span>
              </div>
              
              <div class="confirmation-content">
                <el-alert
                  title="请仔细核对预约信息"
                  type="info"
                  :closable="false"
                  show-icon
                  class="confirmation-alert"
                />
                
                <el-descriptions title="预约确认" :column="1" border>
                  <el-descriptions-item label="客户姓名">
                    {{ selectedCustomer?.name }}
                  </el-descriptions-item>
                  <el-descriptions-item label="联系方式">
                    {{ selectedCustomer?.phone }}
                  </el-descriptions-item>
                  <el-descriptions-item label="预约时间">
                    {{ formatAppointmentTime() }}
                  </el-descriptions-item>
                  <el-descriptions-item label="服务类型">
                    {{ getServiceTypeText(appointmentForm.service_type) }}
                  </el-descriptions-item>
                  <el-descriptions-item label="预计时长">
                    {{ appointmentForm.duration }}分钟
                  </el-descriptions-item>
                  <el-descriptions-item label="服务地点">
                    {{ getLocationText(appointmentForm.location) }}
                  </el-descriptions-item>
                  <el-descriptions-item label="会议链接" v-if="appointmentForm.location === 'online'">
                    {{ appointmentForm.meeting_url || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="详细地址" v-if="appointmentForm.location === 'customer_site'">
                    {{ appointmentForm.address || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="备注信息">
                    {{ appointmentForm.notes || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="提醒方式">
                    {{ getReminderText() }}
                  </el-descriptions-item>
                </el-descriptions>
              </div>
            </div>
          </el-form>
          
          <!-- 表单操作按钮 -->
          <div class="form-actions">
            <el-button
              v-if="currentStep > 0"
              @click="prevStep"
              :icon="ArrowLeft"
            >
              上一步
            </el-button>
            
            <el-button
              v-if="currentStep < 2"
              type="primary"
              @click="nextStep"
              :icon="ArrowRight"
            >
              下一步
            </el-button>
            
            <el-button
              v-if="currentStep === 2"
              type="primary"
              :loading="submitLoading"
              @click="submitAppointment"
              :icon="Check"
            >
              确认创建
            </el-button>
            
            <el-button @click="goBack">
              取消
            </el-button>
          </div>
        </el-card>
      </el-col>
      
      <!-- 侧边栏信息 -->
      <el-col :lg="8" :md="24">
        <el-card class="info-card" shadow="never">
          <template #header>
            <span class="card-title">预约须知</span>
          </template>
          
          <div class="info-content">
            <el-timeline>
              <el-timeline-item
                timestamp="预约前"
                placement="top"
                type="primary"
              >
                <div class="timeline-content">
                  <h4>准备工作</h4>
                  <ul>
                    <li>确认客户联系方式</li>
                    <li>了解客户基本需求</li>
                    <li>准备相关资料</li>
                  </ul>
                </div>
              </el-timeline-item>
              
              <el-timeline-item
                timestamp="预约中"
                placement="top"
                type="success"
              >
                <div class="timeline-content">
                  <h4>服务流程</h4>
                  <ul>
                    <li>按时到达或准时上线</li>
                    <li>专业服务态度</li>
                    <li>详细记录服务内容</li>
                  </ul>
                </div>
              </el-timeline-item>
              
              <el-timeline-item
                timestamp="预约后"
                placement="top"
                type="warning"
              >
                <div class="timeline-content">
                  <h4>后续跟进</h4>
                  <ul>
                    <li>及时更新预约状态</li>
                    <li>收集客户反馈</li>
                    <li>安排后续服务</li>
                  </ul>
                </div>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
        
        <!-- 快速操作 -->
        <el-card class="quick-actions-card" shadow="never">
          <template #header>
            <span class="card-title">快速操作</span>
          </template>
          
          <div class="quick-actions">
            <el-button
              type="primary"
              :icon="User"
              @click="showCreateCustomerDialog"
              class="quick-action-btn"
            >
              新建客户
            </el-button>
            
            <el-button
              type="success"
              :icon="Calendar"
              @click="viewCalendar"
              class="quick-action-btn"
            >
              查看日历
            </el-button>
            
            <el-button
              type="info"
              :icon="Document"
              @click="viewTemplates"
              class="quick-action-btn"
            >
              服务模板
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 新建客户对话框 -->
    <el-dialog
      v-model="createCustomerDialogVisible"
      title="新建客户"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="customerFormRef"
        :model="customerForm"
        :rules="customerRules"
        label-width="80px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="customerForm.name" placeholder="请输入客户姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="customerForm.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="customerForm.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number
                v-model="customerForm.age"
                :min="1"
                :max="120"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="customerForm.email" placeholder="请输入邮箱地址" />
        </el-form-item>
        
        <el-form-item label="职业">
          <el-input v-model="customerForm.occupation" placeholder="请输入职业" />
        </el-form-item>
        
        <el-form-item label="地址">
          <el-input
            v-model="customerForm.address"
            type="textarea"
            :rows="2"
            placeholder="请输入详细地址"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="createCustomerDialogVisible = false">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="createCustomerLoading"
            @click="createCustomer"
          >
            确认创建
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  ArrowRight,
  Plus,
  User,
  Calendar,
  CircleCheck,
  Check,
  Document
} from '@element-plus/icons-vue'
import { appointmentsApi } from '@/api/appointments'
import dayjs from 'dayjs'

const router = useRouter()

// 响应式数据
const currentStep = ref(0)
const submitLoading = ref(false)
const customerLoading = ref(false)
const timeSlotLoading = ref(false)
const createCustomerLoading = ref(false)
const createCustomerDialogVisible = ref(false)

const customers = ref([])
const selectedCustomer = ref(null)
const availableTimeSlots = ref([])

// 表单引用
const appointmentFormRef = ref()
const customerFormRef = ref()

// 预约表单
const appointmentForm = reactive({
  customer_id: '',
  date: '',
  time: '',
  service_type: '',
  duration: 60,
  location: 'office',
  meeting_url: '',
  address: '',
  notes: '',
  reminders: ['email', 'system']
})

// 客户表单
const customerForm = reactive({
  name: '',
  gender: 'male',
  phone: '',
  email: '',
  age: null,
  occupation: '',
  address: ''
})

// 表单验证规则
const appointmentRules = {
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
    { required: true, message: '请输入会议链接', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入详细地址', trigger: 'blur' }
  ]
}

const customerRules = {
  name: [
    { required: true, message: '请输入客户姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ]
}

// 方法
const goBack = () => {
  router.back()
}

const nextStep = async () => {
  if (!appointmentFormRef.value) return
  
  // 验证当前步骤的表单
  const fieldsToValidate = getStepFields(currentStep.value)
  try {
    await appointmentFormRef.value.validateField(fieldsToValidate)
    currentStep.value++
  } catch (error) {
    console.log('验证失败:', error)
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const getStepFields = (step) => {
  const stepFieldsMap = {
    0: ['customer_id'],
    1: ['date', 'time', 'service_type', 'duration', 'location']
  }
  return stepFieldsMap[step] || []
}

const searchCustomers = async (query) => {
  if (!query) {
    customers.value = []
    return
  }
  
  customerLoading.value = true
  try {
    const response = await appointmentsApi.searchCustomers({ search: query })
    customers.value = response.data.results || []
  } catch (error) {
    console.error('搜索客户失败:', error)
  } finally {
    customerLoading.value = false
  }
}

const handleCustomerChange = async (customerId) => {
  if (!customerId) {
    selectedCustomer.value = null
    return
  }
  
  try {
    const response = await appointmentsApi.getCustomer(customerId)
    selectedCustomer.value = response.data
  } catch (error) {
    ElMessage.error('获取客户信息失败')
    console.error('获取客户信息失败:', error)
  }
}

const handleDateChange = async (date) => {
  if (!date) {
    availableTimeSlots.value = []
    return
  }
  
  await loadAvailableTimeSlots(date)
}

const loadAvailableTimeSlots = async (date) => {
  timeSlotLoading.value = true
  try {
    const response = await appointmentsApi.getAvailableTimeSlots({
      date: dayjs(date).format('YYYY-MM-DD')
    })
    
    availableTimeSlots.value = response.data.map(slot => ({
      value: slot.time,
      label: slot.time,
      disabled: !slot.available
    }))
  } catch (error) {
    ElMessage.error('获取可用时间段失败')
    console.error('获取时间段失败:', error)
  } finally {
    timeSlotLoading.value = false
  }
}

const handleServiceTypeChange = (serviceType) => {
  // 根据服务类型设置默认时长
  const durationMap = {
    consultation: 60,
    interview: 120,
    analysis: 90,
    report: 60
  }
  
  appointmentForm.duration = durationMap[serviceType] || 60
}

const showCreateCustomerDialog = () => {
  // 重置表单
  Object.assign(customerForm, {
    name: '',
    gender: 'male',
    phone: '',
    email: '',
    age: null,
    occupation: '',
    address: ''
  })
  
  createCustomerDialogVisible.value = true
}

const createCustomer = async () => {
  if (!customerFormRef.value) return
  
  try {
    const valid = await customerFormRef.value.validate()
    if (!valid) return
    
    createCustomerLoading.value = true
    
    const response = await appointmentsApi.createCustomer(customerForm)
    
    ElMessage.success('客户创建成功')
    createCustomerDialogVisible.value = false
    
    // 自动选择新创建的客户
    appointmentForm.customer_id = response.data.id
    selectedCustomer.value = response.data
    
    // 添加到客户列表
    customers.value.unshift(response.data)
  } catch (error) {
    ElMessage.error(error.message || '创建客户失败')
  } finally {
    createCustomerLoading.value = false
  }
}

const submitAppointment = async () => {
  if (!appointmentFormRef.value) return
  
  try {
    const valid = await appointmentFormRef.value.validate()
    if (!valid) return
    
    submitLoading.value = true
    
    const data = {
      ...appointmentForm,
      scheduled_time: `${appointmentForm.date} ${appointmentForm.time}`
    }
    
    // 移除不需要的字段
    delete data.date
    delete data.time
    
    await appointmentsApi.createAppointment(data)
    
    ElMessage.success('预约创建成功')
    router.push('/appointments')
  } catch (error) {
    ElMessage.error(error.message || '创建预约失败')
  } finally {
    submitLoading.value = false
  }
}

const viewCalendar = () => {
  router.push('/appointments?view=calendar')
}

const viewTemplates = () => {
  router.push('/templates')
}

const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7
}

const formatAppointmentTime = () => {
  if (!appointmentForm.date || !appointmentForm.time) return '-'
  return `${dayjs(appointmentForm.date).format('YYYY年MM月DD日')} ${appointmentForm.time}`
}

const getGenderText = (gender) => {
  return gender === 'male' ? '男' : '女'
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

const getReminderText = () => {
  const reminderMap = {
    email: '邮件',
    sms: '短信',
    system: '系统通知'
  }
  
  return appointmentForm.reminders
    .map(reminder => reminderMap[reminder])
    .join('、') || '无'
}

// 监听表单变化
watch(
  () => appointmentForm.location,
  (newLocation) => {
    // 清空相关字段
    if (newLocation !== 'online') {
      appointmentForm.meeting_url = ''
    }
    if (newLocation !== 'customer_site') {
      appointmentForm.address = ''
    }
  }
)

// 组件挂载时初始化
onMounted(() => {
  // 可以在这里加载一些初始数据
})
</script>

<style lang="scss" scoped>
.appointment-create {
  padding: 24px;
  background: var(--el-bg-color-page);
  min-height: calc(100vh - #{$header-height});
}

.page-header {
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
}

.form-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .card-title {
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }
  
  .appointment-form {
    .form-step {
      .step-title {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 24px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--el-border-color-lighter);
        font-size: 16px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }
    }
  }
  
  .customer-selector {
    display: flex;
    gap: 12px;
    
    .create-customer-btn {
      flex-shrink: 0;
    }
  }
  
  .selected-customer {
    margin-top: 20px;
  }
  
  .confirmation-content {
    .confirmation-alert {
      margin-bottom: 20px;
    }
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 32px;
    padding-top: 20px;
    border-top: 1px solid var(--el-border-color-lighter);
  }
}

.customer-option {
  .customer-name {
    font-weight: 500;
    color: var(--el-text-color-primary);
  }
  
  .customer-info {
    font-size: 12px;
    color: var(--el-text-color-secondary);
    margin-top: 2px;
  }
}

.info-card {
  margin-bottom: 20px;
  
  .card-title {
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
  
  .info-content {
    .timeline-content {
      h4 {
        margin: 0 0 8px 0;
        font-size: 14px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }
      
      ul {
        margin: 0;
        padding-left: 16px;
        
        li {
          font-size: 13px;
          color: var(--el-text-color-secondary);
          line-height: 1.6;
          margin-bottom: 4px;
        }
      }
    }
  }
}

.quick-actions-card {
  .card-title {
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
  
  .quick-actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
    
    .quick-action-btn {
      width: 100%;
      justify-content: flex-start;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 响应式适配
@include respond-to(lg) {
  .info-card,
  .quick-actions-card {
    margin-top: 20px;
  }
}

@include respond-to(md) {
  .appointment-create {
    padding: 16px;
  }
  
  .page-header {
    .page-title {
      flex-direction: column;
      gap: 12px;
      align-items: stretch;
    }
  }
  
  .customer-selector {
    flex-direction: column;
    
    .create-customer-btn {
      align-self: flex-start;
    }
  }
  
  .form-actions {
    flex-direction: column-reverse;
    
    .el-button {
      width: 100%;
    }
  }
  
  .quick-actions {
    .quick-action-btn {
      justify-content: center;
    }
  }
}
</style>