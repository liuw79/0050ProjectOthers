<template>
  <div class="customer-edit">
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
          <h1>编辑客户</h1>
          <p class="page-description">修改客户基本信息，更新客户档案。</p>
        </div>
      </div>
      
      <div class="page-actions">
        <el-button
          :icon="View"
          @click="$router.push(`/customers/${customerId}`)"
        >
          查看详情
        </el-button>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>
    
    <!-- 表单内容 -->
    <el-card v-else class="form-card" shadow="never">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="customer-form"
        @submit.prevent="handleSubmit"
      >
        <el-row :gutter="24">
          <!-- 基本信息 -->
          <el-col :span="24">
            <div class="form-section">
              <h3 class="section-title">基本信息</h3>
              
              <el-row :gutter="24">
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="客户姓名" prop="name" required>
                    <el-input
                      v-model="form.name"
                      placeholder="请输入客户姓名"
                      maxlength="50"
                      show-word-limit
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="性别" prop="gender" required>
                    <el-radio-group v-model="form.gender">
                      <el-radio label="male">男</el-radio>
                      <el-radio label="female">女</el-radio>
                    </el-radio-group>
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="年龄" prop="age">
                    <el-input-number
                      v-model="form.age"
                      :min="0"
                      :max="150"
                      placeholder="请输入年龄"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="出生日期" prop="birth_date">
                    <el-date-picker
                      v-model="form.birth_date"
                      type="date"
                      placeholder="选择出生日期"
                      format="YYYY-MM-DD"
                      value-format="YYYY-MM-DD"
                      style="width: 100%"
                      @change="handleBirthDateChange"
                    />
                  </el-date-picker>
                </el-col>
              </el-row>
            </div>
          </el-col>
          
          <!-- 联系信息 -->
          <el-col :span="24">
            <div class="form-section">
              <h3 class="section-title">联系信息</h3>
              
              <el-row :gutter="24">
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="手机号" prop="phone" required>
                    <el-input
                      v-model="form.phone"
                      placeholder="请输入手机号"
                      maxlength="20"
                    >
                      <template #prepend>
                        <el-select
                          v-model="form.phone_country_code"
                          style="width: 80px"
                        >
                          <el-option label="+86" value="+86" />
                          <el-option label="+1" value="+1" />
                          <el-option label="+44" value="+44" />
                          <el-option label="+81" value="+81" />
                          <el-option label="+82" value="+82" />
                        </el-select>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="邮箱" prop="email" required>
                    <el-input
                      v-model="form.email"
                      type="email"
                      placeholder="请输入邮箱地址"
                      maxlength="100"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="微信号" prop="wechat">
                    <el-input
                      v-model="form.wechat"
                      placeholder="请输入微信号"
                      maxlength="50"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="QQ号" prop="qq">
                    <el-input
                      v-model="form.qq"
                      placeholder="请输入QQ号"
                      maxlength="20"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-col>
          
          <!-- 职业信息 -->
          <el-col :span="24">
            <div class="form-section">
              <h3 class="section-title">职业信息</h3>
              
              <el-row :gutter="24">
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="职业" prop="occupation">
                    <el-input
                      v-model="form.occupation"
                      placeholder="请输入职业"
                      maxlength="100"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="公司" prop="company">
                    <el-input
                      v-model="form.company"
                      placeholder="请输入公司名称"
                      maxlength="100"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="职位" prop="position">
                    <el-input
                      v-model="form.position"
                      placeholder="请输入职位"
                      maxlength="100"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="行业" prop="industry">
                    <el-select
                      v-model="form.industry"
                      placeholder="请选择行业"
                      filterable
                      allow-create
                      style="width: 100%"
                    >
                      <el-option
                        v-for="industry in industries"
                        :key="industry"
                        :label="industry"
                        :value="industry"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-col>
          
          <!-- 地址信息 -->
          <el-col :span="24">
            <div class="form-section">
              <h3 class="section-title">地址信息</h3>
              
              <el-row :gutter="24">
                <el-col :xl="8" :lg="8" :md="24" :sm="24">
                  <el-form-item label="省份" prop="province">
                    <el-select
                      v-model="form.province"
                      placeholder="请选择省份"
                      filterable
                      style="width: 100%"
                      @change="handleProvinceChange"
                    >
                      <el-option
                        v-for="province in provinces"
                        :key="province.code"
                        :label="province.name"
                        :value="province.code"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                
                <el-col :xl="8" :lg="8" :md="24" :sm="24">
                  <el-form-item label="城市" prop="city">
                    <el-select
                      v-model="form.city"
                      placeholder="请选择城市"
                      filterable
                      style="width: 100%"
                      @change="handleCityChange"
                    >
                      <el-option
                        v-for="city in cities"
                        :key="city.code"
                        :label="city.name"
                        :value="city.code"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                
                <el-col :xl="8" :lg="8" :md="24" :sm="24">
                  <el-form-item label="区县" prop="district">
                    <el-select
                      v-model="form.district"
                      placeholder="请选择区县"
                      filterable
                      style="width: 100%"
                    >
                      <el-option
                        v-for="district in districts"
                        :key="district.code"
                        :label="district.name"
                        :value="district.code"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                
                <el-col :span="24">
                  <el-form-item label="详细地址" prop="address">
                    <el-input
                      v-model="form.address"
                      type="textarea"
                      :rows="3"
                      placeholder="请输入详细地址"
                      maxlength="200"
                      show-word-limit
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-col>
          
          <!-- 其他信息 -->
          <el-col :span="24">
            <div class="form-section">
              <h3 class="section-title">其他信息</h3>
              
              <el-row :gutter="24">
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="客户来源" prop="source">
                    <el-select
                      v-model="form.source"
                      placeholder="请选择客户来源"
                      style="width: 100%"
                    >
                      <el-option label="线上推广" value="online" />
                      <el-option label="朋友推荐" value="referral" />
                      <el-option label="线下活动" value="offline" />
                      <el-option label="老客户介绍" value="existing_customer" />
                      <el-option label="其他" value="other" />
                    </el-select>
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="客户标签" prop="tags">
                    <el-select
                      v-model="form.tags"
                      multiple
                      filterable
                      allow-create
                      placeholder="请选择或输入客户标签"
                      style="width: 100%"
                    >
                      <el-option
                        v-for="tag in customerTags"
                        :key="tag"
                        :label="tag"
                        :value="tag"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                
                <el-col :span="24">
                  <el-form-item label="备注" prop="notes">
                    <el-input
                      v-model="form.notes"
                      type="textarea"
                      :rows="4"
                      placeholder="请输入备注信息"
                      maxlength="500"
                      show-word-limit
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-col>
          
          <!-- 系统信息 -->
          <el-col :span="24">
            <div class="form-section">
              <h3 class="section-title">系统信息</h3>
              
              <el-row :gutter="24">
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="注册时间">
                    <el-input
                      :value="formatDate(customerData?.created_at)"
                      readonly
                      placeholder="--"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="更新时间">
                    <el-input
                      :value="formatDate(customerData?.updated_at)"
                      readonly
                      placeholder="--"
                    />
                  </el-form-item>
                </el-col>
                
                <el-col :xl="12" :lg="12" :md="24" :sm="24">
                  <el-form-item label="客户状态">
                    <el-select
                      v-model="form.status"
                      placeholder="请选择客户状态"
                      style="width: 100%"
                    >
                      <el-option label="活跃" value="active" />
                      <el-option label="非活跃" value="inactive" />
                      <el-option label="已删除" value="deleted" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
            </div>
          </el-col>
        </el-row>
        
        <!-- 表单操作 -->
        <div class="form-actions">
          <el-button @click="$router.back()">
            取消
          </el-button>
          
          <el-button
            type="primary"
            :loading="submitting"
            @click="handleSubmit"
          >
            {{ submitting ? '保存中...' : '保存修改' }}
          </el-button>
          
          <el-button
            type="success"
            @click="handleCreateAppointment"
          >
            创建预约
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, View } from '@element-plus/icons-vue'
import { appointmentsApi } from '@/api/appointments'
import dayjs from 'dayjs'

const router = useRouter()
const route = useRoute()

// 响应式数据
const formRef = ref()
const loading = ref(true)
const submitting = ref(false)
const customerData = ref(null)
const customerId = computed(() => route.params.id)

// 表单数据
const form = reactive({
  name: '',
  gender: 'male',
  age: null,
  birth_date: '',
  phone: '',
  phone_country_code: '+86',
  email: '',
  wechat: '',
  qq: '',
  occupation: '',
  company: '',
  position: '',
  industry: '',
  province: '',
  city: '',
  district: '',
  address: '',
  source: '',
  tags: [],
  notes: '',
  status: 'active'
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入客户姓名', trigger: 'blur' },
    { min: 2, max: 50, message: '姓名长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  age: [
    { type: 'number', min: 0, max: 150, message: '年龄必须在 0 到 150 之间', trigger: 'blur' }
  ]
}

// 选项数据
const industries = ref([
  '互联网/电商',
  '金融/投资',
  '房地产/建筑',
  '教育/培训',
  '医疗/健康',
  '制造业',
  '服务业',
  '政府/非营利',
  '媒体/广告',
  '咨询/专业服务',
  '零售/贸易',
  '交通/物流',
  '能源/环保',
  '文化/娱乐',
  '其他'
])

const customerTags = ref([
  'VIP客户',
  '潜在客户',
  '老客户',
  '高价值客户',
  '活跃客户',
  '重点关注',
  '需要跟进',
  '满意度高',
  '推荐客户'
])

// 地区数据（简化版，实际项目中应该从API获取）
const provinces = ref([
  { code: '110000', name: '北京市' },
  { code: '120000', name: '天津市' },
  { code: '130000', name: '河北省' },
  { code: '140000', name: '山西省' },
  { code: '150000', name: '内蒙古自治区' },
  { code: '210000', name: '辽宁省' },
  { code: '220000', name: '吉林省' },
  { code: '230000', name: '黑龙江省' },
  { code: '310000', name: '上海市' },
  { code: '320000', name: '江苏省' },
  { code: '330000', name: '浙江省' },
  { code: '340000', name: '安徽省' },
  { code: '350000', name: '福建省' },
  { code: '360000', name: '江西省' },
  { code: '370000', name: '山东省' },
  { code: '410000', name: '河南省' },
  { code: '420000', name: '湖北省' },
  { code: '430000', name: '湖南省' },
  { code: '440000', name: '广东省' },
  { code: '450000', name: '广西壮族自治区' },
  { code: '460000', name: '海南省' },
  { code: '500000', name: '重庆市' },
  { code: '510000', name: '四川省' },
  { code: '520000', name: '贵州省' },
  { code: '530000', name: '云南省' },
  { code: '540000', name: '西藏自治区' },
  { code: '610000', name: '陕西省' },
  { code: '620000', name: '甘肃省' },
  { code: '630000', name: '青海省' },
  { code: '640000', name: '宁夏回族自治区' },
  { code: '650000', name: '新疆维吾尔自治区' }
])

const cities = ref([])
const districts = ref([])

// 计算属性
const fullAddress = computed(() => {
  const parts = []
  if (form.province) {
    const province = provinces.value.find(p => p.code === form.province)
    if (province) parts.push(province.name)
  }
  if (form.city) {
    const city = cities.value.find(c => c.code === form.city)
    if (city) parts.push(city.name)
  }
  if (form.district) {
    const district = districts.value.find(d => d.code === form.district)
    if (district) parts.push(district.name)
  }
  if (form.address) {
    parts.push(form.address)
  }
  return parts.join(' ')
})

// 方法
const formatDate = (date) => {
  return date ? dayjs(date).format('YYYY-MM-DD HH:mm:ss') : '--'
}

const handleBirthDateChange = (date) => {
  if (date) {
    const age = dayjs().diff(dayjs(date), 'year')
    form.age = age
  }
}

const handleProvinceChange = (provinceCode) => {
  form.city = ''
  form.district = ''
  cities.value = []
  districts.value = []
  
  if (provinceCode) {
    loadCities(provinceCode)
  }
}

const handleCityChange = (cityCode) => {
  form.district = ''
  districts.value = []
  
  if (cityCode) {
    loadDistricts(cityCode)
  }
}

const loadCities = (provinceCode) => {
  // 模拟数据，实际项目中应该从API获取
  const cityData = {
    '110000': [
      { code: '110100', name: '北京市' }
    ],
    '310000': [
      { code: '310100', name: '上海市' }
    ],
    '440000': [
      { code: '440100', name: '广州市' },
      { code: '440300', name: '深圳市' },
      { code: '440600', name: '佛山市' },
      { code: '441900', name: '东莞市' }
    ]
  }
  
  cities.value = cityData[provinceCode] || []
}

const loadDistricts = (cityCode) => {
  // 模拟数据，实际项目中应该从API获取
  const districtData = {
    '110100': [
      { code: '110101', name: '东城区' },
      { code: '110102', name: '西城区' },
      { code: '110105', name: '朝阳区' },
      { code: '110106', name: '丰台区' },
      { code: '110107', name: '石景山区' },
      { code: '110108', name: '海淀区' }
    ],
    '440100': [
      { code: '440103', name: '荔湾区' },
      { code: '440104', name: '越秀区' },
      { code: '440105', name: '海珠区' },
      { code: '440106', name: '天河区' },
      { code: '440111', name: '白云区' },
      { code: '440112', name: '黄埔区' }
    ]
  }
  
  districts.value = districtData[cityCode] || []
}

const loadCustomerData = async () => {
  try {
    loading.value = true
    const response = await appointmentsApi.getCustomer(customerId.value)
    customerData.value = response.data
    
    // 填充表单数据
    Object.keys(form).forEach(key => {
      if (response.data[key] !== undefined) {
        form[key] = response.data[key]
      }
    })
    
    // 处理地址数据
    if (response.data.province) {
      await loadCities(response.data.province)
      if (response.data.city) {
        await loadDistricts(response.data.city)
      }
    }
    
  } catch (error) {
    ElMessage.error(error.message || '获取客户信息失败')
    console.error('获取客户信息失败:', error)
  } finally {
    loading.value = false
  }
}

const validateForm = async () => {
  try {
    await formRef.value.validate()
    return true
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
    return false
  }
}

const handleSubmit = async () => {
  if (!(await validateForm())) return
  
  submitting.value = true
  try {
    const formData = {
      ...form,
      full_address: fullAddress.value
    }
    
    await appointmentsApi.updateCustomer(customerId.value, formData)
    ElMessage.success('客户信息更新成功')
    router.push(`/customers/${customerId.value}`)
  } catch (error) {
    ElMessage.error(error.message || '更新客户信息失败')
    console.error('更新客户信息失败:', error)
  } finally {
    submitting.value = false
  }
}

const handleCreateAppointment = () => {
  router.push(`/appointments/create?customer_id=${customerId.value}`)
}

// 生命周期
onMounted(() => {
  loadCustomerData()
})
</script>

<style lang="scss" scoped>
.customer-edit {
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

.loading-container {
  background: white;
  border-radius: 8px;
  padding: 24px;
}

.form-card {
  .customer-form {
    .form-section {
      margin-bottom: 32px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .section-title {
        margin: 0 0 20px 0;
        padding-bottom: 12px;
        font-size: 18px;
        font-weight: 600;
        color: var(--el-text-color-primary);
        border-bottom: 2px solid var(--el-color-primary);
        position: relative;
        
        &::after {
          content: '';
          position: absolute;
          bottom: -2px;
          left: 0;
          width: 60px;
          height: 2px;
          background: var(--el-color-primary);
        }
      }
    }
    
    .el-form-item {
      margin-bottom: 20px;
      
      .el-input,
      .el-select,
      .el-date-picker,
      .el-input-number {
        width: 100%;
      }
      
      .el-textarea {
        .el-textarea__inner {
          resize: vertical;
        }
      }
    }
    
    .el-radio-group {
      .el-radio {
        margin-right: 24px;
      }
    }
  }
  
  .form-actions {
    display: flex;
    justify-content: center;
    gap: 16px;
    padding-top: 32px;
    border-top: 1px solid var(--el-border-color-lighter);
    margin-top: 32px;
  }
}

// 响应式适配
@include respond-to(md) {
  .customer-edit {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    
    .page-title {
      flex-direction: column;
      gap: 8px;
      
      .back-button {
        align-self: flex-start;
        margin-top: 0;
      }
    }
    
    .page-actions {
      align-self: stretch;
      
      .el-button {
        flex: 1;
      }
    }
  }
  
  .customer-form {
    .el-form-item {
      .el-input,
      .el-select,
      .el-date-picker,
      .el-input-number {
        width: 100% !important;
      }
    }
    
    .el-radio-group {
      .el-radio {
        margin-right: 16px;
        margin-bottom: 8px;
      }
    }
  }
  
  .form-actions {
    flex-direction: column;
    
    .el-button {
      width: 100%;
    }
  }
}

@include respond-to(sm) {
  .form-actions {
    .el-button {
      font-size: 16px;
      padding: 12px 20px;
    }
  }
}
</style>