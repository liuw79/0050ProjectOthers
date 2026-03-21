<template>
  <div class="customer-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-title">
        <h1>客户管理</h1>
        <p class="page-description">管理客户信息，查看客户详情和预约历史。</p>
      </div>
      
      <div class="page-actions">
        <el-button
          type="primary"
          :icon="Plus"
          @click="createCustomer"
        >
          新建客户
        </el-button>
        
        <el-dropdown trigger="click" @command="handleBatchAction">
          <el-button :icon="More">
            批量操作
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="export" :icon="Download">
                导出客户
              </el-dropdown-item>
              <el-dropdown-item command="import" :icon="Upload">
                导入客户
              </el-dropdown-item>
              <el-dropdown-item command="delete" :icon="Delete" divided>
                批量删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
    
    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="never">
      <el-form
        ref="searchFormRef"
        :model="searchForm"
        :inline="true"
        class="search-form"
      >
        <el-form-item label="客户姓名">
          <el-input
            v-model="searchForm.name"
            placeholder="请输入客户姓名"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        
        <el-form-item label="手机号">
          <el-input
            v-model="searchForm.phone"
            placeholder="请输入手机号"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        
        <el-form-item label="邮箱">
          <el-input
            v-model="searchForm.email"
            placeholder="请输入邮箱"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        
        <el-form-item label="性别">
          <el-select
            v-model="searchForm.gender"
            placeholder="选择性别"
            clearable
            style="width: 120px"
          >
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="年龄范围">
          <el-input-number
            v-model="searchForm.age_min"
            :min="0"
            :max="150"
            placeholder="最小年龄"
            style="width: 100px"
          />
          <span style="margin: 0 8px">-</span>
          <el-input-number
            v-model="searchForm.age_max"
            :min="0"
            :max="150"
            placeholder="最大年龄"
            style="width: 100px"
          />
        </el-form-item>
        
        <el-form-item label="注册时间">
          <el-date-picker
            v-model="searchForm.date_range"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 240px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">
            搜索
          </el-button>
          <el-button :icon="Refresh" @click="handleReset">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="table-header">
          <div class="table-title">
            <span>客户列表</span>
            <el-tag type="info" class="count-tag">
              共 {{ pagination.total }} 条记录
            </el-tag>
          </div>
          
          <div class="table-actions">
            <el-button-group>
              <el-button
                :type="viewMode === 'table' ? 'primary' : ''"
                :icon="Grid"
                @click="viewMode = 'table'"
              >
                表格视图
              </el-button>
              <el-button
                :type="viewMode === 'card' ? 'primary' : ''"
                :icon="Postcard"
                @click="viewMode = 'card'"
              >
                卡片视图
              </el-button>
            </el-button-group>
          </div>
        </div>
      </template>
      
      <!-- 表格视图 -->
      <div v-if="viewMode === 'table'">
        <el-table
          ref="tableRef"
          v-loading="loading"
          :data="customers"
          stripe
          @selection-change="handleSelectionChange"
          @sort-change="handleSortChange"
        >
          <el-table-column type="selection" width="55" />
          
          <el-table-column
            prop="id"
            label="ID"
            width="80"
            sortable="custom"
          />
          
          <el-table-column
            prop="name"
            label="客户姓名"
            min-width="120"
            sortable="custom"
          >
            <template #default="{ row }">
              <div class="customer-name">
                <el-avatar
                  :size="32"
                  :src="row.avatar"
                  class="customer-avatar"
                >
                  {{ row.name.charAt(0) }}
                </el-avatar>
                <span>{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column
            prop="gender"
            label="性别"
            width="80"
            align="center"
          >
            <template #default="{ row }">
              <el-tag
                :type="row.gender === 'male' ? 'primary' : 'danger'"
                size="small"
              >
                {{ row.gender === 'male' ? '男' : '女' }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column
            prop="age"
            label="年龄"
            width="80"
            align="center"
            sortable="custom"
          >
            <template #default="{ row }">
              {{ row.age }}岁
            </template>
          </el-table-column>
          
          <el-table-column
            prop="phone"
            label="手机号"
            width="140"
          >
            <template #default="{ row }">
              <el-link :href="`tel:${row.phone}`" type="primary">
                {{ row.phone }}
              </el-link>
            </template>
          </el-table-column>
          
          <el-table-column
            prop="email"
            label="邮箱"
            min-width="180"
            show-overflow-tooltip
          >
            <template #default="{ row }">
              <el-link :href="`mailto:${row.email}`" type="primary">
                {{ row.email }}
              </el-link>
            </template>
          </el-table-column>
          
          <el-table-column
            prop="occupation"
            label="职业"
            min-width="120"
            show-overflow-tooltip
          >
            <template #default="{ row }">
              {{ row.occupation || '-' }}
            </template>
          </el-table-column>
          
          <el-table-column
            prop="total_appointments"
            label="预约次数"
            width="100"
            align="center"
            sortable="custom"
          >
            <template #default="{ row }">
              <el-link
                type="primary"
                @click="viewAppointments(row.id)"
              >
                {{ row.total_appointments || 0 }}
              </el-link>
            </template>
          </el-table-column>
          
          <el-table-column
            prop="last_appointment_date"
            label="最近预约"
            width="120"
            align="center"
            sortable="custom"
          >
            <template #default="{ row }">
              <span v-if="row.last_appointment_date">
                {{ formatDate(row.last_appointment_date) }}
              </span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
          
          <el-table-column
            prop="created_at"
            label="注册时间"
            width="120"
            align="center"
            sortable="custom"
          >
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          
          <el-table-column
            label="操作"
            width="200"
            align="center"
            fixed="right"
          >
            <template #default="{ row }">
              <el-button
                type="primary"
                size="small"
                :icon="View"
                @click="viewCustomer(row.id)"
              >
                查看
              </el-button>
              
              <el-button
                type="warning"
                size="small"
                :icon="Edit"
                @click="editCustomer(row.id)"
              >
                编辑
              </el-button>
              
              <el-dropdown trigger="click" @command="(cmd) => handleRowAction(cmd, row)">
                <el-button size="small" :icon="More" />
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="appointment" :icon="Calendar">
                      创建预约
                    </el-dropdown-item>
                    <el-dropdown-item command="message" :icon="Message">
                      发送消息
                    </el-dropdown-item>
                    <el-dropdown-item command="export" :icon="Download">
                      导出信息
                    </el-dropdown-item>
                    <el-dropdown-item command="delete" :icon="Delete" divided>
                      删除客户
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 卡片视图 -->
      <div v-else class="card-view">
        <el-row :gutter="20" v-loading="loading">
          <el-col
            v-for="customer in customers"
            :key="customer.id"
            :xl="6"
            :lg="8"
            :md="12"
            :sm="24"
            class="customer-card-col"
          >
            <el-card class="customer-card" shadow="hover">
              <div class="customer-header">
                <el-avatar
                  :size="60"
                  :src="customer.avatar"
                  class="customer-avatar"
                >
                  {{ customer.name.charAt(0) }}
                </el-avatar>
                
                <div class="customer-info">
                  <h3 class="customer-name">{{ customer.name }}</h3>
                  <div class="customer-meta">
                    <el-tag
                      :type="customer.gender === 'male' ? 'primary' : 'danger'"
                      size="small"
                    >
                      {{ customer.gender === 'male' ? '男' : '女' }}
                    </el-tag>
                    <span class="age">{{ customer.age }}岁</span>
                  </div>
                </div>
              </div>
              
              <div class="customer-details">
                <div class="detail-item">
                  <el-icon><Phone /></el-icon>
                  <span>{{ customer.phone }}</span>
                </div>
                
                <div class="detail-item">
                  <el-icon><Message /></el-icon>
                  <span>{{ customer.email }}</span>
                </div>
                
                <div class="detail-item" v-if="customer.occupation">
                  <el-icon><Briefcase /></el-icon>
                  <span>{{ customer.occupation }}</span>
                </div>
                
                <div class="detail-item">
                  <el-icon><Calendar /></el-icon>
                  <span>预约 {{ customer.total_appointments || 0 }} 次</span>
                </div>
              </div>
              
              <div class="customer-actions">
                <el-button
                  type="primary"
                  size="small"
                  @click="viewCustomer(customer.id)"
                >
                  查看详情
                </el-button>
                
                <el-button
                  type="success"
                  size="small"
                  @click="createAppointment(customer.id)"
                >
                  创建预约
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 导入对话框 -->
    <el-dialog
      v-model="importDialogVisible"
      title="导入客户"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-upload
        ref="uploadRef"
        :action="uploadAction"
        :headers="uploadHeaders"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
        :file-list="fileList"
        accept=".xlsx,.xls,.csv"
        drag
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 Excel (.xlsx, .xls) 和 CSV 格式文件，文件大小不超过 10MB
          </div>
        </template>
      </el-upload>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="importDialogVisible = false">
            取消
          </el-button>
          <el-button
            type="primary"
            @click="downloadTemplate"
          >
            下载模板
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  More,
  ArrowDown,
  Download,
  Upload,
  Delete,
  Search,
  Refresh,
  Grid,
  Postcard,
  View,
  Edit,
  Calendar,
  Message,
  Phone,
  Briefcase,
  UploadFilled
} from '@element-plus/icons-vue'
import { appointmentsApi } from '@/api/appointments'
import dayjs from 'dayjs'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const viewMode = ref('table')
const customers = ref([])
const selectedCustomers = ref([])
const importDialogVisible = ref(false)
const fileList = ref([])

// 表单引用
const searchFormRef = ref()
const tableRef = ref()
const uploadRef = ref()

// 搜索表单
const searchForm = reactive({
  name: '',
  phone: '',
  email: '',
  gender: '',
  age_min: null,
  age_max: null,
  date_range: []
})

// 分页数据
const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

// 排序数据
const sortData = reactive({
  prop: '',
  order: ''
})

// 计算属性
const uploadAction = computed(() => {
  return `${import.meta.env.VITE_API_BASE_URL}/customers/import/`
})

const uploadHeaders = computed(() => {
  const token = localStorage.getItem('access_token')
  return {
    'Authorization': `Bearer ${token}`
  }
})

// 方法
const loadCustomers = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...searchForm
    }
    
    // 处理日期范围
    if (searchForm.date_range && searchForm.date_range.length === 2) {
      params.created_at_start = searchForm.date_range[0]
      params.created_at_end = searchForm.date_range[1]
    }
    delete params.date_range
    
    // 处理排序
    if (sortData.prop && sortData.order) {
      params.ordering = sortData.order === 'ascending' ? sortData.prop : `-${sortData.prop}`
    }
    
    const response = await appointmentsApi.getCustomers(params)
    customers.value = response.data.results || []
    pagination.total = response.data.count || 0
  } catch (error) {
    ElMessage.error('加载客户列表失败')
    console.error('加载客户失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadCustomers()
}

const handleReset = () => {
  if (searchFormRef.value) {
    searchFormRef.value.resetFields()
  }
  Object.assign(searchForm, {
    name: '',
    phone: '',
    email: '',
    gender: '',
    age_min: null,
    age_max: null,
    date_range: []
  })
  pagination.page = 1
  loadCustomers()
}

const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  loadCustomers()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadCustomers()
}

const handleSortChange = ({ prop, order }) => {
  sortData.prop = prop
  sortData.order = order
  loadCustomers()
}

const handleSelectionChange = (selection) => {
  selectedCustomers.value = selection
}

const handleBatchAction = async (command) => {
  switch (command) {
    case 'export':
      await exportCustomers()
      break
    case 'import':
      importDialogVisible.value = true
      break
    case 'delete':
      await batchDeleteCustomers()
      break
  }
}

const handleRowAction = async (command, row) => {
  switch (command) {
    case 'appointment':
      createAppointment(row.id)
      break
    case 'message':
      sendMessage(row)
      break
    case 'export':
      await exportCustomer(row.id)
      break
    case 'delete':
      await deleteCustomer(row.id)
      break
  }
}

const createCustomer = () => {
  router.push('/customers/create')
}

const viewCustomer = (id) => {
  router.push(`/customers/${id}`)
}

const editCustomer = (id) => {
  router.push(`/customers/${id}/edit`)
}

const viewAppointments = (customerId) => {
  router.push(`/appointments?customer_id=${customerId}`)
}

const createAppointment = (customerId) => {
  router.push(`/appointments/create?customer_id=${customerId}`)
}

const sendMessage = (customer) => {
  // 实现发送消息功能
  ElMessage.info('发送消息功能开发中')
}

const exportCustomers = async () => {
  try {
    const params = selectedCustomers.value.length > 0
      ? { ids: selectedCustomers.value.map(c => c.id) }
      : { ...searchForm }
    
    const response = await appointmentsApi.exportCustomers(params)
    
    // 下载文件
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `customers_${dayjs().format('YYYY-MM-DD')}.xlsx`
    link.click()
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
    console.error('导出客户失败:', error)
  }
}

const exportCustomer = async (id) => {
  try {
    const response = await appointmentsApi.exportCustomers({ ids: [id] })
    
    // 下载文件
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `customer_${id}_${dayjs().format('YYYY-MM-DD')}.xlsx`
    link.click()
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
    console.error('导出客户失败:', error)
  }
}

const batchDeleteCustomers = async () => {
  if (selectedCustomers.value.length === 0) {
    ElMessage.warning('请先选择要删除的客户')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedCustomers.value.length} 个客户吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const ids = selectedCustomers.value.map(c => c.id)
    await appointmentsApi.batchDeleteCustomers({ ids })
    
    ElMessage.success('删除成功')
    selectedCustomers.value = []
    await loadCustomers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const deleteCustomer = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个客户吗？删除后无法恢复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await appointmentsApi.deleteCustomer(id)
    ElMessage.success('删除成功')
    await loadCustomers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const beforeUpload = (file) => {
  const isValidType = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                      'application/vnd.ms-excel',
                      'text/csv'].includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10
  
  if (!isValidType) {
    ElMessage.error('只能上传 Excel 或 CSV 格式的文件！')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB！')
    return false
  }
  return true
}

const handleUploadSuccess = (response) => {
  ElMessage.success(`导入成功，共导入 ${response.success_count} 条记录`)
  if (response.error_count > 0) {
    ElMessage.warning(`有 ${response.error_count} 条记录导入失败`)
  }
  importDialogVisible.value = false
  fileList.value = []
  loadCustomers()
}

const handleUploadError = (error) => {
  ElMessage.error('导入失败，请检查文件格式')
  console.error('导入失败:', error)
}

const downloadTemplate = async () => {
  try {
    const response = await appointmentsApi.downloadCustomerTemplate()
    
    // 下载模板文件
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'customer_import_template.xlsx'
    link.click()
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('模板下载成功')
  } catch (error) {
    ElMessage.error('模板下载失败')
    console.error('下载模板失败:', error)
  }
}

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD')
}

// 组件挂载时加载数据
onMounted(() => {
  loadCustomers()
})
</script>

<style lang="scss" scoped>
.customer-list {
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

.search-card {
  margin-bottom: 20px;
  
  .search-form {
    .el-form-item {
      margin-bottom: 16px;
    }
  }
}

.table-card {
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .table-title {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 600;
      color: var(--el-text-color-primary);
      
      .count-tag {
        font-weight: normal;
      }
    }
  }
  
  .customer-name {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .customer-avatar {
      flex-shrink: 0;
    }
  }
  
  .text-muted {
    color: var(--el-text-color-secondary);
  }
}

.card-view {
  .customer-card-col {
    margin-bottom: 20px;
  }
  
  .customer-card {
    height: 100%;
    
    .customer-header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 16px;
      
      .customer-info {
        flex: 1;
        
        .customer-name {
          margin: 0 0 8px 0;
          font-size: 16px;
          font-weight: 600;
          color: var(--el-text-color-primary);
        }
        
        .customer-meta {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .age {
            font-size: 12px;
            color: var(--el-text-color-secondary);
          }
        }
      }
    }
    
    .customer-details {
      margin-bottom: 16px;
      
      .detail-item {
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
    
    .customer-actions {
      display: flex;
      gap: 8px;
      
      .el-button {
        flex: 1;
      }
    }
  }
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 响应式适配
@include respond-to(md) {
  .customer-list {
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
  
  .search-form {
    .el-form-item {
      width: 100%;
      
      .el-input,
      .el-select,
      .el-date-picker {
        width: 100% !important;
      }
    }
  }
  
  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .customer-card {
    .customer-actions {
      flex-direction: column;
      
      .el-button {
        width: 100%;
      }
    }
  }
}
</style>