<template>
  <div class="appointment-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-title">
        <h1>预约管理</h1>
        <p class="page-description">管理所有客户预约，包括创建、编辑和跟踪预约状态。</p>
      </div>
      <div class="page-actions">
        <el-button type="primary" :icon="Plus" @click="createAppointment">
          创建预约
        </el-button>
        <el-button :icon="Download" @click="exportAppointments">
          导出数据
        </el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选 -->
    <el-card class="search-card" shadow="never">
      <el-form :model="searchForm" :inline="true" class="search-form">
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="搜索客户姓名、手机号或备注"
            :prefix-icon="Search"
            clearable
            style="width: 300px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="选择状态" clearable style="width: 120px">
            <el-option label="待确认" value="pending" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="服务类型">
          <el-select v-model="searchForm.serviceType" placeholder="选择服务类型" clearable style="width: 140px">
            <el-option label="咨询服务" value="consultation" />
            <el-option label="深度访谈" value="interview" />
            <el-option label="数据分析" value="analysis" />
            <el-option label="报告解读" value="report" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
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
          <el-button :icon="Refresh" @click="resetSearch">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <div class="table-header">
        <div class="table-title">
          <span>预约列表</span>
          <el-tag type="info" size="small">共 {{ pagination.total }} 条记录</el-tag>
        </div>
        <div class="table-actions">
          <el-button-group>
            <el-button
              :type="viewMode === 'table' ? 'primary' : ''"
              :icon="Grid"
              @click="viewMode = 'table'"
              size="small"
            >
              表格视图
            </el-button>
            <el-button
              :type="viewMode === 'calendar' ? 'primary' : ''"
              :icon="Calendar"
              @click="viewMode = 'calendar'"
              size="small"
            >
              日历视图
            </el-button>
          </el-button-group>
        </div>
      </div>
      
      <!-- 表格视图 -->
      <div v-show="viewMode === 'table'">
        <el-table
          v-loading="loading"
          :data="appointments"
          stripe
          @selection-change="handleSelectionChange"
          @sort-change="handleSortChange"
        >
          <el-table-column type="selection" width="55" />
          
          <el-table-column label="预约ID" prop="id" width="100" sortable="custom">
            <template #default="{ row }">
              <el-link type="primary" @click="viewAppointment(row.id)">
                #{{ row.id }}
              </el-link>
            </template>
          </el-table-column>
          
          <el-table-column label="客户信息" min-width="180">
            <template #default="{ row }">
              <div class="customer-info">
                <div class="customer-name">{{ row.customer_name }}</div>
                <div class="customer-phone">{{ row.customer_phone }}</div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="预约时间" prop="scheduled_time" width="160" sortable="custom">
            <template #default="{ row }">
              <div class="appointment-time">
                <div class="date">{{ formatDate(row.scheduled_time) }}</div>
                <div class="time">{{ formatTime(row.scheduled_time) }}</div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="服务类型" prop="service_type" width="120">
            <template #default="{ row }">
              <el-tag :type="getServiceTypeColor(row.service_type)" size="small">
                {{ getServiceTypeText(row.service_type) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="时长" prop="duration" width="80">
            <template #default="{ row }">
              {{ row.duration }}分钟
            </template>
          </el-table-column>
          
          <el-table-column label="状态" prop="status" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="创建时间" prop="created_at" width="160" sortable="custom">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
            </template>
          </el-table-column>
          
          <el-table-column label="备注" prop="notes" min-width="150">
            <template #default="{ row }">
              <el-tooltip :content="row.notes" placement="top" :disabled="!row.notes">
                <span class="notes-text">{{ row.notes || '-' }}</span>
              </el-tooltip>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button
                  text
                  type="primary"
                  size="small"
                  @click="viewAppointment(row.id)"
                >
                  查看
                </el-button>
                
                <el-button
                  text
                  type="warning"
                  size="small"
                  @click="editAppointment(row.id)"
                  v-if="canEdit(row.status)"
                >
                  编辑
                </el-button>
                
                <el-dropdown trigger="click" @command="(command) => handleAction(command, row)">
                  <el-button text type="primary" size="small">
                    更多
                    <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item
                        command="confirm"
                        v-if="row.status === 'pending'"
                      >
                        <el-icon><Check /></el-icon>
                        确认预约
                      </el-dropdown-item>
                      
                      <el-dropdown-item
                        command="complete"
                        v-if="row.status === 'confirmed'"
                      >
                        <el-icon><CircleCheck /></el-icon>
                        完成预约
                      </el-dropdown-item>
                      
                      <el-dropdown-item
                        command="reschedule"
                        v-if="canReschedule(row.status)"
                      >
                        <el-icon><Clock /></el-icon>
                        重新安排
                      </el-dropdown-item>
                      
                      <el-dropdown-item
                        command="cancel"
                        v-if="canCancel(row.status)"
                        divided
                      >
                        <el-icon><Close /></el-icon>
                        取消预约
                      </el-dropdown-item>
                      
                      <el-dropdown-item
                        command="delete"
                        v-if="canDelete(row.status)"
                        divided
                      >
                        <el-icon><Delete /></el-icon>
                        删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 批量操作 -->
        <div class="batch-actions" v-show="selectedAppointments.length > 0">
          <div class="batch-info">
            已选择 {{ selectedAppointments.length }} 项
          </div>
          <div class="batch-buttons">
            <el-button size="small" @click="batchConfirm" :disabled="!canBatchConfirm">
              批量确认
            </el-button>
            <el-button size="small" @click="batchCancel" :disabled="!canBatchCancel">
              批量取消
            </el-button>
            <el-button size="small" type="danger" @click="batchDelete" :disabled="!canBatchDelete">
              批量删除
            </el-button>
          </div>
        </div>
      </div>
      
      <!-- 日历视图 -->
      <div v-show="viewMode === 'calendar'" class="calendar-view">
        <el-calendar v-model="calendarDate" @panel-change="handleCalendarChange">
          <template #date-cell="{ data }">
            <div class="calendar-cell">
              <div class="date-number">{{ data.day.split('-').slice(-1)[0] }}</div>
              <div class="appointments-count" v-if="getDateAppointments(data.day).length > 0">
                {{ getDateAppointments(data.day).length }} 个预约
              </div>
              <div class="appointment-dots">
                <span
                  v-for="appointment in getDateAppointments(data.day).slice(0, 3)"
                  :key="appointment.id"
                  class="appointment-dot"
                  :class="`status-${appointment.status}`"
                  @click="viewAppointment(appointment.id)"
                ></span>
              </div>
            </div>
          </template>
        </el-calendar>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-wrapper" v-show="viewMode === 'table'">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
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
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Download,
  Search,
  Refresh,
  Grid,
  Calendar,
  ArrowDown,
  Check,
  CircleCheck,
  Clock,
  Close,
  Delete
} from '@element-plus/icons-vue'
import { appointmentsApi } from '@/api/appointments'
import dayjs from 'dayjs'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const rescheduleLoading = ref(false)
const rescheduleDialogVisible = ref(false)
const viewMode = ref('table')
const calendarDate = ref(new Date())
const appointments = ref([])
const selectedAppointments = ref([])
const currentRescheduleId = ref(null)

// 表单引用
const rescheduleFormRef = ref()

// 搜索表单
const searchForm = reactive({
  search: '',
  status: '',
  serviceType: '',
  dateRange: []
})

// 重新安排表单
const rescheduleForm = reactive({
  date: '',
  time: '',
  reason: ''
})

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 排序数据
const sortData = reactive({
  prop: '',
  order: ''
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
const canBatchConfirm = computed(() => {
  return selectedAppointments.value.some(app => app.status === 'pending')
})

const canBatchCancel = computed(() => {
  return selectedAppointments.value.some(app => canCancel(app.status))
})

const canBatchDelete = computed(() => {
  return selectedAppointments.value.some(app => canDelete(app.status))
})

// 方法
const loadAppointments = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm
    }
    
    // 处理日期范围
    if (searchForm.dateRange && searchForm.dateRange.length === 2) {
      params.start_date = searchForm.dateRange[0]
      params.end_date = searchForm.dateRange[1]
    }
    
    // 处理排序
    if (sortData.prop) {
      params.ordering = sortData.order === 'descending' ? `-${sortData.prop}` : sortData.prop
    }
    
    const response = await appointmentsApi.getAppointments(params)
    appointments.value = response.data.results || []
    pagination.total = response.data.count || 0
  } catch (error) {
    ElMessage.error('加载预约数据失败')
    console.error('加载预约失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadAppointments()
}

const resetSearch = () => {
  Object.assign(searchForm, {
    search: '',
    status: '',
    serviceType: '',
    dateRange: []
  })
  pagination.page = 1
  loadAppointments()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  loadAppointments()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadAppointments()
}

const handleSortChange = ({ prop, order }) => {
  sortData.prop = prop
  sortData.order = order
  loadAppointments()
}

const handleSelectionChange = (selection) => {
  selectedAppointments.value = selection
}

const createAppointment = () => {
  router.push('/appointments/create')
}

const viewAppointment = (id) => {
  router.push(`/appointments/${id}`)
}

const editAppointment = (id) => {
  router.push(`/appointments/${id}/edit`)
}

const handleAction = async (command, row) => {
  switch (command) {
    case 'confirm':
      await confirmAppointment(row.id)
      break
    case 'complete':
      await completeAppointment(row.id)
      break
    case 'reschedule':
      showRescheduleDialog(row.id)
      break
    case 'cancel':
      await cancelAppointment(row.id)
      break
    case 'delete':
      await deleteAppointment(row.id)
      break
  }
}

const confirmAppointment = async (id) => {
  try {
    await appointmentsApi.confirmAppointment(id)
    ElMessage.success('预约确认成功')
    await loadAppointments()
  } catch (error) {
    ElMessage.error(error.message || '确认预约失败')
  }
}

const completeAppointment = async (id) => {
  try {
    await appointmentsApi.completeAppointment(id)
    ElMessage.success('预约完成')
    await loadAppointments()
  } catch (error) {
    ElMessage.error(error.message || '完成预约失败')
  }
}

const showRescheduleDialog = (id) => {
  currentRescheduleId.value = id
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
    
    await appointmentsApi.rescheduleAppointment(currentRescheduleId.value, data)
    
    ElMessage.success('预约重新安排成功')
    rescheduleDialogVisible.value = false
    await loadAppointments()
  } catch (error) {
    ElMessage.error(error.message || '重新安排失败')
  } finally {
    rescheduleLoading.value = false
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
    ElMessage.success('预约已取消')
    await loadAppointments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '取消预约失败')
    }
  }
}

const deleteAppointment = async (id) => {
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
    
    await appointmentsApi.deleteAppointment(id)
    ElMessage.success('预约已删除')
    await loadAppointments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除预约失败')
    }
  }
}

const batchConfirm = async () => {
  const pendingIds = selectedAppointments.value
    .filter(app => app.status === 'pending')
    .map(app => app.id)
  
  if (pendingIds.length === 0) {
    ElMessage.warning('没有可确认的预约')
    return
  }
  
  try {
    await appointmentsApi.batchConfirm({ ids: pendingIds })
    ElMessage.success(`成功确认 ${pendingIds.length} 个预约`)
    await loadAppointments()
  } catch (error) {
    ElMessage.error(error.message || '批量确认失败')
  }
}

const batchCancel = async () => {
  const cancelableIds = selectedAppointments.value
    .filter(app => canCancel(app.status))
    .map(app => app.id)
  
  if (cancelableIds.length === 0) {
    ElMessage.warning('没有可取消的预约')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要取消选中的 ${cancelableIds.length} 个预约吗？`,
      '确认批量取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await appointmentsApi.batchCancel({ ids: cancelableIds })
    ElMessage.success(`成功取消 ${cancelableIds.length} 个预约`)
    await loadAppointments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '批量取消失败')
    }
  }
}

const batchDelete = async () => {
  const deletableIds = selectedAppointments.value
    .filter(app => canDelete(app.status))
    .map(app => app.id)
  
  if (deletableIds.length === 0) {
    ElMessage.warning('没有可删除的预约')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${deletableIds.length} 个预约吗？删除后无法恢复。`,
      '确认批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await appointmentsApi.batchDelete({ ids: deletableIds })
    ElMessage.success(`成功删除 ${deletableIds.length} 个预约`)
    await loadAppointments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '批量删除失败')
    }
  }
}

const exportAppointments = async () => {
  try {
    const params = { ...searchForm }
    if (searchForm.dateRange && searchForm.dateRange.length === 2) {
      params.start_date = searchForm.dateRange[0]
      params.end_date = searchForm.dateRange[1]
    }
    
    await appointmentsApi.exportAppointments(params)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error(error.message || '导出失败')
  }
}

const handleCalendarChange = (date) => {
  // 当日历面板改变时，可以加载对应月份的预约数据
  console.log('Calendar changed:', date)
}

const getDateAppointments = (date) => {
  return appointments.value.filter(app => {
    return dayjs(app.scheduled_time).format('YYYY-MM-DD') === date
  })
}

const canEdit = (status) => {
  return ['pending', 'confirmed'].includes(status)
}

const canReschedule = (status) => {
  return ['pending', 'confirmed'].includes(status)
}

const canCancel = (status) => {
  return ['pending', 'confirmed'].includes(status)
}

const canDelete = (status) => {
  return ['cancelled', 'completed'].includes(status)
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

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD')
}

const formatTime = (date) => {
  return dayjs(date).format('HH:mm')
}

const formatDateTime = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 监听视图模式变化
watch(viewMode, (newMode) => {
  if (newMode === 'calendar') {
    // 切换到日历视图时，可能需要加载不同的数据
    // loadCalendarAppointments()
  }
})

// 组件挂载时加载数据
onMounted(() => {
  loadAppointments()
})
</script>

<style lang="scss" scoped>
.appointment-list {
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
      margin-bottom: 0;
    }
  }
}

.table-card {
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    .table-title {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }
}

.customer-info {
  .customer-name {
    font-weight: 500;
    color: var(--el-text-color-primary);
    margin-bottom: 4px;
  }
  
  .customer-phone {
    font-size: 12px;
    color: var(--el-text-color-secondary);
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

.notes-text {
  @include text-ellipsis;
  max-width: 150px;
  display: inline-block;
}

.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.batch-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--el-fill-color-lighter);
  border-radius: 6px;
  margin-top: 16px;
  
  .batch-info {
    font-size: 14px;
    color: var(--el-text-color-primary);
  }
  
  .batch-buttons {
    display: flex;
    gap: 8px;
  }
}

.calendar-view {
  .calendar-cell {
    height: 100px;
    padding: 4px;
    
    .date-number {
      font-weight: 600;
      margin-bottom: 4px;
    }
    
    .appointments-count {
      font-size: 10px;
      color: var(--el-color-primary);
      margin-bottom: 4px;
    }
    
    .appointment-dots {
      display: flex;
      gap: 2px;
      flex-wrap: wrap;
      
      .appointment-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        cursor: pointer;
        
        &.status-pending {
          background: var(--el-color-warning);
        }
        
        &.status-confirmed {
          background: var(--el-color-primary);
        }
        
        &.status-completed {
          background: var(--el-color-success);
        }
        
        &.status-cancelled {
          background: var(--el-color-danger);
        }
      }
    }
  }
}

.pagination-wrapper {
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
@include respond-to(lg) {
  .search-form {
    .el-form-item {
      margin-bottom: 16px;
    }
  }
}

@include respond-to(md) {
  .appointment-list {
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
  
  .table-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .batch-actions {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
    
    .batch-buttons {
      justify-content: center;
    }
  }
}
</style>